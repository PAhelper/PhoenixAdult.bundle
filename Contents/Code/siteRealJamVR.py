import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchString = searchTitle.replace(" ","_").replace(",","").replace("'","").replace("?","")
    Log("searchString: " + searchString)
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchString
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    titleNoFormatting = searchResults.xpath('//div[@class="title"]//a//h1')[0].text_content().strip()
    Log("titleNoFormatting: " + titleNoFormatting)
    curID = url.replace('/','+').replace('?','!')
    Log("curID: " + curID)
    releaseDate = parse(searchResults.xpath('//div[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
    Log("releaseDate: " + releaseDate)

    if searchDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 95

    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) , name = titleNoFormatting + " [VRConk] " + releaseDate, score = score, lang = lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('+','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()
    urlBase = PAsearchSites.getSearchBaseURL(siteID)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="title"]//a//h1')[0].text_content().strip()
    Log("title: " + metadata.title)

    #Tagline and Collection(s)
    siteName = "RealJamVR"
    metadata.studio = siteName
    metadata.tagline = siteName
    metadata.collections.add(siteName)
    Log("siteName: " + siteName)

    # Summary
    summary = detailsPageElements.xpath('//div[@class="desc"]')[0].text_content().strip()
    metadata.summary = " ".join(summary.splitlines())
    
    # Release Date
    date = detailsPageElements.xpath('//div[@class="date"]')[0].text_content().strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Video trailer background image
    previewBG = detailsPageElements.xpath('//div[@class="splash-screen fullscreen-message is-visible"]')[0].get("style").replace("background-image: url(","").replace(");","")
    metadata.art[previewBG] = Proxy.Preview(HTTP.Request(previewBG, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    Log('previewBG: ' + previewBG)

    # Posters
    posterNum = 1
    posters = detailsPageElements.xpath('//div[@class="scene-previews-container"]//a')
    for poster in posters:
        posterURL = poster.get("href")
        posterURL = posterURL
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum += 1
        Log('posterURL: ' + posterURL)

    # Actors
    actors = detailsPageElements.xpath('//div[@class="featuring commed"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            Log("actor: " + actorName)
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[contains(@class, "actor-info")]//img')[0]
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="tags"]//a')
    for genre in genres:
        genreName = genre.text_content().strip()
        movieGenres.addGenre(genreName)

    return metadata