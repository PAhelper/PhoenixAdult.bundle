import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    url = PAsearchSites.getSearchSearchURL(searchSiteID) + searchTitle.lower().replace(" ","-")
    searchPage = HTML.ElementFromURL(url)

    titleNoFormatting = searchPage.xpath('//h1')[0].text_content().replace("VR Porn video","").strip()
    Log("Result Title: " + titleNoFormatting)
    curID = searchTitle.lower().replace(" ","-")
    Log("ID: " + curID)
    resultActors = searchPage.xpath('//div[@class="w-portfolio-item-image modelBox"]//img')
    actorList = []
    for actor in resultActors:
        actorList.append(actor.get("alt"))
    actors = ", ".join(actorList)

    titleNoFormatting = actors + " - " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(searchSiteID) + "]"
    score = 100

    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0]
    Log('temp: ' + temp)
    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    Log('url: ' + url)
    detailsPageElements = HTML.ElementFromURL(url)
    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    Log('Studio: ' + metadata.studio)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="g-cols onlydesktop"]/p')[0].text_content()

    # Tagline and Collection
    metadata.collections.clear()
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.add(metadata.studio)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@class="g-btn type_default"]//span')
    if len(genres) > 0:
        for genre in genres:
            Log('genre: ' + genre.text_content())
            movieGenres.addGenre(genre.text_content())

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="w-portfolio-item-image modelBox"]//img')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.get("alt")
            Log('actor: ' + actorName)
            actorPhotoURL = actorLink.get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//a[contains(@class,"w-gallery-tnail")]')
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get("href")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1

    backgroundURL = detailsPageElements.xpath('//dl8-video')[0].get("poster")
    metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)


    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().replace("VR Porn video","").strip()
    Log('Title: ' + metadata.title)

    return metadata
