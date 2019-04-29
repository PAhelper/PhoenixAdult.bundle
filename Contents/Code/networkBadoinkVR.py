import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(searchSiteID) + encodedTitle)
    Log("Results found: " + str(len(searchResults.xpath('//div[@class="tile-grid-item"]'))))
    for searchResult in searchResults.xpath('//div[@class="tile-grid-item"]'):
        titleNoFormatting = searchResult.xpath('.//span[@itemprop="name"]')[0].text_content().strip()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').replace("/","+")
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//span[@itemprop="datePublished"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        girlName = searchResult.xpath('.//a[@itemprop="actor"]')[0].text_content().strip()
        Log("firstGirlname: " + girlName)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        Log("Score: " + str(score))

        results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = girlName + " in " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(searchSiteID) + "] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0].replace("+","/")
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="video-rating-and-details"]//h1[@class="heading heading--2 video-title"]')[0].text_content()

    # Studio
    metadata.studio = 'BadoinkVR'

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="video-description"]')[0].text_content().strip()

    # Tagline and Collection
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@class="video-tag"]')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())


    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[contains(@class,"video-actor-link")]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="girl-details-photo"]')[0].get("src").split('?')
            movieActors.addActor(actorName,actorPhotoURL[0])

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//div[contains(@class,"gallery-item")]')
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get("data-big-image")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1

    backgroundURL = detailsPageElements.xpath('//img[@class="video-image"]')[0].get("src").split('?')
    metadata.art[backgroundURL[0]] = Proxy.Preview(HTTP.Request(backgroundURL[0], headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Date
    date = detailsPageElements.xpath('.//div[@class="video-details"]//p[@class="video-upload-date"]')[0].text_content().split(":")
    dateFixed = date[1].strip()
    Log('DateFixed: ' + dateFixed)
    date_object = datetime.strptime(dateFixed, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    return metadata
