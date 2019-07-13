import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchPageNum = 1
    while searchPageNum <= 2:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "&page=" + str(searchPageNum))
        for searchResult in searchResults.xpath('//article'):
            if len(searchResult.xpath('//article')) > 0:
                titleNoFormatting = searchResult.xpath('.//h1')[0].text_content().strip()
                curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
                releaseDate = parse(searchResult.xpath('.//time')[0].text_content()).strftime('%Y-%m-%d')
                subSite = searchResult.xpath('.//aside//div//a')[0].text_content().replace('.com','').strip()
                if searchDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [TMW/" + subSite + "] " + releaseDate, score = score, lang = lang))
        searchPageNum += 1
    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?').replace('https','http')
    detailsPageElements = HTML.ElementFromURL(url)
    urlBase = PAsearchSites.getSearchBaseURL(siteID)

    # Title
    metadata.title = detailsPageElements.xpath('//section[@class="video-block"]//h1')[0].text_content().strip()
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "Teen Mega World"
    subSite = detailsPageElements.xpath('//a[@class="site"]')[0].text_content().replace('.com','').strip()
    metadata.tagline = subSite
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//p[@class="description"]')[0].text_content().strip()
    except:
        Log('No summary found')

    # Date
    date = detailsPageElements.xpath('//section[@class="video-block"]//time')[0].text_content().strip()
    Log("date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//ul[@class="girls"]//a')
    Log("actors #: " + str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            Log("Actor: " + actorName)
            actorPageURL = actorLink.get('href').replace('https','http')
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = urlBase + actorPageElements.xpath('//div[@class="information"]//img')[0].get("src").replace('https','http')
            Log("ActorPhotoURL: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[@class="tags"]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genre = genreLink.text_content()
            movieGenres.addGenre(genre)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    try:
        background = urlBase + detailsPageElements.xpath('//div[@class="media-wrapper"]//video')[0].get("poster").replace('https','http')
    except:
        background = urlBase + detailsPageElements.xpath('//div[@class="media-wrapper"]//dl8-video')[0].get("poster").replace('https','http')

    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    Log("BG URL: " + background)

    posters = detailsPageElements.xpath('//section[@class="photo-list"]//img')
    Log(str(len(posters)) + " thumbs found.")
    posterNum = 2
    for posterCur in posters:
        posterURL = urlBase + posterCur.get("src").replace('https','http')
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum += 1

    return metadata