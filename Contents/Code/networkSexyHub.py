import PAsearchSites
import PAgenres

def searchSexy(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//article[contains(@class,"release-card scene")]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="card-title"]/a | .//a[@class="release-card__info__title"] | .//a[@class="card-title"]')[0].get('title')
        curID = (PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//div[@class="card-title"]/a | .//a[@class="release-card__info__title"] | .//a[@class="card-title"]')[0].get('href')).replace('/','_').replace('?','!')
        if "fakehostel" in PAsearchSites.getSearchSearchURL(siteNum):
            subSite = "Fake Hostel"
        elif "fitnessrooms" in PAsearchSites.getSearchSearchURL(siteNum):
            subSite = "Fitness Rooms"
        elif "fakedrivingschool" in PAsearchSites.getSearchSearchURL(siteNum):
            subSite = "Fake Driving School"
        else:
            subSite = searchResult.xpath('.//div[@class="site-domain"]')[0].text_content().strip()

        if siteNum != 406 and siteNum != 407:
            network = "SexyHub"
        else:
            network = "FakeHub"
        try:
            releaseDate = parse(searchResult.xpath('.//div[@class="release-date"] | .//div[@class="release-card__info__release-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        except:
            detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//div[@class="card-title"]/a | .//a[@class="release-card__info__title"] | .//a[@class="card-title"]')[0].get('href'))
            releaseDate = parse(detailsPageElements.xpath('//time | //span[@class="release-date"] | //div[@class="release-card__info__release-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+network+"/"+subSite+"] " + releaseDate, score = score, lang = lang))
    return results

def searchFake(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//a[@class="release-card"]'):
        titleNoFormatting = searchResult.xpath('.//h2[@class="title"]')[0].text_content().strip()
        curID = (PAsearchSites.getSearchBaseURL(siteNum) + searchResult.get('href')).replace('/','_').replace('?','!')
        if PAsearchSites.getSearchSiteName(siteNum) == "Fitness Rooms":
            subSite = "Fitness Rooms"
        else:
            subSite = searchResult.xpath('.//div[@class="sub-site-name"]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//div[@class="release-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [FakeHub/"+subSite+"] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    # Studio
    if siteID == 340 or (siteID >= 397 and siteID <= 407):
        metadata.studio = 'FakeHub'
    else:
        metadata.studio = 'SexyHub'
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.summary  = detailsPageElements.xpath('//div[@class="overview"]/p | //div[@class="expandable"]/p | //div[@class="player-info"]/p | //div[@class="release-player__description__text scrollable"]/p')[0].text_content().strip()
    metadata.collections.clear()

    # Tagline
    try:
        subSite = detailsPageElements.xpath('//div[@class="collection-logo"]/img | //a[@class="network-site"]/img')[0].get('alt')
    except:
        subSite = detailsPageElements.xpath('//div[@class="site-logo"]/img | //a[@class="site-logo"]/img')[0].get('alt')

    Log("subSite: "+str(subSite))

    if "danejones" in subSite:
        tagline = "Dane Jones"
    elif "lesbea" in subSite:
        tagline = "Lesbea"
    elif "momxxx" in subSite:
        tagline = "MomXXX"
    elif "Fitnessrooms" in subSite:
        tagline = "Fitness Rooms"
    elif "girlfriends" in subSite:
        tagline = "Girlfriends"
    elif "massagerooms" in subSite:
        tagline = "Massage Rooms"
    elif "Fakehostel" in subSite:
        tagline = "Fake Hostel"
    elif "Fakedrivingschool" in subSite:
        tagline = "Fake Driving School"
    else:
        tagline = subSite
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[contains(@class,"col-tags")]//a[@rel="nofollow"] | //div[contains(@class,"tags tag-container")]//a | //div[contains(@class,"release-player__tags__inner")]//a[@rel="nofollow"]')
    Log("Genres found: "+str(len(genres)))
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//time | //span[@class="release-date"] | //div[@class="release-card__info__release-date"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//article[@class="tag-card"]/a[contains(@href,"/tour/model/")] | //div[contains(@class,"cast-categories tag-container")]/header[contains(text(),"Cast:")]/following-sibling::ul[1]/li/a | //header[@class="release-player__description__header"]/a')
    Log("Actors found: "+str(len(actors)))
    if len(actors) > 0:
        if metadata.title == "Geeky Graduates":
            movieActors.addActor('Alexis Crystal','')
            movieActors.addActor('Barbara Bieber','')
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ''
            try:
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID)+actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = "http:" + actorPage.xpath('//img[@class="card-image load"]')[0].get("src")
            except:
                pass
            
            if actorPhotoURL == '':
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + "/tour/models/"
                actorPage = HTML.ElementFromURL(actorPageURL)
                nextPage = actorPage
                while actorPhotoURL == "" and nextPage:
                    try:
                        actorPhotoURL = "http:"+actorPage.xpath('//img[@class="card-image lazy" and contains(@title,"'+actorName+'")]')[0].get('data-original')
                    except Exception as e:
                        Log("Error: " + str(e))
                        try:
                            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorPage.xpath('//li[@class="paginationui-nav next"]/a')[0].get('href')
                            actorPage = HTML.ElementFromURL(actorPageURL)
                        except:
                            break
            movieActors.addActor(actorName,actorPhotoURL)

    #Posters

    # SexyHub poster
    try:
        tmp = detailsPageElements.xpath('//div[@id="player"]')[0].get('style')
        k = tmp.find("url(")
        j = tmp.rfind(")")
        background = "http:" + tmp[k+4:j].replace('960x540','1021x574')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        background = background.replace('_1.jpg','_2.jpg')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass
 
     # Video poster from script + one extra
    try:
        background = "http:"+detailsPageElements.xpath('//img[@class="trailer-cover"]')[0].get('src').replace('main','1021x574_1')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        background = background.replace('1021x574_1','1021x574_2')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 2)
        metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 2)
    except:
        pass

    try:
        background = "http:"+detailsPageElements.xpath('//img[@class="trailer-cover"]')[0].get('src')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    return metadata
