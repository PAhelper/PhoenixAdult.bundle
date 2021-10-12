import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if '/session/' in sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//h3[@class="mas_title"]')[0].text_content().strip(), siteNum)
        subSite = detailsPageElements.xpath('//title')[0].text_content().split('|')[1].strip().replace('.com', '')
        curID = PAutils.Encode(sceneURL)

        date = ' '.join(detailsPageElements.xpath('//div[@class="lch"]/span')[0].text_content().rsplit(',', 2)[1:]).strip()
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        displayDate = releaseDate if date else ''

        if searchData.date and displayDate:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, subSite, displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h3[@class="mas_title"]')[0].text_content().strip(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="mas_longdescription"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Deranged Dollars'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//title')[0].text_content().split('|')[1].strip().replace('.com', '')
    metadata.tagline = tagline
    metadata.collections.add(metadata.tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//p[@class="tags"]/a'):
        genreName = PAutils.parseTitle(genreLink.text_content().strip(), siteNum)

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="lch"]/span')[0].text_content().rsplit(',', 2)[0]
    if ':' in actors:
        actors = re.split(',|&|/|And', actors.split(':', 1)[1])
    else:
        actors = re.split(',|&|/|And', actors)

    modelURL = PAsearchSites.getSearchSearchURL(siteNum) + '?models'
    req = PAutils.HTTPRequest(modelURL)
    modelPageElements = HTML.ElementFromString(req.text)
    models = modelPageElements.xpath('//div[@class="item"]')
    modelURL = PAsearchSites.getSearchSearchURL(siteNum) + '?models/2'
    req = PAutils.HTTPRequest(modelURL)
    modelPageElements = HTML.ElementFromString(req.text)
    models += modelPageElements.xpath('//div[@class="item"]')

    for actorLink in actors:
        actorName = actorLink.strip()
        actorName = re.sub(r'\W', ' ', actorName).replace('Nurses', '').replace('Nurse', '')

        actorPhotoURL = ''
        for model in models:
            if ':' in model.text_content().strip():
                if actorName in model.text_content().split(':', 1)[1].strip():
                    actorName = model.text_content().split(':', 1)[1].strip()
                    actorPhotoURL = PAsearchSites.getSearchSearchURL(siteNum) + model.xpath('.//@src')[0]
                    break
            else:
                if actorName in model.text_content().strip():
                    actorName = model.text_content().strip()
                    actorPhotoURL = PAsearchSites.getSearchSearchURL(siteNum) + model.xpath('.//@src')[0]
                    break

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="stills clearfix"]//img/@src',
        '//div[@class="mainpic"]//script/text()',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if '\'' in img:
                img = img.split('\'')[1]
            if 'http' not in img:
                img = PAsearchSites.getSearchSearchURL(siteNum) + img

            art.append(img)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
