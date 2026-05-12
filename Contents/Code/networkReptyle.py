import PAsearchSites
import PAutils
from PAdata18ImageSearch import getSceneURLFromData18, getData18Images


def getJSONfromPage(url):
    cookies = {'age_verified': 'yes'}
    req = PAutils.HTTPRequest(url, cookies=cookies)

    if req:
        jsonData = re.search(r'window\.__INITIAL_STATE__ = (.*);', req.text)
        if jsonData:
            return json.loads(jsonData.group(1))['content']

    return None


def getSubNetwork(subSite, type=None):
    subSiteLower = subSite.lower().replace(' ', '')

    # All MYLF X Videos are now only hosted on TeamSkeet
    if subSiteLower.startswith('teamskeetx') or (type == 'search' and subSiteLower.startswith('mylfx')):
        return 'TeamSkeet'

    if not type and subSiteLower.startswith('mylfx'):
        return 'MYLF'

    for db, subNetwork in ((mylfDB, 'MYLF'), (teamskeetDB, 'TeamSkeet'), (swappzDB, 'Swappz'), (freeuseDB, 'FreeUse'), (pervzDB, 'Pervz'), (familystrokesDB, 'Family Strokes')):
        if re.sub(r'\W', '', subSite).lower() in map(lambda x: re.sub(r'\W', '', x).lower(), db):
            return subNetwork

    return None


def getArtwork(metadata, art):
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

    return


def getSubSite(subSite):
    for db in (mylfDB, teamskeetDB, swappzDB, freeuseDB, pervzDB, familystrokesDB):
        for site in db:
            if re.sub(r'\W', '', subSite).lower() == re.sub(r'\W', '', site).lower():
                return site

    return subSite


def search(results, lang, siteNum, searchData):
    directURL = slugify(searchData.title.replace('\'', ''), lowercase=True)

    subSite = re.sub(r'\W', '', PAsearchSites.getSearchSiteName(siteNum))

    searchNetwork = getSubNetwork(subSite, 'search')
    searchNetworkCleanLower = re.sub(r'\W', '', searchNetwork).lower()

    directURL1 = '%s%s' % (PAsearchSites.getSearchSearchURL(siteNum), directURL)
    directURL2 = 'https://www.%s.com/movies/%s' % (searchNetworkCleanLower, directURL)

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

                results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, releaseDate, sceneType), name='%s [%s] %s' % (titleNoFormatting, getSubSite(subSite), displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneName = metadata_id[0]
    sceneDate = metadata_id[2]
    sceneType = metadata_id[3].replace('content', 'Content')

    searchNetwork = getSubNetwork(PAsearchSites.getSearchSiteName(siteNum), 'search')
    searchNetworkCleanLower = re.sub(r'\W', '', searchNetwork).lower()

    detailsPageJson = getJSONfromPage(PAsearchSites.getSearchSearchURL(siteNum) + sceneName)
    detailsPageElements = None

    if sceneType in detailsPageJson and sceneName in detailsPageJson[sceneType]:
        detailsPageElements = detailsPageJson[sceneType][sceneName]
    elif 'videosContent' in detailsPageJson and sceneName in detailsPageJson['videosContent']:
        detailsPageElements = detailsPageJson['videosContent'][sceneName]
    else:
        for pageJson in (detailsPageJson, getJSONfromPage('https://www.%s.com/movies/%s' % (searchNetworkCleanLower, sceneName))):
            if sceneType in pageJson and sceneName in pageJson[sceneType]:
                detailsPageElements = pageJson[sceneType][sceneName]
                break
            if 'videosContent' in pageJson and sceneName in pageJson['videosContent']:
                detailsPageElements = pageJson['videosContent'][sceneName]
                break

    subSite = getSubSite(detailsPageElements['site']['name'] if 'site' in detailsPageElements else PAsearchSites.getSearchSiteName(siteNum))
    subNetwork = getSubNetwork(subSite)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements['title'], siteNum)

    # Summary
    metadata.summary = PAutils.strip_tags(detailsPageElements['description'])

    # Studio
    metadata.studio = subNetwork if subNetwork else 'Reptyle'

    # Tagline and Collection(s)
    if not subSite == subNetwork:
        metadata.tagline = subSite
    movieCollections.addCollection(subSite)

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
                actorData = getJSONfromPage('https://www.%s.com/models/%s' % (searchNetworkCleanLower, actorID))
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

    if (len(actors) > 1) and subSite != 'Mylfed':
        genres.append('Threesome')

    for genreLink in genres:
        genreName = genreLink

        movieGenres.addGenre(genreName)

    # Posters
    art.append(detailsPageElements['img'])
    if Prefs['data18_enable']:
        scene_id = PAutils.getDictKeyFromValues(data18ManualMappings, detailsPageElements['id'])
        if scene_id:
            data18Url = ('https://www.data18.com/scenes/%s' % scene_id[0])
        else:
            providers = ['TeamSkeet', 'MYLF', 'Family Strokes', 'Pervz', 'FreeUse', 'Swappz', subSite]
            data18Url = getSceneURLFromData18(metadata.title, providers, date_object if sceneDate else None)

        getData18Images(data18Url, art, metadata) if data18Url else getArtwork(metadata, art)
    else:
        getArtwork(metadata, art)

    return metadata


