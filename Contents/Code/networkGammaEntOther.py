import PAsearchSites
import PAutils


def getAPIKey(siteNum):
    url = PAsearchSites.getSearchBaseURL(siteNum) + '/en/login'
    token_key = urlparse.urlparse(url).hostname

    token = None
    if token_key and token_key in Dict:
        data = Dict[token_key]
        data = base64.b64decode(data).decode('UTF-8')
        if 'validUntil=' in data:
            timestamp = int(data.split('validUntil=')[1].split('&')[0])
            if timestamp > time.time():
                token = Dict[token_key]

    if not token:
        req = PAutils.HTTPRequest(url)
        match = re.search(r'\"apiKey\":\"(.*?)\"', req.text)
        if match:
            token = match.group(1)

    if token_key and token:
        if token_key not in Dict or Dict[token_key] != token:
            Dict[token_key] = token
            Dict.Save()

    return token


def getAlgolia(url, indexName, params, referer):
    headers = {
        'Content-Type': 'application/json',
        'Referer': referer
    }
    params = json.dumps({'requests': [{'indexName': indexName, 'params': params}]})
    data = PAutils.HTTPRequest(url, headers=headers, params=params)
    data = data.json()

    return data['results'][0]['hits']


def search(results, lang, siteNum, searchData):
    searchData.title = searchData.encoded.replace('%20', ' ')
    sceneID = searchData.title.split(' ', 1)[0]
    if unicode(sceneID, 'UTF-8').isdigit():
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    apiKEY = getAPIKey(siteNum)
    for sceneType in ['scenes', 'movies']:
        url = PAsearchSites.getSearchSearchURL(siteNum) + '?x-algolia-application-id=TSMKFA364Q&x-algolia-api-key=' + apiKEY
        if sceneID and not searchData.title:
            if sceneType == 'scenes':
                params = 'filters=clip_id=' + sceneID
            else:
                params = 'filters=movie_id=' + sceneID
        else:
            params = 'query=' + searchData.title

        searchResults = getAlgolia(url, 'all_' + sceneType, params, PAsearchSites.getSearchBaseURL(siteNum))
        for searchResult in searchResults:
            if sceneType == 'scenes':
                releaseDate = parse(searchResult['release_date'])
                curID = searchResult['clip_id']
            else:
                date = 'last_modified' if searchResult['last_modified'] else 'date_created'
                releaseDate = parse(searchResult[date])
                curID = searchResult['movie_id']

            titleNoFormatting = searchResult['title']
            releaseDate = releaseDate.strftime('%Y-%m-%d')

            if sceneID:
                score = 100 - Util.LevenshteinDistance(sceneID, curID)
            elif searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%d|%d|%s|%s' % (curID, siteNum, sceneType, releaseDate), name='[%s] %s %s' % (sceneType.capitalize(), titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneID = int(metadata_id[0])
    sceneType = metadata_id[2]
    sceneIDName = 'clip_id' if sceneType == 'scenes' else 'movie_id'
    sceneDate = metadata_id[3]

    apiKEY = getAPIKey(siteNum)

    url = PAsearchSites.getSearchSearchURL(siteNum) + '?x-algolia-application-id=TSMKFA364Q&x-algolia-api-key=' + apiKEY
    data = getAlgolia(url, 'all_' + sceneType, 'filters=%s=%d' % (sceneIDName, sceneID), PAsearchSites.getSearchBaseURL(siteNum))
    detailsPageElements = data[0]

    data = getAlgolia(url, 'all_scenes', 'query=%s' % detailsPageElements['url_title'], PAsearchSites.getSearchBaseURL(siteNum))
    data = sorted(data, key=lambda i: i['clip_id'])
    scenesPagesElements = list(enumerate(data, 1))

    # Title
    title = None
    if sceneType == 'scenes' and len(scenesPagesElements) > 1:
        for idx, scene in scenesPagesElements:
            if scene['clip_id'] == sceneID:
                title = '%s, Scene %d' % (detailsPageElements['title'], idx)
                break
    if not title:
        title = detailsPageElements['title']

    metadata.title = title

    # Summary
    metadata.summary = detailsPageElements['description'].replace('</br>', '\n').replace('<br>', '\n')

    # Studio
    metadata.studio = detailsPageElements['network_name']

    # Tagline and Collection(s)
    metadata.collections.clear()
    for collectionName in ['studio_name', 'serie_name']:
        if collectionName in detailsPageElements:
            metadata.collections.add(detailsPageElements[collectionName])
    if (':' in detailsPageElements['title'] or '#' in detailsPageElements['title']) and len(scenesPagesElements) > 1:
        if 'movie_title' in detailsPageElements:
            metadata.collections.add(detailsPageElements['movie_title'])

    # Release Date
    date_object = parse(sceneDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements['categories']:
        genreName = genreLink['name']
        if genreName:
            movieGenres.addGenre(genreName)

    if sceneType == 'movies':
        for idx, scene in scenesPagesElements:
            for genreLink in scene['categories']:
                genreName = genreLink['name']
                if genreName:
                    movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    female = []
    male = []
    for actorLink in detailsPageElements['actors']:
        actorName = actorLink['name']

        actorData = getAlgolia(url, 'all_actors', 'filters=actor_id=' + actorLink['actor_id'], PAsearchSites.getSearchBaseURL(siteNum))[0]
        if 'pictures' in actorData and actorData['pictures']:
            max_quality = sorted(actorData['pictures'].keys())[-1]
            actorPhotoURL = 'https://images-fame.gammacdn.com/actors' + actorData['pictures'][max_quality]
        else:
            actorPhotoURL = ''

        if actorLink['gender'] == 'female':
            female.append((actorName, actorPhotoURL))
        else:
            male.append((actorName, actorPhotoURL))

    combined = female + male
    for actor in combined:
        movieActors.addActor(actor[0], actor[1])

    # Posters
    art = []

    if not PAsearchSites.getSearchBaseURL(siteNum).endswith(('girlsway.com', 'puretaboo.com')):
        art.append('https://images-fame.gammacdn.com/movies/{0}/{0}_{1}_front_400x625.jpg'.format(detailsPageElements['movie_id'], detailsPageElements['url_title'].lower().replace('-', '_')))
        if 'url_movie_title' in detailsPageElements:
            art.append('https://images-fame.gammacdn.com/movies/{0}/{0}_{1}_front_400x625.jpg'.format(detailsPageElements['movie_id'], detailsPageElements['url_movie_title'].lower().replace('-', '_')))

    if 'pictures' in detailsPageElements and detailsPageElements['pictures']:
        max_quality = detailsPageElements['pictures']['nsfw']['top'].keys()[0]
        pictureURL = 'https://images-fame.gammacdn.com/movies/' + detailsPageElements['pictures'][max_quality]

        if sceneType == 'movies':
            art.append(pictureURL)
        else:
            art.insert(0, pictureURL)

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
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
