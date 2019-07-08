import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchString = searchTitle.replace(" ","_").replace(",","").replace("'","").replace("?","")
    Log("searchString: " + searchString)
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    titleNoFormatting = searchResults.xpath('//h1[@class="latest-scene-title"]')[0].text_content().strip()
    Log("titleNoFormatting: " + titleNoFormatting)
    curID = searchResults.xpath('//link[@rel="canonical"]')[0].get('href').replace('/','+').replace('?','!')
    Log("curID: " + curID)
    releaseDate = parse(searchResults.xpath('//div[contains(@class,"latest-scene-meta")]//div[contains(@class,"text-left")]')[0].text_content().strip()).strftime('%Y-%m-%d')
    Log("releaseDate: " + releaseDate)
    if searchDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 95

    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) , name = titleNoFormatting + " [VRHush] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):

    url = str(metadata.id).split("|")[0].replace('+','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()
    urlBase = PAsearchSites.getSearchBaseURL(siteID)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="latest-scene-title"]')[0].text_content().strip()
    Log("title: " + metadata.title)

    #Tagline and Collection(s)
    siteName = "VRHush"
    metadata.studio = siteName
    metadata.tagline = siteName
    metadata.collections.add(siteName)
    Log("siteName: " + siteName)

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[contains(@class,"full-description")]')[0].text_content().strip()

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class,"latest-scene-meta")]//div[contains(@class,"text-left")]')[0].text_content().strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Video trailer background image
    previewBG = detailsPageElements.xpath('//dl8-video')[0].get('poster')
    previewBG = "https:" + previewBG
    metadata.art[previewBG] = Proxy.Preview(HTTP.Request(previewBG, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    Log('previewBG: ' + previewBG)

    # Posters
    posterNum = 1
    posters = detailsPageElements.xpath('//div[contains(@class,"owl-carousel")]//img')
    for poster in posters:
        posterURL = poster.get("src")
        posterURL = "https:" + posterURL
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum += 1
        Log('posterURL: ' + posterURL)

    # Actors
    actors = detailsPageElements.xpath('//h5[@class="latest-scene-subtitle"]//a[contains(@href,"/models/")]')
    if len(actors) > 0:
        for actor in actors:
            actorName = actor.text_content().strip()
            actorPageURL = actor.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = "https:" + actorPage.xpath('//img[@id="model-thumbnail"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)
            metadata.posters[actorPhotoURL] = Proxy.Preview(HTTP.Request(actorPhotoURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            Log('actor: ' + actorName + ", " + actorPhotoURL)
            posterNum += 1

    # Genres
    genres = detailsPageElements.xpath('//a[contains(@class,"label")]')
    for genre in genres:
        genreName = genre.text_content().strip()
        movieGenres.addGenre(genreName)

    return metadata
