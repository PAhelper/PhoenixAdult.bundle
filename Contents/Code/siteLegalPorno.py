import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    if "Search for" in searchResults.xpath('//title')[0].text_content():
        for searchResult in searchResults.xpath('//div[@class="thumbnails"]//div[contains(@class,"thumbnail ")]'):
            
            #Log(searchResult.text_content())
            titleNoFormatting = searchResult.xpath('.//div[@class="thumbnail-title gradient"]//a[contains(@href,"/watch/")]')[0].get("title")
            curID = searchResult.xpath('.//a')[0].get("href")[27:]
            curID = curID.replace('/','+')
            Log("ID: " + curID)
            releaseDate = searchResult.xpath('.//div[@class="thumbnail-description gradient"]//div[@class="col-xs-7"]')[0].text_content().replace("\n","")[14:-1]
            releaseDate = datetime.strptime(releaseDate, '%b %d, %Y').strftime('%Y-%m-%d')
            Log(releaseDate)
            Log(str(curID))
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting  + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))

    else:
        Log("single match redirect")
        curID = urllib.unquote(searchResults.xpath('//a[@class="logout-button clear-user-cache"]')[0].get("href"))[83:-1]
        Log("ID:" + curID)
        titleNoFormatting = searchResults.xpath('//title')[0].text_content()[:-13]
        curID = curID.replace('/','+')
        Log("ID: " + curID)
        #releasedDate = searchResult.xpath('.//div[@class="thumbnail-description gradient"]//div[@class="col-xs-7"]')[0].text_content().replace("\n","")[14:-1]
        #releasedDate = datetime.strptime(releaseDate, '%b %d, %Y').strftime('%Y-%m-%d')
        #Log(releaseDate)
        Log(str(curID))
        LOWERRESULTTITLE = str(titleNoFormatting).lower()
        score = 102 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        titleNoFormatting = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "]"
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))

    return results



def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('+','/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "LegalPorno"
    #metadata.summary = detailsPageElements.xpath('//p[@class="description"]')[0].text_content()
    metadata.title = detailsPageElements.xpath('//title')[0].text_content()[2:-15]
    releaseDate = detailsPageElements.xpath('//span[@title="Release date"]//a')[0].text_content()
    Log(releaseDate)
    date_object = datetime.strptime(releaseDate, '%Y-%m-%d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year 
    
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//dd/a[contains(@href,"/niche/")]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)
    
    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//dd/a[contains(@href,"model/")]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="model--avatar"]//img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    background = detailsPageElements.xpath('//div[contains(@id,"player")]')[0].get("style").replace("&amp;","&")[21:-1]
    try:
        metadata.art[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    except:
        pass
    
    posters = detailsPageElements.xpath('//div[contains(@class,"thumbs2 gallery")]//a//img')
    posterNum = 1
    Log(str(len(posters)))
    for poster in posters:
        posterURL = poster.get("src")
    #    metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL).content, sort_order = posterNum)
        posterNum += 1
    
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = posterNum) 


    
    return metadata
