import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="gallery"]/div'):
        titleNoFormatting = searchResult.xpath('.//div[@class="video-title truncate"]/a')[0].text_content().strip()
        Log("Title: " + titleNoFormatting)
        curID =('https://fuckingawesome.com' + searchResult.xpath('.//div[@class="video-title truncate"]/a')[0].get('href')).replace('/','_').replace('?','!')
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//span[@class="small date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        firstActor = searchResult.xpath('.//span[@class="subtitle small"]/a')[0].text_content().strip()
        Log("firstActor: " + firstActor)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = releaseDate + " " + firstActor + " in " + titleNoFormatting + " [FuckingAwesome.com] ", score = score, lang = lang))

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
    metadata.studio = 'FuckingAwesome'

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="more text-justify"]')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="tags"]/ul/li/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)
    movieGenres.addGenre("Genre")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="videodate"]/strong')[0].text_content().strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="pornstarnames"]/ul/li/a[contains(@href, "pornstars")]')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = 'https://fuckingawesome.com' + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="pornstar-pic "]/img')[0].get("src")
            if 'http' not in actorPhotoURL:
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//span[@class="et_pb_image_wrap "]/img')[0].get('content')
        art.append(twitterBG)
    except:
        pass


    # Scene photos page
    try:
        photoPageUrl = PAsearchSites.getSearchBaseURL(siteID)+detailsPageElements.xpath('//li[@class="photos"]/a')[0].get('href')
        photoPage = HTML.ElementFromURL(photoPageUrl)
        unlockedPhotos = photoPage.xpath('//div[@class="my-gallery"]/a')
        for unlockedPhoto in unlockedPhotos:
            if 'http' not in unlockedPhoto.get('href'):
                art.append(PAsearchSites.getSearchBaseURL(siteID) + unlockedPhoto.get('href'))
            else:
                art.append(unlockedPhoto.get('href'))
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