familystrokesDB = {
    'Ask Your Mother', 'Black Step Dad', 'Dad Crush', 'Family Strokes', 'Family Strokes Features',
    'Foster Tapes', 'Not My Grandpa', 'Perv Mom', 'Perv Nana', 'Sis Loves Me', 'Tiny Sis',
}


freeuseDB = {
    'Freaky Fembots', 'FreeUse', 'FreeUse Fantasy', 'FreeUse MILF', 'FreeUse Singles', 'Use POV',
}


mylfDB = {
    'Anal Mom', 'BBC Paradise', 'Blue Collar Babes', 'Full Of JOI', 'Got MYLF', 'Hijab MYLFs',
    'Hookup Pad', 'Lone MILF', 'MILF Body', 'Milfty', 'Mom Drips', 'Mom Shoot', 'Mommy\'s Little Man',
    'MYLF', 'MYLF After Dark', 'MYLF Blows', 'MYLF Boss', 'MYLF Features', 'MYLF of the Month',
    'MYLF Singles', 'Mylfdom', 'Mylfed', 'MylfWood', 'New MYLFs', 'Oye Mami', 'Secrets', 'Shag Street',
    'Stay Home MILF', 'Tiger Moms',
}


pervzDB = {
    'Charmed', 'MILF Taxi', 'Perv Doctor', 'Perv Driver', 'Perv Massage', 'Perv Principal',
    'Perv Singles', 'Perv Therapy', 'Pervz', 'Pervz Features', 'Shoplyfter MYLF', 'Shoplyfter',
}


swappzDB = {
    'Daughter Swap', 'Mom Swap', 'Sis Swap', 'Swappz',
}


teamskeetDB = {
    'After Dark', 'Anal Euro', 'Bad MILFs', 'BFFs', 'Black Valley Girls', 'Brace Faced', 'Brat Tamer',
    'Breeding Material', 'CFNM Teens', 'Ciao Bella', 'Daddy Pounds', 'Dyked', 'Exxxtra Small', 'Ginger Patch',
    'Glowupz', 'Her Freshman Year', 'Hijab Hookup', 'Hussie Pass', 'I Made Porn', 'Innocent High', 'Kissing Sis',
    'Latina Team', 'Little Asians', 'Lust HD', 'Messy Jessy', 'Mormon Girlz', 'My Babysitters Club', 'My Dirty Uncle',
    'My First', 'MYLF Classics', 'MYLF Labs', 'Our Little Secret', 'Oye Loca', 'Passport Bros', 'Petite Teens 18',
    'POV Life', 'Reptyle Classics', 'Reptyle Labs', 'Rub A Teen', 'Self Desire', 'Sex and Grades',
    'She\'s New', 'Solo Interviews', 'Spanish 18', 'Stay Home POV', 'Step Siblings', 'TeamSkeet AllStars',
    'TeamSkeet Classics', 'TeamSkeet Extras', 'TeamSkeet Features', 'TeamSkeet Labs', 'TeamSkeet Singles',
    'TeamSkeet VIP', 'TeamSkeet', 'Teen Curves', 'Teen JOI', 'Teen Pies', 'Teens Do Porn', 'Teens Love Anal',
    'Teens Love Black Cocks', 'Teens Love Money', 'Teeny Black', 'The Loft', 'The Real Workout', 'Thickumz',
    'This Girl Sucks', 'Titty Attack', 'Tomboyz',
}


data18ManualMappings = {
    169646: ['thats-better-than-stealing-it'],
    1313219: ['delicious-firsts'],
    1349311: ['thanksgiving-the-hijab-way'],
    1341218: ['the-vamp-next-door'],
    1341212: ['home-for-the-holidays'],
}
