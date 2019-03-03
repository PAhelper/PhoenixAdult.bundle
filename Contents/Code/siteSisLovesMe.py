import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    if unicode(searchTitle, 'utf-8').isnumeric():
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
        searchResult = searchResults
        
        titleNoFormatting = searchResult.xpath('//div[@class="red_big"]/text()')[0].strip()
        Log(titleNoFormatting)
        curID = searchResult.xpath('//link[@rel="canonical"]')[0].get('href').replace('/','_').replace('?','!')
        Log("ID: " + curID)
#        releaseDate = parse(searchResult.xpath(no    clue     .text_content().strip()).strftime('%Y-%m-%d')

        score = 100
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] ", score = score, lang = lang))

    return results



def update(metadata,siteID,movieGenres,movieActors):
    art =[]
    Log('******UPDATE CALLED*******')   
    detailsPageElements = HTML.ElementFromURL(str(metadata.id).split("|")[0].replace('_', '/'))
    Log("urlName: " + detailsPageElements.xpath('//video[@id="preview"]')[0].get("poster").split('/')[5])
    urlName = detailsPageElements.xpath('//video[@id="preview"]')[0].get("poster").split('/')[5]

    # Summary
    metadata.studio = "TeamSkeet"
    metadata.summary = detailsPageElements.xpath('(//div[@class="vid-desc-mobile"]/span)[not(position()=1)][not(position()=last())]')[0].text_content()
    metadata.title = detailsPageElements.xpath('//div[@class="red_big"]/text()')[0].strip()
#    releaseDate = detailsPageElements.xpath

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="red_big"]/span/text()')[0].split(" and ")
    if len(actors) > 0:
        for actor in actors:
            actorName = actor
            actorPhotoURL = "http://cdn.teamskeetimages.com/design/tour/slm/tour/pics/"+urlName+"/"+urlName+".jpg"
            Log("actorPhoto: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    try:
        art.append("http:" + detailsPageElements.xpath('//video[@id="preview"]')[0].get("poster"))
    except:
        pass

    try:
        art.append("http://cdn1.teamskeetimages.com/design/tour/slm/tour/pics/"+urlName+"/v2.jpg")
    except:
        pass

    try:
        art.append("https://cdn.teamskeetimages.com/design/tour/slm/tour/pics/"+urlName+"/bio_small.jpg")
    except:
        pass

    try:
        art.append("https://cdn.teamskeetimages.com/design/tour/slm/tour/pics/"+urlName+"/bio_small2.jpg")
    except:
        pass

    try:
        art.append("https://cdn.teamskeetimages.com/design/tour/slm/tour/pics/"+urlName+"/bio_big.jpg")
    except:
        pass

    try:
        art.append("http://cdn.teamskeetimages.com/teamskeet/slm/"+urlName+"/shared/low.jpg")
    except:
        pass

    try:
        art.append("http://cdn.teamskeetimages.com/teamskeet/slm/"+urlName+"/shared/med.jpg")
    except:
        pass

    try:
        art.append("http://cdn.teamskeetimages.com/teamskeet/slm/"+urlName+"/shared/hi.jpg")
    except:
        pass

    #Extra Posters
    import random
    from googlesearch import search
	
    # Check first X google results. Set Stop = X to search more
    urls = search('site:teamskeetfans.com" ' + actorName + ' ' + metadata.title , stop=2)

    match = 0
    for url in urls:
        if match is 0:
            googleSearchURL = url
            fanPageElements = HTML.ElementFromURL(googleSearchURL)

            try:
                try:
                    nameinheader = fanPageElements.xpath('//span[@itemprop="articleSection"]')[0].text_content()
                    Log("Actress name in header: " + nameinheader)
                except:
                    Log("No Actress found in the fansite header")
                    pass
                    
                if actorName.lower() in nameinheader.lower():
                    Log(siteName + " Fansite Match Found")
                    match = 1
                else:
                # When there are multiple actors listed we need to check all of them.
                    try:
                        for actor in actors:
                            for name in nameinheader:
                                if actor.lower() == name.lower():
                                    Log(siteName + " Fansite Match Found")
                                    match = 1
                    except:
                        Log("No Match")
                        pass
                        
                if match is 1:
                    # Summary
                    try:
                        paragraphs = fanPageElements.xpath('//div[@class="entry-content g1-typography-xl"]')[0].text_content().split('\n')
                        Log(len(paragraphs))
                        if len(paragraphs) > 13:
                            summary = ""
                            for paragraph in paragraphs:
                                summary = (summary + '\n\n' + paragraph).replace("LinkEmbedCopy and paste this HTML code into your webpage to embed.", '').replace("--> Click Here for More Sis Loves Me! <--", '').strip()
                            if len(metadata.summary) < len(summary):
                                metadata.summary = summary.strip()
                        else:
                            summary = fanPageElements.xpath('(//div[@class="entry-content g1-typography-xl"]//p)[position()=1]')[0].text_content()
                        if len(metadata.summary) < len(summary):
                            metadata.summary = summary.strip()   
                    except:
                        Log("Error grabbing fansite summary")
                        pass                    
                     
                    # Posters
                    try:
                        Log("Searching Fan site")
                        for posterURL in fanPageElements.xpath('//div[contains(@class, "tiled-gallery")]//a/img'):
                            art.append(posterURL.get('data-orig-file'))
                    except:
                        Log("No fansite images found")
                        pass
            except:
                pass
    
    if match is 1 and len(art) >= 10:
        Log("Artwork found: " + str(len(art)))
        # Return, first, last and randóm selection of images
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
    


    
    return metadata
