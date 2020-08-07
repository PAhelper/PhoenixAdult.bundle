import PAsearchSites
import PAgenres
import PAactors
import PAutils


def getToken(url):
    req = PAutils.HTTPRequest(url)

    if req:
        return re.search(r'\.access_token=\"(.*?)\"', req.text).group(1)
    return None


def getDatafromAPI(baseURL, searchData, token, search=True):
    data = {}
    headers = {'Authorization': 'Bearer ' + token}

    if search:
        headers['Content-Type'] = 'application/json'
        params = json.dumps({'query': searchData})
        req = PAutils.HTTPRequest(baseURL, headers=headers, params=params)
    else:
        url = baseURL + '/api/movies/slug/' + str(searchData)
        headers = {'Authorization': 'Bearer ' + token}
        req = PAutils.HTTPRequest(url, headers=headers)

    if req:
        data = req.json()
        if 'data' in data:
            return data['data']
    return data


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    token = getToken(PAsearchSites.getSearchBaseURL(siteNum))
    if token:
        searchResults = getDatafromAPI(PAsearchSites.getSearchSearchURL(siteNum), searchTitle, token)
        for searchResult in searchResults:
            if searchResult['resourceType'] == 'confessions':
                curID = searchResult['slug']
                titleNoFormatting = searchResult['title']

                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s' % (titleNoFormatting), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneID = metadata_id[0]

    token = getToken(PAsearchSites.getSearchBaseURL(siteID))
    detailsPageElements = getDatafromAPI(PAsearchSites.getSearchBaseURL(siteID), sceneID, token, False)

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = detailsPageElements['synopsis_clean']

    # Studio
    producerLink = detailsPageElements['producer']
    metadata.studio = '%s %s' % (producerLink['name'], producerLink['last_name'])

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date_object = parse(detailsPageElements['release_date'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements['tags']:
        genreName = genreLink['title']
        movieGenres.addGenre(genreName)

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
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.google.com'})
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
