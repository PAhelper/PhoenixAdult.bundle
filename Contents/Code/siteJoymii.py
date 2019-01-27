import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchString = encodedTitle.replace(" ","+")
    # if not searchAll:
    #     searchString = searchString + "+" + PAsearchSites.getSearchSiteName(searchSiteID).replace(" ","+")
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    for searchResult in searchResults.xpath('//div[contains(@class,"set set-photo")]'):
        resultURL = searchResult.xpath('.//a')[0].get('href')
        if resultURL[10:15] == "video":
            titleNoFormatting = searchResult.xpath('.//div[contains(@class,"title")]//a')[0].text_content().title()
            Log("Result Title: " + titleNoFormatting)
            curID = searchResult.xpath('.//a')[0].get('href')
            curID = curID.replace("_","!").replace('/','_')
            Log("curID: " + curID)
            releasedDate = searchResult.xpath('.//div[contains(@class,"release_date")]')[0].text_content()
            Log("releasedDate: " + releasedDate.strip())
            resultActors = searchResult.xpath('.//div[contains(@class,"actors")]//a')
            actorList = []
            for actor in resultActors:
                actorList.append(actor.text_content())
            actors = ", ".join(actorList)
            Log("actors: " + actors)
            lowerResultTitle = str(titleNoFormatting).lower()
            searchString = searchString.replace("+"," ")
            score = 102 - Util.LevenshteinDistance(searchString.lower(), titleNoFormatting.lower())

            titleNoFormatting = actors + " in " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + ", " + releasedDate +"]"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releasedDate, name = titleNoFormatting, score = score, lang = lang))

    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace("!","_")
    Log("scene url: " + url)
    detailsPageElements = HTML.ElementFromURL(url)

    # Studio/Tagline/Collection
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Date
    date = str(metadata.id).split("|")[2]
    Log('date: ' + date)
    date_object = datetime.strptime(date.strip(), '%b %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@id="video-set-details"]//p[@class="text"]')[0].text_content()
    Log('summary: ' +  metadata.summary)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//div[@id="video-set-details"]//video[@id="video-playback"]')
    background = posters[0].get("poster")
    Log("background: " + background)
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@id="video-set-details"]//h2[@class="starring-models"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPhotoURL = PAactors.actorDBfinder(actorName)
            Log(actorName)
            movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.addGenre("Glamcore")
    if len(actors) == 3:
        movieGenres.addGenre("Threesome")
    if len(actors) == 4:
        movieGenres.addGenre("Foursome")
    if len(actors) > 4:
        movieGenres.addGenre("Orgy")


    # TITLE

    title = detailsPageElements.xpath('//div[@id="video-set-details"]//h1[@class="title"]')[0].text_content().title()
    metadata.title = metadata.studio + " - " + title


    return metadata
