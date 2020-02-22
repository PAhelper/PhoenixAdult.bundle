import PAsearchSites
import PAgenres
import PAextras
import googlesearch


def getDataFromAPI(url):
    data = urllib.urlopen(url).read()

    return json.loads(data)


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    sceneID = searchTitle.split(' ', 1)[0]
    if not unicode(sceneID, 'utf8').isdigit():
        sceneID = None

    searchResults = []
    domain = PAsearchSites.getSearchBaseURL(siteNum).split('://')[1]
    for sceneURL in googlesearch.search('site:%s %s' % (domain, searchTitle), stop=10):
        sceneName = None
        if ('/movies/' in sceneURL):
            sceneName = sceneURL.split('/')[-1]
        elif sceneID and sceneID in sceneURL and '/girls/' not in sceneURL:
            sceneName = sceneURL.split('/')[-2]

        if sceneName:
            searchResults.append(sceneName)

    for sceneName in searchResults:
        detailsPageElements = getDataFromAPI('%s/moviesContent/%s.json' % (PAsearchSites.getSearchSearchURL(siteNum), sceneName))

        if detailsPageElements:
            curID = detailsPageElements['id']
            titleNoFormatting = detailsPageElements['title']
            siteName = PAsearchSites.getSearchSiteName(siteNum)
            releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, siteName), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneName = metadata_id[0]
    sceneDate = metadata_id[2]

    detailsPageElements = getDataFromAPI('%s/moviesContent/%s.json' % (PAsearchSites.getSearchSearchURL(siteID), sceneName))

    # Studio
    metadata.studio = 'TeamSkeet'

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = detailsPageElements['description']

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    if siteName == 'Sis Loves Me':
        movieGenres.addGenre('Step Sister')
    elif siteName == 'DadCrush' or siteName == 'DaughterSwap':
        movieGenres.addGenre('Step Dad')
        movieGenres.addGenre('Step Daughter')
    elif siteName == 'PervMom':
        movieGenres.addGenre('Step Mom')
    elif siteName == 'Family Strokes':
        movieGenres.addGenre('Taboo Family')
    elif siteName == 'Foster Tapes':
        movieGenres.addGenre('Taboo Sex')
    elif siteName == 'BFFs':
        movieGenres.addGenre('Teen')
        movieGenres.addGenre('Group Sex')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements['models']
    for actorLink in actors:
        actorData = getDataFromAPI('%s/modelsContent/%s.json' % (PAsearchSites.getSearchSearchURL(siteID), actorLink['modelId']))
        actorName = actorData['name']
        actorPhotoURL = actorData['img']

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [
        detailsPageElements['img']
    ]

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
                req = urllib.Request(posterUrl, headers=headers)
                img_file = urllib.urlopen(req)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers=headers).content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers=headers).content, sort_order=idx)
            except:
                pass

    return metadata
