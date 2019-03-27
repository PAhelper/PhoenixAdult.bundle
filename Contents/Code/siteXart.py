import PAsearchSites
import PAgenres
import PAextras
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
    if searchTitle == "Naughty  Nice":
        Log("Manual Search Match")
        curID = ("/videos/Naughty_&_Nice")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Naughty & Nice" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Out Of This World":
        Log("Manual Search Match")
        curID = ("/videos/Out_of_This_World")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Out Of This World" + " [X-Art]", score = 101, lang = lang))
    return results

# Scenes with No matches but will get false match
noMatch = [None] * 24
noMatch[0] = ["Close to The Edge"]
noMatch[1] = ["After Sunset"]
noMatch[2] = ["No Turning Back Part Two"]
noMatch[3] = ["Dont Keep Me Waiting  Part 2"]
noMatch[4] = ["Drinks for 2"]
noMatch[5] = ["From 3 to 4 part 1"]
noMatch[6] = ["Girlfriends"]
noMatch[7] = ["Intimo"]
noMatch[8] = ["Perfect Girls"]
noMatch[9] = ["Stairway to Heaven"]
noMatch[10] = ["Through the Looking Glass"]
noMatch[11] = ["For your Enyes Only"]
noMatch[12] = ["Like the First Time"]
noMatch[13] = ["Little Play Thing"]
noMatch[14] = ["Lovers Quarrel"]
noMatch[15] = ["No Turning Back Part One"]
noMatch[16] = ["Private Tutor"]
noMatch[17] = ["Red Hot Christmas"]
noMatch[18] = ["Young Passion"]
noMatch[19] = ["Classic beauty"]
noMatch[20] = ["If Only"]
noMatch[21] = ["Poolside Pleasure"]
noMatch[22] = ["She Bad"]
noMatch[23] = ["The Rich Girl - part one"]


# Scenes with incorrect matches
    # second field is 1 for xartfan 2 for nudegals and 3 for xartbeauties
