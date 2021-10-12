import PAsearchSites
import PAextras
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if ('/search/' not in sceneURL and '/page/' not in sceneURL and '/tag/' not in sceneURL and sceneURL not in searchResults):
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)
            if detailsPageElements.xpath('//meta[@property="og:type"]/@content')[0].strip() == 'video':
                titleNoFormatting = detailsPageElements.xpath('//meta[@property="og:title"]/@content')[0].strip()
                curID = PAutils.Encode(sceneURL)

                date = detailsPageElements.xpath('//div[@class="post_date"]')[0].text_content().strip()
                if date:
                    releaseDate = parse(date).strftime('%Y-%m-%d')
                else:
                    releaseDate = searchData.dateFormat() if searchData.date else ''
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
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)
    photosetPageElements = ''

    if sceneURL.endswith('-2/'):
        photosetURL = sceneURL.replace('-2/', '/')
        req = PAutils.HTTPRequest(photosetURL)
        photosetPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//meta[@property="og:title"]/@content')[0].strip()

    # Summary
    if photosetPageElements:
        description = photosetPageElements.xpath('//div[@class="video-embed"]/p')
        if description:
            metadata.summary = description[0].text_content().replace('<a href="/allfinegirls">18OnlyGirls</a>', '').strip()

    # Studio
    metadata.studio = '18OnlyGirls'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@itemprop="keywords"]//a'):
        genreName = genreLink.text_content().replace('Movies', '').strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@itemprop="actor"]//a')

    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            actorPageURL = 'https://18onlygirls.tv/models/' + actorName.replace(' ', '-')
            req = PAutils.HTTPRequest(actorPageURL)

            try:
                actorPage = HTML.ElementFromString(req.text)
                actorPhotoURL = actorPage.xpath('//div[@id="mod_info"]/img/@src')[0]
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteNum) + actorPhotoURL
            except:
                pass

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[contains(@id, "gallery")]//@href',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

    if photosetPageElements:
        for xpath in xpaths:
            for poster in photosetPageElements.xpath(xpath):
                art.append(poster)

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
                if width < height:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
