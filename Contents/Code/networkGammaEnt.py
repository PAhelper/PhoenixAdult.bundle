import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    networkscene = True
    networkscenepages = True
    networkdvd = True
    directmatch = False
    network_sep_scene_prev = ''
    network_sep_scene = ''
    network_sep_scene_pages_prev = ''
    network_sep_scene_pages = '/'
    network_sep_scene_pages_next = ''
    network_sep_dvd_prev = ''
    network_sep_dvd = '/1/dvd'

    if siteNum == 278 or (siteNum >= 285 and siteNum <= 287) or siteNum == 843:
        network = 'XEmpire'
        network_sep_scene_prev = 'scene/'
        network_sep_scene_pages_prev = 'scene/'
        network_sep_dvd_prev = 'dvd/'
        network_sep_dvd = '/1'
    elif siteNum == 329 or (siteNum >= 351 and siteNum <= 354) or siteNum == 861:
        network = 'Blowpass'
        networkdvd = False
    elif siteNum == 330 or (siteNum >= 355 and siteNum <= 360) or siteNum == 750:
        network = 'Fantasy Massage'
        networkdvd = False
        network_sep_scene = '/scene'
        network_sep_scene_pages = '/scene/'
    elif (siteNum >= 365 and siteNum <= 372) or siteNum == 466 or siteNum == 692:
        network = '21Sextury'
        networkdvd = False
    elif siteNum == 183 or (siteNum >= 373 and siteNum <= 374):
        network = '21Naturals'
        networkdvd = False
        network_sep_scene = '/scene'
        network_sep_scene_pages = '/scene/'
    elif siteNum >= 383 and siteNum <= 386:
        network = 'Fame Digital'
        if siteNum == 383:
            networkdvd = False
            network_sep_scene = '/scene'
            network_sep_scene_pages = '/scene/'
            network_sep_dvd = '/dvd'
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
        network_sep_scene = '/scene'
        network_sep_scene_pages = '/scene/'
    elif siteNum == 381:
        network = 'Burning Angel'
        networkdvd = False
        network_sep_scene = '/scene'
        network_sep_scene_pages = '/scene/'
    elif siteNum == 382:
        network = 'Pretty Dirty'
        networkdvd = False
        network_sep_scene = '/scene'
        network_sep_scene_pages = '/scene/'
    elif siteNum >= 460 and siteNum <= 465:
        network = '21Sextreme'
        networkdvd = False
        network_sep_scene = '/scene'
        network_sep_scene_pages = '/scene/'

    if network == PAsearchSites.getSearchSiteName(siteNum):
        network = ''
    else:
        network = network

    if networkscene:
        # Result to check
        resultfirst = []
        # Result next page
        resultsecond = []

        # searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded + "?query=" + searchData.encoded)
        searchData.encoded = searchData.encoded.replace('%27', '').replace('%3F', '').replace('%2C', '')  # Remove troublesome punctuation (, . ?)
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + network_sep_scene_prev + searchData.encoded + network_sep_scene)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@class="tlcDetails"]'):
            titleNoFormatting = searchResult.xpath('.//a[1]')[0].text_content().strip()
            titleNoFormatting = titleNoFormatting.replace('BONUS-', 'BONUS - ')
            titleNoFormatting = titleNoFormatting.replace('BTS-', 'BTS - ')

            curID = PAutils.Encode(searchResult.xpath('.//a[1]/@href')[0])
            resultfirst.append(curID)

            try:
                actorLink = searchResult.xpath('.//div[@class="tlcActors"]/a')
                actor = ' - '
                if 'BONUS' in titleNoFormatting or 'BTS' in titleNoFormatting:
                    for actorText in actorLink:
                        actorName = actorText.text_content().strip()
                        if 'Rocco Siffredi' not in actorName and 'Peter North' not in actorName:
                            actor = actor + actorName + ', '
                else:
                    actor = actor + actorLink[0].text_content().strip()
                actor = actor.strip()
                actor = actor.strip(',')
                actor = ' ' + actor
            except:
                actor = ''

            try:
                releaseDate = parse(searchResult.xpath('.//div[@class="tlcSpecs"]/span[@class="tlcSpecsDate"]/span[@class="tlcDetailsValue"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            except:
                try:
                    req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a[1]')[0].get('href'))
                    detailsPageElements = HTML.ElementFromString(req.text)
                    releaseDate = parse(detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')
                except:
                    releaseDate = ''

            if searchData.date and releaseDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s %s [%s/%s] %s' % (titleNoFormatting, actor, network, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

        if networkscenepages:
            # Other pages
            i = 2
            while i < 3:
                pagenum = i
                req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + network_sep_scene_pages_prev + searchData.encoded + network_sep_scene_pages + str(pagenum) + network_sep_scene_pages_next)
                searchResultsSec = HTML.ElementFromString(req.text)
                i += 1
                searchResultSec = searchResultsSec.xpath('//div[@class="tlcDetails"]')
                if searchResultSec:
                    titleText = searchResultSec[0].xpath('.//a[1]/@href')[0]
                    resultSEARCH = PAutils.Encode(titleText)

                    for resultCheck in resultfirst:
                        if resultCheck == resultSEARCH:
                            i = 100
                            break

                    for searchResultSec in searchResultsSec.xpath('//div[@class="tlcDetails"]'):
                        titleText = searchResultSec.xpath('.//a[1]')[0]
                        titleNoFormatting = titleText.text_content().strip()
                        titleNoFormatting = titleNoFormatting.replace('BONUS-', 'BONUS - ')
                        titleNoFormatting = titleNoFormatting.replace('BTS-', 'BTS - ')

                        curID = PAutils.Encode(titleText.get('href'))
                        resultsecond.append(curID)

                        try:
                            actorLink = searchResultSec.xpath('.//div[@class="tlcActors"]/a')
                            actor = ' - '
                            if 'BONUS' in titleNoFormatting or 'BTS' in titleNoFormatting:
                                for actorText in actorLink:
                                    actorName = actorText.text_content().strip()
                                    if 'Rocco Siffredi' not in actorName and 'Peter North' not in actorName:
                                        actor = actor + actorName + ', '
                            else:
                                actor = actor + actorLink[0].text_content().strip()
                            actor = actor.strip()
                            actor = actor.strip(',')
                            actor = ' ' + actor
                        except:
                            actor = ''

                        try:
                            releaseDate = parse(searchResultSec.xpath('.//div[@class="tlcSpecs"]/span[@class="tlcSpecsDate"]/span[@class="tlcDetailsValue"]')[0].text_content().strip()).strftime('%Y-%m-%d')
                        except:
                            try:
                                req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + searchResultSec.xpath('.//a[1]/@href')[0])
                                detailsPageElements = HTML.ElementFromString(req.text)
                                releaseDate = parse(detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')
                            except:
                                releaseDate = ''

                        if searchData.date and releaseDate:
                            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
                        else:
                            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s %s [%s/%s] %s' % (titleNoFormatting, actor, network, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

                    resultfirst = resultsecond
                    resultsecond = []
                else:
                    i = 100

    if directmatch:
        # Result to check
        resultfirst = []
        searchString = searchData.encoded.replace('%20', '-').lower()
        # searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded + "?query=" + searchData.encoded)
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@id="infoWrapper"]'):
            titleNoFormatting = searchResult.xpath('.//h1[1]')[0].text_content().strip()
            titleNoFormatting = titleNoFormatting.replace('BONUS-', 'BONUS - ')
            titleNoFormatting = titleNoFormatting.replace('BTS-', 'BTS - ')

            curID = PAutils.Encode(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
            resultfirst.append(curID)

            try:
                releaseDate = (searchResult.xpath('//li[@class="updatedDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            except:
                releaseDate = ''

            if searchData.date and releaseDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s/%s] %s' % (titleNoFormatting, network, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    if networkdvd:
        try:
            req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + network_sep_dvd_prev + searchData.encoded + network_sep_dvd)
            dvdResults = HTML.ElementFromString(req.text)
            for dvdResult in dvdResults.xpath('//div[contains(@class, "tlcItem playlistable_dvds")] | //div[@class="tlcDetails"]'):
                titleNoFormatting = dvdResult.xpath('.//div[@class="tlcTitle"]/a/@title')[0].strip()
                curID = PAutils.Encode(dvdResult.xpath('.//a/@href')[0])
                try:
                    releaseDate = parse(dvdResult.xpath('.//div[@class="tlcSpecs"]/span[@class="tlcSpecsDate"]/span[@class="tlcDetailsValue"]')[0].text_content().strip())
                except:
                    try:
                        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + dvdResult.xpath('.//a[1]/@href')[0])
                        detailsPageElements = HTML.ElementFromString(req.text)
                        releaseDate = parse(detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().strip())
                    except:
                        releaseDate = ''

                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s (%s) - Full Movie [%s]' % (titleNoFormatting, releaseDate.strftime('%Y'), PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))
        except:
            pass

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = metadata.id.split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    metadata.directors.clear()
    director = metadata.directors.new()

    if siteNum == 278 or (siteNum >= 285 and siteNum <= 287) or siteNum == 843:
        metadata.studio = 'XEmpire'
        director.name = 'Mason'
    elif siteNum == 329 or (siteNum >= 351 and siteNum <= 354) or siteNum == 861:
        metadata.studio = 'Blowpass'
    elif siteNum == 331 or (siteNum >= 355 and siteNum <= 360) or siteNum == 750:
        metadata.studio = 'Fantasy Massage'
    elif (siteNum >= 365 and siteNum <= 372) or siteNum == 466 or siteNum == 690:
        metadata.studio = '21Sextury'
    elif siteNum == 183 or (siteNum >= 373 and siteNum <= 374):
        metadata.studio = '21Naturals'
    elif siteNum >= 383 and siteNum <= 386:
        metadata.studio = 'Fame Digital'
    elif siteNum >= 387 and siteNum <= 392:
        metadata.studio = 'Open Life Network'
    elif siteNum == 281:
        metadata.studio = 'Pure Taboo'
    elif siteNum == 381:
        metadata.studio = 'Burning Angel'
    elif siteNum == 382:
        metadata.studio = 'Pretty Dirty'
    elif siteNum >= 460 and siteNum <= 466:
        metadata.studio = '21Sextreme'

    art = []

    # Summary
    try:
        paragraph = detailsPageElements.xpath('//meta[@name="twitter:description"]/@content')[0].strip()
    except:
        paragraph = ''

    if not paragraph:
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
    metadata.summary = paragraph.replace('</br>', '\n').replace('<br>', '\n').replace('<br/>', '\n').strip()
    metadata.collections.clear()

    # Tagline
    try:
        tagline = detailsPageElements.xpath('//div[@class="studioLink"]')[0].text_content().strip()
    except:
        tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Title DVD
    try:
        dvdTitle = detailsPageElements.xpath('//a[contains(@class, "dvdLink")][1]/@title')[0].strip()
        metadata.collections.add(dvdTitle.replace('#0', '').replace('#', ''))
    except:
        try:
            dvdTitleScript = detailsPageElements.xpath('//script[contains(text(), "dvdName")]')[0].text_content()
            alpha = dvdTitleScript.find('"dvdName"') + 11
            omega = dvdTitleScript.find('"', alpha)
            dvdTitle = dvdTitleScript[alpha:omega]
            if dvdTitle:
                metadata.collections.add(dvdTitle.replace('#0', '').replace('#', ''))
        except:
            try:
                dvdTitle = detailsPageElements.xpath('//h1[@class="sceneTitle"]')[0].text_content().strip()
                dvdTitle = dvdTitle.replace('BONUS-', '').replace('BONUS - ', '')
                dvdTitle = dvdTitle.replace('BONUS', '')
                dvdTitle = dvdTitle.replace('BTS-', '').replace('BTS - ', '')
                dvdTitle = dvdTitle.replace('BTS', '')
                metadata.collections.add(dvdTitle.replace('#0', '').replace('#', ''))
            except:
                dvdTitle = 'This is some damn nonsense that should never match the scene title'

    # Director
    try:
        directors = detailsPageElements.xpath('//div[@class="sceneCol sceneColDirectors"]//a | //ul[@class="directedBy"]/li/a')
        for dirname in directors:
            director.name = dirname.text_content().strip()
    except:
        pass

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="sceneCol sceneColCategories"]//a | //div[@class="sceneCategories"]//a | //p[@class="dvdCol"]/a')
    for genreLink in genres:
        genreName = genreLink.text_content().strip('\n').lower()

        movieGenres.addGenre(genreName)

    # Release Date
    try:
        date = detailsPageElements.xpath('//*[@class="updatedDate"]')[0].text_content().replace('|', '').strip()
        if date:
            date_object = parse(date)
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
    except:
        try:
            date = detailsPageElements.xpath('//*[@class="updatedOn"]')[0].text_content().strip()
            date = date[8:].strip()
            if date:
                date_object = parse(date)
                metadata.originally_available_at = date_object
                metadata.year = metadata.originally_available_at.year
        except:
            try:
                datePublished = detailsPageElements.xpath('//script[contains(text(), "datePublished")]')[0].text_content()
                alpha = datePublished.find('"datePublished"') + 17
                omega = datePublished.find('"', alpha)
                date = datePublished[alpha:omega]
                if date:
                    date_object = parse(date)
                    metadata.originally_available_at = date_object
                    metadata.year = metadata.originally_available_at.year
            except:
                pass

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="sceneCol sceneColActors"]//a | //div[@class="sceneCol sceneActors"]//a | //div[@class="pornstarNameBox"]/a[@class="pornstarName"] | //div[@id="slick_DVDInfoActorCarousel"]//a | //div[@id="slick_sceneInfoPlayerActorCarousel"]//a')
    if metadata.title == 'Kennedy Leigh' and metadata.tagline == 'Only Teen Blowjobs':
        movieActors.addActor('Kennedy Leigh', 'https://imgs1cdn.adultempire.com/actors/649607h.jpg')

    if not actors:  # Try pulling the mobile site
        try:
            req = PAutils.HTTPRequest(url.replace('www', 'm'), headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'})
            mobilePageElements = HTML.ElementFromString(req.text)
            actors = mobilePageElements.xpath('//a[@class="pornstarName"] | //a[@class="pornstarImageLink"]')

        except:
            pass
    if actors:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            actorPageURL = actorLink.get('href')
            req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]/@src | //span[@class="removeAvatarParent"]/img/@src')[0]

            movieActors.addActor(actorName, actorPhotoURL)
    else:
        try:
            dataLayer = detailsPageElements.xpath('//script[contains(text(), "dataLayer")]')[0].text_content()
            alpha = dataLayer.find('"sceneActors"') + 14
            omega = dataLayer.find(']', alpha)
            sceneActors = dataLayer[alpha:omega]
            i = 1
            while i <= int(sceneActors.count('actorId')):
                alpha = sceneActors.find('"actorId"', omega) + 11
                omega = sceneActors.find('"', alpha)
                actorId = sceneActors[alpha:omega]
                alpha = sceneActors.find('"actorName"', omega) + 13
                omega = sceneActors.find('"', alpha)
                actorName = sceneActors[alpha:omega]
                # Search for the actor to get their page (then photo) or hardcode the URL pattern if feeling frisky
                actorPageURL = '/en/pornstar/' + actorName.replace(' ', '-') + '/' + actorId
                req = PAutils.HTTPRequest((PAsearchSites.getSearchBaseURL(siteNum) + actorPageURL))
                actorPage = HTML.ElementFromString(req.text)
                actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]/@src | //span[@class="removeAvatarParent"]/img/@src')[0]
                movieActors.addActor(actorName, actorPhotoURL)
                i += 1
        except:
            pass

    # Title
    try:
        title = detailsPageElements.xpath('//meta[@name="twitter:title"]/@content')[0].strip()
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
                    title = 'I couldn\'t find the title, please report this on github: https://github.com/PAhelper/PhoenixAdult.bundle/issues'

    if 'Scene #' in detailsPageElements.xpath('//title')[0].text_content().strip() and "Scene #" not in title:
        pageTitle = detailsPageElements.xpath('//title')[0].text_content().strip()
        alpha = pageTitle.find('Scene') + 6
        omega = pageTitle.find(' ', alpha)
        title = '%s - Scene %s' % (title, pageTitle[alpha:omega].strip()).replace('#0', '').replace('#', '')

    if 'BONUS' in title or 'BTS' in title:
        if actors:
            actorTitle = ' - '
            for actorLink in actors:
                actorName = actorLink.text_content().strip()
                if 'Rocco Siffredi' not in actorName and 'Peter North' not in actorName:
                    actorTitle = actorTitle + actorName + ', '

            title = title + actorTitle
            title = title.strip()
            title = title.strip(',')

    title = title.replace('BONUS-', 'BONUS - ').replace('BTS-', 'BTS - ')

    metadata.title = title

    # Posters

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//meta[@name="twitter:image"]/@content')[0]
        art.append(twitterBG)
    except:
        pass

    try:
        picScript = detailsPageElements.xpath('//script[contains(text(), "picPreview")]')[0].text_content()
        alpha = picScript.find('"picPreview":"') + 14
        omega = picScript.find('"', alpha)
        art.append(picScript[alpha:omega].replace('\\', ''))
    except:
        pass

    try:
        sceneImg = detailsPageElements.xpath('//img[@class="sceneImage"]/@src')[0]
        art.append(sceneImg)
    except:
        pass

    # Scene photos page
    try:
        photoPageUrl = PAsearchSites.getSearchBaseURL(siteNum) + detailsPageElements.xpath('//a[@class="controlButton GA_Track GA_Track_Action_Pictures GA_Track_Category_Player GA GA_Click GA_Id_ScenePlayer_Pictures"]')[0].get('href')
        req = PAutils.HTTPRequest(photoPageUrl)
        photoPage = HTML.ElementFromString(req.text)
        unlockedPhotoImg = photoPage.xpath('//div[@class="previewImage"]/img/@src')[0]
        art.append(unlockedPhotoImg)
        unlockedPhotos = photoPage.xpath('//a[@class="imgLink"]/@href | //a[@class="imgLink pgUnlocked"]/@href')
        for unlockedPhoto in unlockedPhotos:
            art.append(unlockedPhoto)
    except:
        photoPageUrl = sceneURL

    # DVD Covers
    if '/movie/' in sceneURL:
        try:
            dvdFrontCover = detailsPageElements.xpath('//a[@class="frontCoverImg"]/@href')[0]
            art.append(dvdFrontCover)

            dvdBackCover = detailsPageElements.xpath('//a[@class="backCoverImg"]/@href')[0]
            art.append(dvdBackCover)
        except:
            pass

        # DVD scene images
        try:
            sceneImgs = detailsPageElements.xpath('//img[@class="tlcImageItem img"]/@src')
            for sceneImg in sceneImgs:
                art.append(sceneImg)
        except:
            pass

        try:
            sceneImgs = detailsPageElements.xpath('//img[@class="img lazy"]/@data-original')
            for sceneImg in sceneImgs:
                art.append(sceneImg)
        except:
            pass

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
