import PAsearchSites
import PAgenres
import PAactors
import re


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    sceneID = searchTitle.split(' ', 1)[0]
    if unicode(sceneID, 'utf8').isdigit():
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()
    else:
        sceneID = None


    req = urllib.Request(PAsearchSites.getSearchBaseURL(siteNum))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    data = urllib.urlopen(req).read()
    apiKEY = re.search(r'\"apiKey\":\"(.*?)\"', data).group(1)

    for sceneType in ['scenes', 'movies']:
        url = PAsearchSites.getSearchSearchURL(siteNum).replace('*', 'girlfriendsfilms_' + sceneType, 1) + '?x-algolia-application-id=TSMKFA364Q&x-algolia-api-key=' + apiKEY
        params = json.dumps({'params':'query=' + searchTitle})
        req = urllib.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Referer', PAsearchSites.getSearchBaseURL(siteNum))
        data = urllib.urlopen(req, params).read()

        searchResults = json.loads(data)['hits']
        for searchResult in searchResults:
            if sceneType == 'scenes':
                foundID = str(searchResult['clip_id'])
                url = '/en/video/1/' + foundID
                releaseDate = parse(searchResult['release_date']).strftime('%Y-%m-%d')

                actors = []
                for actorLink in searchResult['female_actors']:
                    actors.append(actorLink['name'])
                sceneInfo = ', '.join(actors)
            else:
                foundID = str(searchResult['movie_id'])
                url = '/en/dvd/1/' + foundID
                releaseDate = parse(searchResult['last_modified']).strftime('%Y-%m-%d')
                sceneInfo = 'Movie'

            curID = (PAsearchSites.getSearchBaseURL(siteNum) + url).replace('/','_').replace('?','!')
            titleNoFormatting = searchResult['title']
            if sceneID:
                score = 100 - Util.LevenshteinDistance(sceneID, foundID)
            elif searchDate:
                score = 80 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 80 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s %s' % (sceneInfo, titleNoFormatting, releaseDate), score=score, lang=lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Girlfriends Films'

    if "video" in url:
        sceneType = 'Scene'
        Log('SceneType: ' + sceneType)

        # Title
        metadata.title = detailsPageElements.xpath('//h1[@class="sceneTitle"]')[0].text_content().strip()

        # Summary
        try:
            metadata.summary = detailsPageElements.xpath('//div[@class="descriptionText"]')[0].text_content().strip()
        except:
            pass

        #Tagline and Collection(s)
        tagline = PAsearchSites.getSearchSiteName(siteID).strip()
        metadata.tagline = tagline
        metadata.collections.add(tagline)
        # DVD Release
        try:
            dvdRel = detailsPageElements.xpath('//img[@class="sceneImage"]')[0].get('title').strip()
            metadata.collections.add(dvdRel)
        except:
            pass

        # Genres
        genres = detailsPageElements.xpath('//div[@class="sceneCol categories"]/a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.get('title').strip().lower()
                movieGenres.addGenre(genreName)

        # Release Date
        date = detailsPageElements.xpath('//li[@class="updatedDate"]')[0].text_content().replace('|','').strip()
        if len(date) > 0:
            date_object = datetime.strptime(date, '%m-%d-%Y')
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year

        # Actors
        actors = detailsPageElements.xpath('//div[@class="sceneCol actors"]/a')
        if len(actors) > 0:
            if len(actors) == 3:
                movieGenres.addGenre("Threesome")
            if len(actors) == 4:
                movieGenres.addGenre("Foursome")
            if len(actors) > 4:
                movieGenres.addGenre("Orgy")
            for actorLink in actors:
                actorName = str(actorLink.text_content().strip())
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]')[0].get("src")
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
                movieActors.addActor(actorName,actorPhotoURL)

        ### Posters and artwork ###

        # Video trailer background image
        try:
            picScript = detailsPageElements.xpath('//script[contains(text(),"picPreview")]')[0].text_content()
            alpha = picScript.find('"picPreview":"') + 14
            omega = picScript.find('"', alpha)
            Log('BG in <script>: ' + picScript[alpha:omega].replace('\\', ''))
            art.append(picScript[alpha:omega].replace('\\', '').replace("https:", "http:"))
        except:
            pass

        # Photos
        try:
            photoPageUrl = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//a[@class="controlButton GA_Track GA_Track_Action_Pictures GA_Track_Category_Player GA GA_Click GA_Id_ScenePlayer_Pictures"]')[0].get('href')
            photoPage = HTML.ElementFromURL(photoPageUrl)
            unlockedPhotoImg = photoPage.xpath('//div[@class="previewImage"]/img')[0].get('src')
            art.append(unlockedPhotoImg)
            unlockedPhotos = photoPage.xpath('//a[@class="imgLink"] | //a[@class="imgLink pgUnlocked"]')
            for unlockedPhoto in unlockedPhotos:
                art.append(unlockedPhoto.get('href'))
        except:
            pass

        # DVD Cover
        dvdCover = detailsPageElements.xpath('//img[@class="sceneImage"]')[0].get('src')
        art.append(dvdCover)

    else:
        sceneType = 'Movie'
        Log('SceneType: ' + sceneType)

        # Title
        metadata.title = detailsPageElements.xpath('//h3[@class="dvdTitle"]')[0].text_content().strip()

        # Summary
        try:
            metadata.summary = detailsPageElements.xpath('//p[@class="descriptionText"]')[0].text_content().strip()
        except:
            pass

        #Tagline and Collection(s)
        tagline = PAsearchSites.getSearchSiteName(siteID).strip()
        metadata.tagline = tagline
        metadata.collections.add(tagline)
        # DVD Release
        metadata.collections.add(metadata.title)

        # Genres
        genres = detailsPageElements.xpath('//p[@class="dvdCol"]/a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.get('title').strip().lower()
                movieGenres.addGenre(genreName)

        # Release Date
        try:
            date = detailsPageElements.xpath('//ul[@class="dvdSpecs"]/li[@class="updatedOn"]')[0].text_content().replace('Updated','').strip()
            if len(date) > 0:
                date_object = datetime.strptime(date, '%Y-%m-%d')
                metadata.originally_available_at = date_object
                metadata.year = metadata.originally_available_at.year
        except:
            pass

        # Actors
        actors = detailsPageElements.xpath('//div[@class="Gamma_Carousel Gamma_Component Gamma_Carousel_ActorsCarousel"]//img')
        if len(actors) > 0:
            for actorLink in actors:
                actorName = str(actorLink.get("alt").strip())
                try:
                    actorPhotoURL = actorLink.get("src")
                except:
                    actorPhotoURL = ""
                movieActors.addActor(actorName,actorPhotoURL)

        # DVD Cover
        try:
            dvdFrontCover = detailsPageElements.xpath('//a[@class="frontCoverImg"]')[0].get('href')
            art.append(dvdFrontCover)
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