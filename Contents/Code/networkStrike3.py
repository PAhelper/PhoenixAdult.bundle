import PAsearchSites
import PAutils


def getDatafromAPI(url):
    req = PAutils.HTTPRequest(url)
    Log(req.status_code)
    if req:
        return req.json()['data']
    return req


def search(results, lang, siteNum, searchData):
    url = PAsearchSites.getSearchSearchURL(siteNum) + '/search?q=' + searchData.encoded

    searchResults = getDatafromAPI(url)
    if searchResults:
        for searchResult in searchResults['videos']:
            titleNoFormatting = PAutils.parseTitle(searchResult['title'], siteNum)
            releaseDate = parse(searchResult['releaseDate']).strftime('%Y-%m-%d')
            curID = PAutils.Encode(searchResult['targetUrl'])

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneName = PAutils.Decode(metadata_id[0])
    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneName

    detailsPageElements = getDatafromAPI(sceneURL)
    video = detailsPageElements['video']
    pictureset = detailsPageElements['pictureset']

    # Title
    metadata.title = PAutils.parseTitle(video['title'], siteNum)

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

    for tag in ['categories', 'tags']:
        for genreLink in video[tag]:
            if isinstance(genreLink, dict):
                genreName = genreLink['name']
            else:
                genreName = genreLink

            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = video['modelsSlugged']
    for actorLink in actors:
        actorName = actorLink['name']
        actorPageURL = PAsearchSites.getSearchSearchURL(siteNum) + '/' + actorLink['slugged']
        actorData = getDatafromAPI(actorPageURL)['model']
        actorPhotoURL = ''
        if hasattr(actorData, '__getitem__') and actorData['images']['profile']:
            actorPhotoURL = actorData['images']['profile'][0]['highdpi']['3x']
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
                image = PAutils.HTTPRequest(posterUrl)
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
