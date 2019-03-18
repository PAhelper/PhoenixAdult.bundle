import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchPageNum = 1
    while searchPageNum <= 2:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "/relevance~0~4~-~-~-~-~-~-/" + str(searchPageNum))
        for searchResult in searchResults.xpath('//div[@class="custom-list-item-default"]'):
            if len(searchResult.xpath('.//a[@class="custom-list-item-name"]')) > 0:
                titleNoFormatting = searchResult.xpath('.//a[@class="custom-list-item-name"]')[0].text_content()
                Log("Result Title: " + titleNoFormatting)
                curID = searchResult.xpath('.//a[@class="custom-list-item-name"]')[0].get('href').replace('_','+').replace('/','_').replace('?','!')
                Log("curID: " + curID)
                releaseDateRaw = searchResult.xpath('.//span[@class="custom-list-item-date"]//span')[0].text_content()
                Log("releaseDateRaw: " + releaseDateRaw)
                releaseDateFixed = searchResult.xpath('.//span[@class="custom-list-item-date"]')[0].text_content().replace(releaseDateRaw, "").strip()
                Log("releaseDateFixed: " + releaseDateFixed)
                releaseDate = parse(releaseDateFixed).strftime('%Y-%m-%d')
                Log("releaseDate: " + releaseDate)
                if searchDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [SexArt] " + releaseDate, score = score, lang = lang))
        searchPageNum += 1
    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?').replace('+','_')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    sceneTitle = detailsPageElements.xpath('//a[contains(@class,"gallery-title")]')[0].text_content().strip()
    metadata.title = sceneTitle
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "MetArt"
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class,"custom-description-long")]//p')[0].text_content().replace("Synopsis:","").strip()
    Log("Scene Summary: " + metadata.summary[:20])

    # Date
    date = detailsPageElements.xpath('//div[contains(@class,"details")]//li[2]')[0].text_content().replace("Released:","").strip()
    Log("Scene Date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class,"details")]//span[@itemprop="actor"]//span[@itemprop="name"]//a')
    Log("actors #: " + str(len(actors)))
    if len(actors) > 0:
        for actorObject in actors:
            actorName = actorObject.text_content()
            Log("Actor: " + actorName)
            actorPageURL = actorObject.get("href")
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPageElements.xpath('//div[contains(@class,"custom-photo-modal")]//a/img')[0].get("src").split("?")[0]
            Log("ActorPhotoURL: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = ["Glamcore", "Glamour Porn"] # site has no genres listed, but some should be put in manually describing the overall genre of the site?
    for genre in genres:
        movieGenres.addGenre(genre)
        Log("Genre: " + genre)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    # Poster
    try:
        posterURL = detailsPageElements.xpath('//img[contains(@class,"cover")]')[0].get("src")
    except:
        posterURL = ''
        Log("posterURL: " + posterURL)
    metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Background
    try:
        backgroundURL = posterURL.replace("cover","wide")
        Log("backgroudURL: " + backgroundURL)
    except:
        backgroundURL = ''
    metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata
