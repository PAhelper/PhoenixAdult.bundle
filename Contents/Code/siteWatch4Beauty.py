import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    modelStrings = []

    # start by attempting to fetch the list of scenes for a model
    if searchData.title.lower().find('veronica da souza') >= 0:
        # this is the only 3-word model nickname
        modelString = 'veronica-da-souza'
        modelStrings.append(modelString)
    else:
        # try the first word or two of the searchData.title as the model name
        splitWords = searchData.title.lower().split()
        searchWords = []
        for i, searchWord in enumerate(splitWords):
            if i >= 2:
                break
            searchWords.append(searchWord)
            modelString = '-'.join(searchWords)
            modelStrings.append(modelString)

    for modelString in modelStrings:
        scenesReq = PAutils.HTTPRequest('%s/%s/updates' % (w4bApiUrl('model'), modelString))
        scenesJson = scenesReq.json()
        if scenesJson:
            break

    if not scenesJson:
        # no model matches, so try to get the scene info with the searchData.title
        Log('No model matches, attempting to match scene title')

        modelsReq = PAutils.HTTPRequest('%s/%s/models' % (w4bApiUrl('scene'), searchData.title.replace(' ', '-').lower()))
        modelsJson = modelsReq.json()
        if modelsJson:
            modelsJson = json.loads(modelsReq.text)
            modelString = modelsJson[0]['Models'][0].get('model_simple_nickname')  # only need one at this point

            scenesReq = PAutils.HTTPRequest('%s/%s/updates' % (w4bApiUrl('model'), modelString))
            scenesJson = scenesReq.json()

    if not scenesJson:
        Log('Unable to resolve request to a model name, can not continue')
        return results

    for scene in scenesJson[0]['Issues']:
        sceneName = scene.get('issue_title')
        sceneString = scene.get('issue_simple_title')
        sceneDateTime = scene.get('issue_datetime')
        sceneDateString = parse(sceneDateTime).strftime('%Y-%m-%d')
        modelName = modelString.replace('-', ' ').title()

        if searchData.date:
            if sceneDateString == searchData.date:
                results.Append(MetadataSearchResult(id='%s|%d|%s' % (modelString, siteNum, sceneString), name='%s, %s [Watch4Beauty]' % (sceneName, sceneDateString), score=100, lang=lang))
        elif searchData.title:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), sceneName.lower())
            results.Append(MetadataSearchResult(id='%s|%d|%s' % (modelString, siteNum, sceneString), name='%s, %s [Watch4Beauty]' % (sceneName, sceneDateString), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')

    modelString = metadata_id[0]
    sceneString = metadata_id[2]

    sceneReq = PAutils.HTTPRequest('%s/%s' % (w4bApiUrl('scene'), sceneString))
    sceneJson = sceneReq.json()
    if not sceneJson:
        return

    # Scene object
    scene = sceneJson[0]

    # Title
    metadata.title = scene.get('issue_title')

    # Summary
    metadata.summary = scene.get('issue_text')

    # Studio
    metadata.studio = 'Watch4Beauty'

    # Director
    director = metadata.directors.new()
    director.name = 'MarK'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    dateObj = parse(scene.get('issue_datetime'))
    metadata.originally_available_at = dateObj
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genreText = scene.get('issue_tags')
    if genreText:
        for genreName in genreText.split(', '):
            movieGenres.addGenre(genreName.strip())

    # Actors
    movieActors.clearActors()

    # Posters
    artPrefix = w4bArtUrl() + dateObj.strftime('%Y%m%d')
    art = [
        artPrefix + '-issue-cover-1280.jpg',
        artPrefix + '-issue-video-cover-2560.jpg',
        artPrefix + '-issue-cover-wide-2560.jpg'
    ]

    modelsReq = PAutils.HTTPRequest('%s/%s/models' % (w4bApiUrl('scene'), sceneString))
    if modelsReq and not modelsReq.text == '[]' and not modelsReq.text == '':
        modelsJson = json.loads(modelsReq.text)
        for model in modelsJson[0]['Models']:
            modelName = model.get('model_nickname')
            modelString = model.get('model_simple_nickname')
            modelPhotoURL = artPrefix + 'model-%s-320.jpg' % modelString
            movieActors.addActor(modelName, modelPhotoURL)

            art.append(w4bArtUrl() + 'model-%s-wide-2560.jpg' % modelString)
            art.append(w4bArtUrl() + 'model-%s-1280.jpg' % modelString)

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
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata


def w4bApiUrl(type):
    key = '3yAjOB66l2A566U' if type == 'model' else '7Wywy44w9G9Bbtf'
    return 'https://www.watch4beauty.com/api/%s' % key


def w4bArtUrl():
    return 'https://s5q3w2t8.ssl.hwcdn.net/production/'
