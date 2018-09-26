import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="video-item-big"]'):
        
        #Log(searchResult.text_content())
        titleNoFormatting = searchResult.xpath('.//a[@class="v-title"]')[0].text_content()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get("href")
        curID = curID.replace('/','+')
        Log("ID: " + curID)
        releasedDate = searchResult.xpath('.//span[@class="v-stat"]//span[@class="txt"]')[0].text_content()
        releasedDate = datetime.strptime(releasedDate, '%d.%m.%y').strftime('%Y-%m-%d')
        Log(releasedDate)
        Log(str(curID))
        lowerResultTitle = str(titleNoFormatting).lower()
        if searchByDateActor != True:
            score = 102 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        else:
            searchDateCompare = datetime.strptime(searchDate, '%Y-%m-%d').strftime('%Y-%m-%d')
            score = 102 - Util.LevenshteinDistance(searchDateCompare.lower(), releasedDate.lower())
        titleNoFormatting = "[" + releasedDate + "] " + titleNoFormatting + " [" + PAsearchSites.searchSites[siteNum][1] + "]"
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))




    return results



def update(metadata,siteID,movieGenres):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('+','/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "Porndoe Premium"
    metadata.summary = detailsPageElements.xpath('//p[@class="description"]')[0].text_content()
    metadata.title = detailsPageElements.xpath('//h1[@class="big-container-title"]')[0].text_content()
    releasedDate = detailsPageElements.xpath('//div[@class="col date"]')[0].text_content()[71:-37]
    Log(releasedDate)
    date_object = datetime.strptime(releasedDate, '%d.%m.%y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year 
    metadata.tagline = detailsPageElements.xpath('//div[@class="col channel"]//a')[0].text_content()
    Log(metadata.tagline)
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[contains(@href,"/videos/category/")]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)
    
    genres = detailsPageElements.xpath('//a[contains(@href,"/videos/tag/")]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    metadata.roles.clear()
    actors = detailsPageElements.xpath('//a[contains(@class,"pornstar")]')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = actorLink.text_content()
            role.name = actorName
            actorPageURL = "https://porndoepremium.com" + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@alt="PS"]')[0].get("src")
            role.photo = actorPhotoURL

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    background = detailsPageElements.xpath('//img[@class="owl-lazy"]')[0].get("data-src").replace("thumb/0x250/","crop/1920x1080/")
    try:
        metadata.art[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    except:
        pass
    
    posters = detailsPageElements.xpath('//img[@class="owl-lazy"]')
    posterNum = 1
    for poster in posters:
        posterURL = poster.get("data-src")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL).content, sort_order = posterNum)
        posterNum += 1
    


    
    return metadata
