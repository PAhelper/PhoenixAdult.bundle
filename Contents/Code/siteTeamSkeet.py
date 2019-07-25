import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="info"]'):
        try:
            sceneURL = searchResult.xpath('.//a')[0].get("href").split("?")[0]
            if 'http' not in sceneURL:
                sceneURL = 'https' + str(sceneURL)
            scenePage = HTML.ElementFromURL(sceneURL)
            titleNoFormatting = scenePage.xpath('//title')[0].text_content().split(" | ")[1]
            curID = sceneURL.replace('/','+')
            releaseDate = parse(scenePage.xpath('//div[@style="width:430px;text-align:left;margin:8px;border-right:3px dotted #bbbbbb;position:relative;"]//div[@class="gray"]')[0].text_content()[12:]).strftime('%Y-%m-%d')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [TeamSkeet/" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
        except:
            pass

    if searchTitle == "Eavesdropping And Pussy Popping":
        Log("Manual Search Match")
        curID = ("https://www.teamskeet.com/t1/trailer/view/55019").replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Eavesdropping And Pussy Popping" + " [TeamSkeet/TeenPies] " + "2019-02-27", score = 101, lang = lang))
    if searchTitle == "Zoe's Fantasy":
        Log("Manual Search Match")
        curID = ("https://www.teamskeet.com/t1/trailer/view/47562").replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Zoe's Fantasy" + " [TeamSkeet/She's New] " + "2016-06-12", score = 101, lang = lang))
    if searchTitle == "She Has Her Ways":
        Log("Manual Search Match")
        curID = ("https://www.teamskeet.com/t1/trailer/view/43061").replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "She Has Her Ways" + " [TeamSkeet/TeamSkeet Extras] " + "2014-08-28", score = 101, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    url = str(metadata.id).split("|")[0].replace('+','/')
    detailsPageElements = HTML.ElementFromURL(url)
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = "TeamSkeet"

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().split(" | ")[1]

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="gray"]')[1].text_content().replace('ï¿½', '')

    # Release Date
    releaseDate = detailsPageElements.xpath('//div[@style="width:430px;text-align:left;margin:8px;border-right:3px dotted #bbbbbb;position:relative;"]//div[@class="gray"]')[0].text_content()[12:].replace("th,",",").replace("st,",",").replace("nd,",",").replace("rd,",",")
    date_object = datetime.strptime(releaseDate, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    #Tagline and Collection(s)
    tagline = detailsPageElements.xpath('//div[@style="white-space:nowrap;"]')[0].text_content()[6:].strip()
    endofsubsite = tagline.find('.com')
    tagline = tagline[:endofsubsite].strip()
    metadata.tagline = tagline
    metadata.collections.add(metadata.tagline)

    # Genres
    genres = detailsPageElements.xpath('//a[contains(@href,"?tags=")]')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    try:
        actortext = detailsPageElements.xpath('//title')[0].text_content().split('|')[0].strip()
        actors = actortext.split(' and ')
        if len(actors) > 0:
            for actorLink in actors:
                actorName = actorLink
                actorPhotoURL = ''
                movieActors.addActor(actorName, actorPhotoURL)
    except:
        pass

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//video')[0].get("poster")
        metadata.art[twitterBG] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    except:
        pass
    
    #Extra Posters
    import random
    art = []
    match = 0
    siteName = PAsearchSites.getSearchSiteName(siteID)

    
    for site in ["SkeetScenes.com", "TeamSkeetFan.com"]:
        try:
            match = fanSite[2]
        except:
            pass
        if match is 1:	
            break
        fanSite = PAextras.getFanArt(site, art, actors, actorName, metadata.title, match, siteName)

        
    try:
        match = fanSite[2]
    except:
        pass
    
    if match is 1:
        # Return, first, last and randóm selection of images
        # If you want more or less posters edít the value in random.sample below or refresh metadata to get a different sample.	
        sample = [art[0], art[1], art[2], art[3], art[-1]] + random.sample(art, 4)     
        art = sample
        Log("Selecting first 5, last and random 4 images from set")

        j = 1
											  
        for posterUrl in art:
            Log("Trying next Image")
            if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
                try:
                    hdr = {
                            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                    }
                    req = urllib.Request(posterUrl, headers=hdr)
                    img_file = urllib.urlopen(req)
                    im = StringIO(img_file.read())
                    resized_image = Image.open(im)
                    width, height = resized_image.size
                    #Add the image proxy items to the collection
                    if width > 1 or height > width:
                        # Item is a poster
                        metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers=hdr).content, sort_order = j)
                    if width > 100 and width > height:
                        # Item is an art item
                        metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers=hdr).content, sort_order = j)
                    j = j + 1
                except:
                    Log("there was an issue")
    else:
    
        posterPageElements = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteID) + metadata.title.replace(" ", "_"))
        posterLink = posterPageElements.xpath('//img[contains(@src, "shared/scenes/new/")]')[0].get('src').split("0")[0]
        posterNum = 1
        for poster in ["01.jpg", "02.jpg", "03.jpg", "04.jpg", "05.jpg"]:
            posterURL = posterLink + poster
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL).content, sort_order = posterNum)
            posterNum += 1

    return metadata
