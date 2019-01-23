import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchString = encodedTitle.replace(" ","+")
    # if not searchAll:
    #     searchString = searchString + "+" + PAsearchSites.getSearchSiteName(searchSiteID).replace(" ","+")
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    for searchResult in searchResults.xpath('//section[@class="compact wrap"]//article'):
        titleNoFormatting = searchResult.xpath('.//a//h3')[0].get("title")
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href')
        # curID = curID[:-26]
        curID = curID.replace('/','_')
        Log("curID: " + curID)
        releasedDate = searchResult.xpath('.//div[@class="date"]')[0].text_content()
        Log("releasedDate: " + releasedDate.strip())

        lowerResultTitle = str(titleNoFormatting).lower()
        searchString = searchString.replace("+"," ")
        score = 102 - Util.LevenshteinDistance(searchString.lower(), titleNoFormatting.lower())

        titleNoFormatting = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + ", " + releasedDate +"]"
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))

    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/')
    Log("scene url: " + url)
    detailsPageElements = HTML.ElementFromURL(url)

    # Studio/Tagline/Collection
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Date
    date = detailsPageElements.xpath('//div[@class="date"]')[0].text_content()
    Log('date: ' + date)
    date_object = datetime.strptime(date.strip(), '%d %B, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="description"]')[0].text_content().strip()

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//a//img[@class="swiper-lazy"]')
    background = posters[0].get("src")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
# unneccesary binocular pictures
    # for posterCur in posters:
    #     posterURL = posterCur.get("data-src")
    #     if posterURL is not None:
    #         metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
    #         posterNum = posterNum + 1

    # Actors / possible posters
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//header//h4//a')
    if len(actors) > 0:
        posterNum = 1
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
            Log(actorName + ": " + actorPageURL)
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="profile"]//img')[0].get("src")
            Log('actorPhotoURL: ' + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)
            # Actor profile pic as possible poster
            metadata.posters[actorPhotoURL] = Proxy.Preview(HTTP.Request(actorPhotoURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            posterNum = posterNum + 1

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('.//div[@class="tags"]//a')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())

    # TITLE

    title = detailsPageElements.xpath('//div[@class="contentContainer"]//h2')[0].text_content()
    metadata.title = metadata.studio + " - " + title


    return metadata
