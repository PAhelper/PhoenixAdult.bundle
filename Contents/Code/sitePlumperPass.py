import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []

    url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded + '&sid=587'
    req = PAutils.HTTPRequest(url)
    siteSearchResults = HTML.ElementFromString(req.text)
    for searchResult in siteSearchResults.xpath('//div[@class="itemm"]'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/tour/%s' % searchResult.xpath('.//@href')[0]

        searchResults.append(sceneURL)

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for result in googleResults:
        pattern = re.search(r'(?<=\dpp\/).*(?=\/)', result)
        if pattern:
            sceneID = pattern.group(0)
            sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/t1/refstat.php?lid=%s&sid=584' % sceneID

            if ('content' in result) and sceneURL not in searchResults:
                searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        if ('content' in req.url):
            titleNoFormatting = detailsPageElements.xpath('//h1[@id="mve"]/span')[0].text_content().strip().replace('\"', '')
            curID = PAutils.Encode(sceneURL)
            date = detailsPageElements.xpath('//div[@class="movie-date"]')[0].text_content().strip()

            if date:
                releaseDate = parse(date).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''
            displayDate = releaseDate if date else ''

            if searchData.date and displayDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@id="mve"]/span')[0].text_content().strip().replace('\"', '')

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="movie-desc"]')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//meta[@name="keywords"]/@content')[0].split(','):
        genreName = genreLink.strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@id="pornstar-img"]')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.xpath('.//@alt')[0].strip()
            actorPhotoURL = PAsearchSites.getSearchBaseURL(siteNum) + '/t1/%s' % actorLink.xpath('.//@src')[0].strip()

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="movie-trailer"]//@src',
    ]

    videoImage = detailsPageElements.xpath('//div[@class="movie-big"]//script')[0].text_content()
    pattern = re.compile(r'(?<=image: ").*(?=")')
    if pattern.search(videoImage):
        imageID = pattern.search(videoImage).group(0)
        img = PAsearchSites.getSearchBaseURL(siteNum) + '/t1/%s' % imageID

        art.append(img)

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if 'http' not in img:
                img = PAsearchSites.getSearchBaseURL(siteNum) + '/t1/%s' % img

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
