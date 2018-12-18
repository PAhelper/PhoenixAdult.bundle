import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchsiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//article[@class="videolist-item"]'):
        
        
        Log(searchResult.text_content())
        titleNoFormatting = searchResult.xpath('.//h4[@class="videolist-caption-title"]')[0].text_content()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a[@class="videolist-link ajaxable"]')[0].get('href')
        curID = curID.replace('/','_')
        Log("ID: " + curID)
        releasedDate = searchResult.xpath('.//div[@class="videolist-caption-date"]')[0].text_content()

        Log(str(curID))
        lowerResultTitle = str(titleNoFormatting).lower()
        if searchByDateActor != True:
            score = 102 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        else:
            searchDateCompare = datetime.strptime(searchDate, '%Y-%m-%d').strftime('%B %d, %y')
            score = 102 - Util.LevenshteinDistance(searchDateCompare.lower(), releasedDate.lower())
        titleNoFormatting = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + ", " + releasedDate + "]"
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    return results
def update(metadata,siteID,movieGenres):
    temp = str(metadata.id).split("|")[0].replace('_','/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "Vixen"
    paragraph = detailsPageElements.xpath('//span[@class="moreless js-readmore"]')[0].text_content()
    paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = paragraph
    metadata.title = detailsPageElements.xpath('//h1[@id="castme-title"]')[0].text_content()
    date = detailsPageElements.xpath('//span[@class="player-description-detail"]//span')[0].text_content()
    date_object = datetime.strptime(date, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year    
        
    
    # Genres
    movieGenres.clearGenres()
    # No Source for Genres, add manual

    movieGenres.addGenre("Hardcore")
    movieGenres.addGenre("Heterosexual")
    movieGenres.addGenre("Boy Girl")
    movieGenres.addGenre("Caucasian Men")
    movieGenres.addGenre("Glamcore")

    # Actors
    metadata.roles.clear()
    actors = detailsPageElements.xpath('//p[@id="castme-subtitle"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = actorLink.text_content()
            role.name = actorName
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL("https://www.vixen.com"+actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="thumb-img"]')[0].get("src")
            role.photo = actorPhotoURL

    # Posters/Background
    posters = detailsPageElements.xpath('//div[@class="swiper-slide"]')
    background = detailsPageElements.xpath('//img[contains(@class,"player-img")]')[0].get("src")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.xpath('.//img[@class="swiper-content-img"]')[0].get("src")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1
    return metadata