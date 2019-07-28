import PAsearchSites
import PAgenres
import PAactors
import PAextras
import ssl
from lxml.html.soupparser import fromstring

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    url = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

    try:
        searchResults = HTML.ElementFromURL(url)
    except:
        # its helpful for linux users, who has "sslv3 alert handshake failure (_ssl.c:590)>" @kamuk90
        req = urllib.Request(url, headers=headers)
        resp = urllib.urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = resp.read()
        searchResults = fromstring(htmlstring)

    for searchResult in searchResults.xpath('//div[@class="video-post-content"]'):
        titleNoFormatting = searchResult.xpath('.//a[@class="video-post-main"]//img')[0].get('alt')
        sceneUrl = searchResult.xpath('.//a[@class="video-post-main"]')[0].get('href')
        Log("titleNoFormatting: " + titleNoFormatting)
        Log("sceneUrl: " + sceneUrl)
        femaleActor = searchResult.xpath('.//span[@class="video-model-list w-100"]//a')[0].text_content()
        Log("femaleActor: " + femaleActor) # I think dont need add Markus Dupree
        curID = sceneUrl.replace('/','_').replace('?','!')
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//span[@class="video-data float-right"]//em')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        ### special for claygoldfinch - start
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        ### special for claygoldfinch - end
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + femaleActor + "] [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    pageURL = str(metadata.id).split("|")[0].replace('_', '/')
    Log('scene url: ' + pageURL)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    try:
        detailsPageElements = HTML.ElementFromURL(pageURL)
    except:
        req = urllib.Request(pageURL, headers=headers)
        resp = urllib.urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = resp.read()
        detailsPageElements = fromstring(htmlstring)

    # Summary
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.studio = siteName
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="info-video-description"]//p')[0].text_content().strip()
        metadata.title = detailsPageElements.xpath('//div[@class="video-page-header"]//h1')[0].text_content().strip()
    except:
        pass

    # Director
    metadata.directors.clear()
    director = metadata.directors.new()
    director.name = "Markus Dupree"

    # Collections / Tagline
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Genres
    try:
        genres = detailsPageElements.xpath('//div[@class="info-video-category"]//a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip().lower()
                movieGenres.addGenre(genreName)
    except:
        pass

    # Release Date
    try:
        date = detailsPageElements.xpath('//ul[@class="list-unstyled info-video-details"]//li[1]//span')
        if len(date) > 0:
            date = date[0].text_content().strip()
            date_object = parse(date)
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
    except:
        pass

    # Actors
    movieActors.clearActors()

    actors = detailsPageElements.xpath('//div[@class="info-video-models"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = actorLink.get("href")
            try:
                detailsActorPage = HTML.ElementFromURL(actorPageURL)
            except:
                req = urllib.Request(actorPageURL, headers=headers)
                resp = urllib.urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                htmlstring = resp.read()
                detailsActorPage = fromstring(htmlstring)
            actorPhotoURL = detailsActorPage.xpath('//div[@class="m-images"]//img')[0].get('src')
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background

    for poster in detailsPageElements.xpath('//div[@class="swiper-wrapper"]//figure//a'):
        posterUrl = poster.get('href')
        Log("DownLoad Posters/Arts: " + posterUrl)
        if len(posterUrl) > 0:
            try:
                metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
                metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
            except:
                req = urllib.Request(posterUrl, headers=headers)
                resp = urllib.urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                content = resp.read()
                metadata.art[posterUrl] = Proxy.Media(content)
                metadata.posters[posterUrl] = Proxy.Media(content)

    return metadata