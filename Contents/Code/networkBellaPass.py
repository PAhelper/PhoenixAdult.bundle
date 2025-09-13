import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.lower().replace(' ', '-')
    directURL = PAsearchSites.getSearchSearchURL(siteNum).replace('/search.php?query=', '/trailers/') + searchData.encoded + '.html'

    directResults = [directURL]

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "item-video")]'):
        sceneURL = searchResult.xpath('./div[1]//a/@href')[0]

        time = searchResult.xpath('.//div[contains(@class, "time")]/text()')[0].strip()
        if time.replace(':', '').isdigit():
            if not sceneURL.startswith('http'):
                sceneURL = 'http:' + sceneURL
            directResults.append(sceneURL)

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if '/trailers/' in sceneURL and sceneURL not in searchResults:
            directResults.append(sceneURL)

    for sceneURL in directResults:
        try:
            req = PAutils.HTTPRequest(sceneURL)
            detailsPageElements = HTML.ElementFromString(req.text)

            titleNoFormatting = detailsPageElements.xpath('//h1 | //h3')[0].text_content().strip()
            curID = PAutils.Encode(sceneURL)

            date = detailsPageElements.xpath('//div[contains(@class, "videoInfo")]/p/text()')
            if date:
                releaseDate = parse(date[0].strip()).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''

            displayDate = releaseDate if date else ''

            if searchData.date and displayDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))
        except:
            pass

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    if siteNum in [1246, 1553]:
        metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content().strip(), siteNum)
    else:
        metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h3')[0].text_content().strip(), siteNum)

    # Summary
    description = detailsPageElements.xpath('//div[contains(@class, "videoDetails")]//p')
    if description:
        metadata.summary = description[0].text_content().strip()

    # Studio, Tagline and Collection(s)
    if PAsearchSites.getSearchSiteName(siteNum) in ['Hussie Pass', 'Babe Archives', 'See Him Fuck']:
        tagline = PAsearchSites.getSearchSiteName(siteNum)
        metadata.studio = tagline
    else:
        metadata.studio = 'BellaPass'
        tagline = PAsearchSites.getSearchSiteName(siteNum)
        metadata.tagline = tagline
    movieCollections.addCollection(tagline)

    # Genres
    for genreLink in detailsPageElements.xpath('//div[contains(@class, "featuring")]//a[contains(@href, "/categories/")]'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actor(s)
    actors = detailsPageElements.xpath('//div[contains(@class, "featuring")]//a[contains(@href, "/models/")]')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        re_actorName = re.compile(r' *?[^\w\s]+')
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorName = re_actorName.sub('', actorName).strip()

            actorPageURL = actorLink.get('href')
            if actorPageURL.startswith('//'):
                actorPageURL = 'https:' + actorPageURL
            elif not actorPageURL.startswith('http'):
                actorPageURL = PAsearchSites.getSearchBaseURL(siteNum) + actorPageURL

            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            actorPhotoURL = PAsearchSites.getSearchBaseURL(siteNum) + actorPage.xpath('//div[@class="profile-pic"]/img/@src0_3x')[0]

            movieActors.addActor(actorName, actorPhotoURL)

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class, "videoInfo")]/p/text()')
    if date:
        releaseDate = parse(date[0].strip()).strftime('%Y-%m-%d')
    else:
        releaseDate = sceneDate

    if releaseDate:
        date_object = parse(releaseDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Posters
    xpaths = [
        '//img[contains(@class, "thumbs")]/@src0_3x',
        '//div[contains(@class, "item-thumb")]//img/@src0_3x',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if not img.startswith('http'):
                img = PAsearchSites.getSearchBaseURL(siteNum) + img
            art.append(img)

    setID = detailsPageElements.xpath('//img[contains(@class, "thumbs")]/@id | //div[contains(@class, "item-thumb")]//img/@id')
    if setID:
        setID = setID[0]

        # Search Page
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + metadata.title.replace(' ', '+'))
        searchPageElements = HTML.ElementFromString(req.text)
        cnt = searchPageElements.xpath('//img[@id="%s"]/@cnt' % setID)
        if cnt:
            for i in range(int(cnt[0])):
                img = searchPageElements.xpath('//img[@id="%s"]/@src%d_3x' % (setID, i))
                if img:
                    art.append(PAsearchSites.getSearchBaseURL(siteNum) + img[0])

        # Photo page
        req = PAutils.HTTPRequest(sceneURL.replace('/trailers/', '/preview/'))
        photoPageElements = HTML.ElementFromString(req.text)
        for image in photoPageElements.xpath('//img[@id="%s"]/@src0_3x' % setID):
            art.append(PAsearchSites.getSearchBaseURL(siteNum) + image)

    images = []
    posterExists = False
    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
                im = StringIO(image.content)
                images.append(image)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                    posterExists = True
                if width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    if not posterExists:
        for idx, image in enumerate(images, 1):
            try:
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[art[idx - 1]] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
