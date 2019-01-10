import PAsearchSites
import PAgenres

def posterAlreadyExists(posterUrl,metadata):
    for p in metadata.posters.keys():
        Log(p.lower())
        if p.lower() == posterUrl.lower():
            Log("Found " + posterUrl + " in posters collection")
            return True

    for p in metadata.art.keys():
        if p.lower() == posterUrl.lower():
            return True
    return False

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(searchSiteID) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="update animation-element bounce-up"]'):
        if searchSiteID != 9999:
            siteNum = searchSiteID
        titleNoFormatting = searchResult.xpath('.//a[@class="title"]')[0].text_content().strip()
        Log("Result Title: " + titleNoFormatting)
        curID = PAsearchSites.getSearchSearchURL(searchSiteID) + titleNoFormatting.lower().replace(' ','+')
        curID = curID.replace('/','_').replace('?','!')
        Log("ID: " + curID)
        releaseDate = parse(searchResult.xpath('.//div[@class="info-column video-data"]/span[last()]')[0].text_content().strip()).strftime('%Y-%m-%d')
        lowerResultTitle = str(titleNoFormatting).lower()
        if searchDate:
            searchDateCompare = datetime.strptime(searchDate, '%Y-%m-%d').strftime('%B %d, %y')
            score = 102 - Util.LevenshteinDistance(searchDateCompare.lower(), releaseDate.lower())
        else:
            score = 102 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        titleNoFormatting = titleNoFormatting + " [FPN/" + PAsearchSites.getSearchSiteName(searchSiteID) + "] " + releaseDate
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
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
    if siteID == 343:
        movieGenres.addGenre("Anal")

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//span[@class="update_models"]/a')
    if len(actors) > 0:
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

    # Posters
    art.append(detailsPageElements.xpath('//img[contains(@class,"videos-preload")]')[0].get('src0_2x'))

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not posterAlreadyExists(posterUrl,metadata):            
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