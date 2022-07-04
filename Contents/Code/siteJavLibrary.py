import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchJAVID = None
    splitSearchTitle = searchData.title.split()
    if splitSearchTitle[0].startswith('3dsvr'):
        splitSearchTitle[0] = splitSearchTitle[0].replace('3dsvr', 'dsvr')
    elif splitSearchTitle[0].startswith('13dsvr'):
        splitSearchTitle[0] = splitSearchTitle[0].replace('13dsvr', 'dsvr')

    if len(splitSearchTitle) > 1:
        if unicode(splitSearchTitle[1], 'UTF-8').isdigit():
            searchJAVID = '%s%%2B%s' % (splitSearchTitle[0], splitSearchTitle[1])

    if searchJAVID:
        searchData.encoded = searchJAVID

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    if req.status_code == 302 or req.status_code == 200:
        searchResult = HTML.ElementFromString(req.text)
        titleNoFormatting = searchResult.xpath('//h3[@class="post-title text"]/a')[0].text_content().strip()
        JAVID = searchResult.xpath('//td[contains(text(), "ID:")]/following-sibling::td')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('//meta[@property="og:url"]/@content')[0].strip())
        score = 100 - Util.LevenshteinDistance(searchJAVID.lower(), JAVID.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s' % (JAVID, titleNoFormatting), score=score, lang=lang))

    else:
        searchResultsURLs = []
        googleResults = PAutils.getFromGoogleSearch('%s %s' % (splitSearchTitle[0], splitSearchTitle[1]), siteNum)
        for sceneURL in googleResults:
            if sceneURL not in searchResultsURLs:
                if '?v=jav' in sceneURL and sceneURL not in searchResultsURLs:
                    englishSceneURL = sceneURL.replace('/ja/', '/en/').replace('/tw/', '/en/').replace('/cn/', '/en/')
                    searchResultsURLs.append(englishSceneURL)

        for sceneURL in searchResultsURLs:
            req = PAutils.HTTPRequest(sceneURL)
            if req.ok:
                try:
                    searchResult = HTML.ElementFromString(req.text)
                    titleNoFormatting = searchResult.xpath('//h3[@class="post-title text"]/a')[0].text_content().strip()
                    JAVID = searchResult.xpath('//td[contains(text(), "ID:")]/following-sibling::td')[0].text_content().strip()
                    curID = PAutils.Encode(searchResult.xpath('//meta[@property="og:url"]/@content')[0].strip().replace('//www', 'https://www'))
                    score = 100 - Util.LevenshteinDistance(searchJAVID.lower(), JAVID.lower())

                    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s' % (JAVID, titleNoFormatting),score=score, lang=lang))
                except:
                    pass

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL_broken = PAutils.Decode(metadata_id[0])
    # No idea why but metadata_id[0] is base58 of the URL without the schema
    # part for some reason
    sceneURL = "https:" + sceneURL_broken
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h3[@class="post-title text"]/a')[0].text_content().strip()

    # Studio
    maybeStudio = detailsPageElements.xpath('//td[contains(text(), "Maker:")]/following-sibling::td/span/a')
    if maybeStudio:
        metadata.studio = maybeStudio[0].text_content().strip()

    # Director
    director = metadata.directors.new()
    maybeDirectorName = detailsPageElements.xpath('//td[contains(text(), "Director:")]/following-sibling::td/span/a')
    if maybeDirectorName:
        director.name = maybeDirectorName[0].text_content().strip()

    # Release Date
    maybeDate = detailsPageElements.xpath('//td[contains(text(), "Release Date:")]/following-sibling::td')
    if maybeDate:
        date_object = datetime.strptime(maybeDate[0].text_content().strip(), '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actor in detailsPageElements.xpath('//span[@class="star"]/a'):
        actorName = actor.text_content().strip()

        movieActors.addActor(actorName, '')

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//a[@rel="category tag"]'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    metadata.collections.add('Japan Adult Video')

    # Poster
    posterURL = detailsPageElements.xpath('//img[@id="video_jacket_img"]/@src')[0]

    art.append(posterURL)

    # Images
    urlRegEx = re.compile(r'-([1-9]+).jpg')
    for image in detailsPageElements.xpath('//div[@class="previewthumbs"]/img'):
        thumbnailURL = image.get('src')
        idxSearch = urlRegEx.search(thumbnailURL)
        if idxSearch:
            imageURL = thumbnailURL[:idxSearch.start()] + 'jp' + thumbnailURL[idxSearch.start():]
            art.append(imageURL)
        else:
            art.append(thumbnailURL)

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
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
