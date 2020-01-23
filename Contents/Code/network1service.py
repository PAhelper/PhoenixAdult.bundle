import PAsearchSites
import PAgenres
import PAactors
import json


def get_Cookies(url):
    import cookielib

    cookies = {}
    cookie_jar = cookielib.CookieJar()
    opener = urllib.build_opener(urllib.HTTPCookieProcessor(cookie_jar))
    urllib.install_opener(opener)

    urllib.urlopen(url)
    for cookie in cookie_jar:
        cookies[cookie.name] = cookie.value

    return cookies


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    cookies = get_Cookies(PAsearchSites.getSearchBaseURL(siteNum))
    headers = {
        'Instance': cookies['instance_token'],
    }

    sceneID = None
    for splited in searchTitle.split(' '):
        if unicode(splited, 'utf8').isdigit():
            sceneID = splited
            break

    for sceneType in ['scene', 'movie', 'serie']:
        url = PAsearchSites.getSearchSearchURL(siteNum) + '/v2/releases?type=%s&search=%s' % (sceneType, encodedTitle)
        req = urllib.Request(url, headers=headers)
        data = urllib.urlopen(req).read()

        searchResults = json.loads(data)
        for searchResult in searchResults['result']:
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

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, sceneType), name='%s [%s] %s' % (titleNoFormatting, siteDisplay, releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneID = metadata_id[0]
    sceneType = metadata_id[2]

    cookies = get_Cookies(PAsearchSites.getSearchBaseURL(siteID))
    headers = {
        'Instance': cookies['instance_token'],
    }
    url = PAsearchSites.getSearchSearchURL(siteID) + '/v2/releases?type=%s&id=%s' % (sceneType, sceneID)
    req = urllib.Request(url, headers=headers)
    data = urllib.urlopen(req).read()
    detailsPageElements = json.loads(data)['result'][0]

    # Studio
    metadata.studio = detailsPageElements['brand'].title()

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

    # Release Date
    date_object = parse(detailsPageElements['dateReleased'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

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

        req = urllib.Request(actorPageURL, headers=headers)
        data = urllib.urlopen(req).read()
        actorData = json.loads(data)['result'][0]

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
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100 and width > height and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
