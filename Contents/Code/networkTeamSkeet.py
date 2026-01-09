import PAsearchSites
import PAutils


def getJSONfromPage(url):
    cookies = {'age_verified': 'yes'}
    req = PAutils.HTTPRequest(url, cookies=cookies)

    if req:
        jsonData = re.search(r'window\.__INITIAL_STATE__ = (.*);', req.text)
        if jsonData:
            return json.loads(jsonData.group(1))['content']
    return None


def search(results, lang, siteNum, searchData):
    directURL = slugify(searchData.title.replace('\'', ''), lowercase=True)

    directURL1 = PAsearchSites.getSearchSearchURL(siteNum) + directURL
    directURL2 = 'https://www.teamskeet.com/movies/' + directURL

    if directURL1 == directURL2:
        searchResultsURLs = [directURL1]
    else:
        searchResultsURLs = [directURL1, directURL2]

    googleResults = PAutils.getFromSearchEngine(searchData.title, siteNum)

    for sceneURL in googleResults:
        sceneURL = sceneURL.rsplit('?', 1)[0]
        if sceneURL not in searchResultsURLs:
            if ('/movies/' in sceneURL):
                searchResultsURLs.append(sceneURL)

    for sceneURL in searchResultsURLs:
        detailsPageElements = getJSONfromPage(sceneURL)

        if detailsPageElements:
            sceneType = None
            for type in ['moviesContent', 'videosContent']:
                if type in detailsPageElements and detailsPageElements[type]:
                    sceneType = type
                    break

            if sceneType:
                detailsPageElements = detailsPageElements[sceneType]
                curID = detailsPageElements.keys()[0]
                detailsPageElements = detailsPageElements[curID]
                titleNoFormatting = PAutils.parseTitle(detailsPageElements['title'], siteNum)
                if 'site' in detailsPageElements:
                    subSite = detailsPageElements['site']['name']
                else:
                    subSite = PAsearchSites.getSearchSiteName(siteNum)

                if 'publishedDate' in detailsPageElements:
                    releaseDate = parse(detailsPageElements['publishedDate']).strftime('%Y-%m-%d')
                else:
                    releaseDate = searchData.dateFormat() if searchData.date else ''
                displayDate = releaseDate if 'publishedDate' in detailsPageElements else ''

                if searchData.date and displayDate:
                    score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, releaseDate, sceneType), name='%s [%s] %s' % (titleNoFormatting, subSite, displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    cookies = {'age_verified': 'yes'}
    metadata_id = str(metadata.id).split('|')
    sceneName = metadata_id[0]
    sceneDate = metadata_id[2]
    sceneType = metadata_id[3].replace('content', 'Content')

    try:
        detailsPageElements = getJSONfromPage(PAsearchSites.getSearchSearchURL(siteNum) + sceneName)[sceneType][sceneName]
    except:
        detailsPageElements = getJSONfromPage('https://www.teamskeet.com/movies/%s' % sceneName)[sceneType][sceneName]

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements['title'], siteNum)

    # Summary
    metadata.summary = PAutils.strip_tags(detailsPageElements['description'])

    # Studio
    metadata.studio = 'TeamSkeet'

    # Tagline and Collection(s)
    if 'site' in detailsPageElements:
        tagline = detailsPageElements['site']['name']
    else:
        tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    movieCollections.addCollection(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actor(s)
    actors = detailsPageElements['models']
    for actorLink in actors:
        try:
            actorID = actorLink['modelId']
            actorName = actorLink['modelName']
        except:
            actorID = actorLink['id']
            actorName = actorLink['name']
        actorPhotoURL = ''

        try:
            try:
                actorData = getJSONfromPage('%s/models/%s' % (PAsearchSites.getSearchBaseURL(siteNum), actorID))
                actorPhotoURL = actorData['modelsContent'][actorID]['img']
            except:
                actorData = getJSONfromPage('https://www.teamskeet.com/models/%s' % actorID)
                actorPhotoURL = actorData['modelsContent'][actorID]['img']
        except:
            pass

        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    genres = []

    if 'tags' in detailsPageElements and detailsPageElements['tags']:
        for genreLink in detailsPageElements['tags']:
            genreName = genreLink.strip()

            genres.append(genreName)

    genres.extend(PAutils.getDictValuesFromKey(genresDB, tagline))

    for genreLink in genres:
        genreName = genreLink

        movieGenres.addGenre(genreName)

    # Posters
    art.append(detailsPageElements['img'])

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
