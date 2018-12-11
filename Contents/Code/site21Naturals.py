import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchsiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[contains(@class,"tlcItem")]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].get('title')
        curID = searchResult.xpath('.//a')[0].get('href')
        curID = curID.replace('/','_')
        Log("ID: " + curID)
        releasedDate = searchResult.xpath('.//span[@class="tlcSpecsDate"]//span[@class="tlcDetailsValue"]')[0].text_content()

        Log(str(curID))
        lowerResultTitle = str(titleNoFormatting).lower()
        if searchByDateActor != True:
            score = 102 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        else:
            searchDateCompare = datetime.strptime(searchDate, '%Y-%m-%d').strftime('%Y-%m-%d')
            score = 102 - Util.LevenshteinDistance(searchDateCompare.lower(), releasedDate.lower())
        titleNoFormatting = titleNoFormatting + " [" + PAsearchSites.searchSites[siteNum][1] + ", " + releasedDate + "]"
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    return results
def update(metadata,siteID,movieGenres):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('_','/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "21Naturals"
    metadata.summary = detailsPageElements.xpath('//div[contains(@class,"sceneDesc")]')[0].text_content()[70:].strip()
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()
    releasedDate = detailsPageElements.xpath('//div[@class="updatedDate"]')[0].text_content()[14:24]
    date_object = datetime.strptime(releasedDate, '%Y-%m-%d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year 


    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[contains(@class,"sceneColCategories")]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    metadata.roles.clear()
    actors = detailsPageElements.xpath('//div[contains(@class,"sceneColActors")]//a')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = actorLink.text_content()
            role.name = actorName
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]')[0].get("src")
            role.photo = actorPhotoURL

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    background = detailsPageElements.xpath('//meta[contains(@name,"twitter:image")]')[0].get("content")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    return metadata
