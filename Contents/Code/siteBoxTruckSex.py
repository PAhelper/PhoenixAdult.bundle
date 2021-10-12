import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.replace(' ', '+').replace('--', '+').lower()
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    
    for searchResult in searchResults.xpath('//ul[@class="slides"]/li'):
        titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//h5')[0].text_content().strip(), siteNum)
        sceneURL = searchResult.xpath('.//@href')[0]
        curID = PAutils.Encode(sceneURL)

        date = searchResult.xpath('.//p/strong')[0].text_content().strip()
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        releaseDate = parse(date).strftime('%Y-%m-%d')
        displayDate = releaseDate if date else ''

        if searchData.date and displayDate:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h2')[0].text_content(), siteNum)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="desc"]')[0].text_content().strip()
    except:
        pass

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Actors
    actors = detailsPageElements.xpath('//h5/a[contains(@href, "models")]')
    actorPhotoURL = ''

    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 5:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content()

            modelURL = PAsearchSites.getSearchBaseURL(siteNum) + "/tour/models/" + actorName[0] + "/models.html"
            req = PAutils.HTTPRequest(modelURL)
            modelsPageElements = HTML.ElementFromString(req.text)

            img = modelsPageElements.xpath('//a[contains(@title, "' + actorName + '")]//@src')[0]

            if img:
                actorPhotoURL = img
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteNum) + actorPhotoURL

            movieActors.addActor(actorName, actorPhotoURL)

    # Release Date
    date = detailsPageElements.xpath('//p[@class="mb0"]')[0].text_content().replace('Date Added: ', '').strip()

    if not date and sceneDate:
        date = sceneDate

    date = parse(date).strftime('%d-%m-%Y')

    if date:
        date_object = datetime.strptime(date, '%d-%m-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genreLink in detailsPageElements.xpath('//h5[contains(@class, "video_categories")]')[0].text_content().replace('Tags:', '').replace('XXX', '').split(','):
        genreName = genreLink.strip()

        movieGenres.addGenre(genreName)

    # Posters
    art = []
    xpaths = [
        '//div[@class="mb clearfix"]//a[contains(@class, "stills")]//@src',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if 'http' not in img:
                img = PAsearchSites.getSearchBaseURL(siteNum) + img
            art.append(img)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': sceneURL})
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
