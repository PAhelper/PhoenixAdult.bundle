import PAsearchSites
import PAgenres
import PAactors
import PAextras
import ssl
from lxml.html.soupparser import fromstring

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="entry clearfix latest"]'):
        titleNoFormatting = searchResult.xpath('.//h3[@class="title"]/a')[0].text_content().strip()
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        if searchDate:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d')
        else:
            releaseDate = ''
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " [18OnlyGirls] ", score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')

    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = '18OnlyGirls'

    try:
        detailsPageElements = HTML.ElementFromURL(url)
    except:
        request = urllib.Request(url, headers=headers)
        response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = response.read()
        detailsPageElements = fromstring(htmlstring)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="entry post clearfix"]/p')[1].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//p[@class="meta-info"]/a[@rel="tag"]')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = str(metadata.id).split("|")[2]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
        Log("Date from file")

    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
        
    # Actors
    actors = detailsPageElements.xpath('//p[@class="meta-info"]/a[@rel="category tag"]')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            try:
                actorPage = HTML.ElementFromURL(actorPageURL)
            except:
                request = urllib.Request(actorPageURL, headers=headers)
                response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                htmlstring = response.read()
                actorPage = fromstring(htmlstring)

            actorPhotoURL = actorPage.xpath('//div[@id="mod_info"]/img')[0].get("src")
            if 'http' not in actorPhotoURL:
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    for poster in detailsPageElements.xpath('//div[@id="gallery-1"]/dl/dt/img'):
        posterUrl = poster.get('src')
        Log("DownLoad Posters/Arts: " + posterUrl)
        if len(posterUrl) > 0:
            try:
                metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
                metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
            except:
                request = urllib.Request(posterUrl, headers=headers)
                response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                content = response.read()
                metadata.art[posterUrl] = Proxy.Media(content, sort_order=1)
                metadata.posters[posterUrl] = Proxy.Media(content, sort_order=1)

    return metadata