import PAsearchSites
import PAgenres
import json

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    url = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "&page=1&pageSize=30&sortBy=relevance&query%5BcontentType%5D=movies&filters%5BcontentType%5D=movies"
    Log(url)
    data = urllib.urlopen(url).read()
    searchResults = json.loads(data)

    for searchResult in searchResults['items']:
        titleNoFormatting = searchResult['item']['name']
        Log(titleNoFormatting)
        curID = searchResult['item']['path'].replace('/','+').replace('?','!')
        Log(curID)
        subSite = PAsearchSites.getSearchSiteName(siteNum)
        Log(subSite)
        releaseDate = parse(searchResult['item']['publishedAt'][:10]).strftime('%Y-%m-%d')
        Log(releaseDate)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [MetArt/" + subSite + "] " + releaseDate, score = score, lang = lang))

    return results

def update (metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('+','/').replace('!','?')
    urlBase = PAsearchSites.getSearchBaseURL(siteID)
    if "http" not in url:
        url = urlBase + url
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    sceneTitle = detailsPageElements.xpath('//div[@class="info-container"]//h3[contains(@class, "headline")]')[0].text_content().split("(")[0].strip()
    metadata.title = sceneTitle

    # Studio/Tagline/Collection
    metadata.studio = "MetArt"
    subSite = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = subSite
    metadata.collections.clear()
    metadata.collections.add(subSite)

    # Summary
    try:
        summary = detailsPageElements.xpath('//p[@class="description-text"]')[0].text_content().replace('Read More','').strip()
        metadata.summary = summary
    except:
        pass

    # Date
    date = detailsPageElements.xpath('//div[@class="movie-data"]//span[@class="attr-value"]')[2].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="movie-data"]//span[@class="attr-value"]')[0].xpath('.//a')
    for actorObject in actors:
        actorName = actorObject.text_content()
        actorPageURL = actorObject.get("href")
        if "http" not in actorPageURL:
            actorPageURL = urlBase + actorPageURL

        actorPageElements = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPageElements.xpath('//img[contains(@src,"/headshots/")]')[0].get("src").split("?")[0]
        if "http" not in actorPhotoURL:
            actorPhotoURL = urlBase + actorPhotoURL
        movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="tag-list"]//a')
    for genre in genres:
        genreName = genre.text_content().strip()
        movieGenres.addGenre(genreName)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    # Poster
    try:
        posterURL = detailsPageElements.xpath('//img[contains(@class,"cover")] | //img[contains(@src,"/cover_")]')[0].get("src")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
    except:
        pass

    # Background
    try:
        backgroundURL = posterURL.replace("cover","wide")
        metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
    except:
        pass

    return metadata