import PAsearchSites
import PAgenres
import PAactors
import PAextras
import ssl
from lxml.html.soupparser import fromstring

# maybe helpful for linux users, who has "sslv3 alert handshake failure (_ssl.c:590)>" @kamuk90
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    url = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

    try:
        searchResults = HTML.ElementFromURL(url)
    except:
        request = urllib.Request(url, headers=headers)
        response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = response.read()
        searchResults = fromstring(htmlstring)

    for searchResult in searchResults.xpath('//div[@id="list_videos_videos_list_search_result_items"]/div[1]'):
        titleNoFormatting = searchResult.xpath('//a[@class="video-title-title"]')[0].get('title')
        Log("titleNoFormatting: " + titleNoFormatting)
        actors = searchResults.xpath('//span[@class="video-model-list w-100"]//a')
        femaleActor = actors[0].text_content()
        sceneUrl = searchResult.xpath('//a[@class="video-title-title"]')[0].get('href')
        curID = sceneUrl.replace('/','_').replace('?','!')
        Log("curID: " + curID)
        releaseDate = parse(searchResults.xpath('//span[@class="video-data float-right"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        score = 100
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + femaleActor + "] [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    pageURL = str(metadata.id).split("|")[0].replace('_', '/')
    Log('scene url: ' + pageURL)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    try:
        detailsPageElements = HTML.ElementFromURL(pageURL)
    except:
        request = urllib.Request(pageURL, headers=headers)
        response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = response.read()
        detailsPageElements = fromstring(htmlstring)

    # Summary
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.studio = siteName
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="info-video-description"]//p')[0].text_content().strip().replace("...", "").replace("Less", "")
        metadata.title = detailsPageElements.xpath('//div[@class="video-page-header"]//h1')[0].text_content().strip()
    except:
        pass

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
                request = urllib.Request(actorPageURL, headers=headers)
                response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                htmlstring = response.read()
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
                request = urllib.Request(posterUrl, headers=headers)
                response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                content = response.read()
                metadata.art[posterUrl] = Proxy.Media(content)
                metadata.posters[posterUrl] = Proxy.Media(content)

    return metadata