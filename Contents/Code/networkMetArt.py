import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchPageNum = 1
    while searchPageNum <= 2:
        url = PAsearchSites.getSearchSearchURL(searchSiteID) + encodedTitle + "/relevance~0~68~-~-~-~-~-~-/" + str(searchPageNum)
        Log("url: " + url)
        searchResults = HTML.ElementFromURL(url)
        pageTitle = searchResults.xpath('//h1')[0].text_content().lower()
        if "found" in pageTitle:
            resultsNum = len(searchResults.xpath('//li[@class="list-group-item"] | //div[contains(@class,"item")]'))
            Log("resultsNum: " + str(resultsNum))
            if resultsNum > 0:
                for searchResult in searchResults.xpath('//li[@class="list-group-item"] | //div[contains(@class,"item")]'):
                    curID = searchResult.xpath('.//a[contains(@class,"item-name")]')[0].get('href').replace('/','+').replace('?','!')
                    if "+movie+" in curID: # model page and photos in search results
                        Log(">>>VALID RESULT<<<")
                        titleNoFormatting = searchResult.xpath('.//a[contains(@class,"item-name")]')[0].text_content()
                        Log("Result title: " + titleNoFormatting)
                        Log("curID: " + curID)
                        releaseDate = searchResult.xpath('.//span[contains(@class,"item-date")]')[0].text_content().split("Rated")[0].strip()
                        Log("releaseDate: " + releaseDate)
                        if searchDate:
                            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                        else:
                            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                        Log("Score: " + str(score))
                        results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(searchSiteID) + "] " + releaseDate, score = score, lang = lang))
        else:
            Log("Redirected to actress page")
            movieResults = searchResults.xpath('//div[contains(@class,"row container")][1]//li[@class="list-group-item"]')
            resultsNum = len(movieResults)
            Log("resultsNum: " + str(resultsNum))
            if resultsNum > 0:
                for searchResult in movieResults:
                    titleNoFormatting = searchResult.xpath('.//a[contains(@class,"item-name")]')[0].text_content()
                    Log("Result title: " + titleNoFormatting)
                    curID = searchResult.xpath('.//a[contains(@class,"item-name")]')[0].get('href').replace('/','+').replace('?','!')
                    Log("curID: " + curID)
                    releaseDate = searchResult.xpath('.//span[contains(@class,"item-date")]')[0].text_content().split("Rated")[0].strip()
                    Log("releaseDate: " + releaseDate)
                    if searchDate:
                        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                    else:
                        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                    Log("Score: " + str(score))

                    results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(searchSiteID) + "] " + releaseDate, score = score, lang = lang))

            break
        searchPageNum += 1


    return results

def updateSexArt(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('+','/').replace('!','?')
    urlBase = PAsearchSites.getSearchBaseURL(siteID)
    if "http" not in url:
        url = urlBase + url
    detailsPageElements = HTML.ElementFromURL(url)


    # Title
    sceneTitle = detailsPageElements.xpath('//a[contains(@class,"gallery-title")] | //a[contains(@class,"title")]')[0].text_content().split("(")[0].strip()
    metadata.title = sceneTitle
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "MetArt"
    subSite = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = subSite
    metadata.collections.clear()
    metadata.collections.add(subSite)

    # Summary

    try:
        summary = detailsPageElements.xpath('//div[contains(@class,"custom-description-long")]//p | //p[@class="description-text"]')[0].text_content().replace('Read More','').strip()
        Log("Scene Summary found")
        metadata.summary = summary
    except:
        Log("Scene Summary not found")

    # Date
    date = detailsPageElements.xpath('//div[contains(@class,"details font-13")]//li[2] | //span[contains(@class,"penel")]//span[2] | //span[contains(@class,"about")]//span[2]')[0].text_content().replace("Released:","").strip()
    Log("Scene Date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class,"details")]//span[@itemprop="actor"]//a | //span[contains(@class,"penel")]//a | //span[contains(@class,"about")]//a')
    Log("actors #: " + str(len(actors)))
    if len(actors) > 0:
        for actorObject in actors:
            actorName = actorObject.text_content()
            Log("Actor: " + actorName)
            actorPageURL = actorObject.get("href")
            if "http" not in actorPageURL:
                actorPageURL = urlBase + actorPageURL
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPageElements.xpath('//img[contains(@src,"/headshots/")]')[0].get("src").split("?")[0]
            if "http" not in actorPhotoURL:
                actorPhotoURL = urlBase + actorPhotoURL
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            Log("ActorPhotoURL: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = ["Glamorous"]
    for genre in genres:
        movieGenres.addGenre(genre)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    # Poster
    try:
        posterURL = detailsPageElements.xpath('//img[contains(@class,"cover")] | //img[contains(@src,"/cover_")]')[0].get("src")
    except:
        posterURL = ''
        Log("posterURL: " + posterURL)
    metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Background
    try:
        backgroundURL = posterURL.replace("cover","wide")
        Log("backgroudURL: " + backgroundURL)
    except:
        backgroundURL = ''
    metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata

def updateMetArt(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('+','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    sceneTitle = detailsPageElements.xpath('//h3[@class="truncate"]')[0].text_content().split('(')[0].strip()
    metadata.title = sceneTitle
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "MetArt"
    metadata.tagline = "MetArt"
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Summary
    try:
        summary = detailsPageElements.xpath('//div[contains(@class,"panel-tags-group")]//p')[0].text_content().strip()
        Log("Scene Summary found")
        metadata.summary = summary
    except:
        Log("Scene Summary not found")

    # Date
    date = detailsPageElements.xpath('//span[@class="custom-age"]')[0].text_content().strip()
    Log("Scene Date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//span[@itemprop="name"]//a')
    Log("actors #: " + str(len(actors)))
    if len(actors) > 0:
        for actorObject in actors:
            actorName = actorObject.text_content()
            Log("Actor: " + actorName)
            actorPageURL = actorObject.get("href")
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = "https://static.metart.com/media/headshots/" + actorName.lower().replace(' ','-') + ".jpg"
            Log("ActorPhotoURL: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@id="list-of-tags-wrapper-Gallery-0"]//a')
    for genre in genres:
        genreName = genre.text_content()
        movieGenres.addGenre(genreName)
        # Log("Genre: " + genre)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    # Poster
    try:
        posterURL = detailsPageElements.xpath('//div[@id="details_series"]//img')[0].get('src').replace("t_","")
    except:
        posterURL = ''
        Log("posterURL: " + posterURL)
    metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Background
    try:
        backgroundURL = posterURL.replace("cover","wide")
        Log("backgroudURL: " + backgroundURL)
    except:
        backgroundURL = ''
    metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Director
    metadata.directors.clear()
    director = metadata.directors.new()
    dirName = detailsPageElements.xpath('//a[@rel="details_photographer_0"]')[0].text_content().replace("Director:","").strip()
    director.name = dirName
    Log("director: " + dirName)

    return metadata
