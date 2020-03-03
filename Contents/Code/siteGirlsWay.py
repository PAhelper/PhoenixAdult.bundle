import PAsearchSites
import PAgenres
import PAactors


def getAPIKey(url):
    req = urllib.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    data = urllib.urlopen(req).read()

    return re.search(r'\"apiKey\":\"(.*?)\"', data).group(1)


def getAlgolia(url, indexName, params, referer):
    params = json.dumps({'requests':[{'indexName': indexName,'params': params}]})
    req = urllib.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Referer', referer)
    data = urllib.urlopen(req, params).read()

    return json.loads(data)


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    sceneID = searchTitle.split(' ', 1)[0]
    if unicode(sceneID, 'utf8').isdigit():
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    apiKEY = getAPIKey(PAsearchSites.getSearchBaseURL(siteNum))
    url = PAsearchSites.getSearchSearchURL(siteNum) + '?x-algolia-application-id=TSMKFA364Q&x-algolia-api-key=' + apiKEY
    params = 'filters=clip_id=' + sceneID if sceneID and not searchTitle else 'query=' + searchTitle
    data = getAlgolia(url, 'all_scenes', params, PAsearchSites.getSearchBaseURL(siteNum))

    searchResults = data['results'][0]['hits']
    for searchResult in searchResults:
        curID = searchResult['clip_id']
        titleNoFormatting = searchResult['title']
        releaseDate = parse(searchResult['release_date']).strftime('%Y-%m-%d')

        if sceneID:
            score = 100 - Util.LevenshteinDistance(sceneID, curID)
        elif searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%d|%d' % (curID, siteNum), name='%s %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')

    sceneID = metadata_id[0]
    apiKEY = getAPIKey(PAsearchSites.getSearchBaseURL(siteID))
    urlParams = '?x-algolia-application-id=TSMKFA364Q&x-algolia-api-key=' + apiKEY

    url = PAsearchSites.getSearchSearchURL(siteID) + urlParams
    data = getAlgolia(url, 'all_scenes', 'filters=clip_id=' + sceneID, PAsearchSites.getSearchBaseURL(siteID))
    detailsPageElements = data['results'][0]['hits'][0]

    # Studio
    metadata.studio = detailsPageElements['studio_name']

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = detailsPageElements['description']

    # Release Date
    date_object = parse(detailsPageElements['release_date'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Tagline and Collection(s)
    metadata.collections.clear()
    for collectionName in ['studio_name', 'serie_name']:
        metadata.collections.add(detailsPageElements[collectionName])

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements['categories']
    for genreLink in genres:
        genreName = genreLink['name']
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements['actors']
    for actorLink in actors:
        url = PAsearchSites.getSearchSearchURL(siteID) + urlParams
        data = getAlgolia(url, 'all_actors', 'filters=actor_id=' + actorLink['actor_id'], PAsearchSites.getSearchBaseURL(siteID))
        actorData = data['results'][0]['hits'][0]
        actorName = actorData['name']
        if actorData['pictures']:
            max_quality = sorted(actorData['pictures'].keys())[-1]
            actorPhotoURL = 'https://images-fame.gammacdn.com/actors' + actorData['pictures'][max_quality]
        else:
            actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    if 'pictures' in detailsPageElements:
        max_quality = sorted(detailsPageElements['pictures'].keys())[-4]
        art.append('https://images-fame.gammacdn.com/movies/' + detailsPageElements['pictures'][max_quality])

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
