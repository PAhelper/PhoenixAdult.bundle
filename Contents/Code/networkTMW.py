import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchPageNum = 1
    while searchPageNum <= 5:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "&page=" + str(searchPageNum))
        for searchResult in searchResults.xpath('//article'):
            if len(searchResult.xpath('//article')) > 0:
                titleNoFormatting = searchResult.xpath('.//h1')[0].text_content().strip()
                curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
                releaseDate = parse(searchResult.xpath('.//time')[0].text_content()).strftime('%Y-%m-%d')
                subSite = searchResult.xpath('.//div[@class="site"]/a')[0].text_content().replace('.com','').strip()
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
    metadata.title = detailsPageElements.xpath('//div[@class="title-line"]/h1')[0].text_content().strip()
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "Teen Mega World"
    subSite = detailsPageElements.xpath('//div[@class="site"]/a')[0].text_content().replace('.com','').strip()
    metadata.tagline = subSite
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="text"]//p')[0].text_content().strip()
    except:
        Log('No summary found')

    # Date
    date = detailsPageElements.xpath('//div[@class="date"]//time')[0].text_content().strip()
    Log("date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="video"]//div[@class="site"]//a[position()>1]')
    Log("actors #: " + str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            Log("Actor: " + actorName)
            actorPageURL = actorLink.get('href').replace('https','http')
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = urlBase + actorPageElements.xpath('//div[@class="photo"]//img')[0].get("data-src").replace('https','http')
            Log("ActorPhotoURL: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[@class="tag-list"]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genre = genreLink.text_content()
            movieGenres.addGenre(genre)

    return metadata