import PAsearchSites
import PAutils


def search(results, media, lang, siteNum, searchTitle, encodedTitle, searchDate):
    encodedTitle = urllib.quote(searchTitle.lower())
    searchURL = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
    req = PAutils.HTTPRequest(searchURL)
    sceneJson = req.json()

    if not sceneJson.get('results') and media.filename:
        mediaFilename = urllib.unquote(media.filename)
        filename = mediaFilename[mediaFilename.rindex('/')+1:]

        # femjoy.17.03.12.maria.rya.girl.in.the.mirror.mp4
        # try to extract as much of the title as possible without including the model
        m = re.search(r'femjoy\.(\d{2}\.\d{2}\.\d{2})\.(.+)\.(mp4|wmv|mov|m4a)', filename, re.IGNORECASE)
        if m:
            searchDate = parse('20' + m.group(1)).strftime('%Y-%m-%d')
            searchWords = m.group(2).split('.')
            wordCount = len(searchWords)
            if wordCount > 2:
                searchTitle = ' '.join(searchWords[2:])
            elif wordCount > 1:
                searchTitle = urlsearchWords[1]
            else:
                searchTitle = searchWords[0]

            # Log('alternate match 1: %s / %s' % (searchDate, searchTitle))
            encodedTitle = urllib.quote(searchTitle.lower())
            searchURL = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
            req = PAutils.HTTPRequest(searchURL)
            sceneJson = req.json()

            if not sceneJson or not sceneJson.get('results'):
                return results
        else:
            # Belinda & Fiva - Give me your hand 29-Mar-2010.mp4
            # take everything from after the dash and before the date
            m = re.search(r'.+ - (.+) (\d{2}-[a-z]{3}-\d{4})\.(mp4|wmv|mov|m4a)', filename, re.IGNORECASE)
            if m:
                searchDate = parse(m.group(2)).strftime('%Y-%m-%d')
                searchTitle = m.group(1)

                # Log('alternate match 2: ' + searchTitle)
                encodedTitle = urllib.quote(searchTitle.lower())
                searchURL = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
                req = PAutils.HTTPRequest(searchURL)
                sceneJson = req.json()

                if not sceneJson or not sceneJson.get('results'):
                    return results

    # Log('search for %s on %s' % (searchTitle, searchDate))

    curID = PAutils.Encode(searchURL)

    for scene in sceneJson['results']:
        titleNoFormatting = scene.get('title')
        slug = scene.get('slug')

        date = scene.get('release_date')
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
        releaseDate = parse(date).strftime('%Y-%m-%d')
        displayDate = releaseDate if date else ''

        actorsString = getActorsString(scene.get('actors'))

        if searchDate and displayDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, slug), name='%s - %s [%s] %s' % (titleNoFormatting, actorsString, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    searchURL = PAutils.Decode(metadata_id[0])
    slug = metadata_id[2]
    req = PAutils.HTTPRequest(searchURL)
    sceneJson = req.json()
    if not sceneJson:
        # couldn't load the specified JSON
        return metadata

    movieGenres.clearGenres()
    movieActors.clearActors()

    for sceneTest in sceneJson['results']:
        if sceneTest.get('slug') == slug:
            scene = sceneTest
            break

    if not scene:
        # couldn't find the specified scene in the JSON
        return metadata

    # Title
    # metadata.title = '%s - %s' % (scene.get('title'), getActorsString(scene.get('actors'))) # do we want the actor names in the title?
    metadata.title = scene.get('title')

    # Summary
    metadata.summary = re.sub(r'<.*?>', '', scene.get('long_description')) # must strip HTML tags

    # Release date
    dateObj = parse(scene.get('release_date'))
    metadata.originally_available_at = dateObj
    metadata.year = metadata.originally_available_at.year

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    Log('%s, %s, %s' % (metadata.title, dateObj.strftime('%Y-%m-%d'), metadata.summary))

    # Actors
    if scene.get('actors'):
        for actor in scene['actors']:
            # Log('actor: %s' % actor.get('name'))
            actorName = actor.get('name')
            actorPic = actor['thumb']['image']
            Log('actor from JSON: %s / %s' % (actorName, actorPic))

            if actorPic.find('noimageavailable.gif') >= 0:
                actorID = actor.get('id')
                modelSearchUrl = 'https://femjoy.com/api/v2/search/actors?thumb_size=355x475&limit=50&query=' + actorName.split(' ')[0]
                req = PAutils.HTTPRequest(modelSearchUrl)
                modelsJson = req.json()
                if modelsJson:
                    for model in modelsJson['results']:
                        if model.get('id') == actorID:
                            actorPic = model['thumb']['image']
                            Log('actor from HTTP: %s / %s' % (actorName, actorPic))
                            break

            movieActors.addActor(actorName, actorPic)

    # Director
    if scene.get('directors'):
        for directorJson in scene['directors']:
            director = metadata.directors.new()
            director.name = directorJson.get('name')

    # Posters
    art = [
        scene['thumb']['image']
    ]

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'https://femjoy.com/' + scene.get('slug')})
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
    # produce 'a, b, c and d' from a list of actor objects
    names = []
    for actor in actors:
        names.append(actor.get('name'))

    count = len(names)
    if count == 1:
        return names[0]
    else:
        names[count - 2] = ' and '.join(names[-2:])
        names.pop(count - 1)
        return ', '.join(names)
