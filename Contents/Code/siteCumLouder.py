import PAsearchSites
import PAgenres
import PAactors
import ssl
from dateutil.relativedelta import relativedelta
from lxml.html.soupparser import fromstring

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    url = PAsearchSites.getSearchSearchURL(siteNum) + "%22" + encodedTitle + "%22"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

    try:
        searchResults = HTML.ElementFromURL(url)
    except:
        # its helpful for linux users, who has "sslv3 alert handshake failure (_ssl.c:590)>" @kamuk90
        req = urllib.Request(url, headers=headers)
        resp = urllib.urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = resp.read()
        searchResults = fromstring(htmlstring)


    for searchResult in searchResults.xpath('//div[@class="listado-escenas listado-busqueda"]//div[@class="medida"]/a'):
        titleNoFormatting = searchResult.xpath('.//h2')[0].text_content().strip()
        curID = (PAsearchSites.getSearchBaseURL(siteNum) + searchResult.get('href')).replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [CumLouder] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    pageURL = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')

    Log('scene url: ' + pageURL)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    try:
        detailsPageElements = HTML.ElementFromURL(pageURL)
    except:
        req = urllib.Request(pageURL, headers=headers)
        resp = urllib.urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = resp.read()
        detailsPageElements = fromstring(htmlstring)

    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'CumLouder'

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@id="content-more-less"]/p')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//ul[@class="tags"]/li/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date - no actual date aviable, guessing (better than nothing)
    date = detailsPageElements.xpath('//div[@class="added"]')[0].text_content().strip()
    timeframe = date.split(" ")[2]
    timenumber = int(date.split(" ")[1])
    today = datetime.now()

    if len(timeframe) > 0:
        if timeframe =="minutes":
            date_object = today
        elif timeframe == "hour" or timeframe == "hours":
            date_object = today - relativedelta(hours=timenumber)
        elif timeframe == "day" or timeframe == "days":
            date_object = today - relativedelta(days=timenumber)
        elif timeframe == "week" or timeframe == "weeks":
            date_object = today - relativedelta(weeks=timenumber)
        elif timeframe == "month" or timeframe == "months":
            date_object = today - relativedelta(months=timenumber)
        elif timeframe == "year" or timeframe == "years":
            date_object = today - relativedelta(years=timenumber)
    
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//a[@class="pornstar-link"]')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            
            #images not working (javascript?)

            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)


    # Posters/Background

    posterUrl = detailsPageElements.xpath('//div[@class="box-video box-video-html5"]/video')[0].get("lazy")
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