import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    for searchPageNum in range(1, 3):
        url = PAsearchSites.getSearchSearchURL(searchSiteID) + encodedTitle + "/relevance/" + str(searchPageNum)
        searchResults = HTML.ElementFromURL(url)
        pageTitle = searchResults.xpath('//h1')[0].text_content().lower()
        if "found" in pageTitle:
            for searchResult in searchResults.xpath('//div[contains(@class, "grid-card-wrapper")]'):
                curID = searchResult.xpath('.//a[contains(@class,"item-name")]')[0].get('href').replace('/','+').replace('?','!')
                if "+movie+" in curID: # model page and photos in search results
                    titleNoFormatting = searchResult.xpath('.//a[contains(@class,"item-name")]')[0].text_content()
                    releaseDate = searchResult.xpath('.//div[contains(@class, "card-info-2")]//div[@class="card-information-sub-title"]')[0].text_content().strip()
                    if searchDate:
                        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                    else:
                        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

                    results.Append(MetadataSearchResult(id='%s|%d' % (curID, searchSiteID), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(searchSiteID), releaseDate), score=score, lang=lang))
        else:
            Log("Redirected to actress page")
            movieResults = searchResults.xpath('//div[contains(@class,"row container")][1]//li[@class="list-group-item"]')
            for searchResult in movieResults:
                titleNoFormatting = searchResult.xpath('.//a[contains(@class,"item-name")]')[0].text_content()
                curID = searchResult.xpath('.//a[contains(@class,"item-name")]')[0].get('href').replace('/','+').replace('?','!')
                releaseDate = searchResult.xpath('.//div[contains(@class, "card-info-2")]//div[@class="card-information-sub-title"]')[0].text_content().strip()
                if searchDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d' % (curID, searchSiteID), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(searchSiteID), releaseDate), score=score, lang=lang))

            break

    return results

def updateSexArt(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('+','/').replace('!','?')
    urlBase = PAsearchSites.getSearchBaseURL(siteID)
    if "http" not in url:
        url = urlBase + url
    detailsPageElements = HTML.ElementFromURL(url)


    # Title
    sceneTitle = detailsPageElements.xpath('//h3[contains(@class, "headline")]')[0].text_content().split("(")[0].strip()
    metadata.title = sceneTitle

    # Studio/Tagline/Collection
    metadata.studio = "MetArt"
    subSite = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = subSite
    metadata.collections.clear()
    metadata.collections.add(subSite)

    # Summary

    try:
        summary = detailsPageElements.xpath('//p[@class="description-text"]')[0].text_content().replace('Read More','').strip()
        metadata.summary = summary
    except:
        pass

    # Date
    date = detailsPageElements.xpath('//div[@class="movie-data"]//span[@class="attr-value"]')[2].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="movie-data"]//span[@class="attr-value"]')[0].xpath('.//a')
    for actorObject in actors:
        actorName = actorObject.text_content()
        actorPageURL = actorObject.get("href")
        if "http" not in actorPageURL:
            actorPageURL = urlBase + actorPageURL

        actorPageElements = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPageElements.xpath('//img[contains(@src,"/headshots/")]')[0].get("src").split("?")[0]
        if "http" not in actorPhotoURL:
            actorPhotoURL = urlBase + actorPhotoURL

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
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
    except:
        pass

    # Background
    try:
        backgroundURL = posterURL.replace("cover","wide")
        metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
    except:
        pass

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
