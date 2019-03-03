import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.lower().replace(" ","-").replace("'","-")
    searchResults = HTML.ElementFromURL(url)

    searchResult = searchResults.xpath('//div[@class="details col-sm-6 col-md-3 order-md-2 mb-2"]')[0]
    titleNoFormatting = searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//h1')[0].text_content()
    curID = searchTitle.lower().replace(" ","-").replace("'","-")
    releaseDate = parse(searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//p')[0].text_content().strip()).strftime('%Y-%m-%d')

    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0]
    art = []

    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    Log('scene url: ' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    metadata.studio = "Porn Pros"

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)
    
    # Summary
    try:
        if siteName.lower() == "Cum4K".lower():
        
            summaryurl = "https://cum4k.tube/" + temp
            Log(summaryurl)
            summaryPageElements = HTML.ElementFromURL(summaryurl)
            metadata.summary = summaryPageElements.xpath('//p[@class="more"]/text()')[0].strip()
    except:
        Log("Did not pull cum4k.tube summary")
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
    # Based on number of actors
    if len(actors) == 3:
        movieGenres.addGenre('Threesome')
    if len(actors) == 4:
        movieGenres.addGenre('Foursome')
    if len(actors) > 4:
        movieGenres.addGenre('Orgy')

    # Posters
    background = "http:" + detailsPageElements.xpath('//video[@id="player"]')[0].get('poster')
    Log("BG DL: " + background)
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

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
    from googlesearch import search
	
    # Check first X google results. Set Stop = X to search more
    urls = search('"' + siteName + 'fan" ' + actorName + ' ' + metadata.title , stop=2)
    if siteName.lower() == "Holed".lower():
        urls = search('"AnalPornfan "' + actorName + ' ' + metadata.title , stop=2)
    elif siteName.lower() == "SpyFam".lower():
        urls = search('site:SpyFams.com ' + actorName + ' ' + metadata.title , stop=2)

    match = 0
    for url in urls:
        if match is 0:
            googleSearchURL = url
            fanPageElements = HTML.ElementFromURL(googleSearchURL)

            try:
                try:
                    if siteName.lower() == "Holed".lower():
                        nameinheader = fanPageElements.xpath('//div[@class="page-title pad group"]//a[2]')[0].text_content()
                    elif siteName.lower() == "SpyFam".lower():
                        nameinheader = fanPageElements.xpath('(//span[@itemprop="articleSection"])')[0].text_content()
                    else:
                        nameinheader = fanPageElements.xpath('//div[@class="page-title pad group"]//a')[0].text_content()
                    Log("Actress name in header: " + nameinheader)
                except:
                    pass
                    
                if actorName in nameinheader:
                    Log(siteName + " Fansite Match Found")
                    match = 1
                else:
                    # When there are multiple actors listed we need to check all of them.
                    try:
                        for actorLink in actors:
                            actorName = actorLink.text_content()
                            for name in nameinheader:
                                if actorName.lower() == name.lower():
                                    Log(siteName + " Fansite Match Found")
                                    match = 1
                    except:
                        pass
                        
                if match is 1:
                    # Summary
                    if siteName.lower() == "SpyFam".lower():
                        paragraphs = fanPageElements.xpath('(//div[@class="entry-content g1-typography-xl"]//p)[not(*[contains(@class, "jp-relatedposts-post")])]')
                        if len(paragraphs) > 3:
                            pNum = 1
                            summary = ""
                            for paragraph in paragraphs:
                                if pNum >= 1 and pNum <= 7:
                                    summary = summary + '\n\n' + paragraph.text_content()
                                pNum += 1
                            metadata.summary = summary.strip()
                        else:
                            metadata.summary = fanPageElements.xpath('(//div[@class="entry-content g1-typography-xl"]//p)[position()=1]')[0].text_content().strip()
                    else:
                        metadata.summary = fanPageElements.xpath('//div[@class="entry-inner"]//p')[0].text_content().replace("---->Click Here to Download<----", '').strip()
                    
                     
                # Various Poster xpaths needed for different sites
                try:
                    if siteName.lower() == "Lubed".lower():
                        Log("Searching LubedFan")
                        for posterURL in fanPageElements.xpath('(//div[@class="entry-inner"]//a)[position()>1][position()<last()]'):
                            art.append(posterURL.get('href'))
                    elif siteName.lower() == "Holed".lower():
                        Log("Searching AnalPornFan")
                        for posterURL in fanPageElements.xpath('//div[contains(@class, "rgg-imagegrid")]//a'):
                            art.append(posterURL.get('href'))
                    else:
                        # Works for PassionHD and SpyFam
                        Log("Searching Fan site")
                        for posterURL in fanPageElements.xpath('//div[contains(@class, "tiled-gallery")]//a/img'):
                            art.append(posterURL.get('data-orig-file'))
                except:
                    pass
            except:
                Log("No Actress found in the site header")
                pass
    
    if match is 1:
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




