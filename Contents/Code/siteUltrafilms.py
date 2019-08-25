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
    url = PAsearchSites.getSearchSearchURL(siteNum) + '%22' + encodedTitle + '%22'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    maxscore = 0

    try:
        searchResults = HTML.ElementFromURL(url)
    except:
        request = urllib.Request(url, headers=headers)
        response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = response.read()
        searchResults = fromstring(htmlstring)

    for searchResult in searchResults.xpath('//ul[@class="listing-videos listing-tube"]/*[div[@class="format-infos"]/div[@class="time-infos"]]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].get('title').strip()
        Log("titleNoFormatting: " + titleNoFormatting)
        actors = searchResult.xpath('.//img')[0].get('alt')
        Log(actors)
        sceneUrl = searchResult.xpath('.//a')[0].get('href')
        curID = sceneUrl.replace('/','_').replace('?','!')
        Log("curID: " + curID)
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " with "+ actors + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] ", score = score, lang = lang))
        if maxscore < score:
            maxscore = score

        Log("MaxScore:" + str(maxscore))

    if maxscore < 100:
        Log("no exact match, trying with normal search")
        url = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

        try:
            searchResults = HTML.ElementFromURL(url)
        except:
            request = urllib.Request(url, headers=headers)
            response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
            htmlstring = response.read()
            searchResults = fromstring(htmlstring)

        for searchResult in searchResults.xpath('//ul[@class="listing-videos listing-tube"]/*[div[@class="format-infos"]/div[@class="time-infos"]]'):
            titleNoFormatting = searchResult.xpath('.//a')[0].get('title').strip()
            Log("titleNoFormatting: " + titleNoFormatting)
            actors = searchResult.xpath('.//img')[0].get('alt')
            Log(actors)
            sceneUrl = searchResult.xpath('.//a')[0].get('href')
            curID = sceneUrl.replace('/','_').replace('?','!')
            Log("curID: " + curID)
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " with "+ actors + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] ", score = score, lang = lang))

    return results
        

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    pageURL = str(metadata.id).split("|")[0].replace('_', '/').replace('?','!')
    Log('scene url: ' + pageURL)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    try:
        detailsPageElements = HTML.ElementFromURL(pageURL)
    except:
        request = urllib.Request(pageURL, headers=headers)
        response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = response.read()
        detailsPageElements = fromstring(htmlstring)

    # Studio
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.studio = siteName

    # Title
    try:
        metadata.title = detailsPageElements.xpath('//span[@property="name"]')[3].text_content().strip()
    except:
        pass

    # Summary
    metadata.summary = ''

    # Collections / Tagline
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Genres
    try:
        genres = detailsPageElements.xpath('//div[@itemprop="keywords"]//ul//li//a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().replace('Movies','').strip().lower()
                movieGenres.addGenre(genreName)
    except:
        pass

    # Release Date
    try:
        date = detailsPageElements.xpath('//div[@class="post_date"]')
        Log('Date from Site:' + str(date))
        if len(date) > 0:
            date = date[0].text_content().strip()
            date_object = parse(date)
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
    except:
        pass

    # Actors
    movieActors.clearActors()

    actors = detailsPageElements.xpath('//h1/span/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background

    for poster in detailsPageElements.xpath('//div[@class="ngg-gallery-thumbnail"]//a'):
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
                metadata.art[posterUrl] = Proxy.Media(content, sort_order = 1)
                metadata.posters[posterUrl] = Proxy.Media(content, sort_order = 1)

    return metadata