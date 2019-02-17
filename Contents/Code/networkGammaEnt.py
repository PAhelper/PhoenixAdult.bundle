import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    if siteNum == 278 or (siteNum >= 285 and siteNum <= 287):
        network = 'XEmpire'
    elif siteNum == 329 or (siteNum >= 351 and siteNum <= 354):
        network = 'Blowpass'
    elif siteNum == 331 or (siteNum >= 355 and siteNum <= 360):
        network = 'Fantasy Massage'
    elif siteNum == 330 or siteNum == 332 or (siteNum >= 361 and siteNum <= 364):
        network = 'Mile High Network'
    elif (siteNum >= 365 and siteNum <= 372) or siteNum == 466:
        network = '21Sextury'
    elif siteNum == 183 or (siteNum >= 373 and siteNum <= 374):
        network = '21Naturals'
    elif siteNum == 53 or (siteNum >= 375 and siteNum <= 379):
        network = 'Girlsway'
    elif siteNum >= 383 and siteNum <= 386:
        network = 'Fame Digital'
    elif siteNum >= 387 and siteNum <= 392:
        network = 'Open Life Network'
    elif siteNum == 281:
        network = 'Pure Taboo'
    elif siteNum == 380:
        network = 'Girlfriends Films'
    elif siteNum == 381:
        network = 'Burning Angel'
    elif siteNum == 277:
        network = 'Evil Angel'
    elif siteNum == 382:
        network = 'Pretty Dirty'
    elif siteNum >= 460 and siteNum <= 466:
        network = '21Sextreme'

    if network == PAsearchSites.getSearchSiteName(siteNum):
        network = ''
    else:
        network = network + "/"

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    Log(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    Log("Results Found: "+str(len(searchResults.xpath('//div[@class="tlcDetails"]'))))
    for searchResult in searchResults.xpath('//div[@class="tlcDetails"]'):
        titleNoFormatting = searchResult.xpath('.//a[1]')[0].text_content().strip()
        curID = searchResult.xpath('.//a[1]')[0].get('href').replace('/','_').replace('?','!')
        try:
            releaseDate = parse(searchResult.xpath('.//div[@class="tlcSpecs"]/span[@class="tlcSpecsDate"]/span[@class="tlcDetailsValue"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        except:
            try:
                detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a[1]')[0].get('href'))
                releaseDate = parse(detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            except:
                releaseDate = ''
        if searchDate and releaseDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+network+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))

    try:
        dvdResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "/dvd")
        for dvdResult in dvdResults.xpath('//div[contains(@class,"tlcItem playlistable_dvds")] | //div[@class="tlcDetails"]'):
            titleNoFormatting = dvdResult.xpath('.//a | .//div[@class="tlcTitle"]/a')[0].get('title').strip()
            curID = dvdResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
            try:
                releaseDate = parse(dvdResult.xpath('.//div[@class="tlcSpecs"]/span[@class="tlcSpecsDate"]/span[@class="tlcDetailsValue"]')[0].text_content().strip())
            except:
                try:
                    detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + dvdResult.xpath('.//a[1]')[0].get('href'))
                    releaseDate = parse(detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().strip())
                except:
                    releaseDate = ''
            
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ("+releaseDate.strftime('%Y')+") - Full Movie ["+PAsearchSites.getSearchSiteName(siteNum)+"]", score = score, lang = lang))
    except:
        pass
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.directors.clear()
    director = metadata.directors.new()
    
    if siteID == 278 or (siteID >= 285 and siteID <= 287):
        metadata.studio = 'XEmpire'
        director.name = 'Mason'
    elif siteID == 329 or (siteID >= 351 and siteID <= 354):
        metadata.studio = 'Blowpass'
    elif siteID == 331 or (siteID >= 355 and siteID <= 360):
        metadata.studio = 'Fantasy Massage'
    elif siteID == 330 or siteID == 332 or (siteID >= 361 and siteID <= 364):
        metadata.studio = 'Mile High Network'
    elif (siteID >= 365 and siteID <= 372) or siteID == 466:
        metadata.studio = '21Sextury'
    elif siteID == 183 or (siteID >= 373 and siteID <= 374):
        metadata.studio = '21Naturals'
    elif siteID == 53 or (siteID >= 375 and siteID <= 379):
        metadata.studio = 'Girlsway'
        director.name = 'Stills by Alan'
    elif siteID >= 383 and siteID <= 386:
        metadata.studio = 'Fame Digital'
    elif siteID >= 387 and siteID <= 392:
        metadata.studio = 'Open Life Network'
    elif siteID == 281:
        metadata.studio = 'Pure Taboo'
    elif siteID == 380:
        metadata.studio = 'Girlfriends Films'
    elif siteID == 381:
        metadata.studio = 'Burning Angel'
    elif siteID == 277:
        metadata.studio = 'Evil Angel'
    elif siteID == 382:
        metadata.studio = 'Pretty Dirty'
    elif siteID >= 460 and siteID <= 466:
        metadata.studio = '21Sextreme'
    temp = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    url = (PAsearchSites.getSearchBaseURL(siteID) + temp).replace("https:","http:")
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Summary
    try:
        paragraph = detailsPageElements.xpath('//meta[@name="twitter:description"]')[0].get('content').strip()
    except:
        try:
            paragraph = detailsPageElements.xpath('//div[@class="sceneDesc bioToRight showMore"]')[0].text_content().strip()
            paragraph = paragraph[20:]
        except:
            try:
                paragraph = detailsPageElements.xpath('//div[@class="sceneDescText"]')[0].text_content().strip()
            except:
                try:
                    paragraph = detailsPageElements.xpath('//p[@class="descriptionText"]')[0].text_content().strip()
                except:
                    paragraph = ''
    metadata.summary = paragraph.strip()
    metadata.collections.clear()

    # Tagline
    try:
        tagline = detailsPageElements.xpath('//div[@class="studioLink"]')[0].text_content().strip()
    except:
        tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Title
    try:
        dvdTitle = detailsPageElements.xpath('//a[contains(@class,"dvdLink")][1]')[0].get('title').strip()
        metadata.collections.add(dvdTitle.replace('#0','').replace('#',''))
    except:
        dvdTitle = 'This is some damn nonsense that should never match the scene title'

    try:
        title = detailsPageElements.xpath('//meta[@name="twitter:title"]')[0].get('content').strip()
    except:
        try:
            title = detailsPageElements.xpath('//h1 | //h3[@class="dvdTitle"]')[0].text_content().strip()
        except:
            try:
                dataLayer = detailsPageElements.xpath('//script[contains(text(),"dataLayer")]')[0].text_content()
                alpha = dataLayer.find('"sceneTitle"')+14
                omega = dataLayer.find('"',alpha)
                title = dataLayer[alpha:omega]
            except:
                title = "I couldn't find the title, please report this on github: https://github.com/PAhelper/PhoenixAdult.bundle/issues"

    if dvdTitle == title:
        pageTitle = detailsPageElements.xpath('//title')[0].text_content().strip()
        alpha = pageTitle.find('Scene')+6
        omega = pageTitle.find(' ',alpha)
        title = (title + " - Scene " + pageTitle[alpha:omega].strip()).replace('#0','').replace('#','')

    metadata.title = title

    # Director
    try:
        directors = detailsPageElements.xpath('//div[@class="sceneCol sceneColDirectors"]//a | //ul[@class="directedBy"]/li/a')
        Log("Directors found: "+str(len(directors)))
        for dirname in directors:
            Log("Director: "+str(dirname.text_content().strip()))
            #metadata.directors.add(director.text_content().strip())
            director.name = dirname.text_content().strip()
    except:
        pass

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="sceneCol sceneColCategories"]//a | //div[@class="sceneCategories"]//a | //p[@class="dvdCol"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Release Date
    try:
        date = detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().strip()
    except:
        date = detailsPageElements.xpath('//*[@class="updatedOn"]')[0].text_content().strip()
        date = date[8:].strip()

    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="sceneCol sceneColActors"]//a | //div[@class="sceneCol sceneActors"]//a | //div[@class="pornstarNameBox"]/a[@class="pornstarName"] | //div[@id="slick_DVDInfoActorCarousel"]//a')
    if metadata.title == 'Kennedy Leigh' and metadata.tagline == 'Only Teen Blowjobs':
        movieActors.addActor('Kennedy Leigh','')

    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL((PAsearchSites.getSearchBaseURL(siteID)+actorPageURL).replace("https:","http:"))
            actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"] | //span[@class="removeAvatarParent"]/img')[0].get("src").replace("https:","http:")
            movieActors.addActor(actorName,actorPhotoURL)

    #Posters

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//meta[@name="twitter:image"]')[0].get('content').replace("https:","http:")
        art.append(twitterBG)
    except:
        pass

    try:
        picScript = detailsPageElements.xpath('//script[contains(text(),"picPreview")]')[0].text_content()
        alpha = picScript.find('"picPreview":"')+14
        omega = picScript.find('"',alpha)
        Log('BG in <script>: '+picScript[alpha:omega].replace('\\',''))
        art.append(picScript[alpha:omega].replace('\\','').replace("https:","http:"))
    except:
        pass

    try:
        sceneImg = detailsPageElements.xpath('//img[@class="sceneImage"]')[0].get('src').replace("https:","http:")
        art.append(sceneImg)
    except:
        pass
    
    # Scene photos page
    try:
        photoPageUrl = PAsearchSites.getSearchBaseURL(siteID)+detailsPageElements.xpath('//a[@class="controlButton GA_Track GA_Track_Action_Pictures GA_Track_Category_Player GA GA_Click GA_Id_ScenePlayer_Pictures"]')[0].get('href').replace("https:","http:")
        photoPage = HTML.ElementFromURL(photoPageUrl)
        unlockedPhotos = photoPage.xpath('//a[@class="imgLink"] | //a[@class="imgLink pgUnlocked"]')
        for unlockedPhoto in unlockedPhotos:
            art.append(unlockedPhoto.get('href').replace("https:","http:"))
    except:
        photoPageUrl = url

    # DVD Covers
    if "/movie/" in url:
        try:
            dvdFrontCover = detailsPageElements.xpath('//a[@class="frontCoverImg"]')[0].get('href').replace("https:","http:")
            art.append(dvdFrontCover)

            dvdBackCover = detailsPageElements.xpath('//a[@class="backCoverImg"]')[0].get('href').replace("https:","http:")
            art.append(dvdBackCover)
        except:
            pass

        # DVD scene images
        try:
            sceneImgs = detailsPageElements.xpath('//img[@class="tlcImageItem img"]')
            for sceneImg in sceneImgs:
                art.append(sceneImg.get('src').replace("https:","http:"))
        except:
            pass
        
        try:
            sceneImgs = detailsPageElements.xpath('//img[@class="img lazy"]')
            for sceneImg in sceneImgs:
                art.append(sceneImg.get('data-original').replace("https:","http:"))
        except:
            pass
    j = 1
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
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': photoPageUrl}).content, sort_order = j)
                if(width > 100):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': photoPageUrl}).content, sort_order = j)
                j = j + 1
            except Exception as e:
                Log("Error: " + str(e))

    return metadata