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
    Log("Scene Title: " + sceneTitle)

    url = PAsearchSites.getSearchSearchURL(siteNum) + sceneID + "/1"
    searchResult = HTML.ElementFromURL(url)
    titleNoFormatting = searchResult.xpath('//h1[@class="wxt7nk-4 fSsARZ"]')[0].text_content().replace('Trailer for','').replace('Trailer','').strip()
    curID = url.replace('/','_').replace('?','!')
    try:
        subSite = searchResult.xpath('//div[@class="sc-11m21lp-2 fOadtn"]')[0].text_content().strip()
    except:
        subSite = "DigitalPlayground"
    if sceneTitle:
        score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
    else:
        score = 90
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [DigitalPlayground/" + subSite + "] ", score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()
    try:
        sceneType = detailsPageElements.xpath('//div[contains(@class, "i01da7-0 bRuuus")]/a[2]')[0].text_content().strip()
    except:
        try:
            sceneType = detailsPageElements.xpath('//div[contains(@class, "i01da7-0 bRuuus")]/a[1]')[0].text_content().strip()
        except:
            sceneType = 'Scene'
            Log("SceneType check failed, assuming SceneType is Scene")
    if "Movie" in sceneType:
        sceneType = "Movie"
        Log("Is Movie")

    # Studio
    metadata.studio = 'DigitalPlayground'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="wxt7nk-4 fSsARZ"]')[0].text_content().replace('Trailer for','').replace('Trailer','').strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="tjb798-2 flgKJM"]/span[2]/div[2]')[0].text_content().strip()
    except:
        pass

    #Tagline and Collection(s)
    try:
        tagline = detailsPageElements.xpath('//div[@class="sc-11m21lp-2 fOadtn"]')[0].text_content().strip()
        metadata.tagline = tagline
        metadata.collections.add(tagline)
    except:
        tagline = PAsearchSites.getSearchSiteName(siteID).strip()
        metadata.tagline = tagline
        metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="tjb798-2 flgKJM"]/span[1]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().replace(',','').strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="tjb798-2 flgKJM"]/span[last()]')
    if len(date) > 0:
        date = date[0].text_content().strip().replace('Release Date:','')
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    try:
        actors = detailsPageElements.xpath('//a[@class="wxt7nk-6 czvZQW"]')
        if len(actors) > 0:
            if len(actors) == 3:
                movieGenres.addGenre("Threesome")
            if len(actors) == 4:
                movieGenres.addGenre("Foursome")
            if len(actors) > 4:
                movieGenres.addGenre("Orgy")
            for actorLink in actors:
                actorName = str(actorLink.text_content().strip())
                try:
                    actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
                    detailsActorPage = HTML.ElementFromURL(actorPageURL)
                    actorPhotoURL = detailsActorPage.xpath('//img[@class="sc-1p8qg4p-2 ibyLSN"]')[0].get('src')
                except:
                    actorPhotoURL = ''
                movieActors.addActor(actorName, actorPhotoURL)
    except:
        pass

    ### Posters and artwork ###

    # Video trailer background image (Scene)
    try:
        twitterBG = detailsPageElements.xpath('//div[@class="tg5e7m-2 evtSOm"]/img')[0].get('src')
        art.append(twitterBG)
    except:
        pass

    # Video trailer background image (Movie)
    try:
        photoPageUrl = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//div[@class="i01da7-0 bRuuus"]/a[2]')[0].get('href')
        photoPage = HTML.ElementFromURL(photoPageUrl)
        videoBGText = photoPage.xpath('//div[@class="tg5e7m-0 dNBgus"]/div/div[1]')[0].get('class')
        Log(videoBGText)
        videoBG = videoBGText.replace(' ','')[:-3]
        art.append(videoBG)
    except:
        pass


    # Movie Poster / Photos
    if sceneType == "Movie":
        moviePageURL = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//div[@class="i01da7-0 bRuuus"]/a[1]')[0].get('href')
        moviePage = HTML.ElementFromURL(moviePageURL)
        photos = moviePage.xpath('//img[@class="sc-1p8qg4p-2 ibyLSN"]')
        if len(photos) > 0:
            for photoLink in photos:
                photo = photoLink.get('src')
                art.append(photo)

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
