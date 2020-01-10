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
        searchResult = searchResult['_source']
        titleNoFormatting = searchResult['name']
        studioScene = searchResult['studio']['name'].title()
        seriesScene = searchResult['series']['name']
        curID = searchResult['identifier']
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        name = '[%s] %s' % (seriesScene.title() if seriesScene else studioScene, titleNoFormatting)
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name=name, score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    id = str(metadata.id).split('|')
    identifier = id[0]
    siteNum = int(id[1])

    headers = {
        'Authorization': 'Basic YmFuZy1yZWFkOktqVDN0RzJacmQ1TFNRazI=',
        'Content-Type': 'application/json'
    }
    params = json.dumps({"query":{"bool":{"must":[{"match":{"identifier": identifier}},{"match":{"type":"movie"}}],"must_not":[{"match":{"type":"trailer"}}]}}})
    req = urllib.Request(PAsearchSites.getSearchSearchURL(siteNum), data=params, headers=headers)
    data = urllib.urlopen(req).read()
    detailsPageElements = json.loads(data)['hits']['hits'][0]['_source']

    # Title
    metadata.title = detailsPageElements['name']

    # Summary
    metadata.summary = detailsPageElements['description']

    # Studio
    metadata.studio = detailsPageElements['studio']['name'].title()

    # Release Date
    date = detailsPageElements['releaseDate']
    date_object = datetime.strptime(date, '%Y-%m-%d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements['actors']
    if len(actors) > 0:
        for actor in actors:
            movieActors.addActor(actor['name'], 'https://i.bang.com/pornstars/%d.jpg' % actor['id'])

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements['genres']
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre['name'])

    metadata.collections.add(metadata.studio)
    seriesScene = detailsPageElements['series']['name']
    if seriesScene:
        metadata.collections.add(seriesScene.title())

    # Posters
    art = []
    dvdID = detailsPageElements['dvd']['id']
    photos = detailsPageElements['photos']

    art.append('https://i.bang.com/covers/%d/front.jpg' % dvdID)

    imgs = detailsPageElements['screenshots']
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
