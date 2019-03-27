import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    # actress search
    searchString = searchTitle.lower().split('and')[0].strip().replace(" ","-")
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(searchSiteID) + searchString + "/")
    for searchResult in searchResults.xpath('//div[@class="panel-body"]'):
        actorList = []
        firstActor = searchResult.xpath('.//span[@class="scene-actors"]//a')[0].text_content()
        Log("firstActor: " + firstActor)
        actors = searchResult.xpath('.//span[@class="scene-actors"]//a')
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorList.append(actorName)
        titleNoFormatting = ", ".join(actorList)
        Log("Title (actress(es) in this case): " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').split('?')[0].replace('_', '+').replace("/", "_").replace('?', '!')
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//span[@class="scene-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), firstActor.lower())
        Log("score: " + str(score))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Tonight's Girlfriend] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace("_","/").replace('!','?').replace('+','_')
    detailsPageElements = HTML.ElementFromURL(url)

    # Actors
    movieActors.clearActors()
    actorList = []
    actors = detailsPageElements.xpath('//div[@class="scenepage-info"]//a')
        # sceneInfo contains actresses, who are links and have actress pages, actors (plain text), and date
    sceneInfo = detailsPageElements.xpath('//div[@class="scenepage-info"]//p')[0].text_content()
    for actorLink in actors:
        actorName = actorLink.text_content()
        actorList.append(actorName)
            # remove actress from sceneInfo
        sceneInfo = sceneInfo.replace(actorName + ",","").strip()
        actorPageURL = actorLink.get("href").split('?')[0]
        Log(actorName + ": " + actorPageURL)
        actorPageElements = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPageElements.xpath('//div[contains(@class,"modelpage-info")]//img')[0].get("src").split('?')[0]
        Log("actorPhotoURL: " + actorPhotoURL)
        movieActors.addActor(actorName,actorPhotoURL)

    # Title
    # scenes on this page have no title, making title = actress names
    metadata.title = ', '.join(actorList).replace(', ',' and ', -1)
    Log("title: " + metadata.title)

    # Date
    dateRaw = detailsPageElements.xpath('//span[@class="scenepage-date"]')[0].text_content()
    date = dateRaw.replace('Added:','').strip()
    Log("date: " + date)
    date_object = datetime.strptime(date, '%m-%d-%y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    backgroundURL = detailsPageElements.xpath('//img[@class="playcard"]')[0].get("src")
    metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    Log("BG URL: " + backgroundURL)

    # add actress image as possible poster if only one actress (could be picture from scene)
    posterBGNum = 1
    if len(actors) == 1:
        actorScenes = actorPageElements.xpath('//div[@class="panel-body"]')
        if len(actorScenes) == 1:
            # poster 1 if actress only has one scene (must be from current scene)
            Log("actor photo to poster 1")
            metadata.posters[actorPhotoURL] = Proxy.Preview(HTTP.Request(actorPhotoURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
            posterBGNum = 2
        else:
            # poster 2 if actress has > 1 scene (possibly from current scene)
            Log("actor photo to poster 2")
            metadata.posters[actorPhotoURL] = Proxy.Preview(HTTP.Request(actorPhotoURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 2)
    metadata.posters[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterBGNum)

    # rest of actors (male actors without pages on the site)
    sceneInfo = sceneInfo.replace(dateRaw,'')
    maleActors = sceneInfo.split(',')
    for maleActor in maleActors:
        actorName = maleActor.strip()
        # not working for now, but providing non '' value so actorDBfinder isnt used
        actorPhotoURL = '../Resources/actorDummy.png'
        movieActors.addActor(actorName,actorPhotoURL)



    # Tagline, Studio, Collections
        # note: I think only tonight's girlfriend classic (old scenes) is part of NA so keeping this separate
    studio = "Tonight's Girlfriend"
    metadata.studio = studio
    metadata.tagline = studio
    metadata.collections.clear()
    metadata.collections.add(studio)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="scenepage-description"]//p')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    genres = ["GFE", "Girlfriend Experience", "Pornstar", "Hotel", "PSE", "Pornstar Experience"]
    if (len(actors) + len(maleActors)) == 3:
        genres.append("Threesome")
        if len(actors) == 2:
            genres.append("BGG")
        else:
            genres.append("BBG")
    for genre in genres:
        movieGenres.addGenre(genre)





    return metadata
