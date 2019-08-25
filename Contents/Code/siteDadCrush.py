import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    sceneID = encodedTitle.split('%20', 1)[0]
    Log("SceneID: " + sceneID)
    try:
        sceneTitle = encodedTitle.split('%20', 1)[1].replace('%20',' ')
    except:
        sceneTitle = ''
    url = PAsearchSites.getSearchSearchURL(siteNum) + sceneID + "/1/1"
    searchResult = HTML.ElementFromURL(url)
    titleNoFormatting = searchResult.xpath('//div[@class="container form-player"]/div[1]/div')[0].text_content().strip()
    curID = url.replace('/','_').replace('?','!')
    subSite = "DadCrush"
    if searchDate:
        releaseDate = parse(searchDate).strftime('%Y-%m-%d')
    else:
        releaseDate = ''
    if sceneTitle:
        score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
    else:
        score = 90
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
    metadata.title = detailsPageElements.xpath('//div[@class="container form-player"]/div[1]/div')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="container form-player"]/div[2]/p')[0].text_content().strip()

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
    actors = []
    actorList = detailsPageElements.xpath('//link[@rel="canonical"]')[0].get('href')
    Log('actorList:' + actorList)
    actorList = actorList.split("/")[-1].replace('-',' ').strip()
    Log('actorList:' + actorList)
    if 'and' in actorList:
        actors = actorList.split('and')
    else:
        actors.append(actorList)
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.replace('2','').strip())
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###
    
    # Girls page image
    girlsPageElements = HTML.ElementFromURL('https://www.dadcrush.com/girls')
    try:
        art.append(girlsPageElements.xpath('//a[contains(@href,"'+sceneID+'")]//img')[0].get('data-src'))
    except:
        pass

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//video[@id="main-movie-player"]')[0].get('poster')
        art.append(twitterBG)
    except:
        pass
    
    # Sometimes hi.jpg is just a bigger version of med.jpg, sometimes it's a different image entirely; grabbing both to be safe
    try:
        twitterBG = detailsPageElements.xpath('//video[@id="main-movie-player"]')[0].get('poster').replace('med.jpg','hi.jpg')
        art.append(twitterBG)
    except:
        pass

    # Scenes page images
    scenesPageElements = HTML.ElementFromURL('https://www.dadcrush.com/scenes')
    posters = scenesPageElements.xpath('//a[@id="'+sceneID+'"]/img[contains(@class,"bio")]')
    for poster in posters:
        try:
            art.append(poster.get('src'))
        except:
            pass


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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                j = j + 1
            except:
                pass

    return metadata