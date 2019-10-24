import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchString = searchTitle.replace(" ","-")
    Log("searchString: " + searchString)
    if "/" not in searchString:
        i = searchString.rfind("-")
        searchString = searchString[:i] + "/" + searchString[i+1:]
        Log("searchString formatted: " + searchString)

        # Direct URL (DVD Page) search - preferred
    if "scene" not in searchString.lower():
        Log("Direct URL (DVD page)")
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
        for searchResult in searchResults.xpath('//div[@class="sceneContainer"]'):
            titleNoFormatting = searchResult.xpath('.//h3')[0].text_content().strip().title().replace("Xxx","XXX")
            curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
            releaseDate = parse(searchResult.xpath('.//p[@class="sceneDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            Log(titleNoFormatting+"/"+curID+"/"+releaseDate+"/"+str(score))
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Wicked/Scene] " + releaseDate, score = score, lang = lang))

        # Full DVD match added to results as an option
        dvdTitle = searchResults.xpath('//h3[@class="dvdTitle"]')[0].text_content().strip().title().replace("Xxx","XXX")
        curID = searchResults.xpath('//link[@rel="canonical"]')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResults.xpath('//li[@class="updatedOn"]')[0].text_content().replace("Updated","").strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), dvdTitle.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = dvdTitle + " [Wicked/Full Movie] " + releaseDate, score = score, lang = lang))

        # Direct URL (scene page search)
    else:
        Log("Direct URL (Scene page)")
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + "/en/video/" + searchString)
        titleNoFormatting = searchResults.xpath('//h1//span')[0].text_content().strip().title().replace("Xxx","XXX")
        curID = searchResults.xpath('//link[@rel="canonical"]')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResults.xpath('//li[@class="updatedDate"]')[0].text_content().replace("Updated","").replace("|","").strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Wicked/Scene] " + releaseDate, score = score, lang = lang))


    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    urlBase = PAsearchSites.getSearchBaseURL(siteID)
    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    if 'http' not in url:
        url = urlBase + url
    Log("url: " + url)
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Wicked Pictures'
    Log("Studio: " + metadata.studio)

    # Title
    metadata.title = detailsPageElements.xpath('//h1//span')[0].text_content().strip().title().replace("Xxx","XXX")
    Log("Title: " + metadata.title)

    # Release Date
    date = detailsPageElements.xpath('//li[@class="updatedOn"] | //li[@class="updatedDate"]')[0].text_content().replace("Updated","").replace("|","").strip()
    Log("date: " + date)
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    # Scene update
    if "/video/" in url:

        # Genres
        genres = detailsPageElements.xpath('//div[contains(@class,"sceneColCategories")]/a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip().lower()
                movieGenres.addGenre(genreName)

        # Actors
        actors = detailsPageElements.xpath('//div[contains(@class,"sceneColActors")]//a')
        if len(actors) > 0:
            for actorLink in actors:
                actorName = actorLink.text_content().strip()
                try:
                    actorPageURL = urlBase + actorLink.get("href")
                    actorPage = HTML.ElementFromURL(actorPageURL)
                    actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]')[0].get("src")
                    movieActors.addActor(actorName,actorPhotoURL)
                except:
                    actorPhotoURL = ""
                    movieActors.addActor(actorName,actorPhotoURL)
                Log("actor: " + actorName + ", PhotoURL: " + actorPhotoURL)

        script_text = detailsPageElements.xpath('//script')[7].text_content()

        # Background
        alpha = script_text.find('picPreview":"')
        omega = script_text.find('"', alpha + 13)
        previewBG = script_text[alpha + 13:omega].replace("\/","/")
        Log("preview BG: " + previewBG)
        metadata.art[previewBG] = Proxy.Preview(HTTP.Request(previewBG, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

        # Get dvd page for some info
        dvdPageURL = urlBase + detailsPageElements.xpath('//div[@class="content"]//a[contains(@class,"dvdLink")]')[0].get("href")
        Log("dvdPageURL: " + dvdPageURL)
        dvdPageElements = HTML.ElementFromURL(dvdPageURL)

        # Tagline and Collection(s)
        tagline = dvdPageElements.xpath('//h3[@class="dvdTitle"]')[0].text_content().strip().title().replace("Xxx","XXX")
        metadata.tagline = tagline
        metadata.collections.add(tagline)
        Log("dvdtitle: " + tagline)

        # Summary
        try:
            metadata.summary = dvdPageElements.xpath('//p[@class="descriptionText"]')[0].text_content().strip()
            Log("Summary: " + metadata.summary)
        except:
            Log("Summary fetch failed")

        # Director
        director = metadata.directors.new()
        try:
            directors = dvdPageElements.xpath('//ul[@class="directedBy"]')
            for dirname in directors:
                director.name = dirname.text_content().strip()
                Log("Director: " + director.name)
        except:
            pass

        # DVD cover
        dvdCover = dvdPageElements.xpath('//img[@class="dvdCover"]')[0].get('src')
        art.append(dvdCover)
        Log("dvdCover URL: " + dvdCover)

        # Extra photos for the completist
        photoPageURL = urlBase + detailsPageElements.xpath('//div[contains(@class,"picturesItem")]//a')[0].get('href').split("?")[0]
        photoPageElements = HTML.ElementFromURL(photoPageURL)

        ## good 2:3 poster picture
        poster = photoPageElements.xpath('//div[@class="previewImage"]//img')[0].get('src')
        Log("poss.poster: " + poster)
        metadata.posters[poster] = Proxy.Preview(HTTP.Request(poster, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

        ## more Pictures
        extraPix = photoPageElements.xpath('//li[@class="preview"]//a[@class="imgLink pgUnlocked"]')
        for picture in extraPix:
            pictureURL = picture.get("href")
            Log("extraPicture: " + pictureURL)
            art.append(pictureURL)

    ## Full DVD update
    else:
        Log("Fetching Full DVD metadata")

        # Genres
        genres = detailsPageElements.xpath('//p[@class="dvdCol"]/a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip().lower()
                movieGenres.addGenre(genreName)

        # Actors
        actors = detailsPageElements.xpath('//div[@class="actorCarousel"]//a')
        Log("Actors#: " + str(len(actors)))
        if len(actors) > 0:
            for actorLink in actors:
                actorName = actorLink.xpath('.//span')[0].text_content().strip()
                try:
                    actorPhotoURL = actorLink.xpath('.//img')[0].get("src")
                    movieActors.addActor(actorName,actorPhotoURL)
                except:
                    actorPhotoURL = ""
                    movieActors.addActor(actorName,actorPhotoURL)
                Log("actor: " + actorName + ", PhotoURL: " + actorPhotoURL)

        # Tagline/collections
        tagline = 'Wicked Pictures'
        metadata.tagline = tagline
        metadata.collections.add(tagline)
        Log("dvdtitle: " + tagline)

        # Summary
        try:
            metadata.summary = detailsPageElements.xpath('//p[@class="descriptionText"]')[0].text_content().strip()
            Log("Summary: " + metadata.summary)
        except:
            Log("Summary fetch failed")

        # Director
        director = metadata.directors.new()
        try:
            directors = detailsPageElements.xpath('//ul[@class="directedBy"]')
            for dirname in directors:
                director.name = dirname.text_content().strip()
                Log("Director: " + director.name)
        except:
            pass

        # Backgrounds
        scenePreviews = detailsPageElements.xpath('//div[@class="sceneContainer"]//img[contains(@id,"clip")]')
        for scenePreview in scenePreviews:
            previewIMG = scenePreview.get('data-original').split('?')[0]
            Log("scene preview IMG: " + previewIMG)
            art.append(previewIMG)

        # DVD cover
        dvdCover = detailsPageElements.xpath('//img[@class="dvdCover"]')[0].get('src')
        metadata.posters[dvdCover] = Proxy.Preview(HTTP.Request(dvdCover, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        Log("dvdCover URL: " + dvdCover)


    # Extra Picture processing
    j = 2
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
