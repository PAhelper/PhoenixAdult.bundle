import PAsearchSites
import PAgenres
import PAextras
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum))

    for searchResult in searchResults.xpath('//article[@class="single"]/div[1]/div[4]'):
        searchSceneName = encodedTitle.replace("%20", " ")
        Log("searchSceneName " + searchSceneName)
        titleNoFormatting = searchResult.xpath('//a[contains(text(),"' + searchSceneName + '")]')[0].text_content().strip()
        Log("titleNoFormatting: " + titleNoFormatting)
        sceneUrl = searchResults.xpath('//a[contains(text(),"' + searchSceneName + '")]')[0].get('href')
        curID = (PAsearchSites.getSearchBaseURL(siteNum) + sceneUrl).replace('/','_').replace('?','!')
        Log("curID: " + curID)
        #releaseDate = parse(searchResults.xpath('//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        score = 100
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] ", score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    art =[]
    Log('******UPDATE CALLED*******')
    pageURL = str(metadata.id).split("|")[0].replace('_', '/')
    detailsPageElements = HTML.ElementFromURL(pageURL)
    sceneID = pageURL.split("/")[5]
    Log("sceneID : " + sceneID)

    # Summary
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.studio = siteName
    metadata.summary = detailsPageElements.xpath('//p[@class="episode__synopsis"]')[0].text_content().strip()
    metadata.title = detailsPageElements.xpath('//h1[@class="episode__title"]')[0].text_content().strip()

    # Collections / Tagline
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Genres
    try:
        genres = detailsPageElements.xpath('//li[@class="tags__item--ltr"]/a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip().lower()
                movieGenres.addGenre(genreName)
    except:
        movieGenres.addGenre("Blackmailed")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="episode__created-at"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actorPage = PAsearchSites.getSearchBaseURL(siteID) + (detailsPageElements.xpath('//span[@class="performer-names performer-names--single-episode"]//span//a')[0].get("href"))
    actorName = detailsPageElements.xpath('//span[@class="performer-names performer-names--single-episode"]//span')[0].text_content().strip()
    Log("actorPage: " + actorPage)
    Log("actorName: " + actorName)
    detailsActorPage = HTML.ElementFromURL(actorPage)
    actorPhotoURL = detailsActorPage.xpath('//div[@class="col-xs-12"]//img')[0].get('src')
    Log("actorPhotoURL: " + actorPhotoURL)
    movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    try:
        i = 1
        while i < 6:
            posterUrl = "https://cdn.evilangelvideo.com/paysites/scenes/" + sceneID + "/free/images/1000/" + sceneID + "-preview-1000-000" + str(i) + ".jpg"
            Log("previewBG: " + posterUrl)
            art.append(posterUrl)
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}).content, sort_order=i)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}).content, sort_order=i)
            i = i + 1
    except:
        pass

    Log("Artwork found: " + str(len(art)))

    return metadata
