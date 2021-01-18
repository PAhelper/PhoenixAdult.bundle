import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.replace('/cn/', '/').replace('/de/', '/').replace('/jp/', '/').replace('/ja/', '/').replace('/en/', '/')
        if '/nude_girl/' not in sceneURL and '/shoots/' not in sceneURL and '/fetish/' not in sceneURL and '/updates/' not in sceneURL and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    prevModelURL = ''
    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//title')[0].text_content().split(':')[-1].split('|')[0].strip(), siteNum)
        subSite = PAutils.parseTitle(detailsPageElements.xpath('//div[@id="shoot-featured-image"]//h4')[0].text_content().strip(), siteNum)
        curID = PAutils.Encode(sceneURL)

        modelURL = detailsPageElements.xpath('//tr[contains(.,"Scene")]//a/@href')[0]
        if not modelURL == prevModelURL:
            req = PAutils.HTTPRequest(modelURL)
            actorPageElements = HTML.ElementFromString(req.text)
        prevModelURL = modelURL

        date = ''
        for scene in actorPageElements.xpath('//article[@class="card card-shoot"]'):
            if titleNoFormatting.lower() == scene.xpath('.//h2')[0].text_content().strip().lower() and subSite.lower() == scene.xpath('.//h3/text()')[0].strip().lower():
                date = scene.xpath('.//span')[0].text_content().strip()
                break

        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        displayDate = releaseDate if date else ''

        if searchData.date and displayDate:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [Abby Winters/%s] %s' % (titleNoFormatting, subSite, displayDate), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//title')[0].text_content().split(':')[-1].split('|')[0].strip(), siteNum)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//aside/div[contains(@class,"description")]')[0].text_content().replace('\n', '').strip()
    except:
        pass

    # Studio
    metadata.studio = 'Abby Winters'

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = PAutils.parseTitle(detailsPageElements.xpath('//div[@id="shoot-featured-image"]//h4')[0].text_content().strip(), siteNum)
    metadata.collections.add(metadata.tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//aside/div[contains(@class,"description")]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//tr[contains(.,"Scene")]//a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        modelURL = actorLink.xpath('.//@href')[0]
        req = PAutils.HTTPRequest(modelURL)
        actorPageElements = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPageElements.xpath('//img[@class="img-responsive"]/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="tile tile-image"]/img/@src',
        '//div[contains(@class,"video")]/@data-poster',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            art.append(img)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.abbywinters.com'})
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