badMatch = [None] * 32
badMatch[0] = ["Twice The Fun", 3, "http://www.xartbeauties.com/galleries/aubrey-in-twice-the-fun-7688.html"]
badMatch[1] = ["Party of Three", 1, "https://xartfan.com/party-of-three/"]
badMatch[2] = ["Fun for Three", 3, "http://www.xartbeauties.com/galleries/angelica-heidi-in-fun-for-three-5994.html"]
badMatch[3] = ["One Show For Each", 3, "http://www.xartbeauties.com/galleries/katherine-angelica-in-one-show-for-each-7018.html"]
badMatch[4] = ["Fucking Goddesses", 3, "http://www.xartbeauties.com/galleries/caprice-angelica-in-fucking-goddesses-6814.html"]
badMatch[5] = ["Should Have Seen Your Face", 3, "http://www.xartbeauties.com/galleries/jenna-aubrey-in-should-have-seen-your-face-7719.html"]
badMatch[6] = ["The Sleepover", 3, "http://www.xartbeauties.com/galleries/leila-caprice-angelica-in-the-sleepover-3879.html"]
badMatch[7] = ["Three in the Morning", 1, "https://xartfan.com/x-art-francesca-caprice-tiffany-suite-19/"]
badMatch[8] = ["Triple Play", 3, "http://www.xartbeauties.com/galleries/kenna-alex-grey-blake-in-triple-play-8281.html"]
badMatch[9] = ["Tropical Fantasy", 3, "http://www.xartbeauties.com/galleries/leila-caprice-in-tropical-fantasy-1974.html"]
badMatch[10] = ["Alex Greys First Lesbian Experience", 3, "http://www.xartbeauties.com/galleries/aubrey-alex-grey-in-first-lesbian-experience-8196.html"]
badMatch[11] = ["Come to me now", 3, "http://www.xartbeauties.com/galleries/naomi-the-red-fox-in-come-to-me-now-5971.html"]
badMatch[12] = ["Above the Air", 3, "http://www.xartbeauties.com/galleries/addison-c-in-above-the-air-8148.html"]
badMatch[13] = ["Back for More", 3, "http://www.xartbeauties.com/galleries/aubrey-in-back-for-more-7389.html"]
badMatch[14] = ["Bound By Desire", 3, "http://www.xartbeauties.com/galleries/aubrey-in-bound-by-desire-8228.html"]
badMatch[15] = ["Deep inside Gina", 3, "http://www.xartbeauties.com/galleries/gina-in-deep-inside-gina-9700.html"]
badMatch[16] = ["Double Tease", 3, "http://www.xartbeauties.com/galleries/caprice-in-double-tease-5957.html"]
badMatch[17] = ["Hot Coffee", 1, "https://xartfan.com/hot-cofee-with-alina-edward"]
badMatch[18] = ["Into The Lions Mouth", 1, "https://xartfan.com/x-art-cayla-into-the-lions-mouth"]
badMatch[19] = ["Just Watch Part 2", 3, "http://www.xartbeauties.com/galleries/kate-in-just-watch-part-ii-6206.html"]
badMatch[20] = ["Raw Passion", 3, "http://www.xartbeauties.com/galleries/scarlet-in-raw-passion-5982.html"]
badMatch[21] = ["Sneaking In", 3, "http://www.xartbeauties.com/galleries/angelica-in-sneaking-in-4495.html"]
badMatch[22] = ["The Studio Part II", 3, "http://www.xartbeauties.com/galleries/angelica-in-the-studio-part-ii-7558.html"]
badMatch[23] = ["They Meet Again", 3, "http://www.xartbeauties.com/galleries/silvie-in-they-meet-again-4932.html"]
badMatch[24] = ["Together Again", 1, "https://xartfan.com/x-art-baby-waking-up-from-a-dream/"]
badMatch[25] = ["Heaven Sent", 1, "https://xartfan.com/x-art-ivy-dare-to-dream/"]
badMatch[26] = ["Angelica Means Angel", 3, "http://www.xartbeauties.com/galleries/angelica-in-angelica-means-angel-6456.html"]
badMatch[27] = ["Big Toy Orgasm Video", 3, "http://www.xartbeauties.com/galleries/carlie-in-big-toy-orgasm-588.html"]
badMatch[28] = ["Fashion Fantasy", 3, "http://www.xartbeauties.com/galleries/mila-k-in-fashion-fantasy-7460.html"]
badMatch[29] = ["Girl in a Room", 3, "http://www.xartbeauties.com/galleries/mila-k-in-girl-in-a-room-4499.html"]
badMatch[30] = ["I will See You In the Morning", 3, "http://www.xartbeauties.com/galleries/tiffany-in-i-will-see-you-in-the-morning-5690.html"]
badMatch[31] = ["Just Watch Part 1", 3, "http://www.xartbeauties.com/galleries/kate-in-just-watch-part-i-6432.html"]
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
        if scene.lower().replace(" ","").replace("'","").replace("\\","").replace("&","and") == match[0].lower().replace(" ","").replace("'","").replace("&","and"):
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
    try:
        posters = detailsPageElements.xpath('//div[@class="gallery-item"]')[0]
        poster = posters.xpath('.//img')[0].get('src')
    except:
        pass
    background = detailsPageElements.xpath('//img[contains(@src,"/videos")]')[0].get("src")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    try:
        posterURL = poster[:-21] + "2.jpg"
    except:
        posterURL = background[:-21] + "2.jpg"
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
        
            if match is 0 or match is 2:
                if i is 1:
                    Log("Trying XartFan")
                    urls = search('site:xartfan.com ' + actorName + ' ' + metadata.title, stop=2)
                 # Test PAextras match
                elif i is 2:
                    fanSite = PAextras.getFanArt("hqsluts.com", art, actors, actorName, metadata.title)
                    try:
                        if str(len(art)) > 1:
                            match = 1
                    except:
                        pass
                elif i is 3:
                    Log("Trying XartBeauties")
                    urls = search('site:xartbeauties.com/galleries ' + actorName + ' ' + metadata.title, stop=2)
                elif i is 4:
                    Log("Trying EroticBeauties")
                    urls = search('site:eroticbeauties.net/pics ' + actorName + ' ' + metadata.title, stop=2)
                elif i is 5:
                    Log("Trying Nude-Gals")
                    urls = search('site:nude-gals.com ' + actorName + ' ' + metadata.title, stop=2)
                    
            for url in urls:
                if match is 0 or match is 2:
                    if overrideSettings != 9999:
                        url = overrideURL
                        i = overrideSite
                        Log("Title known for bad fan match. URL set manually.")

                    googleSearchURL = url
                    fanPageElements = HTML.ElementFromURL(googleSearchURL)

                    try:
                        # See if the actress name matches
                        if i is 1:
                            # Xartfan
                            nameinheader = fanPageElements.xpath('//header[@class="entry-header"]/p//a')[0].text_content()
                            Log("Actress name in header: " + nameinheader)
                        if i is 3:
                            # Xart Beauties
                            nameinheader = fanPageElements.xpath('(//div[@id="header-text"]//p//a)[not(position()=last())]')[0].text_content()
                            Log("Actress name in header: " + nameinheader)
                        if i is 4:
                            # Erotic Beauties
                            nameinheader = fanPageElements.xpath('//div[@class="clearfix"]//a[contains(@href, "model")]')[0].text_content()
                            Log("Actress name in header: " + nameinheader)
                        if i is 5:
                            # Nude-Gals
                            nameinheader = fanPageElements.xpath('//div[@class="row photoshoot-title row_margintop"]//a[contains(@href, "model")]')[0].text_content()
                            Log("Actress name in header: " + nameinheader)
                        try: 
                            for actorLink in actors:
                                if match is 0 or match is 2:
                                    actorName = actorLink.text_content()
                                    Log("Comparing with " + actorName)
                                    if actorName in nameinheader or nameinheader in actorName:
                                        Log("Fansite Match Found")
                                        match = 1
                                    else:
                                        try:
                                        # When there are multiple actors listed we need to check all of them.
                                            for name in nameinheader:
                                                if match is 0 or match is 2:
                                                    Log(name + " vs " + actorName)
                                                    if actorName.lower() in name.lower():
                                                        Log(siteName + " Fansite Match Found")
                                                        match = 1
                                            
                                        except:
                                            Log("No Actress Match")
                        except:
                            Log("No Actress Match")
                    except:
                        Log("No Actress found in the site header")
                    
                    # found one example of a badmatch not working because the actress match failed. this forces it to proceed.
                    if overrideSettings != 9999:
                        match = 1
                    
                         
                    # Posters
                    if match is 1:
                        try:
                            Log("Searching for images")
                            if i is 1:
                                # Xart Fan
                                for posterURL in fanPageElements.xpath('//div[contains(@class, "tiled-gallery")]//a//img'):
                                    art.append(posterURL.get('data-orig-file').replace('images.', ''))
                                Log("Images found on Xart Fan.")

                            if i is 3:
                                # Xart Beauties
                                for posterURL in fanPageElements.xpath('//div[@id="gallery-thumbs"]//img'):
                                    art.append(posterURL.get('src').replace('images.', 'www.').replace('/tn', ''))
                                Log("Images found on Xart Beauties.")
                            if i is 4:
                                # Erotic Beauties
                                for posterURL in fanPageElements.xpath('//div[contains(@class, "my-gallery")]//a'):
                                    art.append(posterURL.get('href'))
                                Log("Images found on Erotic Beauties.")
                            if i is 5:
                                # Nude-Gals
                                for posterURL in fanPageElements.xpath('(//div[@class="row row_margintop"]//a)[not(contains(@title, "#"))]'):
                                    art.append("https://nude-gals.com/" + posterURL.get('href'))
                                Log("Images found on Nude-Gals.")
                        except:
                            Log("No Images Found")
                            pass
                            
                        Log("Artwork found: " + str(len(art)))
                        if len(art) < 9 and match is 1:
                            Log("Less than 10 images found. Searching for more")
                            match = 2
                
        if match is 1 or match is 2:
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
    
    return metadata
