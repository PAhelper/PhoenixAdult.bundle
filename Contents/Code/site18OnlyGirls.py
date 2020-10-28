import PAsearchSites
import PAgenres
import PAactors
import PAextras
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.replace(' ', '+').replace('--', '+').lower()
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)

    for searchResult in searchResults.xpath('//li[contains(@class, "box-shadow")][.//*[contains(@class, "video")]]//a[@href]'):
        titleNoFormatting = searchResult.xpath('.//@title')[0].strip()
        sceneURL = searchResult.xpath('.//@href')[0]
        curID = PAutils.Encode(sceneURL)

        req = PAutils.HTTPRequest(sceneURL)
        sceneResult = HTML.ElementFromString(req.text)

        date = sceneResult.xpath('//div[@class="post_date"]')[0].text_content().strip()
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
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
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

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
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
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
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ''

            actorPageURL = 'https://18onlygirls.tv/models/' + actorName.replace(' ', '-')
            req = PAutils.HTTPRequest(actorPageURL)

            try:
                actorPage = HTML.ElementFromString(req.text)
                actorPhotoURL = actorPage.xpath('//div[@id="mod_info"]/img/@src')[0]
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
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
