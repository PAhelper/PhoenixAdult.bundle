import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchString = searchTitle.lower().replace(" ","-")
    Log("searchString: " + searchString)
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchString
    searchResult = HTML.ElementFromURL(url)
    titleNoFormatting = searchResult.xpath('//p[@class="video-title hidden-xs"]')[0].text_content().strip()
    curID = url.replace('/','_').replace('?','!')
    subSite = "DadCrush"
    if searchDate:
        releaseDate = parse(searchDate).strftime('%Y-%m-%d')
    else:
        releaseDate = ''
    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " [TeamSkeet/"+subSite+"] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    sceneID = url.split("/")[3]
    Log("sceneID: "+str(sceneID))
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'TeamSkeet'

    # Title
    metadata.title = detailsPageElements.xpath('//p[@class="video-title hidden-xs"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="scene-story"]/p')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.addGenre("Step Dad")
    movieGenres.addGenre("Step Daughter")

    # Release Date
    date = str(metadata.id).split("|")[2]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
        Log("Date from file")

    # Actors
    # Pull actors from URL
    actors = detailsPageElements.xpath('//p[@class="model-name hidden-xs"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//img[@class="img-responsive"]')[0].get("src")
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###
    
    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//div[@class="embed-responsive embed-responsive-16by9"]/stream')[0].get('poster')
        art.append(twitterBG)
    except:
        pass

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
                metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                j = j + 1

    return metadata