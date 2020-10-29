import PAsearchSites
import PAgenres
import PAactors


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    Log("searchTitle:" + searchTitle)
    searchTitle = searchTitle.replace(' AND ', ' and ').replace(' And ', ' and ').replace(' In ', ' in ').replace(' At ', ' at ')
    parse_siteName = searchTitle.rsplit(' at ', 1)  # only split on last 'at'
    if len(parse_siteName) > 1:
        siteName = parse_siteName[1].strip()
        Log("Manual Site Name: " + siteName)
    else:
        siteName = ''
    parse_sceneName = parse_siteName[0].split(' in ', 1)  # only split on first 'in'
    if len(parse_sceneName) > 1:
        sceneName = parse_sceneName[1].strip().title()
        Log("Manual Scene Name: " + sceneName)
    else:
        sceneName = ''
    actors = parse_sceneName[0].split("and")
    actorsFormatted = []
    for actor in actors:
        actorsFormatted.append(actor.strip().title())
    curID = '+'.join(actorsFormatted).replace(' ', '_')
    Log("curID: " + curID)
    if searchDate:
        releaseDate = parse(searchDate).strftime('%Y-%m-%d')
    else:
        releaseDate = ''

    score = 100
    metadataID = '%s|%d' % (curID, siteNum) + "|" + releaseDate + "|" + sceneName + "|" + siteName
    Log("metadata.id to pass: " + metadataID)
    displayName = curID.replace('+', ', ').replace('_', ' ')
    results.Append(MetadataSearchResult(id=metadataID, name=displayName + "[" + siteName + "] " + releaseDate, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    Log("*******Manual actor input*******")

    # Actors
    movieActors.clearActors()
    Log("metadata.id: " + str(metadata.id))
    actorList = str(metadata.id).split('|')[0].replace('_', ' ').replace('+', ', ')
    actors = actorList.split(',')
    for actor in actors:
        actorName = actor.strip().title()
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
        Log("added actor: " + actorName)

    # Release Date
    date = str(metadata.id).split('|')[2]
    if len(date) > 0:
        Log("Date Found")
        date_Object = parse(date)
        metadata.originally_available_at = date_Object
        metadata.year = metadata.originally_available_at.year
    else:
        Log("No Date Found")

    # Tagline and Collection(s)
    metadata.collections.clear()
    marker = "Actors Manually Added"
    metadata.collections.add(marker)

    # Studio
    siteName = str(metadata.id).split('|')[4].strip().title()
    if len(siteName) > 0:
        metadata.studio = siteName
        metadata.collections.add(siteName)
        Log("Found Studio/SiteName: " + siteName)

    # Title
    sceneName = str(metadata.id).split('|')[3].strip().title()
    if len(sceneName) > 0:
        metadata.title = sceneName
        Log("sceneName: " + sceneName)
    else:
        if len(siteName) > 0:
            metadata.title = actorList + " - " + siteName
            Log('title: ' + metadata.title)
        else:
            metadata.title = actorList
            Log('title/actorList: ' + metadata.title)

    # Genres
    # movieGenres.clearGenres()

    return metadata
