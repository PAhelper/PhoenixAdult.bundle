import PAsearchSites
import PAgenres
import PAactors


def getAPIKey(url):
    req = urllib.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    data = urllib.urlopen(req).read()
    match = re.search(r'\"apiKey\":\"(.*?)\"', data)
    if match:
        return match.group(1)
    return None


def getAlgolia(url, indexName, params, referer):
    params = json.dumps({'requests':[{'indexName': indexName,'params': params}]})
    req = urllib.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Referer', referer)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    data = urllib.urlopen(req, params).read()

    return json.loads(data)


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    sceneID = searchTitle.split(' ', 1)[0]
    if unicode(sceneID, 'utf8').isdigit():
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    apiKEY = getAPIKey(PAsearchSites.getSearchBaseURL(siteNum))
    for sceneType in ['scenes', 'movies']:
        url = PAsearchSites.getSearchSearchURL(siteNum) + '?x-algolia-application-id=TSMKFA364Q&x-algolia-api-key=' + apiKEY
        if sceneID and not searchTitle:
            if sceneType == 'scenes':
                params = 'filters=clip_id=' + sceneID
            else:
                params = 'filters=movie_id=' + sceneID
        else:
            params = 'query=' + searchTitle

        data = getAlgolia(url, 'all_' + sceneType, params, PAsearchSites.getSearchBaseURL(siteNum))

        searchResults = data['results'][0]['hits']
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
            elif searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%d|%d|%s|%s' % (curID, siteNum, sceneType, releaseDate), name='[%s] %s %s' % (sceneType.capitalize(), titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneID = int(metadata_id[0])
    sceneType = metadata_id[2]
    sceneIDName = 'clip_id' if sceneType == 'scenes' else 'movie_id'
    sceneDate = metadata_id[3]

    apiKEY = getAPIKey(PAsearchSites.getSearchBaseURL(siteID))

    url = PAsearchSites.getSearchSearchURL(siteID) + '?x-algolia-application-id=TSMKFA364Q&x-algolia-api-key=' + apiKEY
    data = getAlgolia(url, 'all_' + sceneType, 'filters=%s=%d' % (sceneIDName, sceneID), PAsearchSites.getSearchBaseURL(siteID))
    detailsPageElements = data['results'][0]['hits'][0]

    # Studio
    metadata.studio = detailsPageElements['network_name']

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = detailsPageElements['description'].replace('</br>', '\n')

    # Release Date
    date_object = parse(sceneDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Tagline and Collection(s)
    metadata.collections.clear()
    for collectionName in ['studio_name', 'serie_name']:
        if collectionName in detailsPageElements:
            metadata.collections.add(detailsPageElements[collectionName])
    if ':' in detailsPageElements['title'] or '#' in detailsPageElements['title']:
        if 'movie_title' in detailsPageElements:
            metadata.collections.add(detailsPageElements['movie_title'])

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements['categories']:
        genreName = genreLink['name']
        if genreName:
            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements['actors']:
        actorName = actorLink['name']

        data = getAlgolia(url, 'all_actors', 'filters=actor_id=' + actorLink['actor_id'], PAsearchSites.getSearchBaseURL(siteID))
        actorData = data['results'][0]['hits'][0]
        if actorData['pictures']:
            max_quality = sorted(actorData['pictures'].keys())[-1]
            actorPhotoURL = 'https://images-fame.gammacdn.com/actors' + actorData['pictures'][max_quality]
        else:
            actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    if not PAsearchSites.getSearchBaseURL(siteID).endswith(('girlsway.com', 'puretaboo.com')):
        art.append('https://images-fame.gammacdn.com/movies/{0}/{0}_{1}_front_400x625.jpg'.format(detailsPageElements['movie_id'], detailsPageElements['url_title'].lower().replace('-', '_')))

    if 'pictures' in detailsPageElements:
        keys = [key for key in detailsPageElements['pictures'].keys() if key[0].isdigit()]
        max_quality = sorted(keys)[-1]
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
