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

    for searchResult in searchResults.xpath('//div[@class="item hover videoThumb"]'):
        titleNoFormatting = searchResult.xpath('./div//a')[0].get('title')
        try:
            actor = "w/ " + searchResult.xpath('./div[@class="item-info clear"]//h5//a[contains(@href,".com/models/")]')[0].text_content()
        except:
            actor = "(No actor)"
        sceneUrl = searchResult.xpath('./div//a')[0].get('href').split("?", 1)[0]
        curID = sceneUrl.replace('/','_').replace('?','!')
        score = 100
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + str(titleNoFormatting), name = titleNoFormatting + " " + actor + " [" + PAsearchSites.getSearchSiteName(siteNum) + "]", score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    pageURL = str(metadata.id).split("|")[0].replace('_', '/')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

    request = urllib.Request(pageURL, headers=headers)
    response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
    htmlstring = response.read()
    detailsPageElements = fromstring(htmlstring)

    # Summary
    sceneTitle = str(metadata.id).split("|")[2]
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.studio = siteName
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="gallery-info"]//h1')[0].text_content().strip()
        metadata.title = sceneTitle
    except:
        pass

    # Collections / Tagline
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Genres
    try:
        genres = detailsPageElements.xpath('//span[@class="gallery-meta"]//span//a[contains(@href,"/porn-videos/")]')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip().lower()
                movieGenres.addGenre(genreName)
    except:
        pass

    # Release Date
    # Can someone add release date ? please

    # Actors
    movieActors.clearActors()

    actors = detailsPageElements.xpath('//div[@class="gallery-info"]//h4//a[contains(@href,".com/models/")]')
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
            actorPhotoURL = detailsActorPage.xpath('//div[@class="section-box profile-pic"]//img')[0].get('src0_1x')
            if actorPhotoURL is None:
                actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)


    # Posters/Background
    for poster in detailsPageElements.xpath('//img[@alt="' + sceneTitle + '"]'):
        i = 0
        while i < 6:
            posterUrl = poster.get('src' + str(i) + '_3x')
            if posterUrl is not None:
                try:
                    Log("DownLoad Posters/Arts: " + str(posterUrl))
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
                except:
                    Log("DownLoad Posters/Arts: " + str(posterUrl))
                    request = urllib.Request(posterUrl, headers=headers)
                    response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                    content = response.read()
                    metadata.art[posterUrl] = Proxy.Media(content)
                    metadata.posters[posterUrl] = Proxy.Media(content)
            i += 1

    return metadata