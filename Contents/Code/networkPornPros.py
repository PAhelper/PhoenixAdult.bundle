import PAsearchSites
import PAgenres
import PAactors
import PAextras
from lxml.html.soupparser import fromstring

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.lower().replace(" ","-").replace("'","-")
    try:
        searchResults = HTML.ElementFromURL(url)
    except:
        response = urllib.urlopen(url)
        htmlstring = response.read()
        searchResults = fromstring(htmlstring)

    searchResult = searchResults.xpath('//div[@class="details col-sm-6 col-md-3 order-md-2 mb-2"]')[0]
    titleNoFormatting = searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//h1')[0].text_content()
    curID = searchTitle.lower().replace(" ","-").replace("'","-")
    releaseDate = parse(searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//p')[0].text_content().strip()).strftime('%Y-%m-%d')

    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0]

    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    Log('scene url: ' + url)
    try:
        detailsPageElements = HTML.ElementFromURL(url)
    except:
        response = urllib.urlopen(url)
        htmlstring = response.read()
        detailsPageElements = fromstring(htmlstring)

    metadata.studio = "Porn Pros"

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)
    
    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//meta[@name="description"]')[0].get('content').strip()
    except:
        pass

    try:
        if siteName.lower() == "Cum4K".lower():
        
            summaryurl = "https://cum4k.tube/" + temp
            Log(summaryurl)
            summaryPageElements = HTML.ElementFromURL(summaryurl)
            metadata.summary = summaryPageElements.xpath('//p[@class="more"]/text()')[0].strip()
    except:
        Log("did not pull tube summary")
        pass

    # Actors
    movieActors.clearActors()
    titleActors = ""
    actors = detailsPageElements.xpath('//div[@class="details col-sm-6 col-md-3 order-md-2 mb-2"]//div[@class="row"]//div[@class="col-6 col-md-12"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPhotoURL = PAactors.actorDBfinder(actorName)
            titleActors = titleActors + actorName + " & "
            Log("actorPhoto: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)
        titleActors = titleActors[:-3]

    # Manually Add Actors
    # Add Actor Based on Title
    if "Poke Her In The Front" == metadata.title:
        actorName = "Sara Luv"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
        actorName = "Dillion Harper"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)



    # Genres
    movieGenres.clearGenres()
        # Based on site
    if siteName.lower() == "Lubed".lower():
        for genreName in ['Lube', 'Raw', 'Wet']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "Holed".lower():
        for genreName in ['Anal', 'Ass']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "POVD".lower():
        for genreName in ['Gonzo', 'POV']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "MassageCreep".lower():
        for genreName in ['Massage', 'Oil']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "DeepThroatLove".lower():
        for genreName in ['Blowjob', 'Deep Throat']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "PureMature".lower():
        for genreName in ['MILF', 'Mature']:
            movieGenres.addGenre(genreName)
    elif siteName.lower() == "Cum4K".lower():
        for genreName in ['Creampie']:
            movieGenres.addGenre(genreName)
    # Based on number of actors
    if len(actors) == 3:
        movieGenres.addGenre('Threesome')
    if len(actors) == 4:
        movieGenres.addGenre('Foursome')
    if len(actors) > 4:
        movieGenres.addGenre('Orgy')

    # Posters
    try:
        background = "http:" + detailsPageElements.xpath('//video[@id="player"]')[0].get('poster')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    # Date
    date = detailsPageElements.xpath('//div[contains(@class,"details")]//p')[0].text_content().strip()
    Log('Date: ' + date)
    date_object = datetime.strptime(date, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class,"details")]//h1')[0].text_content().strip()
	
    #Extra Posters
    import random
    art = []
    match = 0
    
    if siteName.lower() == "Holed".lower():
        fanSite = PAextras.getFanArt("AnalPornFan.com", art, actors, actorName, metadata.title, match)
    elif siteName.lower() == "SpyFam".lower():
        fanSite = PAextras.getFanArt("SpyFams.com", art, actors, actorName, metadata.title, match)
    elif siteName.lower() == "Lubed".lower():
        fanSite = PAextras.getFanArt("LubedFan.com", art, actors, actorName, metadata.title, match)
    elif siteName.lower() == "PassionHD".lower():
        for site in ["PassionHDFan.com", "HQSluts.com"]:
            fanSite = PAextras.getFanArt(site, art, actors, actorName, metadata.title, match)
            match = fanSite[2]
    else: 
        fanSite = PAextras.getFanArt("HQSluts.com", art, actors, actorName, metadata.title, match)
    
    summary = fanSite[1]
    match = fanSite[2]

    try:
        if len(summary) > 0:
            metadata.summary = summary 
    except:
        metadata.summary = summary
    
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
