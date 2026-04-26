import PAsearchSites
import PAutils


def getGraphQL(queryType, variable, query, siteNum):
    apiKey = PAutils.getDictValuesFromKey(apiKeyDB, PAsearchSites.getSearchSiteName(siteNum))[0]

    params = json.dumps({'query': queryType, 'variables': {variable: query}})
    headers = {
        'argonath-api-key': apiKey,
        'Content-Type': 'application/json',
        'Referer': PAsearchSites.getSearchBaseURL(siteNum),
    }
    data = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum), headers=headers, params=params).json()

    return data['data']


def search(results, lang, siteNum, searchData):
    searchResults = getGraphQL(searchQuery, 'query', searchData.title, siteNum)['search']['search']['result']

    for searchResult in searchResults:
        if searchResult['type'] == 'VIDEO':
            titleNoFormatting = PAutils.parseTitle(searchResult['name'], siteNum)
            curID = PAutils.Encode(searchResult['itemId'])

            releaseDate = searchData.dateFormat() if searchData.date else ''

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    videoId = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]

    splitted = videoId.split(':')
    modelId = splitted[0]
    scene = splitted[-1]
    sceneNum = int(scene.replace('scene', ''))

    detailsPageElements = getGraphQL(findVideoQuery, 'videoId', videoId, siteNum)['video']['find']['result']

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements['title'], siteNum)

    # Summary
    summary = detailsPageElements['description']['long'].strip()
    if not re.search(r'.$(?<=(!|\.|\?))', summary):
        summary = summary + '.'

    metadata.summary = summary

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    movieCollections.addCollection(metadata.studio)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genreLink in PAutils.getDictValuesFromKey(genresDB, PAsearchSites.getSearchSiteName(siteNum)):
        genreName = genreLink.strip()

        movieGenres.addGenre(genreName)

    # Actor(s)
    for actorLink in detailsPageElements['talent']:
        actorPhoto = []
        actorName = actorLink['talent']['name']

        actorPhoto.append('/members/models/%s/profile-sm.jpg' % actorLink['talent']['talentId'])
        actorPhotoURL = getGraphQL(assetQuery, 'paths', actorPhoto, siteNum)['asset']['batch']['result'][0]['serve']['uri']

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    images = []
    images.append('/members/models/%s/scenes/%s/videothumb.jpg' % (modelId, scene))
    for idx in range(1, detailsPageElements['galleryCount'] + 1):
        path = '/members/models/%s/scenes/%s/photos/thumbs/%s-%s-%d-%d.jpg' % (modelId, scene, PAsearchSites.getSearchSiteName(siteNum).lower(), modelId, sceneNum, idx)
        images.append(path)

    posters = getGraphQL(assetQuery, 'paths', images, siteNum)['asset']['batch']['result']

    for poster in posters:
        if poster:
            art.append(poster['serve']['uri'])

    postersClean = list()
    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        # Remove Timestamp and Token from URL
        cleanUrl = posterUrl.split('?')[0]
        postersClean.append(cleanUrl)
        if not PAsearchSites.posterAlreadyExists(cleanUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if height > width:
                    # Item is a poster
                    metadata.posters[cleanUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > height:
                    # Item is an art item
                    metadata.art[cleanUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    art.extend(postersClean)

    return metadata


searchQuery = 'query Search($query: String!) { search { search(input: {query: $query}) { result { type itemId name description images } } } }'
findVideoQuery = 'query FindVideo($videoId: ID!) { video { find(input: {videoId: $videoId}) { result { videoId title duration galleryCount description { short long } talent { type talent { talentId name } } } } } }'
assetQuery = 'query BatchFindAssetQuery($paths: [String!]!) { asset { batch(input: {paths: $paths}) { result { path mime size serve { type uri } } } } }'


apiKeyDB = {
    'fit18': ['77cd9282-9d81-4ba8-8868-ca9125c76991'],
    'thicc18': ['0e36c7e9-8cb7-4fa1-9454-adbc2bad15f0'],
}


genresDB = {
    'fit18': ['Young', 'Gym'],
    'thicc18': ['Thicc'],
}
