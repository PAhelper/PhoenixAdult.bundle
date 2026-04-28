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

    try:
        detailsPageElements = getJSONfromPage(PAsearchSites.getSearchSearchURL(siteNum) + sceneName)
    except:
        detailsPageElements = getJSONfromPage('https://www.%s.com/movies/%s' % (searchNetworkCleanLower, sceneName))

    if sceneType in detailsPageElements:
        detailsPageElements = detailsPageElements[sceneType][sceneName]
    else:
        detailsPageElements = detailsPageElements['videosContent'][sceneName]
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

    genres.extend(PAutils.getDictValuesFromKey(genresDB, subSite))

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
    'Full Of JOI': ['JOI'],
    'Ginger Patch': ['Redhead'],
    'Innocent High': ['School Girl'],
    'Little Asians': ['Asian', 'Teen'],
    'Lone MILF': ['Solo'],
    'Milf Body': ['Gym', 'Fitness'],
    'Milfty': ['Cheating'],
    'MomDrips': ['Creampie'],
    'MylfBlows': ['Blowjob'],
    'MylfBoss': ['Office', 'Boss'],
    'MylfDom': ['BDSM'],
    'Mylfed': ['Lesbian', 'Girl on Girl', 'GG'],
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
    'Glowupz', 'Her Freshman Year', 'Hijab Hookup', 'I Made Porn', 'Innocent High', 'Kissing Sis', 'Latina Team',
    'Little Asians', 'Lust HD', 'Messy Jessy', 'Mormon Girlz', 'My Babysitters Club', 'My Dirty Uncle',
    'My First', 'MYLF Classics', 'MYLF Labs', 'Our Little Secret', 'Oye Loca', 'Passport Bros', 'Petite Teens 18',
    'POV Life', 'Reptyle Classics', 'Reptyle Labs', 'Rub A Teen', 'Self Desire', 'Sex and Grades',
    'She\'s New', 'Solo Interviews', 'Spanish 18', 'Stay Home POV', 'Step Siblings', 'TeamSkeet AllStars',
    'TeamSkeet Classics', 'TeamSkeet Extras', 'TeamSkeet Features', 'TeamSkeet Labs', 'TeamSkeet Singles',
    'TeamSkeet VIP', 'TeamSkeet', 'Teen Curves', 'Teen JOI', 'Teen Pies', 'Teens Do Porn', 'Teens Love Anal',
    'Teens Love Black Cocks', 'Teens Love Money', 'Teeny Black', 'The Loft', 'The Real Workout', 'Thickumz',
    'This Girl Sucks', 'Titty Attack', 'Tomboyz',
}
