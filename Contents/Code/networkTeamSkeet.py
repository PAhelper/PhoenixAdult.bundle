import PAsearchSites
import PAutils


def getDBURL(url):
    req = PAutils.HTTPRequest(url)

    if req:
        return re.search(r'\.dbUrl.?=.?\"(.*?)\"', req.text).group(1)
    return None


def getDataFromAPI(dbURL, sceneType, sceneName, siteNum):
    is_new = True
    if 'teamskeet.com' in PAsearchSites.getSearchBaseURL(siteNum):
        url = '%s-%s/_doc/%s' % (dbURL, sceneType, sceneName)
    else:
        is_new = False
        sceneType = sceneType.replace('content', 'Content')
        url = '%s/%s/%s.json' % (dbURL, sceneType, sceneName)

    data = PAutils.HTTPRequest(url)
    if data.text != 'null':
        data = data.json()
        if is_new:
            if '_source' in data:
                return data['_source']
        else:
            return data

    return None


def search(results, lang, siteNum, searchData):
    directURL = searchData.title.replace(' ', '-').lower()

    searchResults = [directURL]
    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.split('?', 1)[0]
        sceneName = None
        if ('/movies/' in sceneURL):
            sceneName = sceneURL.split('/')[-1]
        elif unicode(sceneURL.split('/')[-3]).isdigit():
            sceneName = sceneURL.split('/')[-1]

        if sceneName and sceneName not in searchResults:
            searchResults.append(sceneName)

    dbURL = getDBURL(PAsearchSites.getSearchBaseURL(siteNum))

    for sceneName in searchResults:
        for sceneType in ['videoscontent', 'moviescontent']:
            detailsPageElements = getDataFromAPI(dbURL, sceneType, sceneName, siteNum)
            if detailsPageElements:
                break

        if detailsPageElements:
            curID = detailsPageElements['id']
            titleNoFormatting = PAutils.parseTitle(detailsPageElements['title'], siteNum)
            siteName = detailsPageElements['site']['name'] if 'site' in detailsPageElements else PAsearchSites.getSearchSiteName(siteNum)
            if 'publishedDate' in detailsPageElements:
                releaseDate = parse(detailsPageElements['publishedDate']).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''

            displayDate = releaseDate if 'publishedDate' in detailsPageElements else ''

            if searchData.date and displayDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, releaseDate, sceneType), name='%s [%s] %s' % (titleNoFormatting, siteName, displayDate), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneName = metadata_id[0]
    sceneDate = metadata_id[2]
    sceneType = metadata_id[3]

    dbURL = getDBURL(PAsearchSites.getSearchBaseURL(siteNum))
    detailsPageElements = getDataFromAPI(dbURL, sceneType, sceneName, siteNum)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements['title'], siteNum)

    # Summary
    metadata.summary = detailsPageElements['description']

    # Studio
    metadata.studio = 'TeamSkeet'

    # Collections / Tagline
    siteName = detailsPageElements['site']['name'] if 'site' in detailsPageElements else PAsearchSites.getSearchSiteName(siteNum)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    if 'tags' in detailsPageElements and detailsPageElements['tags']:
        for genreLink in detailsPageElements['tags']:
            genreName = genreLink.strip()

            movieGenres.addGenre(genreName)

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
    elif siteName == 'Shoplyfter':
        movieGenres.addGenre('Strip')
    elif siteName == 'ShoplyfterMylf':
        movieGenres.addGenre('Strip')
        movieGenres.addGenre('MILF')
    elif siteName == 'Exxxtra Small':
        movieGenres.addGenre('Teen')
        movieGenres.addGenre('Small Tits')
    elif siteName == 'Little Asians':
        movieGenres.addGenre('Asian')
        movieGenres.addGenre('Teen')
    elif siteName == 'TeenJoi':
        movieGenres.addGenre('Teen')
        movieGenres.addGenre('JOI')
    elif siteName == 'Black Valley Girls':
        movieGenres.addGenre('Teen')
        movieGenres.addGenre('Ebony')
    elif siteName == 'Thickumz':
        movieGenres.addGenre('Thick')
    elif siteName == 'Dyked':
        movieGenres.addGenre('Hardcore')
        movieGenres.addGenre('Teen')
        movieGenres.addGenre('Lesbian')
    elif siteName == 'Teens Love Black Cocks':
        movieGenres.addGenre('Teens')
        movieGenres.addGenre('BBC')
    elif siteName == 'Teen Curves':
        movieGenres.addGenre('Big Ass')
    elif siteName == 'Titty Attack':
        movieGenres.addGenre('Big Tits')
    elif siteName == 'Teeny Black':
        movieGenres.addGenre('Teen')
        movieGenres.addGenre('Ebony')
    elif siteName == 'Teens Do Porn':
        movieGenres.addGenre('Teen')
    elif siteName == 'Teen Pies':
        movieGenres.addGenre('Teen')
        movieGenres.addGenre('Creampie')
    elif siteName == 'POV Life':
        movieGenres.addGenre('POV')
    elif siteName == 'Ginger Patch':
        movieGenres.addGenre('Redhead')
    elif siteName == 'Innocent High':
        movieGenres.addGenre('School Girl')
    elif siteName == 'Oye Loca':
        movieGenres.addGenre('Latina')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements['models']
    for actorLink in actors:
        actorData = getDataFromAPI(dbURL, 'modelscontent', actorLink['modelId'], siteNum)

        if actorData:
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
