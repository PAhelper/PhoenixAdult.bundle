import PAsearchSites
import PAgenres
import PAextras
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    sceneID = encodedTitle.split('%20', 1)[0]
    Log("SceneID: " + sceneID)
    try:
        sceneTitle = encodedTitle.split('%20', 1)[1].replace('%20', ' ')
    except:
        sceneTitle = ''
    Log("Scene Title: " + sceneTitle)
    Log("Try Default URL")
    url = PAsearchSites.getSearchSearchURL(siteNum) + sceneID
    searchResult = HTML.ElementFromURL(url)
    if len(searchResult.xpath('//div[@class="red_big"]/text()')) == 0:
        Log("Try Alternate URL")
        url = PAsearchSites.getSearchBaseURL(siteNum) + "/" + sceneID + '/banner/1'
        searchResult = HTML.ElementFromURL(url)
    titleNoFormatting = searchResult.xpath('//div[@class="red_big"]/text()')[0].strip()
    curID = url.replace('/','_').replace('?','!')
    if searchDate:
        releaseDate = parse(searchDate).strftime('%Y-%m-%d')
    else:
        releaseDate = ''
    if sceneTitle:
        score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
    else:
        score = 90
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] ", score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    art =[]
    Log('******UPDATE CALLED*******')
    detailsPageElements = HTML.ElementFromURL(str(metadata.id).split("|")[0].replace('_', '/').replace('!','?'))
    try:
        Log("urlName: " + detailsPageElements.xpath('//video[@id="main-movie-player"]')[0].get("poster").split('/')[5])
        urlName = detailsPageElements.xpath('//video[@id="main-movie-player"]')[0].get("poster").split('/')[5]
    except:
        Log("urlName: " + detailsPageElements.xpath('//video[@id="preview"]')[0].get("poster").split('/')[5])
        urlName = detailsPageElements.xpath('//video[@id="preview"]')[0].get("poster").split('/')[5]

    # Studio
    metadata.studio = "TeamSkeet"

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="red_big"]/text()')[0].strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('(//div[@class="vid-desc-mobile"]/span)[not(position()=1)][not(position()=last())]')[0].text_content()

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Date
    date = str(metadata.id).split("|")[2]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
        Log("Date from file")

    # Genres
    movieGenres.addGenre("Step Sister")

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
        art.append("http:" + detailsPageElements.xpath('//video[@id="main-movie-player"]')[0].get("poster"))
    except:
        pass

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
    
    fanSite = PAextras.getFanArt("TeamSkeetFans.com", art, actors, actorName, metadata.title, 0)
    summary = fanSite[1]
    match = fanSite[2]

    if len(metadata.summary) < len(summary):
        metadata.summary = summary.strip()   
                    
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
