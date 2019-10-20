import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="update animation-element bounce-up"]'):
        titleNoFormatting = searchResult.xpath('.//a[@class="title"]')[0].text_content().strip()
        Log("Result Title: " + titleNoFormatting)
        curID = PAsearchSites.getSearchSearchURL(siteNum) + titleNoFormatting.lower().replace(' ','+')
        curID = curID.replace('!','').replace('/','_').replace('?','!')
        Log("ID: " + curID)
        releaseDate = parse(searchResult.xpath('.//div[@class="info-column video-data"]/span[last()]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [FPN/" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Summary
    metadata.studio = "Full Porn Network"
    metadata.summary  = detailsPageElements.xpath('//a[@class="title"]')[0].get('title').strip()
    metadata.title = detailsPageElements.xpath('//a[@class="title"]')[0].text_content().strip()
    date_object = parse(detailsPageElements.xpath('.//div[@class="info-column video-data"]/span[last()]')[0].text_content().strip())
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year    
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.clear()
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    # No Source for Genres, add manual

    movieGenres.addGenre("Hardcore")
    if tagline == "Analized":
        movieGenres.addGenre("Anal")
    if tagline == "Only Prince":
        movieGenres.addGenre("Interracial")
    if "Daddy" in tagline:
        movieGenres.addGenre("Incest")

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//span[@class="update_models"]/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + "/models/models.html"
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = ""
            while actorPhotoURL == "":
                try:
                    Log("Looking for "+actorName+" in "+str(actorPageURL))
                    actorPhotoURL = actorPage.xpath('//h4[contains(text(),"'+actorName+'")]/preceding::img[1]')[0].get('src0_1x')
                except Exception as e:
                    Log("Error: " + str(e))
                    try:
                        actorPageURL = actorPage.xpath('//a[@class="pagenav"]')[0].get('href')
                        actorPage = HTML.ElementFromURL(actorPageURL)
                    except:
                        break
            Log("actorPhotoURL: " + str(actorPhotoURL))
            movieActors.addActor(actorName,actorPhotoURL)

    #Manually Add Actors Based on Scene Title
    if metadata.title == "Kate England Incites a Backroom Orgy in Las Vegas Sex Trip Part 2":
        movieActors.addActor('Marilyn Moore','')
        movieActors.addActor('Prince Yahshua','')

    # Posters
    art.append(detailsPageElements.xpath('//img[contains(@class,"videos-preload")]')[0].get('src0_2x'))

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                if(width > 100):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                j = j + 1
            except:
                pass

    return metadata