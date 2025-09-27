import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = None
    parts = searchData.title.split()
    if unicode(parts[0], 'utf8').isdigit():
        sceneID = parts[0]
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + '/vrpornvideo/' + sceneID)
        searchResults = HTML.ElementFromString(req.text)
        titleNoFormatting = searchResults.xpath('//h1[contains(@class, "video-title")]')[0].text_content()
        curID = PAutils.Encode(PAsearchSites.getSearchBaseURL(siteNum) + '/vrpornvideo/' + sceneID)
        girlName = ''

        releaseDate = ''
        date = searchResults.xpath('//p[@itemprop="uploadDate"]/@content')
        if date:
            releaseDate = parse(date[0]).strftime('%Y-%m-%d')

        score = 100

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s in %s %s' % (PAsearchSites.getSearchSiteName(siteNum), girlName, titleNoFormatting, releaseDate), score=score, lang=lang))
    else:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@class="tile-grid-item"]'):
            titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//a[contains(@class, "video-card-title")]/@title')[0], siteNum)
            curID = PAutils.Encode(searchResult.xpath('.//a[contains(@class, "video-card-title")]/@href')[0])

            releaseDate = ''
            date = searchResult.xpath('.//span[@class="video-card-upload-date"]/@content')
            if date:
                releaseDate = parse(date[0]).strftime('%Y-%m-%d')
            girlName = searchResult.xpath('.//a[@class="video-card-link"]')[0].text_content()

            if searchData.date and releaseDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.replace('Parody', '').lower().strip())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s in %s %s' % (PAsearchSites.getSearchSiteName(siteNum), girlName, titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1[contains(@class, "video-title")]')[0].text_content().strip(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="video-description"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'BadoinkVR'

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    movieCollections.addCollection(tagline)

    # Release Date
    sceneDate = detailsPageElements.xpath('//p[@itemprop="uploadDate"]/@content')
    if sceneDate:
        date_object = parse(sceneDate[0])
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genreLink in detailsPageElements.xpath('//a[@class="video-tag"]'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actor(s)
    for actorLink in detailsPageElements.xpath('//a[contains(@class, "video-actor-link")]'):
        actorName = actorLink.text_content().strip()

        actorPageURL = PAsearchSites.getSearchBaseURL(siteNum) + actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        try:
            actorPhotoURL = actorPage.xpath('//img[@class="girl-details-photo"]/@src')[0].split('?')[0]
        except:
            actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL, gender='female')

    # Posters
    xpaths = [
        '//img[@class="video-image"]/@src',
        '//div[contains(@class, "gallery-item")]/@data-big-image'
    ]

    sceneBaseURL = detailsPageElements.xpath('//div[contains(@class, "gallery-item")]/@data-big-image')[0].rsplit('_', 1)[0].split('.jpg')[0]
    photoNum = int(detailsPageElements.xpath('//span[@class="gallery-zip-info"]/text()')[0].split('photos')[0].strip()) + 2
    for idx in range(1, photoNum):
        img = '%s_%d.jpg' % (sceneBaseURL, idx)

        art.append(img)

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            img = img.split('?')[0]

            if img not in art:
                art.append(img)

    images = []
    posterExists = False
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
                if height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                    posterExists = True
                if width > height:
                    # Item is an art item
                    images.append((image, posterUrl))
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                break
        elif PAsearchSites.posterOnlyAlreadyExists(posterUrl, metadata):
            posterExists = True

    if not posterExists:
        for idx, (image, posterUrl) in enumerate(images, 1):
            try:
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
