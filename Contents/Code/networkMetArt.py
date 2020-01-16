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
    if "http" not in url:
        url = PAsearchSites.getSearchBaseURL(siteID) + url
    detailsPageElements = HTML.ElementFromURL(url)

    # Studio
    metadata.studio = 'MetArt'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="info-container"]//h3[contains(@class, "headline")]')[0].text_content().split("(")[0].strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//p[@class="description-text"]')[0].text_content().replace('Read More','').strip()
    except:
        pass

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="tag-list"]//a')
    for genre in genres:
        genreName = genre.text_content().strip()
        movieGenres.addGenre(genreName)
    movieGenres.addGenre("Glamorous")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="movie-data"]//span[@class="attr-value"]')[2].text_content().strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="movie-data"]//span[@class="attr-value"]')[0].xpath('.//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = actorLink.get("href")
                if "http" not in actorPageURL:
                    actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorPageURL
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//div[@class="img-container"]/img')[0].get("src").split("?")[0]
                if "http" not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    # Director
    director = metadata.directors.new()
    try:
        directors = detailsPageElements.xpath('//a[contains(@href,"/photographer/")]')
        for dirname in directors:
            director.name = dirname.text_content().strip()
    except:
        pass

    ### Posters and artwork ###

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