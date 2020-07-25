import PAsearchSites
import PAgenres
import PAutils


def getDatafromAPI(url):
    req = PAutils.HTTPRequest(url)

    if req:
        return req.json()['data']
    return req


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    url = PAsearchSites.getSearchSearchURL(siteNum) + '/search?q=' + encodedTitle

    searchResults = getDatafromAPI(url)
    if searchResults:
        for searchResult in searchResults['videos']:
            titleNoFormatting = searchResult['title']
            releaseDate = parse(searchResult['releaseDate']).strftime('%Y-%m-%d')
            curID = PAutils.Encode(searchResult['targetUrl'])

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneName = PAutils.Decode(metadata_id[0])
    sceneURL = PAsearchSites.getSearchSearchURL(siteID) + sceneName

    detailsPageElements = getDatafromAPI(sceneURL)
    video = detailsPageElements['video']
    pictureset = detailsPageElements['pictureset']

    # Title
    metadata.title = video['title']

    # Summary
    metadata.summary = video['description']

    # Director
    director = metadata.directors.new()
    director.name = video['directorNames']

    # Studio
    metadata.studio = video['primarySite'].title()

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Release Date
    date_object = parse(video['releaseDate'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = video['tags']
    for genreName in genres:
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = video['modelsSlugged']
    for actorLink in actors:
        actorPageURL = PAsearchSites.getSearchSearchURL(siteID) + '/' + actorLink['slugged']
        actorData = getDatafromAPI(actorPageURL)['model']

        actorName = actorData['name']
        actorPhotoURL = actorData['cdnUrl']

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    for name in ['movie', 'poster']:
        if name in video['images'] and video['images'][name]:
            image = video['images'][name][-1]
            if 'highdpi' in image:
                art.append(image['highdpi']['3x'])
            else:
                art.append(image['src'])
            break

    for image in pictureset:
        img = image['main'][0]['src']

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
                if width > 100 and width > height and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
