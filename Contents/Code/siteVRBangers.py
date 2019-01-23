import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    url = "https://vrbangers.com/video/" + searchTitle.lower().replace(" ","-")
    searchResults = HTML.ElementFromURL(url)

    # searchResult = searchResults.xpath('//div[@class="video-rating-and-details"]')[0]
    titleNoFormatting = searchResults.xpath('//div[@class="video-info-title"]//h1[@class="pull-left page-title"]//span')[0].text_content()
    Log("Result Title: " + titleNoFormatting)
    cur = "/video/" + searchTitle.lower().replace(" ","-")
    curID = cur.replace('/','_')
    Log("ID: " + curID)
    releasedDate = searchResults.xpath('//div[@class="col-lg-3 col-md-3 col-sm-12 download-block"]//p[@class="pull-right dates invisible"]')[0].text_content()

    girlName = searchResults.xpath('//div[contains(@class,"girls-name")]//a')[0].text_content()

    Log("CurID: " + str(curID))
    lowerResultTitle = str(titleNoFormatting).lower()

    titleNoFormatting = girlName + " - " + titleNoFormatting + " [VRBangers, " + releasedDate +"]"
    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0].replace("_", "/")
    Log('temp: ' + temp)
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    Log('url: ' + url)
    detailsPageElements = HTML.ElementFromURL(url)
    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    Log('Studio: ' + metadata.studio)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="mainContent"]/p')[0].text_content().strip()

    # Tagline and Collection
    tagline = "VRBangers"
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="video-tags"]//a[@class="tags-item"]')
    if len(genres) > 0:
        for genre in genres:
            Log('genre: ' + genre.text_content())
            movieGenres.addGenre(genre.text_content())

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="girls-name"]//div[@class="girls-name-video-space"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().replace(", ","")
            Log('actor: ' + actorName)
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="single-model-featured"]//img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//*[@id="single-video-gallery-free"]//a')
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get("href")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1

    # backgroundURL = detailsPageElements.xpath('//img[@class="video-image"]')[0].get("src").split('?')
    # metadata.art[backgroundURL[0]] = Proxy.Preview(HTTP.Request(backgroundURL[0], headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Date
    date = detailsPageElements.xpath('//div[@class="col-lg-3 col-md-3 col-sm-12 download-block"]//p[@class="pull-right dates invisible"]')[0].text_content()
    Log('DateRaw: ' + date)
    date_object = datetime.strptime(date, '%d %B , %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Title
    titleOfficial = detailsPageElements.xpath('//div[@class="video-info-title"]//h1[@class="pull-left page-title"]//span')[0].text_content()
    metadata.title = metadata.studio + " - " + titleOfficial
    Log('Title: ' + metadata.title)

    return metadata
