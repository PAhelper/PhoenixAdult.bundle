import PAutils

regexList = [
    r'(?P<actors>.*?) (in\b(?P<title>.*)) (at\b(?P<studio>.*)) (with\b(?P<genres>.*))',
    r'(?P<actors>.*?) (in\b(?P<title>.*)) (with\b(?P<genres>.*))',
    r'(?P<actors>.*?) (in\b(?P<title>.*)) (at\b(?P<studio>.*))',
    r'(?P<actors>.*?) (in\b(?P<title>.*))',
]


def search(results, lang, siteNum, searchData):
    data = {}
    for regex in regexList:
        r = re.search(regex, searchData.title, flags=re.IGNORECASE)
        if r:
            data = r.groupdict()
            break

    if data:
        sceneName = data['title'].strip()
        siteName = data['studio'].strip() if 'studio' in data else ''

        genres = data['genres'].strip() if 'genres' in data else ''
        genresID = PAutils.Encode(genres)

        actors = data['actors'].strip()
        actors = ', '.join(actors.split(' and ')) if ' and ' in actors else actors  # Backward compatibility
        actorsID = PAutils.Encode(actors)

    if searchData.date:
        releaseDate = searchData.dateFormat()
    else:
        releaseDate = ''

    score = 100

    results.Append(MetadataSearchResult(id='%s|%d|%s|%s|%s|%s' % (actorsID, siteNum, releaseDate, sceneName, siteName, genresID), name='%s [%s] %s' % (sceneName, siteName, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneActors = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    sceneName = metadata_id[3]
    siteName = metadata_id[4]
    sceneGenres = PAutils.Decode(metadata_id[5]) if len(metadata_id) > 5 else ''

    # Title
    if sceneName:
        metadata.title = sceneName
    elif siteName:
        metadata.title = '%s - %s' % (sceneActors, siteName)
    else:
        metadata.title = sceneActors

    # Studio
    if siteName:
        metadata.studio = siteName
        metadata.collections.add(siteName)

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = 'Actors Manually Added'
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_Object = parse(sceneDate)
        metadata.originally_available_at = date_Object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in sceneGenres.split(','):
        genreName = genreLink.strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in sceneActors.split(','):
        actorName = actorLink.strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    return metadata
