import PAsearchSites
import PAgenres
import PAextras
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    try:
        Log("Title Search")
        fanSearchBase = "http://familystrokes.org/"
        title_searchString = searchTitle.lower().replace(" ","-").replace(",","").replace("'","")
        url = fanSearchBase + title_searchString
        title_searchResults = HTML.ElementFromURL(url)
        Log("Fan Page url: " + url)
        title_searchResult = title_searchResults.xpath('//div[@id="content-inside"]')[0]
        titleNoFormatting = title_searchResult.xpath('.//h2')[0].text_content().strip()
        Log("SceneTitle: " + titleNoFormatting)
        curID = title_searchResults.xpath('//link[@rel="canonical"]')[0].get('href').replace("/","_").replace("?","!")
        Log("curID: " + curID)
        try:
            releaseDate = parse(title_searchResult.xpath('.//div[@id="title-single"]//span[1]')[0].text_content().strip()).strftime('%Y-%m-%d')
            Log("ReleaseDate Parsed: " + releaseDate)
        except:
            releaseDate = ''
        girlName = title_searchResult.xpath('.//div[@id="title-single"]//a')[0].text_content()
        Log("firstActressName: " + girlName)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = girlName + " in " + titleNoFormatting + " [FamilyStrokes] " + releaseDate, score = score, lang = lang))
# revert to direct url match with official site webpage
    except:
        Log("attempting direct url match")
        searchString = searchTitle.replace(" ","-").replace(",","").replace("'","").replace("?","")
        Log("SearchString: " + searchString)
        fanUrl = PAsearchSites.getSearchSearchURL(searchSiteID) + searchString
        searchResults = HTML.ElementFromURL(fanUrl)
        Log('Source Page: ' + fanUrl)
        searchResult = searchResults.xpath('//div[@id="scenes-card"]')[0]
        titleNoFormatting = searchResult.xpath('.//div[contains(@class,"left-info")]//span')[0].text_content().strip()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResults.xpath('.//link[@rel="canonical"]')[0].get('href').replace('/','_').replace('?','!')
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//div[@class="scene-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        girlName = searchResult.xpath('.//div[@class="starring"]//span')[0].text_content().strip()
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 95
        results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = girlName + " in " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(searchSiteID) + "] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace("_","/").replace("!","?")
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    titleElement = detailsPageElements.xpath('//div[contains(@class,"left-info")]//span')
    sourceSite = True
    if len(titleElement) == 0:
        titleElement = detailsPageElements.xpath('.//h2')
        sourceSite = False
    title = titleElement[0].text_content().strip()
    metadata.title = title

    # Studio
    metadata.studio = 'TeamSkeet'

    if sourceSite:
        Log("Original Site")
        date = detailsPageElements.xpath('//div[@class="scene-date"]')[0].text_content().strip()
        date_object = datetime.strptime(date, '%m/%d/%Y')
        summary = detailsPageElements.xpath('.//div[@class="scene-story"]')[0].text_content().strip()
        actors = detailsPageElements.xpath('//div[@class="starring"]//span')[0].text_content().split(" And ")
        if len(actors) > 0:
            for actorObject in actors:
                actorName = actorObject
                Log("Starring: " + actorName)
                actorPhotoURL = ''
                movieActors.addActor(actorName,actorPhotoURL)
        firstActorName = actors[0]
        backgroundURL = detailsPageElements.xpath('//video')[0].get("poster")
    else:
        Log("Fan info Site")
        date = detailsPageElements.xpath('.//div[@id="title-single"]//span[1]')[0].text_content().strip()
        try:
            date_object = datetime.strptime(date, '%B %dst, %Y')
        except:
            try:
                date_object = datetime.strptime(date, '%B %dnd, %Y')
            except:
                try:
                    date_object = datetime.strptime(date, '%B %drd, %Y')
                except:
                    try:
                        date_object = datetime.strptime(date, '%B %dth, %Y')
                    except:
                        date_object = None
        summary = detailsPageElements.xpath('.//p[@class="more"]')[0].text_content().replace("Story:","").strip()
        actors = detailsPageElements.xpath('//div[@id="title-single"]//a')
        if len(actors) > 0:
            for actorObject in actors:
                actorName = actorObject.text_content()
                Log("Starring: " + actorName)
                actorPhotoURL = ''
                movieActors.addActor(actorName,actorPhotoURL)
        firstActorName = actors[0].text_content()
        backgroundURL = detailsPageElements.xpath('//video')[0].get("poster")

    # Summary
    metadata.summary = summary

    # Tagline and Collection
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Date
    Log('Date: ' + date)
    if date_object != None:
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    # Background
    metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    Log("backgroundURL: " + backgroundURL)

    # try to get posters from fan site
    fanSceneInfo = siteName + "-" + firstActorName + "-" + title
    fanUrl = "https://teamskeetfans.com/" + fanSceneInfo.lower().replace(" ","-").replace("'","").replace("?","").replace("!","").replace(",","")
    Log("Trying fanUrl for posters: " + fanSceneInfo)
    try:
        fanPageElements = HTML.ElementFromURL(fanUrl)
        Log("fanUrl found")
        posters = fanPageElements.xpath('//div[contains(@class,"gallery-group")]//a')
        posterNum = 1
        for poster in posters:
            posterURL = poster.get("href")
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            posterNum = posterNum + 1
            Log("posterURL: " + posterURL)
    except:
        Log("fanUrl failed")
        metadata.posters[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        
        #try for PAextras match
        art=[]
        match = 0
        for site in ["TeamSkeetFans.com", "SkeetScenes.com"]:
            fanSite = PAextras.getFanArt(site, art, actors, actorName, metadata.title, match, siteName)
            match = fanSite[2]
            if match is 1:	
                break
        
        if match is 1 and len(art) >= 10 or match is 2 and len(art) >= 10:
        # Return, first, last and randóm selection of 4 more images
        # If you want more or less posters edít the value in random.sample below or refresh metadata to get a different sample.	
            sample = [art[0], art[-1]] + random.sample(art, 4)     
            art = sample
            Log("Selecting first, last and random 4 images from set")
        
        j = 1
                                          
        for posterUrl in art:
            Log("Trying next Image")
            
            if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
                try:
                    hdr = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
                    req = urllib.Request(posterUrl, headers=hdr)
                    img_file = urllib.urlopen(req)
                    im = StringIO(img_file.read())
                    resized_image = Image.open(im)
                    width, height = resized_image.size
                    #Add the image proxy items to the collection
                    if width > 1 or height > width:
                        # Item is a poster
                        metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                    if width > 100 and width > height:
                        # Item is an art item
                        metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                    j = j + 1
                except:
                    Log("there was an issue")
                    pass

    return metadata
