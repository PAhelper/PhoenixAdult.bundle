import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    sceneID = encodedTitle.split('%20', 1)[0]
    Log("SceneID: " + sceneID)
    try:
        sceneTitle = encodedTitle.split('%20', 1)[1].replace('%20',' ')
    except:
        sceneTitle = ''
    Log("Scene Title: " + sceneTitle)
    url = PAsearchSites.getSearchSearchURL(siteNum) + sceneID + "/1"
    searchResult = HTML.ElementFromURL(url)
    titleNoFormatting = searchResult.xpath('//title')[0].text_content().split("|")[1].strip()
    curID = url.replace('/','_').replace('?','!')
    if searchDate:
        releaseDate = parse(searchDate).strftime('%Y-%m-%d')
    else:
        releaseDate = ''
    if sceneTitle:
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
    else:
        score = 90
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate + "|" + sceneID, name = titleNoFormatting + " [Fitting-Room] ", score = score, lang = lang))

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
    metadata.studio = 'Fitting-Room'

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().split("|")[1].strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//p[@class="description"]')[0].text_content().strip()
    except:
        pass

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    # Get Collection from Related Videos
    try:
        collection = detailsPageElements.xpath('//div[@id="list_videos_related_videos_items"]/div[1]/div[2]/a')[0].text_content().strip()
    except:
        if metadata.title == "Huge Tits":
            collection = "Busty"
        if metadata.title == "Pool Table":
            collection = "Fetishouse"
        if metadata.title == "Spanish Milf":
            collection = "Milf"
        if metadata.title == "Cotton Panty":
            collection = "Pantyhose"
    metadata.collections.add(collection)

    # Actors
    actor = detailsPageElements.xpath('//a[@class="model"]/div[1]/img')[0]
    actorName = actor.get("alt").strip()
    actorPhotoURL = actor.get("src").strip()
    movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    genres = detailsPageElements.xpath('//meta[@property="article:tag"]')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.get("content").replace(actorName,'').strip().lower()
            movieGenres.addGenre(genreName)
    movieGenres.addGenre("Fitting Room")

    # Release Date
    date = str(metadata.id).split("|")[2]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
        Log("Date from file")

    ### Posters and artwork ###
    sceneID = str(metadata.id).split("|")[3]
    Log(sceneID)

    # Poster
    poster = "https://www.fitting-room.com/contents/videos_screenshots/0/" + sceneID + "/preview.jpg"
    Log(poster)
    art.append(poster)

    # Photos
    photoList = [2,3,4,5]
    for photoNum in photoList:
        photo = "https://www.fitting-room.com/contents/videos_screenshots/0/" + sceneID + "/3840x1400/" + str(photoNum) + ".jpg"
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
