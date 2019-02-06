import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    xartpost = {
        "input_search_sm" : encodedTitle
    }
    searchResults = HTML.ElementFromURL('https://www.x-art.com/search/', values = xartpost)

    for searchResult in searchResults.xpath('//a[contains(@href,"videos")]'):
        link = searchResult.xpath('.//img[contains(@src,"videos")]')
        if len(link) > 0:
            if link[0].get("alt") is not None:
                
                titleNoFormatting = link[0].get("alt")
                curID = searchResult.get("href")[21:]
                curID = curID.replace('/','+')
                Log(str(curID))
                score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [X-Art]", score = score, lang = lang))
    return results



def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('+','/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "X-Art"
    paragraphs = detailsPageElements.xpath('//p')
    pNum = 0
    summary = ""
    for paragraph in paragraphs:
        if pNum > 0 and pNum <= (len(paragraphs)-7):
            summary = summary + paragraph.text_content()
        pNum += 1
    metadata.summary = summary
    metadata.title = detailsPageElements.xpath('//title')[0].text_content()[8:]
    date = detailsPageElements.xpath('//h2')[2].text_content()[:-1]
    date_object = datetime.strptime(date, '%b %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year    
        
    
    # Genres
    movieGenres.clearGenres()
    # No Source for Genres, add manual
    movieGenres.addGenre("Artistic")
    movieGenres.addGenre("Glamcore")

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h2//a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="info-img"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//div[@class="gallery-item"]')[0]
    poster = posters.xpath('.//img')[0].get('src')
    background = detailsPageElements.xpath('//img[contains(@src,"/videos")]')[0].get("src")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    posterURL = poster[:-21] + "2.jpg"
    metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL).content, sort_order = 1)

    


    
    return metadata
