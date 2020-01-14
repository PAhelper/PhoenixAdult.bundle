import PAsearchSites
import PAgenres
import PAactors
import json


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    data = urllib.urlopen(PAsearchSites.getSearchSearchURL(siteNum) + '?_method=content.load&limit=0&offset=0&transitParameters[preset]=videos').read()
    searchResults = json.loads(data)
    for searchResult in searchResults['response']['collection']:
        titleNoFormatting = searchResult['title']
        curID = str(searchResult['id'])
        releaseDate = parse(searchResult['sites']['collection'][curID]['publishDate']).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        if (not searchDate and score > 90) or score == 100:
            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name=titleNoFormatting, score=score, lang=lang))

        if score == 100:
            break

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    id = str(metadata.id).split('|')
    contentId = id[0]
    siteNum = int(id[1])

    data = urllib.urlopen(PAsearchSites.getSearchSearchURL(siteNum) + '?_method=content.load&limit=1&filter[id][fields][0]=id&filter[id][values][0]=%s&transitParameters[v1]=OhUOlmasXD&transitParameters[v2]=OhUOlmasXD&transitParameters[preset]=scene' % contentId).read()
    detailsPageElements = json.loads(data)['response']['collection'][0]

    # Title
    metadata.title = detailsPageElements['title']

    # Release Date
    date = detailsPageElements['sites']['collection'][contentId]['publishDate']
    date_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    data = urllib.urlopen(PAsearchSites.getSearchSearchURL(siteNum) + '?_method=model.getModelContent&fields[0]=modelId.stageName&transitParameters[contentId]=%s' % contentId).read()
    actors = json.loads(data)['response']['collection']
    if len(actors) > 0:
        for id in actors:
            actor = actors[id]['modelId']['collection']
            for idx in actor:
                actorName = actor[idx]['stageName']
                movieActors.addActor(actorName, '')

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements['tags']['collection']
    if len(genres) > 0:
        for id in genres:
            genre = genres[id]['alias'].title()
            movieGenres.addGenre(genre)

    metadata.collections.add("JAY's POV")

    # Posters
    art = []
    img = detailsPageElements['_resources']['primary'][0]['url']
    art.append(img)

    for poster in detailsPageElements['_resources']['base']:
        art.append(poster['url'])

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