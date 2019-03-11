import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    xartpost = {
        "input_search_sm" : encodedTitle
    }
    searchResults = HTML.ElementFromURL('https://www.x-art.com/search/', values = xartpost)

    for searchResult in searchResults.xpath('//a[contains(@href,"videos")]'):
        link = searchResult.xpath('.//img[contains(@src,"videos")]')
        if len(link) > 0:
            if link[0].get("alt") is not None:
                
                titleNoFormatting = link[0].get("alt")
                curID = searchResult.get("href")[21:]
                curID = curID.replace('/','+')
                Log(str(curID))
                score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [X-Art]", score = score, lang = lang))
    return results

# Scenes with No matches but will get false match
noMatch = [None] * 3
noMatch[0] = ["Close to The Edge"]
noMatch[1] = ["After Sunset"]
noMatch[2] = ["No Turning Back Part Two"]

# Scenes with incorrect matches
    # second field is 1 for xartfan 2 for nudegals and 3 for xartbeauties
badMatch = [None] * 2
badMatch[0] = ["Twice The Fun", 3, "http://www.xartbeauties.com/galleries/aubrey-in-twice-the-fun-7688.html"]
badMatch[1] = ["Party of Three", 1, "https://xartfan.com/party-of-three/"]

def getNoMatchID(scene):
    matchID = 0
    for match in noMatch:
        if scene.lower().replace(" ","").replace("'","") == match[0].lower().replace(" ","").replace("'",""):
            Log("Title Registered as having no fansite matches.")
            return 0
            
        matchID += 1
    return 9999

def getBadMatchID(scene):
    badID = 0
    for match in badMatch:
        if scene.lower().replace(" ","").replace("'","") == match[0].lower().replace(" ","").replace("'",""):
            Log("Title known for bad fan match. Url set manually.")
            overrideSite = badMatch[badID][1]
            overrideURL = badMatch[badID][2]
            return [overrideSite,overrideURL]
        badID += 1
    return 9999

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('+','/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "X-Art"
    paragraphs = detailsPageElements.xpath('//div[@class="small-12 medium-12 large-12 columns info"]//p')
    summary = ""
    for paragraph in paragraphs:
        summary = summary + '\n\n' + paragraph.text_content()
    metadata.summary = summary.strip()
    metadata.title = detailsPageElements.xpath('//title')[0].text_content()[8:]
    date = detailsPageElements.xpath('//h2')[2].text_content()[:-1]
    date_object = datetime.strptime(date, '%b %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year    
        
    
    # Genres
    movieGenres.clearGenres()
    # No Source for Genres, add manual
    movieGenres.addGenre("Artistic")
    movieGenres.addGenre("Glamcore")
    movieGenres.addGenre("Lesbian")

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h2//a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="info-img"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//div[@class="gallery-item"]')[0]
    poster = posters.xpath('.//img')[0].get('src')
    background = detailsPageElements.xpath('//img[contains(@src,"/videos")]')[0].get("src")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    posterURL = poster[:-21] + "2.jpg"
    metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL).content, sort_order = 1)

    # Extra Posters
    art=[]
    match = 0
    from googlesearch import search
    
    overrideSettings = getBadMatchID(metadata.title)
    
    if overrideSettings != 9999:
        overrideURL = overrideSettings[1]
        overrideSite = overrideSettings[0]
    
    if getNoMatchID(metadata.title) == 9999:
        for i in range(1,4):
        
            if i is 1:
                urls = search('site:xartfan.com ' + actorName + ' ' + metadata.title, stop=2)
            elif i is 2:
                urls = search('site:nude-gals.com ' + actorName + ' ' + metadata.title, stop=2)
            elif i is 3:
                urls = search('site:xartbeauties.com/galleries ' + actorName + ' ' + metadata.title, stop=2)
                
            for url in urls:
                if match is 0:
                    if overrideSettings != 9999:
                        url = overrideURL
                        i = overrideSite

                    googleSearchURL = url
                    fanPageElements = HTML.ElementFromURL(googleSearchURL)

                    try:
                        # See if the actress name matches
                        if i is 1:
                            # Xartfan
                            Log("Trying XartFan")
                            nameinheader = fanPageElements.xpath('//header[@class="entry-header"]/p//a')[0].text_content()
                            Log("Actress name in header: " + nameinheader)
                        if i is 2:
                            # Nude-Gals
                            Log("Trying Nude-Gals")
                            nameinheader = fanPageElements.xpath('//div[@class="row photoshoot-title row_margintop"]//a[contains(@href, "model")]')[0].text_content()
                            Log("Actress name in header: " + nameinheader)
                        if i is 3:
                            # Xart Beauties
                            Log("Trying XartBeauties")
                            nameinheader = fanPageElements.xpath('(//div[@id="header-text"]//p//a)[not(position()=last())]')[0].text_content()
                            Log("Actress name in header: " + nameinheader)
                    except:
                        Log("No Actress found in the site header")
                        pass
                    try:   
                        for actorLink in actors:
                            if match is 0:
                                actorName = actorLink.text_content()
                                Log("Comparing with " + actorName)
                                if actorName in nameinheader or nameinheader in actorName:
                                    Log("Fansite Match Found")
                                    match = 1
                                else:
                                    try:
                                    # When there are multiple actors listed we need to check all of them.
                                        for name in nameinheader:
                                            if match is 0:
                                                Log(name + " vs " + actorName)
                                                if actorName.lower() in name.lower():
                                                    Log(siteName + " Fansite Match Found")
                                                    match = 1
                                        
                                    except:
                                        Log("No Actress Match")
                                        pass
                    except:
                        Log("No Actress Match")
                        pass
                             
                    # Posters
                    if match is 1:
                        try:
                            Log("Searching for images")
                            if i is 1:
                                # Xart Fan
                                for posterURL in fanPageElements.xpath('//div[contains(@class, "tiled-gallery")]//a//img'):
                                    art.append(posterURL.get('data-orig-file').replace('images.', ''))
                                Log("Images found on Xart Fan.")

                            if i is 2:
                                # Nude-Gals
                                for posterURL in fanPageElements.xpath('(//div[@class="row row_margintop"]//a)[not(contains(@title, "#"))]'):
                                    art.append("https://nude-gals.com/" + posterURL.get('href'))
                                Log("Images found on Nude-Gals.")
                            if i is 3:
                                # Xart Beauties
                                for posterURL in fanPageElements.xpath('//div[@id="gallery-thumbs"]//img'):
                                    art.append(posterURL.get('src').replace('images.', 'www.').replace('/tn', ''))
                                Log("Images found on Xart Beauties.")
                        except:
                            Log("No Images Found")
                            pass
                            
                        Log("Artwork found: " + str(len(art)))
                
                    if match is 1:
                        # Return, first few, last one and randóm selection of images
                        # If you want more or less posters edít the value in random.sample below or refresh metadata to get a different sample.	
                        try:
                            sample = [art[0], art[1], art[2], art[3], art[-1]] + random.sample(art, 4)     
                            art = sample
                            Log("Selecting subset of " + str(len(art)) + " images from the set.")
                        except:
                            pass
                    
                j = 1
                                                      
                for posterUrl in art:
                    Log("Trying next Image")
                    Log(posterUrl)
                    if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
                    #Download image file for analysis
                        try:
                            #img_file = requests.get(posterUrl)
                            img_file = urllib.urlopen(posterUrl)
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
            if len(art) < 10 and match is 1:
                Log("Less than 10 images found. Searching for more")
                match = 0
    
    return metadata
