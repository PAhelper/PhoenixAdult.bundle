import PAsearchSites
import PAgenres
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    Log("Results found: " + str(len(searchResults.xpath('//div[@class="tile-grid-item"]'))))
    for searchResult in searchResults.xpath('//div[@class="tile-grid-item"]'):
        titleNoFormatting = searchResult.xpath('.//a[@class="video-card-title heading heading--4"]')[0].get('title')
        Log("Result Title: " + titleNoFormatting)
        curID = PAutils.Encode(searchResult.xpath('.//a[@class="video-card-title heading heading--4"]')[0].get('href'))
        Log("curID: " + curID)
        try:
            releaseDate = parse(searchResult.xpath('.//span[@class="video-card-upload-date"]')[0].get('content')).strftime('%Y-%m-%d')
            Log("releaseDate: " + releaseDate)
        except:
            releaseDate = ""
            Log("No date found (BadoinkVR)")
        girlName = searchResult.xpath('.//a[@class="video-card-link"]')[0].text_content()
        Log("firstGirlname: " + girlName)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        Log("Score: " + str(score))

        name = "[%s] %s in %s %s" % (PAsearchSites.getSearchSiteName(siteNum), girlName, titleNoFormatting, releaseDate)
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name=name, score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    path = PAutils.Decode(str(metadata.id).split("|")[0])
    url = PAsearchSites.getSearchBaseURL(siteID) + path
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
    try:
        date = detailsPageElements.xpath('.//div[@class="video-details"]//p[@class="video-upload-date"]')[0].text_content().split(":")
        dateFixed = date[1].strip()
        Log('DateFixed: ' + dateFixed)
        date_object = datetime.strptime(dateFixed, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    except:
        Log("No date found")

    return metadata
