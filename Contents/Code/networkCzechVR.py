import PAsearchSites
import PAgenres
import ssl


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchString = searchTitle.replace(" ","-")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    try:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    except:
        request = urllib.Request(PAsearchSites.getSearchSearchURL(siteNum) + searchString, headers=headers)
        htmlstring = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1)).read()
        searchResults = HTML.ElementFromString(htmlstring)


    for searchResult in searchResults.xpath('//div[contains(@class,"postTag")]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="nazev"]//h2//a')[0].text_content()
        Log('title: ' + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').replace("./","_")
        Log('curID: ' + curID)
        releaseDate = parse(searchResult.xpath('.//div[@class="datum"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log('releaseDate: ' + releaseDate)
        actors = searchResult.xpath('.//div[@class="nazev"]//div[@class="featuring"]//a')
        actorList = []
        for actor in actors:
            actorName = actor.text_content()
            actorList.append(actorName)
        actorsPrint = ", ".join(actorList)
        Log("actors: " + actorsPrint)

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = actorsPrint + " in " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
        Log(curID + "|" + str(siteNum) + " // " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate + " // " + str(score))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0].replace("_","/")
    urlBase = PAsearchSites.getSearchBaseURL(siteID)
    url = urlBase + temp
    Log('url :' + url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    
    try:
        detailsPageElements = HTML.ElementFromURL(url)
    except:
        request = urllib.Request(url, headers=headers)
        htmlstring = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1)).read()
        detailsPageElements = HTML.ElementFromString(htmlstring)

    # Studio
    metadata.collections.clear()
    metadata.studio = "CzechVR"
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.add(metadata.tagline)
    Log("Studio: CzechVR | Site/Tagline: " + metadata.tagline)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="nazev"]//h2')[0].text_content().replace("Czech VR Fetish","").replace("Czech VR Casting","").replace("Czech VR","").strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="textDetail"]')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="tag"]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().lower().strip()
            movieGenres.addGenre(genreName)

    # Date
    date = detailsPageElements.xpath('//div[@class="nazev"]//div[@class="datum"]')[0].text_content().strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('(//div[@class="nazev"])[1]//div[@class="featuring"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''
            movieActors.addActor(actorName, actorPhotoURL)

    # Background
    background = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//div[@class="foto"]//dl8-video')[0].get("poster")[1:]
    try:
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        request = urllib.Request(background, headers=headers)
        response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        content = response.read()
        metadata.art[background] = Proxy.Media(content, sort_order=1)
    Log("BG DL: " + background)

    # Poster
    posters = detailsPageElements.xpath('//div[@class="galerka"]//a')
    posterNum = 1
    for posterCur in posters:
        posterURL = urlBase + posterCur.get("href")[1:]
        try:
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = (posterNum + 1))
        except:
            request = urllib.Request(posterURL, headers=headers)
            response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
            content = response.read()
            metadata.art[posterURL] = Proxy.Media(content, sort_order=1)
            metadata.posters[posterURL] = Proxy.Media(content, sort_order=1)
        Log("Poster: " + posterURL)




    return metadata
