from googlesearch import search

# HQ Sluts Fansite Search
def getFanArt(site, art, actors, actorName, title):

    summary = ""
    actress = ""
    match = 0
    
    #Some actress name need changing to get matches
    if actorName.lower() == "Lillianne".lower():
        actress = "Ariela"
        actorName = actress
        Log("Actress Name changed to: " + actress)
    elif actorName.lower() == "Rebel Lynn (Contract Star)".lower():
        actress = "Rebel Lynn"
        actorName = actress
        Log("Actress Name changed to: " + actress)
            
    try:
        urls = search('site:'+ site + ' ' + actorName + ' ' + title , stop=2)
        Log('Searching Google for: (site:'+ site + ' ' + actorName + ' ' + title +')')
        for url in urls:
            if match is 0 or matsh is 2:
                googleSearchURL = url
                fanPageElements = HTML.ElementFromURL(googleSearchURL)

                try:
                    #Determine where to look for the Actor Name/s
                    try:
                        if site == "AnalPornFan.com": 
                            nameinheader = fanPageElements.xpath('//div[@class="page-title pad group"]//a[2]')[0].text_content()
                        elif site == "EroticBeauties.net/pics":
                            nameinheader = fanPageElements.xpath('//div[@class="clearfix"]//a[contains(@href, "model")]')[0].text_content()
                        elif site == "HQSluts.com":
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
