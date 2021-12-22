import PAsearchSites
import PAutils


def getDatafromAPI(url):
    req = PAutils.HTTPRequest(url)

    if req:
        return req.json()['data']
    return req


def search(results, lang, siteNum, searchData):
    if searchData.encoded.isdigit():
        url = PAsearchSites.getSearchBaseURL(siteNum) + '/graphql?query=' + search_id_query % (searchData.encoded, PAsearchSites.getSearchSiteName(siteNum).upper())
        searchResult = getDatafromAPI(url)
        if searchResult:
            titleNoFormatting = PAutils.parseTitle(searchResult['findOneVideo']['title'], siteNum)
            releaseDate = parse(searchResult['findOneVideo']['releaseDate']).strftime('%Y-%m-%d')
            curID = PAutils.Encode(searchResult['findOneVideo']['slug'])

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))
    else:
        url = PAsearchSites.getSearchBaseURL(siteNum) + '/graphql?query=' + search_query % (searchData.encoded, PAsearchSites.getSearchSiteName(siteNum).upper())
        searchResults = getDatafromAPI(url)
        if searchResults:
            for searchResult in searchResults['searchVideos']['edges']:
                titleNoFormatting = PAutils.parseTitle(searchResult['node']['title'], siteNum)
                releaseDate = parse(searchResult['node']['releaseDate']).strftime('%Y-%m-%d')
                curID = PAutils.Encode(searchResult['node']['slug'])

                if searchData.date:
                    score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneName = PAutils.Decode(metadata_id[0])
    sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/graphql?query=' + update_query % (sceneName, PAsearchSites.getSearchSiteName(siteNum).upper())

    detailsPageElements = getDatafromAPI(sceneURL)
    video = detailsPageElements['findOneVideo']
    pictureset = video['carousel']

    # Title
    metadata.title = PAutils.parseTitle(video['title'], siteNum)

    # Summary
    metadata.summary = video['description']

    # Director
    if video['directors']:
        director = metadata.directors.new()
        director.name = video['directors'][0]['name']

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum).title()

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Release Date
    date_object = parse(video['releaseDate'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    if metadata.studio == 'Tushy' or metadata.studio == 'TushyRaw':
        movieGenres.addGenre('Anal')

    if video['categories']:
        for tag in video['categories']:
            genreName = tag['name']

            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = video['models']
    for actor in actors:
        actorName = actor['name']
        actorPhotoURL = ''
        if actor['images']:
            actorPhotoURL = actor['images']['listing'][0]['highdpi']['double']

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    for name in ['movie', 'poster']:
        if name in video['carousel'] and video['images'][name]:
            image = video['images'][name][-1]
            if 'highdpi' in image:
                art.append(image['highdpi']['3x'])
            else:
                art.append(image['src'])
            break

    for image in pictureset:
        img = image['listing'][0]['highdpi']['triple']

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


search_query = '{searchVideos(input:{query:\"%s\",site:%s,first:10}){edges{node{videoId,title,releaseDate,slug}}}}'
update_query = '{findOneVideo(input:{slug:\"%s\",site:%s}){videoId,title,description,releaseDate,models{name,slug,images{listing{highdpi{double}}}},directors{name},categories{name},carousel{listing{highdpi{triple}}}}}'
search_id_query = '{findOneVideo(input:{videoId:\"%s\",site:%s}){videoId,title,releaseDate,slug}}'
