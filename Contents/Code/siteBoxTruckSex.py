import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.replace(' ', '+').replace('--', '+').lower()
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//ul[@class="slides"]/li'):
        titleNoFormatting = searchResult.xpath('.//h5')[0].text_content().strip()
        sceneURL = searchResult.xpath('.//@href')[0]
        curID = PAutils.Encode(sceneURL)

        date = searchResult.xpath('.//p/strong')[0].text_content().strip()
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
        releaseDate = parse(date).strftime('%Y-%m-%d')
        displayDate = releaseDate if date else ''

        if searchDate and displayDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    metadata.title = detailsPageElements.xpath('//h2')[0].text_content()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="desc"]')[0].text_content().strip()
    except:
        pass

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Actors
    actors = detailsPageElements.xpath('//h5/a[contains(@href,"models")]')
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

            modelURL = PAsearchSites.getSearchBaseURL(siteID) + "/tour/models/" + actorName[0] + "/models.html"
            req = PAutils.HTTPRequest(modelURL)
            modelsPageElements = HTML.ElementFromString(req.text)

            img = modelsPageElements.xpath('//a[contains(@title,"' + actorName + '")]//@src')[0]

            if img:
                actorPhotoURL = img
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL

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
    for genre in detailsPageElements.xpath('//h5[contains(@class,"video_categories")]')[0].text_content().replace('Tags:', '').replace('XXX', '').split(','):
        movieGenres.addGenre(genre.strip())

    # Posters
    art = []
    xpaths = [
        '//div[@class="mb clearfix"]//a[contains(@class,"stills")]//@src',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if 'http' not in img:
                img = PAsearchSites.getSearchBaseURL(siteID) + img
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
