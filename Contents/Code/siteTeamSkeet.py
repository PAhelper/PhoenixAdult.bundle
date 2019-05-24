import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="info"]'):
        titleURL = searchResult.xpath('.//a')[0].get("href")
        scenePage = HTML.ElementFromURL(titleURL)
        
        titleNoFormatting = scenePage.xpath('//title')[0].text_content().split(" | ")[1]
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get("href").split("?")[0][8:]
        curID = curID.replace('/','+')
        Log("ID: " + curID)
        releaseDate = parse(scenePage.xpath('//div[@style="width:430px;text-align:left;margin:8px;border-right:3px dotted #bbbbbb;position:relative;"]//div[@class="gray"]')[0].text_content()[12:]).strftime('%Y-%m-%d')
        Log(releaseDate)
        Log(str(curID))
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [TeamSkeet/" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))

    return results



def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('+','/')

    url = "https://" + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "TeamSkeet"
    metadata.summary = detailsPageElements.xpath('//div[@class="gray"]')[1].text_content()
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().split(" | ")[1]
    releaseDate = detailsPageElements.xpath('//div[@style="width:430px;text-align:left;margin:8px;border-right:3px dotted #bbbbbb;position:relative;"]//div[@class="gray"]')[0].text_content()[12:].replace("th,",",").replace("st,",",").replace("nd,",",").replace("rd,",",")
    date_object = datetime.strptime(releaseDate, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year 
    tagline = detailsPageElements.xpath('//div[@style="white-space:nowrap;"]')[0].text_content()[6:].strip()
    endofsubsite = tagline.find('.com')
    tagline = tagline[:endofsubsite].strip()
    metadata.tagline = tagline
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[contains(@href,"?tags=")]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    try:
        actors = detailsPageElements.xpath('//a[contains(@href,"/profile/")]')
        if len(actors) > 0:
            for actorLink in actors:
                actorName = actorLink.text_content()
                actorPageURL = actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//img[@id="profile_image"]')[0].get("src")
                movieActors.addActor(actorName, actorPhotoURL)
    except:
        pass

    # Manually Add Actors
    # Add Actor Based on Title
    if "Finger Fucking Debut" == metadata.title:
        actorName = "Lily Lebeau"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)


    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    background = detailsPageElements.xpath('//video')[0].get("poster")
    try:
        metadata.art[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    except:
        pass
    
    posters = detailsPageElements.xpath('//a[contains(@href,"/trailers/")]')
    posterNum = 1
    for poster in posters:
        posterURL = poster.get("href")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL).content, sort_order = posterNum)
        posterNum += 1
    


    
    return metadata
