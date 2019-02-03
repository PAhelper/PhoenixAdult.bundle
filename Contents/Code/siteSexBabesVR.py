import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    url = PAsearchSites.getSearchSearchURL(searchSiteID) + searchTitle.lower().replace(" ","-", 1).replace(" ","_")
    searchResults = HTML.ElementFromURL(url)

    searchResult = searchResults.xpath('//div[@class="video-content-container"]')
    titleNoFormatting = searchResults.xpath('.//div[@class="video-group-left"]//h1[@class="title"]')[0].text_content()
    curID = searchTitle.lower().replace(" ","-", 1).replace(" ","_")
    releaseDate = parse(searchResult.xpath('.//div[@class="grid-one-date"]//span[@class="date-display-single"]')[0].text_content().strip()).strftime('%Y-%m-%d')

    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = titleNoFormatting + " ["+ PAsearchSites.getSearchSiteName(searchSiteID) +"] " + releaseDate, score = score, lang = lang))
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
    metadata.summary = detailsPageElements.xpath('.//div[@class="video-group-bottom"]//p')[0].text_content().strip()

    # Tagline and Collection
    tagline = metadata.studio
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('.//div[@class="video-tags"]//a')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content().title())


    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('.//div[(@class="video-actress-name")]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[contains(@class,"model-img-wrapper")]//div//a')[0].get("href").split('?')
            movieActors.addActor(actorName,actorPhotoURL[0])

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('.//div[contains(@class,"video-gallery")]//div//figure//a')
    posterNum = 1
    for posterCur in posters:
        posterURLfull = posterCur.get("href").split('?')
        posterURL = posterURLfull[0]
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.bing.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1

    # backgroundURL = detailsPageElements.xpath('//img[@class="video-image"]')[0].get("src").split('?')
    # metadata.art[backgroundURL[0]] = Proxy.Preview(HTTP.Request(backgroundURL[0], headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Date
    date = detailsPageElements.xpath('.//div[@class="grid-one-date"]//span[@class="date-display-single"]')[0].text_content()
    Log('DateFixed: ' + date)
    date_object = datetime.strptime(date, '%b %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Title
    titleOfficial = detailsPageElements.xpath('.//div[@class="video-group-left"]//h1[@class="title"]')[0].text_content()
    metadata.title = metadata.studio + " - " + titleOfficial
    Log('Title: ' + metadata.title)

    return metadata
