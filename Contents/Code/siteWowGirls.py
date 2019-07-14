import PAsearchSites
import PAgenres
import PAactors
import PAextras
import ssl
from lxml.html.soupparser import fromstring

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    
    urlWowXXX = PAsearchSites.getSearchSearchURL(siteNum) + '%22' + encodedTitle +'%22'
    urlWowTV = 'https://www.wowgirls.tv/?s=%22' + encodedTitle +'%22'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

    try:
        searchResultsWowXXX = HTML.ElementFromURL(urlWowXXX)
    except:
        request = urllib.Request(urlWowXXX, headers=headers)
        response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = response.read()
        searchResultsWowXXX = fromstring(htmlstring)

    Log('Search-Video-Number: ' + searchResultsWowXXX.xpath('//span[@class="search-video-number"]')[0].text_content().split(' ',1)[0])
    if int(searchResultsWowXXX.xpath('//span[@class="search-video-number"]')[0].text_content().split(' ',1)[0]) > 0:
        Log('Title Found on wowgirls.xxx')

        for searchResult in searchResultsWowXXX.xpath('//div[@class="videos-list"]/article'):
            titleNoFormatting = searchResult.xpath('.//a')[0].get('title').strip()
            curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            if searchDate:
                releaseDate = parse(searchDate).strftime('%Y-%m-%d')
            else:
                releaseDate = ''
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate , name = titleNoFormatting + " [WowGirls.xxx] ", score = score, lang = lang))
    
    else:
        Log('no Tile found on wowgirls.xxx, trying wowgirls.tv')

        try:
            searchResultsWowTV = HTML.ElementFromURL(urlWowTV)
        except:
            request = urllib.Request(urlWowTV, headers=headers)
            response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
            htmlstring = response.read()
            searchResultsWowTV = fromstring(htmlstring)

        if len(searchResultsWowTV.xpath('//h1')) == 0:
            Log('Title found on wowgirls.tv')

            for searchResult in searchResultsWowTV.xpath('//div[@class="entry clearfix latest"]'):
                titleNoFormatting = searchResult.xpath('.//h3/a')[0].text_content().strip()
                curID = searchResult.xpath('.//h3/a')[0].get('href').replace('/','_').replace('?','!')
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                if searchDate:
                    releaseDate = parse(searchDate).strftime('%Y-%m-%d')
                else:
                    releaseDate = ''
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate , name = titleNoFormatting + " [WowGirls.tv] ", score = score, lang = lang))

        else:
            Log('No exact Title found, trying normal Search on wowgirls.xxx and .tv')
            
            urlWowXXX = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
            urlWowTV = 'https://www.wowgirls.tv/?s=' + encodedTitle
            
            try:
                searchResultsWowXXX = HTML.ElementFromURL(urlWowXXX)
            except:
                request = urllib.Request(urlWowXXX, headers=headers)
                response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                htmlstring = response.read()
                searchResultsWowXXX = fromstring(htmlstring)
            
            for searchResult in searchResultsWowXXX.xpath('//div[@class="videos-list"]/article'):
                titleNoFormatting = searchResult.xpath('.//a')[0].get('title').strip()
                curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                if searchDate:
                    releaseDate = parse(searchDate).strftime('%Y-%m-%d')
                else:
                    releaseDate = ''
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate , name = titleNoFormatting + " [WowGirls.xxx] ", score = score, lang = lang))

            try:
                searchResultsWowTV = HTML.ElementFromURL(urlWowTV)
            except:
                request = urllib.Request(urlWowTV, headers=headers)
                response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                htmlstring = response.read()
                searchResultsWowTV = fromstring(htmlstring)
            
            for searchResult in searchResultsWowTV.xpath('//div[@class="entry clearfix latest"]'):
                titleNoFormatting = searchResult.xpath('.//h3/a')[0].text_content().strip()
                curID = searchResult.xpath('.//h3/a')[0].get('href').replace('/','_').replace('?','!')
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                if searchDate:
                    releaseDate = parse(searchDate).strftime('%Y-%m-%d')
                else:
                    releaseDate = ''
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate , name = titleNoFormatting + " [WowGirls.tv] ", score = score, lang = lang))




    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    sitename = str(metadata.id).split("|")[0].split('_')[2]
    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')

    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'WowGirls'

    try:
        detailsPageElements = HTML.ElementFromURL(url)
    except:
        request = urllib.Request(url, headers=headers)
        response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        htmlstring = response.read()
        detailsPageElements = fromstring(htmlstring)

    Log('Sitename '+ sitename)
    if "xxx" in sitename:
        Log('wowporn.xxx')

        # Title
        metadata.title = detailsPageElements.xpath('//div[@class="title-views"]/h1')[0].text_content().strip().rsplit(" ",3)[0]

        # Summary
        metadata.summary = detailsPageElements.xpath('//div[@class="desc "]/p')[0].text_content().strip()

        #Tagline and Collection(s)
        tagline = PAsearchSites.getSearchSiteName(siteID).strip()
        metadata.tagline = tagline
        metadata.collections.add(tagline)

        # Genres
        genres = detailsPageElements.xpath('//div[@class="tags-list"]/a[i[@class="fa fa-folder"]]')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip().lower()
                movieGenres.addGenre(genreName)

        # Release Date
        try:
            date = detailsPageElements.xpath('//meta[@property="article:published_time"]')[0].get('content')
        except:
            date = str(metadata.id).split("|")[2]
            Log("Date from file")

        if len(date) > 0:
            date_object = parse(date)
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
        
        # Actors
        actors = detailsPageElements.xpath('//div[@class="tags-list"]/a[i[@class="fa fa-tag"]]')
        if len(actors) > 0:
            if len(actors) == 3:
                movieGenres.addGenre("Threesome")
            if len(actors) == 4:
                movieGenres.addGenre("Foursome")
            if len(actors) > 4:
                movieGenres.addGenre("Orgy")
            for actorLink in actors:
                actorName = str(actorLink.text_content().strip())
                actorPhotoURL = ''
                movieActors.addActor(actorName,actorPhotoURL)


        ### Posters and artwork ###

        # Video trailer background image
        twitterBG = detailsPageElements.xpath('//meta[@property="og:image"]')[0].get('content')
        Log("TwitterBG: " + twitterBG)
        art.append(twitterBG)


    else:
        Log('wowporn.tv')

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





                movieActors.addActor(actorName,actorPhotoURL)


        ### Posters and artwork ###

        for poster in detailsPageElements.xpath('//div[@id="gallery-1"]/dl/dt/img'):
            posterUrl = poster.get('src')
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

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
            j = j + 1

    return metadata