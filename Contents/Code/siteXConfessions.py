import PAsearchSites
import PAgenres
import PAactors
import PAutils
import re


def getAlgolia(url, indexName, params):
    params = json.dumps({'requests':[{'indexName': indexName,'params': params}]})
    req = urllib.Request(url)
    req.add_header('Content-Type', 'application/json')
    data = urllib.urlopen(req, params).read()

    return json.loads(data)['results'][0]['hits']


def getToken(url):
    data = PAutils.HTTPRequest(url)

    if data:
        return re.search(r'\.access_token=\"(.*?)\"', data).group(1)
    return data


def getDatafromAPI(baseURL, sceneId, token):
    url = baseURL + '/api/movies/' + str(sceneId)
    headers = {'Authorization': 'Bearer ' + token}
    data = json.loads(PAutils.HTTPRequest(url, headers=headers))

    if 'data' in data:
        return data['data']
    return None


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    token = getToken(PAsearchSites.getSearchBaseURL(siteNum))
    url = PAsearchSites.getSearchSearchURL(siteNum) + '?&x-algolia-application-id=2RZI1CNTO2&x-algolia-api-key=797e0814d00bb34f8bcb08e575e26625'
    searchResults = getAlgolia(url, 'production_movies', 'query=' + searchTitle)
    for idx, searchResult in enumerate(searchResults):
        curID = searchResult['id']
        titleNoFormatting = searchResult['title']['def']
        releaseDate = parse(searchResult['release_date']['def']).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        data = getDatafromAPI(PAsearchSites.getSearchBaseURL(siteNum), curID, token)
        if data:
            results.Append(MetadataSearchResult(id='%d|%d' % (curID, siteNum), name='%s %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneId = metadata_id[0]

    token = getToken(PAsearchSites.getSearchBaseURL(siteID))
    detailsPageElements = getDatafromAPI(PAsearchSites.getSearchBaseURL(siteID), sceneId, token)

    # Studio
    producerLink = detailsPageElements['producer']
    metadata.studio = '%s %s' % (producerLink['name'], producerLink['last_name'])

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = detailsPageElements['synopsis_clean']

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements['tags']:
        genreName = genreLink['title']
        movieGenres.addGenre(genreName)

    # Release Date
    date_object = parse(detailsPageElements['release_date'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements['performers']:
        actorName = '%s %s' % (actorLink['name'], actorLink['last_name'])
        actorPhotoURL = actorLink['poster_image'].split('?', 1)[0]
        movieActors.addActor(actorName, actorPhotoURL)

    # Director
    director = metadata.directors.new()
    directorLink = detailsPageElements['director']
    director.name = '%s %s' % (directorLink['name'], directorLink['last_name'])

    # Poster
    art = [
        detailsPageElements['poster_picture'].split('?', 1)[0]
    ]

    for photoLink in detailsPageElements['album']:
        img = photoLink['path'].split('?', 1)[0]
        art.append(img)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
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
