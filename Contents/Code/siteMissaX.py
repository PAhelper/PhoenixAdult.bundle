import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="updateItem"] | //div[@class="photo-thumb video-thumb"]'):
        titleNoFormatting = searchResult.xpath('.//h4//a | .//p[@class="thumb-title"]')[0].text_content().strip()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//span[@class="update_thumb_date"] | .//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        actors = searchResult.xpath('.//span[@class="tour_update_models"]//a | .//p[@class="model-name"]//a')
        numActors = len(actors)
        Log("# actors: " + str(numActors))
        firstActor = actors[0].text_content().strip()
        Log("firstActor: " + firstActor)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = firstActor + " + " + str((numActors - 1)) + " in " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    urlBase = PAsearchSites.getSearchBaseURL(siteID)

    # Title
    metadata.title = detailsPageElements.xpath('//span[@class="update_title"] | //p[@class="raiting-section__title"]')[0].text_content().strip()
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "AllHerLuv/MissaX"
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = siteName
    metadata.collections.clear()
    metadata.collections.add(siteName)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//span[@class="latest_update_description"] | //p[contains(@class,"text")]')[0].text_content().replace("Includes:","").replace("Synopsis:","").strip()
    except:
        Log('No summary found')

    # Date
    try:
        date = detailsPageElements.xpath('//span[@class="update_date"]')[0].text_content().strip()
    except:
        date = detailsPageElements.xpath('//p[@class="dvd-scenes__data"]')[0].text_content().split('|')[1].replace('Added:','').strip()
    Log("date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="update_block"]//span[@class="tour_update_models"]//a | //p[@class="dvd-scenes__data"][1]//a')
    Log("actors #: " + str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            Log("Actor: " + actorName)
            actorPageURL = actorLink.get('href')
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = urlBase + actorPageElements.xpath('//img[contains(@class,"model_bio_thumb")]')[0].get("src0_1x")
            Log("ActorPhotoURL: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//span[@class="tour_update_tags"]//a | //p[@class="dvd-scenes__data"][2]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genre = genreLink.text_content()
            movieGenres.addGenre(genre)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    if siteName == "MissaX":
        urlBase = urlBase + "/tour/"
        background = urlBase + detailsPageElements.xpath('//img[contains(@class,"update_thumb")]')[0].get("src").replace("0.jpg","8.jpg")
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        posterNum = 1
        posters = detailsPageElements.xpath('//a[@class="fancybox"]')
        for posterCur in posters:
            posterURL = urlBase + posterCur.get("href")
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = (posterNum + 1))
            Log("poster/BG URL: " + posterURL)
            posterNum += 1
        posterURL = background.replace("8.jpg","0-large.jpg")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        Log("last posterURL: " + posterURL)
    else:
        background = urlBase + detailsPageElements.xpath('//img[contains(@class,"update_thumb")]')[0].get("src0_1x")
        metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)



    return metadata
