import PAsearchSites
import PAgenres
import PAactors
import PAutils


def getJSONfromPage(url):
    req = PAutils.HTTPRequest(url)

    if req:
        jsonData = re.search(r'window\.__INITIAL_STATE__ = (.*);', req.text)
        if jsonData:
            return json.loads(jsonData.group(1))['content']
    return None


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    directURL = searchTitle.replace(' ', '-').lower()
    if '/' not in directURL:
        directURL = directURL.replace('-', '/', 1)

    shootID = directURL.split('/', 2)[0]
    if not unicode(shootID, 'UTF-8').isdigit():
        shootID = None
        directURL = directURL.replace('/', '-', 1)
    else:
        directURL = directURL.split('/')[1]

    directURL = PAsearchSites.getSearchSearchURL(siteNum) + directURL
    searchResultsURLs = [directURL]

    googleResults = PAutils.getFromGoogleSearch(searchTitle, siteNum)

    for sceneURL in googleResults:
        sceneURL = sceneURL.rsplit('?', 1)[0]
        if sceneURL not in searchResultsURLs:
            if ('/movies/' in sceneURL):
                searchResultsURLs.append(sceneURL)

    for sceneURL in searchResultsURLs:
        detailsPageElements = getJSONfromPage(sceneURL)

        if detailsPageElements:
            contentName = None
            for name in ['moviesContent', 'videosContent']:
                if name in detailsPageElements and detailsPageElements[name]:
                    contentName = name
                    break

            if contentName:
                detailsPageElements = detailsPageElements[contentName]
                curID = detailsPageElements.keys()[0]
                detailsPageElements = detailsPageElements[curID]
                titleNoFormatting = detailsPageElements['title']
                if 'site' in detailsPageElements:
                    subSite = detailsPageElements['site']['name']
                else:
                    subSite = PAsearchSites.getSearchSiteName(siteNum)

                if 'publishedDate' in detailsPageElements:
                    releaseDate = parse(detailsPageElements['publishedDate']).strftime('%Y-%m-%d')
                else:
                    releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
                displayDate = releaseDate if 'publishedDate' in detailsPageElements else ''

                if searchDate and displayDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, releaseDate, contentName), name='%s [Mylf/%s] %s' % (titleNoFormatting, subSite, displayDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneName = metadata_id[0]
    releaseDate = metadata_id[2]
    contentName = metadata_id[3]

    detailsPageElements = getJSONfromPage(PAsearchSites.getSearchSearchURL(siteID) + sceneName)[contentName][sceneName]

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = detailsPageElements['description']

    # Studio
    metadata.studio = 'Mylf'

    # Tagline and Collection(s)
    metadata.collections.clear()
    if 'site' in detailsPageElements:
        subSite = detailsPageElements['site']['name']
    else:
        subSite = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = subSite
    metadata.collections.add(subSite)

    # Release Date
    if releaseDate:
        date_object = parse(releaseDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements['models']
    for actorLink in actors:
        actorID = actorLink['modelId']
        actorName = actorLink['modelName']
        actorPhotoURL = ''

        actorData = getJSONfromPage('%s/models/%s' % (PAsearchSites.getSearchBaseURL(siteID), actorID))
        if actorData:
            actorPhotoURL = actorData['modelsContent'][actorID]['img']

        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = ["MILF", "Mature"]

    if subSite.lower() == 'MylfBoss'.lower():
        for genreName in ['Office', 'Boss']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'MylfBlows'.lower():
        for genreName in ['Blowjob']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'Milfty'.lower():
        for genreName in ['Cheating']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'Mom Drips'.lower():
        for genreName in ['Creampie']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'Milf Body'.lower():
        for genreName in ['Gym', 'Fitness']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'Lone Milf'.lower():
        for genreName in ['Solo']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'Full Of JOI'.lower():
        for genreName in ['JOI']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'Mylfed'.lower():
        for genreName in ['Lesbian', 'Girl on Girl', 'GG']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'MylfDom'.lower():
        for genreName in ['BDSM']:
            movieGenres.addGenre(genreName)
    if (len(actors) > 1) and subSite != 'Mylfed':
        genres.append('Threesome')

    for genre in genres:
        movieGenres.addGenre(genre)

    # Posters
    art = [
        detailsPageElements['img']
    ]

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.google.com'})
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
