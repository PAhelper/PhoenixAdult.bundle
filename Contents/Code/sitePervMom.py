import PAsearchSites
import PAgenres
import PAextras
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    Log("searchTitle.replace: " + searchTitle.replace(' ','-'))
    searchResult = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.replace(' ','-'))
    
    titleNoFormatting = searchResult.xpath('//span[@class="p-small red"]')[0].text_content().strip()
    curID = searchResult.xpath('//link[@rel="canonical"]')[0].get('href').replace('/','_').replace('?','!')
    releaseDate = parse(searchResult.xpath('//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    art =[]
    Log('******UPDATE CALLED*******')   
    detailsPageElements = HTML.ElementFromURL(str(metadata.id).split("|")[0].replace('_', '/'))

    # Summary
    metadata.studio = "TeamSkeet"
    metadata.summary = detailsPageElements.xpath('//div[@class="trailer-content story"]')[0].text_content().strip()
    metadata.title = detailsPageElements.xpath('//span[@class="p-small red"]')[0].text_content().strip()

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="date"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//span[@class="p-small"]')[0].text_content().replace('Starring:','').strip().split(" and ")
    if len(actors) > 0:
        for actor in actors:
            actorName = actor
            posterUrl = detailsPageElements.xpath('//video[@id="preview"]')[0].get("poster")
            actorPhotoURL = posterUrl.replace('trailer_tour',posterUrl.split('/')[8])
            Log("actorPhoto: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    try:
        art.append(detailsPageElements.xpath('//video[@id="preview"]')[0].get("poster"))
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
