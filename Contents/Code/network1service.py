import PAsearchSites
import PAgenres
import PAactors
import PAutils


def get_Token(siteID):
    token_key = None
    if siteID == 2 or (siteID >= 54 and siteID <= 81) or siteID == 582 or siteID == 690:
        token_key = 'brazzers_token'

    token = None
    if token_key and token_key in Dict:
        data = Dict[token_key].split('.')[1] + '=='
        data = base64.b64decode(data).decode('UTF-8')
        if json.loads(data)['exp'] > time.time():
            token = Dict[token_key]

    if not token:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteID), 'HEAD')
        if 'instance_token' in req.cookies:
            token = req.cookies['instance_token']

    if token_key and token:
        if token_key not in Dict or Dict[token_key] != token:
            Dict[token_key] = token
            Dict.Save()

    return token


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    token = get_Token(siteNum)
    headers = {
        'Instance': token,
    }

    sceneID = None
    splited = searchTitle.split(' ')
    if unicode(splited[0], 'UTF-8').isdigit():
        sceneID = splited[0]
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()

    for sceneType in ['scene', 'movie', 'serie', 'trailer']:
        if sceneID and not searchTitle:
            url = PAsearchSites.getSearchSearchURL(siteNum) + '/v2/releases?type=%s&id=%s' % (sceneType, sceneID)
        else:
            url = PAsearchSites.getSearchSearchURL(siteNum) + '/v2/releases?type=%s&search=%s' % (sceneType, encodedTitle)

        req = PAutils.HTTPRequest(url, headers=headers)
        if req:
            searchResults = req.json()['result']
            for searchResult in searchResults:
                titleNoFormatting = searchResult['title']
                releaseDate = parse(searchResult['dateReleased']).strftime('%Y-%m-%d')
                curID = searchResult['id']
                siteName = searchResult['brand'].title()
                subSite = ''
                if 'collections' in searchResult and searchResult['collections']:
                    subSite = searchResult['collections'][0]['name']
                siteDisplay = '%s/%s' % (siteName, subSite) if subSite else siteName

                if sceneID:
                    score = 100 - Util.LevenshteinDistance(sceneID, curID)
                elif searchDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

                if sceneType == 'trailer':
                    titleNoFormatting = '[%s] %s' % (sceneType.capitalize(), titleNoFormatting)
                    score = score - 10

                results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, sceneType), name='%s [%s] %s' % (titleNoFormatting, siteDisplay, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneID = metadata_id[0]
    sceneType = metadata_id[2]

    token = get_Token(siteID)
    headers = {
        'Instance': token,
    }
    url = PAsearchSites.getSearchSearchURL(siteID) + '/v2/releases?type=%s&id=%s' % (sceneType, sceneID)
    req = PAutils.HTTPRequest(url, headers=headers)
    detailsPageElements = req.json()['result'][0]

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    description = None
    if 'description' in detailsPageElements:
        description = detailsPageElements['description']
    elif 'parent' in detailsPageElements:
        if 'description' in detailsPageElements['parent']:
            description = detailsPageElements['parent']['description']

    if description:
        metadata.summary = description

    # Studio
    metadata.studio = detailsPageElements['brand'].title()

    # Tagline and Collection(s)
    metadata.collections.clear()
    seriesNames = []

    if 'collections' in detailsPageElements and detailsPageElements['collections']:
        for collection in detailsPageElements['collections']:
            seriesNames.append(collection['name'])
    if 'parent' in detailsPageElements:
        if 'title' in detailsPageElements['parent']:
            seriesNames.append(detailsPageElements['parent']['title'])

    isInCollection = False
    siteName = PAsearchSites.getSearchSiteName(siteID).lower().replace(' ', '').replace('\'', '')
    for seriesName in seriesNames:
        if seriesName.lower().replace(' ', '').replace('\'', '') == siteName:
            isInCollection = True
            break

    if not isInCollection:
        seriesNames.insert(0, PAsearchSites.getSearchSiteName(siteID))

    for seriesName in seriesNames:
        metadata.collections.add(seriesName)

    # Release Date
    date_object = parse(detailsPageElements['dateReleased'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements['tags']
    for genreLink in genres:
        genreName = genreLink['name']

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements['actors']
    for actorLink in actors:
        actorPageURL = PAsearchSites.getSearchSearchURL(siteID) + '/v1/actors?id=%d' % actorLink['id']

        req = PAutils.HTTPRequest(actorPageURL, headers=headers)
        actorData = req.json()['result'][0]

        actorName = actorData['name']
        actorPhotoURL = ''
        if actorData['images'] and actorData['images']['profile']:
            actorPhotoURL = actorData['images']['profile'][0]['xs']['url']

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    for imageType in ['poster', 'cover']:
        if imageType in detailsPageElements['images']:
            for image in detailsPageElements['images'][imageType]:
                art.append(image['xx']['url'])

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.google.com'})
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
