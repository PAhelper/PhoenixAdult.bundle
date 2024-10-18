import PAsearchSites
import PAutils


def getSearchFromForm(query, siteNum):
    params = {
        'keywords': query,
        's_filters[type]': 'videos',
        's_filters[site]': 'current'
    }
    searchURL = '%s/search-es' % PAsearchSites.getSearchBaseURL(siteNum)
    req = PAutils.HTTPRequest(searchURL, params=params)
    data = HTML.ElementFromString(req.text)

    return data


def search(results, lang, siteNum, searchData):
    searchResults = []
    searchPageResults = []
    searchID = None

    parts = searchData.title.split()
    if unicode(parts[0], 'UTF-8').isdigit():
        sceneID = parts[0]
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
    else:
        sceneID = re.sub(r'\D', '', searchData.title)
        actorName = re.sub(r'\s\d.*', '', searchData.title).replace(' ', '-')
        directURL = '%s%s/%s/' % (PAsearchSites.getSearchSearchURL(siteNum), actorName, sceneID)
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
        searchResults.append(directURL)

    urlID = PAsearchSites.getSearchSearchURL(siteNum).replace(PAsearchSites.getSearchBaseURL(siteNum), '')

    searchPageElements = getSearchFromForm(searchData.title, siteNum)
    for searchResult in searchPageElements.xpath('//div[contains(@class, "compact video")]'):
        titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//a[contains(@class, "title")]')[0].text_content().strip(), siteNum)
        sceneURL = searchResult.xpath('.//a[contains(@class, "title")]/@href')[0].strip().split('?')[0]
        curID = PAutils.Encode(sceneURL)
        searchPageResults.append(sceneURL)
        match = re.search(r'(?<=\/)\d+(?=\/)', sceneURL)
        if match:
            searchID = match.group(0)

        releaseDate = searchData.dateFormat() if searchData.date else ''

        if searchID and searchID == sceneID:
            score = 100
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if urlID in sceneURL and '?' not in sceneURL and sceneURL not in searchResults and sceneURL not in searchPageResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        scenePageElements = HTML.ElementFromString(req.text)
        titleNoFormatting = PAutils.parseTitle(scenePageElements.xpath('//h1')[0].text_content().strip(), siteNum)

        if '404' not in titleNoFormatting and not re.search('Latest.*Videos', titleNoFormatting):
            match = re.search(r'(?<=\/)\d+(?=\/)', sceneURL)
            if match:
                searchID = match.group(0)

            curID = PAutils.Encode(sceneURL)

            date = scenePageElements.xpath('//div[./span[contains(., "Date:")]]//span[@class="value"]')
            if date:
                releaseDate = parse(date[0].text_content().strip()).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''
            displayDate = releaseDate if date else ''

            if searchID and searchID == sceneID:
                score = 100
            elif searchData.date and displayDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content().strip(), siteNum)

    # Summary
    summary_xpaths = [
        '//div[@class="p-desc"]',
        '//div[contains(@class, "desc")]'
    ]

    for xpath in summary_xpaths:
        for summary in detailsPageElements.xpath(xpath):
            metadata.summary = summary.text_content().replace('Read More »', '').strip()
            break

    # Studio
    metadata.studio = 'Score Group'

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(metadata.tagline)

    # Release Date
    try:
        date = detailsPageElements.xpath('//div/span[@class="value"]')[1].text_content().strip()
    except:
        date = None
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    elif sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actor(s)
    for actorLink in detailsPageElements.xpath('//div/span[@class="value"]/a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    if siteNum == 1344:
        movieActors.addActor('Christy Marks', '')

    # Genres
    for genreLink in detailsPageElements.xpath('//div[@class="mb-3"]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Posters/Background
    match = re.search(r'posterImage: \'(.*)\'', req.text)
    if match:
        art.append(match.group(1))

    xpaths = [
        '//script[@type]/text()',
        '//div[contains(@class, "thumb")]/img/@src',
        '//div[contains(@class, "p-image")]/a/img/@src',
        '//div[contains(@class, "dl-opts")]/a/img/@src',
        '//div[contains(@class, "p-photos")]/div/div/a/@href',
        '//div[contains(@class, "gallery")]/div/div/a/@href'
    ]

    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            match = re.search(r'(?<=(poster: \')).*(?=\')', poster)
            if match:
                poster = match.group(0)

            if not poster.startswith('http'):
                poster = 'http:' + poster

            if 'PosterThumbs' in poster:
                match = re.search(r'(?<=PosterThumbs)\/\d\d', poster)
                if match:
                    for idx in range(1, 7):
                        art.append(poster.replace(match.group(0), '/{0:02d}'.format(idx)))
            elif 'shared-bits' not in poster and '/join' not in poster:
                art.append(poster)

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
