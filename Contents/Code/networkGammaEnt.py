import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):

    networkscene = True
    networkscenepages = True
    networkdvd = True
    directmatch = False
    network_sep_scene_prev = ""
    network_sep_scene = ""
    network_sep_scene_pages_prev = ""
    network_sep_scene_pages = "/"
    network_sep_scene_pages_next = ""
    network_sep_dvd_prev = ""
    network_sep_dvd = "/1/dvd"

    if searchSiteID != 9999:
        siteNum = searchSiteID
    if siteNum == 278 or (siteNum >= 285 and siteNum <= 287):
        network = 'XEmpire'
        network_sep_scene_prev = "scene/"
        network_sep_scene_pages_prev = "scene/"
        network_sep_dvd_prev = "dvd/"
        network_sep_dvd = "/1"
    elif siteNum == 329 or (siteNum >= 351 and siteNum <= 354):
        network = 'Blowpass'
        networkdvd = False
    elif siteNum == 331 or (siteNum >= 355 and siteNum <= 360) or siteNum == 750:
        network = 'Fantasy Massage'
        networkdvd = False
        network_sep_scene = "/scene"
        network_sep_scene_pages = "/scene/"
    elif (siteNum >= 365 and siteNum <= 372) or siteNum == 466 or siteNum == 692:
        network = '21Sextury'
        networkdvd = False
    elif siteNum == 183 or (siteNum >= 373 and siteNum <= 374):
        network = '21Naturals'
        networkdvd = False
        network_sep_scene = "/scene"
        network_sep_scene_pages = "/scene/"
    elif siteNum == 53 or (siteNum >= 375 and siteNum <= 379):
        network = 'Girlsway'
        networkdvd = False
    elif siteNum >= 383 and siteNum <= 386:
        network = 'Fame Digital'
        if siteNum == 383:
            networkdvd = False
            network_sep_scene = "/scene"
            network_sep_scene_pages = "/scene/"
            network_sep_dvd = "/dvd"
        if siteNum == 386:
            networkscene = False
            networkscenepages = False
            networkdvd = False
    elif siteNum >= 387 and siteNum <= 392:
        network = 'Open Life Network'
        networkdvd = False
    elif siteNum == 281:
        network = 'Pure Taboo'
        networkdvd = False
        network_sep_scene = "/scene"
        network_sep_scene_pages = "/scene/"
    elif siteNum == 380:
        network = 'Girlfriends Films'
        network_sep_scene = "?query=&pscenes=0&tab=scenes"
        network_sep_scene_pages = "?query=&pscenes="
        network_sep_scene_pages_next = "&tab=scenes"
        network_sep_dvd = "&tab=movies"
    elif siteNum == 381:
        network = 'Burning Angel'
        networkdvd = False
        network_sep_scene = "/scene"
        network_sep_scene_pages = "/scene/"
    elif siteNum == 277:
        network = 'Evil Angel'
        networkscene = False
        networkscenepages = False
        networkdvd = False
        directmatch = True
        network_sep_scene = "/scene"
        network_sep_scene_pages = "/scene/"
        network_sep_dvd = "/dvd"
    elif siteNum == 382:
        network = 'Pretty Dirty'
        networkdvd = False
        network_sep_scene = "/scene"
        network_sep_scene_pages = "/scene/"
    elif siteNum >= 460 and siteNum <= 465:
        network = '21Sextreme'
        networkdvd = False
        network_sep_scene = "/scene"
        network_sep_scene_pages = "/scene/"

    if network == PAsearchSites.getSearchSiteName(siteNum):
        network = ''
    else:
        network = network + "/"

    if networkscene:
        # Result to check
        resultfirst = []
        # Result next page
        resultsecond = []

        #searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "?query=" + encodedTitle)
        encodedTitle = encodedTitle.replace("%27", "").replace("%3F", "").replace("%2C", "") #Remove troublesome punctuation (, . ?)
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + network_sep_scene_prev + encodedTitle + network_sep_scene)
        for searchResult in searchResults.xpath('//div[@class="tlcDetails"]'):
            titleNoFormatting = searchResult.xpath('.//a[1]')[0].text_content().strip()
            titleNoFormatting = titleNoFormatting.replace("BONUS-", "BONUS - ")
            titleNoFormatting = titleNoFormatting.replace("BTS-", "BTS - ")

            curID = searchResult.xpath('.//a[1]')[0].get('href').replace('/','_').replace('?','!')
            resultfirst.append(curID)

            try:
                actorLink = searchResult.xpath('.//div[@class="tlcActors"]/a')
                actor = ' - '
                if "BONUS" in titleNoFormatting or "BTS" in titleNoFormatting:
                    for actorText in actorLink:
                        actorName = str(actorText.text_content().strip())
                        if "Rocco Siffredi" not in actorName and "Peter North" not in actorName:
                            actor = actor + actorName + ", "
                else:
                    actor = actor + str(actorLink[0].text_content().strip())
                actor = actor.strip()
                actor = actor.strip(",")
                actor = " " + actor
            except:
                actor = ''

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

            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + actor + " ["+network+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))

        if networkscenepages:
            # Other pages
            i = 2
            while i < 3:
                pagenum = i
                if siteNum == 380:
                    pagenum = i - 1
                searchResultsSec = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + network_sep_scene_pages_prev + encodedTitle + network_sep_scene_pages + str(pagenum) + network_sep_scene_pages_next)
                i += 1
                searchResultSec = searchResultsSec.xpath('//div[@class="tlcDetails"]')
                if searchResultSec:
                    titleText = searchResultSec[0].xpath('.//a[1]')[0]
                    resultSEARCH = titleText.get('href').replace('/','_').replace('?','!')

                    for resultCheck in resultfirst:
                        if resultCheck == resultSEARCH:
                            i = 100
                            break

                    for searchResultSec in searchResultsSec.xpath('//div[@class="tlcDetails"]'):
                        titleText = searchResultSec.xpath('.//a[1]')[0]
                        titleNoFormatting = titleText.text_content().strip()
                        titleNoFormatting = titleNoFormatting.replace("BONUS-", "BONUS - ")
                        titleNoFormatting = titleNoFormatting.replace("BTS-", "BTS - ")

                        curID = titleText.get('href').replace('/','_').replace('?','!')
                        resultsecond.append(curID)

                        try:
                            actorLink = searchResultSec.xpath('.//div[@class="tlcActors"]/a')
                            actor = ' - '
                            if "BONUS" in titleNoFormatting or "BTS" in titleNoFormatting:
                                for actorText in actorLink:
                                    actorName = str(actorText.text_content().strip())
                                    if "Rocco Siffredi" not in actorName and "Peter North" not in actorName:
                                        actor = actor + actorName + ", "
                            else:
                                actor = actor + str(actorLink[0].text_content().strip())
                            actor = actor.strip()
                            actor = actor.strip(",")
                            actor = " " + actor
                        except:
                            actor = ''

                        try:
                            releaseDate = parse(searchResultSec.xpath('.//div[@class="tlcSpecs"]/span[@class="tlcSpecsDate"]/span[@class="tlcDetailsValue"]')[0].text_content().strip()).strftime('%Y-%m-%d')
                        except:
                            try:
                                detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + searchResultSec.xpath('.//a[1]')[0].get('href'))
                                releaseDate = parse(detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')
                            except:
                                releaseDate = ''

                        if searchDate and releaseDate:
                            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                        else:
                            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

                        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + actor + " ["+network+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))

                    resultfirst = resultsecond
                    resultsecond = []
                else:
                    i = 100

    if directmatch:
        # Result to check
        resultfirst = []
        searchString = encodedTitle.replace("%20", '-').lower()
        #searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "?query=" + encodedTitle)
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
        for searchResult in searchResults.xpath('//div[@id="infoWrapper"]'):
            titleNoFormatting = searchResult.xpath('.//h1[1]')[0].text_content().strip()
            titleNoFormatting = titleNoFormatting.replace("BONUS-", "BONUS - ")
            titleNoFormatting = titleNoFormatting.replace("BTS-", "BTS - ")

            curID = (PAsearchSites.getSearchSearchURL(siteNum) + searchString).replace('/', '_').replace('?', '!')
            resultfirst.append(curID)
            Log (curID + titleNoFormatting + "FOUND")

            # try:
            #     actorLink = searchResult.xpath('.//div[@class="tlcActors"]/a')
            #     actor = ' - '
            #     if "BONUS" in titleNoFormatting or "BTS" in titleNoFormatting:
            #         for actorText in actorLink:
            #             actorName = str(actorText.text_content().strip())
            #             if "Rocco Siffredi" not in actorName and "Peter North" not in actorName:
            #                 actor = actor + actorName + ", "
            #     else:
            #         actor = actor + str(actorLink[0].text_content().strip())
            #     actor = actor.strip()
            #     actor = actor.strip(",")
            #     actor = " " + actor
            # except:
            #     actor = ''

            try:
                releaseDate = (searchResult.xpath('//li[@class="updatedDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')
#            except:
#                try:
#                    detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a[1]')[0].get('href'))
#                    releaseDate = parse(detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            except:
                releaseDate = ''
            Log (releaseDate + "FOUND")
            if searchDate and releaseDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+network+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))


    if networkdvd:
        try:
            dvdResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + network_sep_dvd_prev + encodedTitle + network_sep_dvd)
            for dvdResult in dvdResults.xpath('//div[contains(@class,"tlcItem playlistable_dvds")] | //div[@class="tlcDetails"]'):
                titleNoFormatting = dvdResult.xpath('.//div[@class="tlcTitle"]/a')[0].get('title').strip()
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
    elif siteID == 331 or (siteID >= 355 and siteID <= 360) or siteID == 750:
        metadata.studio = 'Fantasy Massage'
    elif (siteID >= 365 and siteID <= 372) or siteID == 466 or siteID == 690:
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
    if siteID == 277:
        url = temp
    detailsPageElements = HTML.ElementFromURL(url)

    art = []

    # Summary
    try:
        paragraph = detailsPageElements.xpath('//meta[@name="twitter:description"]')[0].get('content').strip()
    except:
        paragraph = ""

    if paragraph == "":
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
    metadata.summary = paragraph.replace('</br>','\n').replace('<br>','\n').strip()
    metadata.collections.clear()

    # Tagline
    try:
        tagline = detailsPageElements.xpath('//div[@class="studioLink"]')[0].text_content().strip()
    except:
        tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Title DVD
    try:
        dvdTitle = detailsPageElements.xpath('//a[contains(@class,"dvdLink")][1]')[0].get('title').strip()
        metadata.collections.add(dvdTitle.replace('#0','').replace('#',''))
    except:
        try:
            dvdTitleScript = detailsPageElements.xpath('//script[contains(text(),"dvdName")]')[0].text_content()
            alpha = dvdTitleScript.find('"dvdName"')+11
            omega = dvdTitleScript.find('"',alpha)
            dvdTitle = dvdTitleScript[alpha:omega]
            if len(dvdTitle) > 0:
                metadata.collections.add(dvdTitle.replace('#0','').replace('#',''))
        except:
            try:
                dvdTitle = detailsPageElements.xpath('//h1[@class="sceneTitle"]')[0].text_content().strip()
                dvdTitle = dvdTitle.replace("BONUS-", "").replace("BONUS - ", "")
                dvdTitle = dvdTitle.replace("BONUS", "")
                dvdTitle = dvdTitle.replace("BTS-", "").replace("BTS - ", "")
                dvdTitle = dvdTitle.replace("BTS", "")
                metadata.collections.add(dvdTitle.replace('#0','').replace('#',''))
            except:
                dvdTitle = "This is some damn nonsense that should never match the scene title"



    # Director
    try:
        directors = detailsPageElements.xpath('//div[@class="sceneCol sceneColDirectors"]//a | //ul[@class="directedBy"]/li/a')
        Log("Directors found: "+str(len(directors)))
        if len(directors) > 0:
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
        date = detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().replace('|','').strip()
        if len(date) > 0:
            date_object = parse(date)
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
    except:
        try:
            date = detailsPageElements.xpath('//*[@class="updatedOn"]')[0].text_content().strip()
            date = date[8:].strip()
            if len(date) > 0:
                date_object = parse(date)
                metadata.originally_available_at = date_object
                metadata.year = metadata.originally_available_at.year
        except:
            try:
                datePublished = detailsPageElements.xpath('//script[contains(text(),"datePublished")]')[0].text_content()
                alpha = datePublished.find('"datePublished"')+17
                omega = datePublished.find('"',alpha)
                date = datePublished[alpha:omega]
                if len(date) > 0:
                    date_object = parse(date)
                    metadata.originally_available_at = date_object
                    metadata.year = metadata.originally_available_at.year
            except:
                pass

    # Actors
    movieActors.clearActors()

    Log("Initial try for actors")
    actors = detailsPageElements.xpath('//div[@class="sceneCol sceneColActors"]//a | //div[@class="sceneCol sceneActors"]//a | //div[@class="pornstarNameBox"]/a[@class="pornstarName"] | //div[@id="slick_DVDInfoActorCarousel"]//a | //div[@id="slick_sceneInfoPlayerActorCarousel"]//a')
    if metadata.title == 'Kennedy Leigh' and metadata.tagline == 'Only Teen Blowjobs':
        movieActors.addActor('Kennedy Leigh','https://imgs1cdn.adultempire.com/actors/649607h.jpg')

    Log("actors found: " + str(len(actors)))
    if len(actors) == 0: # Try pulling the mobile site
        try:
            Log("Trying mobile site for actors")
            HTTP.Headers['User-agent'] = 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'
            mobilePageElements = HTML.ElementFromURL(url.replace('www','m'))
            actors = mobilePageElements.xpath('//a[@class="pornstarName"] | //a[@class="pornstarImageLink"]')
            HTTP.Headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        except Exception as e:
            Log("Error: " + str(e))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL((PAsearchSites.getSearchBaseURL(siteID)+actorPageURL).replace("https:","http:"))
            actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"] | //span[@class="removeAvatarParent"]/img')[0].get("src").replace("https:","http:")
            movieActors.addActor(actorName,actorPhotoURL)
    else:
        Log("Still no actors, trying to pull from Javascript")
        try:
            dataLayer = detailsPageElements.xpath('//script[contains(text(),"dataLayer")]')[0].text_content()
            alpha = dataLayer.find('"sceneActors"')+14
            omega = dataLayer.find(']',alpha)
            sceneActors = dataLayer[alpha:omega]
            i = 1
            alpha = 0
            omega = 0
            while i <= int(sceneActors.count('actorId')):
                alpha = sceneActors.find('"actorId"',omega)+11
                omega = sceneActors.find('"',alpha)
                actorId = sceneActors[alpha:omega]
                alpha = sceneActors.find('"actorName"',omega)+13
                omega = sceneActors.find('"',alpha)
                actorName = sceneActors[alpha:omega]
                #Search for the actor to get their page (then photo) or hardcode the URL pattern if feeling frisky
                actorPageURL = '/en/pornstar/'+actorName.replace(' ','-')+'/'+actorId
                actorPage = HTML.ElementFromURL((PAsearchSites.getSearchBaseURL(siteID)+actorPageURL).replace("https:","http:"))
                actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"] | //span[@class="removeAvatarParent"]/img')[0].get("src").replace("https:","http:")
                movieActors.addActor(actorName,actorPhotoURL)
                Log('i: '+str(i))
                i = int(i) + 1
        except:
            pass

    # Title
    try:
        title = detailsPageElements.xpath('//meta[@name="twitter:title"]')[0].get('content').strip()
    except:
        try:
            # Title DVD
            title = detailsPageElements.xpath('//h3[@class="dvdTitle"]')[0].text_content().strip()
        except:
            try:
                # Title Scene
                title = detailsPageElements.xpath('//h1[@class="sceneTitle"]')[0].text_content().strip()
            except:
                try:
                    title = detailsPageElements.xpath('//h1')[0].text_content().strip()
                except:
                    title = "I couldn't find the title, please report this on github: https://github.com/PAhelper/PhoenixAdult.bundle/issues"


    if "Scene #" in detailsPageElements.xpath('//title')[0].text_content().strip() and "Scene #" not in title:
        pageTitle = detailsPageElements.xpath('//title')[0].text_content().strip()
        alpha = pageTitle.find('Scene')+6
        omega = pageTitle.find(' ',alpha)
        title = (title + " - Scene " + pageTitle[alpha:omega].strip()).replace('#0','').replace('#','')

    if "BONUS" in title or "BTS" in title:
        if len(actors) > 0:
            actorTitle = ' - '
            for actorLink in actors:
                actorName = str(actorLink.text_content().strip())
                if "Rocco Siffredi" not in actorName and "Peter North" not in actorName:
                    actorTitle = actorTitle + actorName + ", "

            title = title + actorTitle
            title = title.strip()
            title = title.strip(",")

    title = title.replace("BONUS-", "BONUS - ").replace("BTS-", "BTS - ")

    metadata.title = title

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
        unlockedPhotoImg = photoPage.xpath('//div[@class="previewImage"]/img')[0].get('src').replace("https:","http:")
        art.append(unlockedPhotoImg)
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
