import PAsearchSites
import PAgenres
import PAactors
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    searchString = encodedTitle.replace(" ","%20")

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(searchSiteID) + searchString)
    for searchResult in searchResults.xpath('//div[@class="video-item"]'):
        resultURL = searchResult.xpath('.//a')[0].get('href')
        titleNoFormatting = searchResult.xpath('.//div[@class="video-title"]//a')[0].text_content()
        Log("Result Title: " + titleNoFormatting)
        curID = titleNoFormatting.lower().replace("'","").replace("!","").replace("?","").replace(",","").replace(" ","-")
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//div[@class="info"]')[0].text_content()[-30:].strip()).strftime('%Y-%m-%d')
        Log("releasedDate: " + releaseDate)
        resultActors = searchResult.xpath('.//div[@class="info"]//a')
        actorList = []
        for actor in resultActors:
            actorList.append(actor.text_content())
        actors = ", ".join(actorList)
        Log("actors: " + actors)
        # lowerResultTitle = str(titleNoFormatting).lower()
        searchString = searchString.replace("+"," ")
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchString.lower(), titleNoFormatting.lower())

        titleNoFormatting = actors + " in " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(searchSiteID) + ", " + releaseDate +"]"
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting, score = score, lang = lang))

    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = PAsearchSites.getSearchBaseURL(siteID).replace("www.","") + "/videos/" + str(metadata.id).split("|")[0]
    Log("scene url: " + url)
    detailsPageElements = HTML.ElementFromURL(url)

    # Studio/Tagline/Collection
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Date
    date = str(metadata.id).split("|")[2].strip()
    Log('date: ' + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="description"]//span[@class="full hidden"]')[0].text_content()
    Log('summary: ' +  metadata.summary)


    # Posters
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//div[@class="gallery-item"]//a')
    for posterCur in posters:
        poster = posterCur.get("href").split("?")[0]
        metadata.posters[poster] = Proxy.Preview(HTTP.Request(poster, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        Log('posterURL: ' + poster)

    # background

    backgroundRawURL = detailsPageElements.xpath('//div[@id="player"]')[0].get("style")
    background = backgroundRawURL.replace("background-image: url('", "").replace("');","").split("?")[0]
    Log("background: " + background)
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class,"right-info")]//div[@class="info"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPhotoURL = ''
            Log(actorName)
            movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="tag-list"]//a')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())



    # TITLE

    metadata.title = detailsPageElements.xpath('//div[contains(@class,"right-info")]//h1')[0].text_content()


    return metadata
