import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    url = PAsearchSites.getSearchSearchURL(searchSiteID) + searchTitle.lower().replace(" ","_").replace("'","_")
    searchResults = HTML.ElementFromURL(url)

    searchResult = searchResults.xpath('//div[@class="video-rating-and-details"]')[0]
    titleNoFormatting = searchResult.xpath('.//h1[@class="heading heading--2 video-title"]')[0].text_content()
    Log("Result Title: " + titleNoFormatting)
    curID = searchTitle.lower().replace(" ","_").replace("'","_")
    Log("ID: " + curID)
    releaseDate = parse(searchResult.xpath('.//div[@class="video-details"]//p[@class="video-upload-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
    girlName = searchResult.xpath('.//div[@class="video-details"]//p[@class="video-actors"]//a')[0].text_content()

    titleNoFormatting = girlName + " - " + titleNoFormatting + " ["+ PAsearchSites.getSearchSiteName(searchSiteID) +"] " + releaseDate[10:]
    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = titleNoFormatting, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0]
    Log('temp: ' + temp)
    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    Log('url:' + url)
    detailsPageElements = HTML.ElementFromURL(url)
    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    Log('Studio: ' + metadata.studio)

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="video-description"]')[0].text_content().strip()

    # Tagline and Collection
    tagline = metadata.studio
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

    # Title
    titleOfficial = detailsPageElements.xpath('//div[@class="video-rating-and-details"]//h1[@class="heading heading--2 video-title"]')[0].text_content()
    metadata.title = metadata.studio + " - " + titleOfficial
    Log('Title: ' + metadata.title)

    return metadata
