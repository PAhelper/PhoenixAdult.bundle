import PAsearchSites
import PAgenres
import PAactors
import PAutils


def getDataFromAPI(url, req_type, query):
    headers = {
        'Authorization': 'Basic YmFuZy1yZWFkOktqVDN0RzJacmQ1TFNRazI=',
        'Content-Type': 'application/json'
    }
    params = json.dumps({'query': {'bool': {'must': [{'match': {req_type: query}}, {'match': {'type': 'movie'}}], 'must_not': [{'match': {'type': 'trailer'}}]}}})
    data = PAutils.HTTPRequest(url, headers=headers, params=params).json()

    return data


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    searchResults = getDataFromAPI(PAsearchSites.getSearchSearchURL(siteNum), 'name', searchTitle)['hits']['hits']
    for searchResult in searchResults:
        searchResult = searchResult['_source']
        titleNoFormatting = searchResult['name']
        studioScene = searchResult['studio']['name'].title()
        seriesScene = searchResult['series']['name']
        curID = searchResult['identifier']
        releaseDate = parse(searchResult['releaseDate']).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s' % (seriesScene.title() if seriesScene else studioScene, titleNoFormatting), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneID = metadata_id[0]

    detailsPageElements = getDataFromAPI(PAsearchSites.getSearchSearchURL(siteID), 'identifier', sceneID)['hits']['hits'][0]['_source']

    # Title
    metadata.title = detailsPageElements['name']

    # Summary
    metadata.summary = detailsPageElements['description']

    # Studio
    metadata.studio = detailsPageElements['studio']['name'].title()

    # Tagline and Collection(s)
    metadata.collections.add(metadata.studio)
    seriesScene = detailsPageElements['series']['name']
    if seriesScene:
        metadata.collections.add(seriesScene.title())

    # Release Date
    date = detailsPageElements['releaseDate']
    date_object = datetime.strptime(date, '%Y-%m-%d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements['actors']:
        actorName = actorLink['name']
        actorPhotoURL = 'https://i.bang.com/pornstars/%d.jpg' % actorLink['id']

        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements['genres']:
        genreName = genreLink['name']

        movieGenres.addGenre(genreName)

    # Posters
    dvdID = detailsPageElements['dvd']['id']
    art = [
        'https://i.bang.com/covers/%d/front.jpg' % dvdID
    ]

    for img in detailsPageElements['screenshots']:
        art.append('https://i.bang.com/screenshots/%d/movie/1/%d.jpg' % (dvdID, img['screenId']))

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
