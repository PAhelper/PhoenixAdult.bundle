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
    directURL = searchData.title.replace(' ', '-').replace('\'', '').lower()

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


def update(metadata, lang, siteNum, movieGenres, movieActors):
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
    movieGenres.clearGenres()
    genres = []

    for key, value in genresDB.items():
        if key.lower() == siteName.lower():
            genres.extend(value)
            break

    if 'tags' in detailsPageElements and detailsPageElements['tags']:
        for genreLink in detailsPageElements['tags']:
            genreName = genreLink.strip()

            genres.append(genreName)

    for genreName in genres:
        movieGenres.addGenre(genreName)

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


genresDB = {
    'Anal Mom': ['Anal', 'MILF'],
    'BFFs': ['Teen', 'Group Sex'],
    'Black Valley Girls': ['Teen', 'Ebony'],
    'DadCrush': ['Step Dad', 'Step Daughter'],
    'DaughterSwap': ['Step Dad', 'Step Daughter'],
    'Dyked': ['Hardcore', 'Teen', 'Lesbian'],
    'Exxxtra Small': ['Teen', 'Small Tits'],
    'Family Strokes': ['Taboo Family'],
    'Foster Tapes': ['Taboo Sex'],
    'Freeuse Fantasy': ['Freeuse'],
    'Ginger Patch': ['Redhead'],
    'Innocent High': ['School Girl'],
    'Little Asians': ['Asian', 'Teen'],
    'Not My Grandpa': ['Older/Younger'],
    'Oye Loca': ['Latina'],
    'PervMom': ['Step Mom'],
    'POV Life': ['POV'],
    'Shoplyfter': ['Strip'],
    'ShoplyfterMylf': ['Strip', 'MILF'],
    'Sis Loves Me': ['Step Sister'],
    'Teen Curves': ['Big Ass'],
    'Teen Pies': ['Teen', 'Creampie'],
    'TeenJoi': ['Teen', 'JOI'],
    'Teens Do Porn': ['Teen'],
    'Teens Love Black Cocks': ['Teens', 'BBC'],
    'Teeny Black': ['Teen', 'Ebony'],
    'Thickumz': ['Thick'],
    'Titty Attack': ['Big Tits'],
}
