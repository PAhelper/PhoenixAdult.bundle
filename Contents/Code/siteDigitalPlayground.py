import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    movieSearchResults = HTML.ElementFromURL("https://www.digitalplayground.com/search/movies/" + encodedTitle)
    for movie in movieSearchResults.xpath('//div[@class="box-card dvd"]'):
        titleNoFormatting = movie.xpath('.//h4[1]/a[1]')[0].get('title').strip()
        Log("Result Title: " + titleNoFormatting)
        moviePage = PAsearchSites.getSearchBaseURL(siteNum) + movie.xpath('.//div[@class="release-info"]/div[@class="info-left"]/div[@class="subtitle-container"]/div/span[@class="subtitle"]/h4/a')[0].get('href')
        curID = moviePage.replace('/','_').replace("?","!")
        Log("ID: " + curID)
        releaseDate = datetime.strptime(movie.xpath('.//div[@class="release-info"]/div[@class="info-left"]/span[2]')[0].text_content().strip(), "%d %B, %Y")
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " (" + str(releaseDate.year) + ") - Full Movie [" + PAsearchSites.getSearchSiteName(siteNum) + "]", score = score, lang = lang))

    videoSearchResults = HTML.ElementFromURL("https://www.digitalplayground.com/search/videos/" + encodedTitle)
    for video in videoSearchResults.xpath('//div[@class="box-card scene"]'):
        titleNoFormatting = video.xpath('.//img[@class=" lazyload"]')[0].get('alt')
        Log("Result Title: " + titleNoFormatting)
        curID = PAsearchSites.getSearchBaseURL(siteNum) + video.xpath('.//a[@class="track"]')[0].get('href')
        #if "/movies/" not in curID: #strip out the videos that are movie scenes or series episodes, because those are caught above
        k = titleNoFormatting.rfind("-")
        titleNoFormatting = titleNoFormatting[:k].strip()
        if "/series/" in curID:
            titleNoFormatting = titleNoFormatting + " - " + video.xpath('.//h4')[0].text_content().replace(":","").strip()
        if "/movies/" in curID:
            titleNoFormatting = titleNoFormatting + " - " + video.xpath('.//h4')[0].text_content().replace(":","").strip()
            curID = curID + "?sceneid=" + video.xpath('.//h4')[0].text_content()[6:8].replace(":","")
        curID = curID.replace('/','_').replace("?","!")
        Log("ID: " + curID)
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "]", score = score, lang = lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    detailsPageURL = str(metadata.id).split("|")[0].replace('_', '/').replace("!","?")
    detailsPageElements = HTML.ElementFromURL(detailsPageURL)
    thisPage = detailsPageElements.xpath('//a[contains(text(),"trailer")]')[0].get('href')

    metadata.collections.clear()
    metadata.studio = "Digital Playground"
    art = []

    # Title
    title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    #Determine what we're looking for and gather the information as needed
    if "/series/" in detailsPageURL:
        # This is an episode in a Series
        seriesInfoPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//a[contains(text(),"info")]')[0].get("href"))
        seriesTrailerPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + seriesInfoPageElements.xpath('//a[@class="watch-now"]')[0].get("href"))
        art.append(seriesTrailerPageElements.xpath('//div[@class="trailer-player "]')[0].get('data-poster-image'))
        tagline = "Series: " + seriesInfoPageElements.xpath('//h1')[0].text_content().strip()
        summary = seriesInfoPageElements.xpath('//div[@class="overview"]//p')[0].text_content().strip()
        genres = detailsPageElements.xpath('//ul[@id="movie-info-format" and last()]/li/div/a')
        try:
            # Series needs to define the Episode Number and pull only actors from that episode
            actors = detailsPageElements.xpath('//a[@href="'+thisPage+'" and last()]//following-sibling::div[@class="model-names-wrapper"]/span[@class="model-names"]/a')
            if len(actors) == 0:
                raise
        except:
            # I could put a backup plan here to pull actors from the Series Info page...
            pass

    elif "/movies/" in detailsPageURL:
        movieInfoPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//a[contains(text(),"info")]')[0].get("href"))
        tagline = "Blockbuster"
        summary = movieInfoPageElements.xpath('//div[@class="overview"]//p')[0].text_content().strip()
        genres = movieInfoPageElements.xpath('//div[@class="box-tag"]/a')
        if "sceneid" in detailsPageURL:
            # This is an individual scene from a Blockbuster
            metadata.collections.add(title)
            k = detailsPageURL.rfind("=")
            sceneID = detailsPageURL[k+1:].strip()
            sceneImg = movieInfoPageElements.xpath('//img[@alt="' + title + ' - Scene ' + sceneID + '"]')[0].get('data-srcset')
            k = sceneImg.rfind("/")
            art.append("https:" + sceneImg[:k+1] + "1290x726_1.jpg")
            title = title + ": Scene " + sceneID
            try:
                # Pull the actors for just that one scene
                actors = movieInfoPageElements.xpath('//h4[text()="Scene '+sceneID+': "]//following-sibling::a')
                if len(actors) == 0:
                    raise
            except:
                pass
        else:
            # This is a full Blockbuster movie
            try:
                actors = movieInfoPageElements.xpath('//div[@class="box-card model  "]/div[@class="title-bar"]/div[@class="title-text"]/div/h4/a')
                if len(actors) == 0:
                    raise
            except:
                pass
            sceneImgs = movieInfoPageElements.xpath('//div[@class="box-card scene"]/div[@class="preview-image"]/a/img')
            for sceneImg in sceneImgs:
                imgSrc = sceneImg.get('data-srcset')
                k = imgSrc.rfind("/")
                art.append("https:" + imgSrc[:k+1] + "1290x726_1.jpg")
        art.append("http:" + movieInfoPageElements.xpath('//img[@id="front-cover-hd"]')[0].get('src'))
        art.append("http:" + movieInfoPageElements.xpath('//img[@id="back-cover-hd"]')[0].get('src'))
    else:
        # This must be a Flixxx or Raw Cuts or something else
        tagline = detailsPageElements.xpath('//a[contains(@class,"full-scene-button")]')[0].text_content().strip()
        genres = detailsPageElements.xpath('//ul[@id="movie-info-format" and last()]/li/div/a')
        try:
            # Sometimes it just doesn't have a synopsis...
            summary = detailsPageElements.xpath('//span[text()="SYNOPSIS"]//following::span')[0].text_content().strip()
        except:
            pass

        try:
            actors = detailsPageElements.xpath('//span[@class="subtitle" and text()="STARRING"]//following::span[1]//a')
            if len(actors) == 0:
                raise
        except:
            Log("Fallback plan for Actors reached")
            searchPageElements = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteID) + urllib.quote(title))
            actors = searchPageElements.xpath('//h4[contains(text(),"'+title+'")]//following-sibling::a')
        art.append(detailsPageElements.xpath('//div[@class="trailer-player "]')[0].get('data-poster-image'))

    art.append(detailsPageElements.xpath('//div[@class="trailer-player "]')[0].get('data-poster-image'))
    tagline = "DP " + tagline

    metadata.collections.add(tagline)
    metadata.tagline = tagline
    metadata.title = title
    metadata.summary = summary

    # Genres
    movieGenres.clearGenres()
    Log("Genres found: " + str(len(genres)))
    if len(genres) > 0:
        for genre in genres:
            genreName = str(genre.text_content().lower().strip())
            if "episode" not in genreName:
                movieGenres.addGenre(genreName)

    # Date
    try:
        releaseDate = detailsPageElements.xpath('//ul[contains(@class,"movie-details")]//span')[0].text_content()
    except:
        releaseDate = detailsPageElements.xpath('.//div[@class="release-info"]/div[@class="info-left"]/span[2]')[0].text_content().strip()

    if len(releaseDate) > 0:
        date_object = datetime.strptime(releaseDate, '%m-%d-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    Log("Actors found: " + str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorPageURL = actorLink.get("href")
            if "/model/" in actorPageURL: # dirty hack to filter out the extra actor I was getting that was named for some other scene; actual problem is probably just my xpath search for actors above
                actorName = str(actorLink.text_content().strip())
                actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
                actorPhotoURL = "https:" + actorPage.xpath('//div[@class="preview-image"]//img')[0].get("src")
                movieActors.addActor(actorName,actorPhotoURL)

    # Posters
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
