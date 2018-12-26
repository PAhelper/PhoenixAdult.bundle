import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchString = encodedTitle.replace(" ","+")
    if not searchAll:
        searchString = searchString + "+in+" + PAsearchSites.getSearchSiteName(searchSiteID).replace(" ","+")
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    for searchResult in searchResults.xpath('//div[@class="scene-item"]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].get("title")
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href')
        curID = curID[31:-26]
        curID = curID.replace('/','_')
        Log("ID: " + curID)
        releasedDate = searchResult.xpath('.//p[@class="entry-date"]')[0].text_content()

        Log("CurID" + str(curID))
        lowerResultTitle = str(titleNoFormatting).lower()
        searchString = searchString.replace("+"," ")
        if searchByDateActor != True:
            score = 102 - Util.LevenshteinDistance(searchString.lower(), titleNoFormatting.lower())
        else:
            searchDateCompare = datetime.strptime(searchDate, '%Y-%m-%d').strftime('%b %d, %y')
            score = 102 - Util.LevenshteinDistance(searchDateCompare.lower(), releasedDate.lower())
        titleNoFormatting = titleNoFormatting + " [NA, " + releasedDate +"]"
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    return results
def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0].replace('_','/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "Naughty America"
    #paragraph = detailsPageElements.xpath('//span[@class="moreless js-readmore"]')[0].text_content()
    #paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = detailsPageElements.xpath('//p[@class="synopsis_txt"]')[0].text_content()
    site = detailsPageElements.xpath('//a[@class="site-title grey-text"]')[0].text_content()
    metadata.title = " in " + site
    date = detailsPageElements.xpath('//p[@class="scenedate"]//span')[0].text_content()
    date_object = datetime.strptime(date, '%b %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year    
        
    # Actors
    movieActors.clearActors()
    titleActors = ""
    actors = detailsPageElements.xpath('//a[@class="scene-title grey-text"]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            titleActors = titleActors + actorName + " & "
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = "http:" + actorPage.xpath('//img[@class="performer-pic"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)
        titleActors = titleActors[:-3]
        metadata.title = titleActors + metadata.title

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@class="cat-tag"]')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())


    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//a[contains(@class,"scene-image")]')
    background = "http:" + detailsPageElements.xpath('//video')[0].get("poster")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    posterNum = 1
    for posterCur in posters:
        posterURL = "http:" + posterCur.get("href")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1
    return metadata
