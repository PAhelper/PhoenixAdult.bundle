import PAsearchSites
import PAgenres
import PAactors
import json


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    headers = {
        'Authorization': 'Basic YmFuZy1yZWFkOktqVDN0RzJacmQ1TFNRazI=',
        'Content-Type': 'application/json'
    }
    params = json.dumps({"query":{"bool":{"must":[{"match":{"name": searchTitle}},{"match":{"type":"movie"}}],"must_not":[{"match":{"type":"trailer"}}]}}})
    req = urllib.Request(PAsearchSites.getSearchSearchURL(siteNum), data=params, headers=headers)
    data = urllib.urlopen(req).read()
    searchResults = json.loads(data)
    for searchResult in searchResults['hits']['hits']:
        titleNoFormatting = searchResult['_source']['name']
        seriesScene = searchResult['_source']['series']['name']
        curID = searchResult['_source']['identifier']
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        if seriesScene:
            name = '[%s] %s' % (seriesScene, titleNoFormatting)
        else:
            name = titleNoFormatting
        results.Append(MetadataSearchResult(id='%s|%s' % (curID, str(siteNum)), name=name, score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    identifier = str(metadata.id).split('|')[0]
    headers = {
        'Authorization': 'Basic YmFuZy1yZWFkOktqVDN0RzJacmQ1TFNRazI=',
        'Content-Type': 'application/json'
    }
    params = json.dumps({"query":{"bool":{"must":[{"match":{"identifier": identifier}},{"match":{"type":"movie"}}],"must_not":[{"match":{"type":"trailer"}}]}}})
    req = urllib.Request(PAsearchSites.getSearchSearchURL(siteID), data=params, headers=headers)
    data = urllib.urlopen(req).read()
    searchResults = json.loads(data)
    detailsPageElements = json.loads(data)

    # Title
    metadata.title = detailsPageElements['hits']['hits'][0]['_source']['name']

    # Summary
    metadata.summary = detailsPageElements['hits']['hits'][0]['_source']['description']

    # Studio
    metadata.studio = detailsPageElements['hits']['hits'][0]['_source']['studio']['name']

    # Release Date
    date = detailsPageElements['hits']['hits'][0]['_source']['releaseDate']
    date_object = datetime.strptime(date, '%Y-%m-%d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = searchResults['hits']['hits'][0]['_source']['actors']
    if len(actors) > 0:
        for actor in actors:
            movieActors.addActor(actor['name'], 'https://i.bang.com/pornstars/%d.jpg?p=big' % actor['id'])

    # Genres
    movieGenres.clearGenres()
    genres = searchResults['hits']['hits'][0]['_source']['genres']
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre['name'])

    genres = searchResults['hits']['hits'][0]['_source']['genres']
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre['name'])
    metadata.collections.add(metadata.studio)    
    metadata.collections.add(detailsPageElements['hits']['hits'][0]['_source']['series']['name'])

    # Posters
    art = []
    dvdID = detailsPageElements['hits']['hits'][0]['_source']['dvd']['id']
    photos = detailsPageElements['hits']['hits'][0]['_source']['photos']

    art.append('https://i.bang.com/covers/%d/front.jpg' % dvdID)

    imgs = searchResults['hits']['hits'][0]['_source']['screenshots']
    if len(imgs) > 0 and photos > 0:
        for img in imgs:
            art.append('https://i.bang.com/screenshots/%d/movie/1/%d.jpg' % (dvdID, img['screenId']))

    i = 1
    Log('Artwork found: ' + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=i)
                if(width > 100 and i > 1):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=i)
                i = i + 1
            except:
                pass

    if len(metadata.art) == 0 and len(metadata.posters) > 1:
        metadata.art[art[0]] = Proxy.Media(HTTP.Request(art[0], headers={'Referer': 'http://www.google.com'}).content, sort_order=1)

    return metadata
