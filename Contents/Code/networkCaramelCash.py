import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = searchData.title.split(' ', 1)[0]
    if unicode(sceneID, 'UTF-8').isdigit():
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    searchResults = []
    if sceneID:
        directURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneID
        searchResults.append(directURL)

    googleResults = PAutils.getFromSearchEngine(searchData.title, siteNum)
    for sceneURL in googleResults:
        if ('video/' in sceneURL or 'videos/' in sceneURL) and '/page/' not in sceneURL and sceneURL not in searchResults:
            searchResults.append(sceneURL.split('?')[0])

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)
            titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content(), siteNum)
            if 'http' not in sceneURL:
                sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneID
            curID = PAutils.Encode(sceneURL)

            date = detailsPageElements.xpath('//div[@class="content-date"]')
            if date:
                releaseDate = datetime.strptime(date[0].text_content().strip(), '%d.%m.%Y').strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''

            displayDate = releaseDate if date else ''

            if searchData.date and releaseDate:
                score = 80 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 80 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='[%s] %s %s' % (PAsearchSites.getSearchSiteName(siteNum), titleNoFormatting, displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//div[contains(@class, "content-title")]')[0].text_content().strip(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "content-desc")]')[1].text_content().strip()

    # Studio
    metadata.studio = 'Caramel Cash'

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    movieCollections.addCollection(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class, "content-date")]')
    if date:
        if (1041 <= siteNum <= 1042):
            cleanDate = re.sub(r'(\d)(st|nd|rd|th)', r'\1', date[0].text_content().split(':')[-1].strip())
            date_object = datetime.strptime(cleanDate, '%d %b %Y')
        else:
            date_object = datetime.strptime(date[0].text_content().strip(), '%d.%m.%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    genres = detailsPageElements.xpath('//div[@class="content-tags"]/a')
    for genreLink in genres:
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actor(s)
    actors = detailsPageElements.xpath('//section[@class="content-sec backdrop"]//div[@class="main__models"]/a')
    for actorLink in actors:
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters/Background
    xpaths = [
        '//section[@class="content-gallery-sec"]//a[@data-lightbox="gallery"]/@href'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            art.append(img)

    Log('Artwork found: %d' % len(art))
    images = []
    posterExists = False
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
                if width > 100 and width > height:
                    # Item is an art item
                    images.append((image, posterUrl))
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass
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
