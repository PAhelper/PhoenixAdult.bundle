import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="video-item"]'):
        #Log(searchResult.text_content())
        titleNoFormatting = searchResult.xpath('.//a[@class="item-top"]')[0].get('data-title')
        subSite = searchResult.xpath('.//a[@class="item-top"]')[0].get('data-brand')
        curID = searchResult.xpath('.//a[@class="item-top"]')[0].get('href')
        curID = curID.replace('/','+')
        lowerResultTitle = str(titleNoFormatting).lower()
        if searchByDateActor != True:
            score = 102 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        else:
            searchDateCompare = datetime.strptime(searchDate, '%Y-%m-%d').strftime('%Y-%m-%d')
            score = 102 - Util.LevenshteinDistance(searchDateCompare.lower(), releasedDate.lower())
        titleNoFormatting = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "/"+subSite+"]"
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('+','/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "Porndoe Premium"
    porndoeJson = detailsPageElements.xpath('//script[@type="application/ld+json"]')[0].text_content()
    j = porndoeJson.find('"uploadDate":')
    k = porndoeJson.find('T', j)
    releaseDate = porndoeJson[j+14:k].replace('"','')
    metadata.summary = detailsPageElements.xpath('//p[@class="description"]')[0].text_content().strip()
    metadata.title = detailsPageElements.xpath('//h1[@class="big-container-title"]')[0].text_content()
    #releasedDate = detailsPageElements.xpath('//div[@class="col date"]')[0].text_content()[71:-37]
    date_object = datetime.strptime(releaseDate, '%Y-%m-%d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year 
    metadata.tagline = detailsPageElements.xpath('//div[@class="col channel"]//a')[0].text_content()
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
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[contains(@class,"pornstar")]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = "https://porndoepremium.com" + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@alt="PS"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

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
