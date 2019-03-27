from googlesearch import search

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

# HQ Sluts Fansite Search
def getFanArt(site, art, actors, actorName, title):

    summary = ""
    actress = ""
    match = 0
    
    overrideSettings = getBadMatchID(title) 
    if overrideSettings != 9999:
        overrideURL = overrideSettings[1]
        overrideSite = overrideSettings[0]
    
    
    
    #Some actress name need changing to get matches
    if actorName.lower() == "Lillianne".lower():
        actress = "Ariela"
        actorName = actress
        Log("Actress Name changed to: " + actress)
    elif actorName.lower() == "Rebel Lynn (Contract Star)".lower():
        actress = "Rebel Lynn"
        actorName = actress
        Log("Actress Name changed to: " + actress)
    
    if getNoMatchID(title) == 9999:    
        try:
            if match is 0 or match is 2:
                urls = search('site:'+ site + ' ' + actorName + ' ' + title , stop=2)
                Log('Searching Google for: (site:'+ site + ' ' + actorName + ' ' + title +')')
                for url in urls:
                    if overrideSettings != 9999:
                        url = overrideURL
                        Log("Title known for bad fan match. URL set manually.")
                    
                    googleSearchURL = url
                    fanPageElements = HTML.ElementFromURL(googleSearchURL)

                    try:
                        #Determine where to look for the Actor Name/s
                        try:
                            if site == "AnalPornFan.com": 
                                nameinheader = fanPageElements.xpath('//div[@class="page-title pad group"]//a[2]')[0].text_content()
                            elif site == "EroticBeauties.net/pics":
                                nameinheader = fanPageElements.xpath('//div[@class="clearfix"]//a[contains(@href, "model")]')[0].text_content()
                            elif "hqsluts.com" in url:
                                nameinheader = fanPageElements.xpath('//p[@class="details"]//a[contains(@href, "sluts")]')[0].text_content()
                            elif site == "Nude-Gals.com":
                                nameinheader = fanPageElements.xpath('//div[@class="row photoshoot-title row_margintop"]//a[contains(@href, "model")]')[0].text_content()
                            elif site in ["PassionHDFan.com", "LubedFan.com"]:
                                nameinheader = fanPageElements.xpath('//div[@class="page-title pad group"]//a')[0].text_content()
                            elif site in ["SpyFams.com", "TeamSkeetFans.com"]:
                                nameinheader = fanPageElements.xpath('(//span[@itemprop="articleSection"])')[0].text_content()
                            elif site == "XartBeauties.com/galleries":
                                nameinheader = fanPageElements.xpath('(//div[@id="header-text"]//p//a)[not(position()=last())]')[0].text_content()
                            elif site == "XartFan.com":
                                nameinheader = fanPageElements.xpath('//header[@class="entry-header"]/p//a')[0].text_content()
                                
                            Log("Actress name in header: " + nameinheader)
                        except:
                            Log("No Actress found in the site header")
                            
                    #CHECK IF WE HAVE A FANSITE MATCH USING ACTOR NAMES    
                        if actorName in nameinheader:
                            Log("Fansite Match Found on " + site)
                            match = 1
                        else:
                            # When there are multiple actors listed we need to check all of them.
                            try:
                                for actorLink in actors:
                                    if site == "teamskeetfans.com":
                                        actorName = actorLink
                                    else:
                                        actorName = actorLink.text_content()
             
                                    for name in nameinheader:
                                        Log("Comparing with: " + actorName) 
                                        if actorName.lower() == name.lower() or actress.lower() == name.lower():
                                            Log(siteName + " Fansite Match Found")
                                            match = 1
                            except:
                                Log("No Actress Match")
                             
                        # found one example of a badmatch not working because the actress match failed. this forces it to proceed.
                        if overrideSettings != 9999:
                            match = 1
                        
                        # POSTERS
                        if match is 1:
                            try:
                            # Various Poster xpaths needed for different sites
                                Log("Searching " + site)
                                if site in ["AnalPornFan.com", "LubedFan.com"]:
                                    for posterURL in fanPageElements.xpath('//div[contains(@class, "rgg-imagegrid")]//a'):
                                        art.append(posterURL.get('href'))
                                elif site == "EroticBeauties.net/pics":
                                    for posterURL in fanPageElements.xpath('//div[contains(@class, "my-gallery")]//a'):
                                        art.append(posterURL.get('href'))
                                elif site == "HQSluts.com":
                                    for posterURL in fanPageElements.xpath('//li[@class="item i"]//a'):
                                        art.append(posterURL.get('href'))
                                elif site == "Nude-Gals.com":
                                    for posterURL in fanPageElements.xpath('(//div[@class="row row_margintop"]//a)[not(contains(@title, "#"))]'):
                                        art.append("https://nude-gals.com/" + posterURL.get('href'))
                                elif site in ["PassionHDFan.com", "SpyFams.com", "TeamSkeetFans.com"]:
                                    for posterURL in fanPageElements.xpath('//div[contains(@class, "tiled-gallery")]//a/img'):
                                        art.append(posterURL.get('data-orig-file'))
                                elif site == "XartBeauties.com/galleries":
                                    for posterURL in fanPageElements.xpath('//div[@id="gallery-thumbs"]//img'):
                                        art.append(posterURL.get('src').replace('images.', 'www.').replace('/tn', ''))
                                elif site == "XartFan.com":
                                    for posterURL in fanPageElements.xpath('//div[contains(@class, "tiled-gallery")]//a//img'):
                                        art.append(posterURL.get('data-orig-file').replace('images.', ''))
                                    
                            except:
                                Log("No Images Found")
                            
                            
                            Log("Artwork found: " + str(len(art)))
                            if len(art) < 9 and match is 1:
                                match = 2
                    except:
                        Log("No Fansite Match")
                        
                    if match is 1 or match is 2:
                        # Summary
                        try:
                            if site in ["AnalPornFan.com", "LubedFan.com", "PassionHDFan.com"]:
                                summary = fanPageElements.xpath('//div[@class="entry-inner"]//p')[0].text_content().replace("---->Click Here to Download<----", '').strip()
                            elif site == "SpyFams.com":
                                paragraphs = fanPageElements.xpath('(//div[@class="entry-content g1-typography-xl"]//p)[not(*[contains(@class, "jp-relatedposts-post")])]')
                                if len(paragraphs) > 3:
                                    pNum = 1
                                    for paragraph in paragraphs:
                                        if pNum >= 1 and pNum <= 7:
                                            summary = summary + '\n\n' + paragraph.text_content()
                                        pNum += 1
                                    summary = summary.strip()
                                else:
                                    summary = fanPageElements.xpath('(//div[@class="entry-content g1-typography-xl"]//p)[position()=1]')[0].text_content().strip()
                            elif site == "TeamSkeetFans.com":
                                paragraphs = fanPageElements.xpath('//div[@class="entry-content g1-typography-xl"]')[0].text_content().split('\n')
                                if len(paragraphs) > 13:
                                    for paragraph in paragraphs:
                                        summary = (summary + '\n\n' + paragraph).replace("LinkEmbedCopy and paste this HTML code into your webpage to embed.", '').replace("--> Click Here for More Sis Loves Me! <--", '').strip()
                                else:
                                    summary = fanPageElements.xpath('(//div[@class="entry-content g1-typography-xl"]//p)[position()=1]')[0].text_content().strip()
                        except:
                            Log("Error grabbing fansite summary")  
                        
        except:
            Log("No Fansite Match")
    return (art, summary, match)
