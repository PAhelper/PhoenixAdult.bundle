import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.split('?')[0].replace('dev.', '', 1)

        if ('/view/' in sceneURL) and ('photoset' not in sceneURL) and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in googleResults:
        if ('/model/' in sceneURL):
            req = PAutils.HTTPRequest(sceneURL)
            actorPageElements = HTML.ElementFromString(req.text)

            for searchResult in actorPageElements.xpath('//div[contains(@class, "content-item")]'):
                sceneURL = searchResult.xpath('.//h3//@href')[0].split('?')[0].replace('dev.', '', 1)

                if sceneURL not in searchResults:
                    titleNoFormatting = searchResult.xpath('.//h3')[0].text_content().strip()
                    curID = PAutils.Encode(sceneURL)

                    date = searchResult.xpath('.//span[@class="pub-date"]')[0].text_content().strip()
                    releaseDate = parse(date).strftime('%Y-%m-%d')

                    if searchData.date:
                        score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
                    else:
                        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()
        curID = PAutils.Encode(sceneURL)

        date = detailsPageElements.xpath('//span[@class="date"]')[0].text_content().strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    description = ''
    for desc in detailsPageElements.xpath('//div[@class="description"]//p'):
        description += desc.text_content().strip() + '\n\n'
    metadata.summary = description

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//p[@class="series"]')[0].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="date"]')[0].text_content().strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//meta[@name="keywords"]/@content')[0].split(','):
        genreName = genreLink.strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="model-wrap"]//li')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.xpath('.//h5')[0].text_content()
            actorPhotoURL = actorLink.xpath('.//img/@src')[0]

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="photo-wrap"]//@href',
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
