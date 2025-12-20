import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []
    searchData.encoded = searchData.title.replace(' ', '+')

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchPageElements = HTML.ElementFromString(req.text)

    googleResults = PAutils.getFromSearchEngine(searchData.title, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.split('?')[0]
        if 'com/video/' in sceneURL and 'index.php/' not in sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for searchURL in searchResults:
        req = PAutils.HTTPRequest(searchURL)
        detailsPageElements = HTML.ElementFromString(req.text)
        
        videoPageElements = None
        json_ld_scripts = detailsPageElements.xpath('//script[@type="application/ld+json"]')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.text_content().replace('\n', '').strip())
                if data.get('@type') == 'VideoObject':
                    videoPageElements = data
                    break
            except:
                pass

        if videoPageElements:
            titleNoFormatting = PAutils.parseTitle(PAutils.cleanHTML(videoPageElements['name']), siteNum)
            curID = PAutils.Encode(searchURL)

            date = videoPageElements.get('datePublished')
            if date:
                releaseDate = parse(date).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''
            displayDate = releaseDate if date else ''

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))

    for searchResult in searchPageElements.xpath('//div[contains(@class, "movie-preview") or contains(@class, "video_container")]'):
        sceneURL = searchResult.xpath('./a[contains(@class, "group")]/@href')[0]
        if 'dvd' in sceneURL:
            titleNoFormatting = PAutils.parseTitle(searchResult.xpath('./a/div')[0].text_content().strip(), siteNum)
        else:
            titleNoFormatting = PAutils.parseTitle(searchResult.xpath('./a/span')[0].text_content().strip(), siteNum)

        if 'http' not in sceneURL:
            sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
        curID = PAutils.Encode(sceneURL)

        date = searchResult.xpath('.//span[@class="hidden xs:inline-block truncate"]')
        if date:
            releaseDate = datetime.strptime(date[0].text_content().split('\xe2\x80\xa2')[-1].strip(), '%b %d, %Y').strftime('%Y-%m-%d')
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        displayDate = releaseDate if date else ''

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        if sceneURL not in searchResults:
            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    videoPageElements = None
    json_ld_scripts = detailsPageElements.xpath('//script[@type="application/ld+json"]')
    for script in json_ld_scripts:
        try:
            data = json.loads(script.text_content().replace('\n', '').strip())
            if data.get('@type') == 'VideoObject':
                videoPageElements = data
                break
        except:
            pass

    # Title
    if videoPageElements:
        metadata.title = PAutils.parseTitle(PAutils.cleanHTML(videoPageElements['name']), siteNum)
    elif detailsPageElements.xpath('//h1'):
        metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content().strip(), siteNum)

    # Summary
    if videoPageElements:
        metadata.summary = PAutils.cleanHTML(videoPageElements['description'])
    elif detailsPageElements.xpath('//div[contains(@class, "description")]'):
        metadata.summary = detailsPageElements.xpath('//div[contains(@class, "description")]')[0].text_content().strip()
    elif detailsPageElements.xpath('//meta[@name="description"]/@content'):
        metadata.summary = detailsPageElements.xpath('//meta[@name="description"]/@content')[0].strip()
    elif detailsPageElements.xpath('//meta[@property="og:description"]/@content'):
        metadata.summary = detailsPageElements.xpath('//meta[@property="og:description"]/@content')[0].strip()

    # Studio
    if videoPageElements and 'productionCompany' in videoPageElements and 'name' in videoPageElements['productionCompany']:
        metadata.studio = re.sub(r'bang(?=(\s|$))(?!\!)', 'Bang!', PAutils.parseTitle(videoPageElements['productionCompany']['name'].strip(), siteNum), flags=re.IGNORECASE)
    else:
        metadata.studio = 'Bang!'

    # Tagline and Collection(s)
    tagline = ""
    dvdTitle = ""
    try:
        tagline = re.sub(r'bang(?=(\s|$))(?!\!)', 'Bang!', PAutils.parseTitle(detailsPageElements.xpath('//p[contains(., "eries:")]/a[contains(@href, "originals") or contains(@href, "videos")]')[0].text_content().strip(), siteNum), flags=re.IGNORECASE)
    except:
        pass

    if tagline:
        metadata.tagline = tagline
        movieCollections.addCollection(tagline)
    else:
        movieCollections.addCollection(metadata.studio)

    try:
        dvdTitle = PAutils.parseTitle(detailsPageElements.xpath('//p[contains(., "Movie")]/a[contains(@href, "dvd")]')[0].text_content(), siteNum)
    except:
        pass

    if dvdTitle and siteNum == 1365:
        movieCollections.addCollection(dvdTitle)

    # Release Date
    date = None
    if videoPageElements:
        date = videoPageElements.get('datePublished')
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    elif sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actor(s)
    if siteNum == 1365:
        actorXpath = '//div[contains(@class, "clear-both")]//a[contains(@href, "pornstar")]'
    else:
        actorXpath = '//div[contains(@class, "name")]/a[contains(@href, "pornstar") and not(@aria-label)]'

    for actorLink in detailsPageElements.xpath(actorXpath):
        actorPhotoURL = ''
        if siteNum == 1365:
            actorName = actorLink.text_content()

            modelURL = PAsearchSites.getSearchBaseURL(siteNum) + actorLink.xpath('.//@href')[0]
            req = PAutils.HTTPRequest(modelURL)
            modelPage = HTML.ElementFromString(req.text)

            try:
                modelPageElements = json.loads(modelPage.xpath('//script[@type="application/ld+json"][contains(., "Person")]')[0].text_content().strip())
                actorPhotoURL = modelPageElements['image'].split('?')[0].strip()
            except:
                pass
        else:
            actorName = actorLink.xpath('.//span')[0].text_content()
            try:
                img = actorLink.xpath('../..//img/@src')[0].split('?')[0]
                if 'placeholder' not in img:
                    actorPhotoURL = img
            except:
                pass

        if actorName:
            movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    for genreLink in detailsPageElements.xpath('//div[@class="actions"]/a | //a[@class="genres"]'):
        genreName = genreLink.text_content()

        movieGenres.addGenre(genreName)

    # Posters
    if videoPageElements and 'thumbnailUrl' in videoPageElements:
        if 'covers' in videoPageElements['thumbnailUrl']:
            art.append(videoPageElements['thumbnailUrl'])
        else:
            match = re.search(r'(?<=shots/)\d+', videoPageElements['thumbnailUrl'])
            if match:
                movieID = match.group(0)
                art.append('https://i.bang.com/covers/%s/front.jpg' % movieID)
            art.append(videoPageElements['thumbnailUrl'])

    if videoPageElements and 'trailer' in videoPageElements:
        for img in videoPageElements['trailer']:
            if 'thumbnailUrl' in img:
                art.append(img['thumbnailUrl'])

    # Fallback for posters
    if not art:
        xpaths = [
            '//meta[@property="og:image"]/@content',
            '//video/@poster',
            '//img[contains(@class, "object-cover aspect-cover mx-auto")]/@src',
            '//img[contains(@class, "object-cover aspect-cover mx-auto")]/@srcset',
            '//img[contains(@class, "w-full h-auto object-cover rounded-md")]/@src'
        ]
        for xpath in xpaths:
            for img in detailsPageElements.xpath(xpath):
                if 'srcset' in xpath:
                    for url in img.split(','):
                        art.append(url.strip().split(' ')[0].split('?')[0])
                else:
                    art.append(img.split('?')[0])

    images = []
    posterExists = False
    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            posterUrl = posterUrl.split('?')[0]
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
