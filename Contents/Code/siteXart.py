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


    #Extra Posters
    import random
    art=[]
    match = 0
            
    for site in ["XartFan.com", "HQSluts.com", "XartBeauties.com/galleries"]:
        fanSite = PAextras.getFanArt(site, art, actors, actorName, metadata.title, match)
        match = fanSite[2]
        if match is 1:	
            break

 
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
