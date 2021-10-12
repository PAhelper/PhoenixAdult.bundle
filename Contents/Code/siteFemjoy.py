import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchURL = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded
    req = PAutils.HTTPRequest(searchURL)
    searchResults = req.json()

    if 'results' not in searchResults or not searchResults['results'] and searchData.filename:
        # femjoy.17.03.12.maria.rya.girl.in.the.mirror.mp4
        # try to extract as much of the title as possible without including the model
        m = re.search(r'femjoy\.(\d{2}\.\d{2}\.\d{2})\.(.+)', searchData.filename, re.IGNORECASE)
        if m:
            searchData.date = parse('20' + m.group(1)).strftime('%Y-%m-%d')
            searchWords = m.group(2).split('.')
            wordCount = len(searchWords)
            if wordCount > 2:
                searchData.title = ' '.join(searchWords[2:])
            else:
                searchData.title = searchWords[-1]

        else:
            # Belinda & Fiva - Give me your hand 29-Mar-2010.mp4
            # take everything from after the dash and before the date
            m = re.search(r'.+ - (.+) (\d{2}-[a-z]{3}-\d{4})', searchData.filename, re.IGNORECASE)
            if m:
                searchData.date = parse(m.group(2)).strftime('%Y-%m-%d')
                searchData.title = m.group(1)

        searchData.encoded = urllib.quote(searchData.title)
        searchURL = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded
        req = PAutils.HTTPRequest(searchURL)
        searchResults = req.json()

    if 'results' in searchResults:
        curID = PAutils.Encode(searchURL)

        for searchResult in searchResults['results']:
            titleNoFormatting = searchResult['title']
            sceneID = searchResult['id']

            date = searchResult['release_date']
            if date:
                releaseDate = parse(date).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''
            displayDate = releaseDate if date else ''

            actorsName = [actorLink['name'] for actorLink in searchResult['actors']]
            actorsString = getActorsString(actorsName)

            if searchData.date and displayDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%d' % (curID, siteNum, sceneID), name='%s - %s [%s] %s' % (titleNoFormatting, actorsString, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    searchURL = PAutils.Decode(metadata_id[0])
    sceneID = int(metadata_id[2])
    req = PAutils.HTTPRequest(searchURL)
    detailsPageElements = None
    searchResults = req.json()
    if 'results' not in searchResults:
        return metadata

    for searchResult in searchResults['results']:
        if searchResult['id'] == sceneID:
            detailsPageElements = searchResult
            break

    if not detailsPageElements:
        return metadata

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = re.sub(r'<.*?>', '', detailsPageElements['long_description']).strip()  # must strip HTML tags

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Release date
    date_object = parse(detailsPageElements['release_date'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = []

    for genreLink in genres:
        genreName = genreLink

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    if 'actors' in detailsPageElements:
        actors = detailsPageElements['actors']
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink['name']
            actorPhotoURL = actorLink['thumb']['image']

            if actorPhotoURL.endswith('noimageavailable.gif'):
                actorSearchURL = PAsearchSites.getSearchBaseURL(siteNum) + '/api/v2/search/actors?thumb_size=355x475&query=' + actorName.split()[0]
                req = PAutils.HTTPRequest(actorSearchURL)
                searchResults = req.json()
                if 'results' in searchResults:
                    for searchResult in searchResults['results']:
                        if searchResult['id'] == actorLink['id']:
                            actorPhotoURL = searchResult['thumb']['image']
                            break

            movieActors.addActor(actorName, actorPhotoURL)

    # Director
    metadata.directors.clear()
    if 'directors' in detailsPageElements:
        for directorLink in detailsPageElements['directors']:
            director = metadata.directors.new()
            director.name = directorLink['name']

    # Posters
    art = [
        detailsPageElements['thumb']['image']
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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata


def getActorsString(actors):
    count = len(actors)
    if count > 1:
        actors[count - 2] = ' and '.join(actors[-2:])
        actors = actors[:-1]

    return ', '.join(actors)
