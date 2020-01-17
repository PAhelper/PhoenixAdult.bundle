import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    try:
        modelID = '-'.join(encodedTitle.split("%20", 2)[:2])
        Log("modelID: " + modelID)
        try:
            sceneTitle = encodedTitle.split("%20", 2)[2]
        except:
            sceneTitle = ''
        Log("Scene Title: " + sceneTitle)

        url = PAsearchSites.getSearchSearchURL(siteNum) + modelID + ".html"
        searchResults = HTML.ElementFromURL(url)
    except:
        modelID = encodedTitle.split("%20", 1)[0]
        Log("modelID: " + modelID)
        try:
            sceneTitle = encodedTitle.split("%20", 1)[1]
        except:
            sceneTitle = ''
        Log("Scene Title: " + sceneTitle)

        url = PAsearchSites.getSearchSearchURL(siteNum) + modelID + ".html"
        searchResults = HTML.ElementFromURL(url)

    for searchResult in searchResults.xpath('//div[@class="update_block"]'):
        titleNoFormatting = searchResult.xpath('.//span[@class="update_title"]')[0].text_content().strip()
        titleNoFormatting = titleNoFormatting.replace('/', '$').replace('?', '+')
        summary = searchResult.xpath('.//span[@class="latest_update_description"]')[0].text_content().strip()
        summary = summary.replace('/', '$').replace('?', '+')
        releaseDate = parse(searchResult.xpath('.//span[@class="update_date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        actorList = []
        actors = searchResult.xpath('.//span[@class="tour_update_models"]/a')
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorList.append(actorName)
        actors = ','.join(actorList)
        videoBG = searchResult.xpath('.//div[@class="update_image"]/a/img')[0].get('src')
        videoBG = videoBG.replace('/', '$').replace('?', '+')

        # Fake Unique CurID
        curID = titleNoFormatting
        # Other Variables
        subSite = PAsearchSites.getSearchSiteName(siteNum)

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        elif sceneTitle:
            score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
        else:
            score = 60
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + titleNoFormatting + "|" + summary + "|" + releaseDate + "|" + actors + "|" + videoBG, name = titleNoFormatting + " [PureCFNM/" + subSite + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE METADATA CALLED*******')

    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'PureCFNM'

    # Title
    metadata.title = str(metadata.id).split("|")[2]
    metadata.title = metadata.title.replace('$', '/').replace('+', '?')

    # Summary
    metadata.summary = str(metadata.id).split("|")[3]
    metadata.summary = metadata.summary.replace('$', '/').replace('+', '?')

    # Tagline and Collection(s)
    subSite = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = subSite
    metadata.collections.add(subSite)

    # Genres
    if subSite.lower() == "AmateurCFNM".lower():
        for genreName in ['CFNM']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "CFNMGames".lower():
        for genreName in ['CFNM','Femdom']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "GirlsAbuseGuys".lower():
        for genreName in ['CFNM','Femdom','Male Humiliation']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "HeyLittleDick".lower():
        for genreName in ['CFNM','Femdom', "Small Penis Humiliation"]:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "LadyVoyeurs".lower():
        for genreName in ['CFNM', 'Voyeur']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "PureCFNM".lower():
        for genreName in ['CFNM']:
            movieGenres.addGenre(genreName)

    # Release Date
    date = str(metadata.id).split("|")[4]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = str(metadata.id).split("|")[5]
    actors = actors.split(",")
    for actorLink in actors:
        actorName = str(actorLink.strip())
        actorPhotoURL = ""
        movieActors.addActor(actorName,actorPhotoURL)
    if len(actors) > 0:
        if len(actors) == 2:
            movieGenres.addGenre("Threesome")
        if len(actors) == 3:
            movieGenres.addGenre("Foursome")
        if len(actors) > 3:
            movieGenres.addGenre("Group")

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = str(metadata.id).split("|")[6]
        twitterBG = PAsearchSites.getSearchBaseURL(siteID) + twitterBG.replace('$', '/').replace('+', '?')
        art.append(twitterBG)
    except:
        pass

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            j = j + 1

    return metadata