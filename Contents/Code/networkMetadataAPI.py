import PAsearchSites
import PAutils


def getDataFromAPI(url):
    headers = {}

    token = Prefs['metadataapi_token']
    if token:
        headers['Accept'] = 'application/json'
        headers['Authorization'] = 'Bearer %s' % token

    req = PAutils.HTTPRequest(url, headers=headers)

    data = None
    if req.ok:
        data = req.json()

    return data


def search(results, lang, siteNum, searchData):
    url = PAsearchSites.getSearchSearchURL(siteNum) + '/scenes?parse=' + urllib.quote(searchData.title)
    if searchData.ohash:
        url += '&hash=%s' % searchData.ohash

    searchResults = getDataFromAPI(url)
    if searchResults and 'data' in searchResults and searchResults['data']:
        for searchResult in searchResults['data']:
            curID = searchResult['_id']
            titleNoFormatting = searchResult['title']
            siteName = searchResult['site']['name']

            date = searchResult['date']
            releaseDate = parse(date).strftime('%Y-%m-%d')

            if searchData.date and releaseDate:
                score = 100 - Util.LevenshteinDistance(searchData.dateFormat(), releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [MetadataAPI/%s] %s' % (titleNoFormatting, siteName, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneID = metadata_id[0]

    url = PAsearchSites.getSearchSearchURL(siteNum) + '/scenes/' + sceneID
    req = getDataFromAPI(url)
    detailsPageElements = req['data']

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = detailsPageElements['description']

    # Studio, Tagline and Collection(s)
    if 'site' in detailsPageElements and detailsPageElements['site']:
        studio_name = detailsPageElements['site']['name']
        collections = [studio_name]

        site_id = detailsPageElements['site']['id']
        network_id = detailsPageElements['site']['network_id']

        if network_id and site_id != network_id:
            url = PAsearchSites.getSearchSearchURL(siteNum) + '/sites/%d' % network_id
            req = getDataFromAPI(url)
            if req and 'data' in req and req['data']:
                studio_name = req['data']['name']
                collections.append(studio_name)

        metadata.tagline = studio_name
        metadata.studio = studio_name

        for collection in collections:
            movieCollections.addCollection(collection)

    # Release Date
    date = detailsPageElements['date']
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    if 'tags' in detailsPageElements:
        for genreLink in detailsPageElements['tags']:
            genreName = genreLink['name']

            movieGenres.addGenre(genreName)

    # Actor(s)
    for actorLink in detailsPageElements['performers']:
        actorName = actorLink['name']
        if actorLink['face'] and 'default' not in actorLink['face']:
            actorPhotoURL = actorLink['face']
        else:
            actorPhotoURL = ''

        if 'parent' in actorLink and actorLink['parent'] and 'name' in actorLink['parent']:
            actorName = actorLink['parent']['name']
            actorPhotoURL = actorLink['parent']['face']

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art.append(detailsPageElements['posters']['large'])
    art.append(detailsPageElements['background']['large'])

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
