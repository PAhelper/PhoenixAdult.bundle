import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    Log("searchTitle:" + searchTitle)
    searchTitle = searchTitle.replace(' And ',',').replace(' and ',',').replace(' AND ',',')
    Log("searchTitle replaced:" + searchTitle)
    actors = searchTitle.split(",")
    actorsFormatted = []
    for actor in actors:
        actorsFormatted.append(actor.strip().title())
    curID = '+'.join(actorsFormatted).replace(' ','_')
    Log("curID: " + curID)
    if searchDate:
        releaseDate = parse(searchDate).strftime('%Y-%m-%d')
        Log("releaseDate found: " + releaseDate)
    else:
        releaseDate = 'no_date'
    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = curID + "[Add Actor] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log("*******Manual actor input*******")


    # Title
    actorList = str(metadata.id).split("|")[0].replace('_',' ').replace('+',', ')
    metadata.title = actorList
    Log('title: ' + actorList)

    # Actors
    movieActors.clearActors()
    Log("metadata.id: " + str(metadata.id))
    actors = actorList.split(',')
    for actor in actors:
        actorName = actor.strip().title()
        actorPhotoURL = ''
        movieActors.addActor(actorName,actorPhotoURL)
        Log("added actor: " + actorName)

    # Release Date
    date = str(metadata.id).split("|")[2]
    if date != 'no_date':
        Log("Date Found")
        date_Object = parse(date)
        metadata.originally_available_at = date_Object
        metadata.year = metadata.originally_available_at.year

    # Studio


    # Tagline and Collection(s)
    metadata.collections.clear()
    marker = "Actors Manually Added"
    metadata.collections.add(marker)
    # Genres
    movieGenres.clearGenres()


    return metadata
