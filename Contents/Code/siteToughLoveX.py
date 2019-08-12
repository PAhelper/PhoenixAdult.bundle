import PAsearchSites
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchString = searchTitle.replace(" ","-").replace(",","").replace("'","").replace("?","").lower().strip()
    Log("searchString " + searchString)
    modelsPageSortByLetter = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle[:1] #here we get first letter of searchTitle
    actorResults = HTML.ElementFromURL(modelsPageSortByLetter)
    actorPage = actorResults.xpath('//a[contains(@href,"' + searchString + '")]')[0].get('href') # looking for our model
    searchResults = HTML.ElementFromURL(actorPage) # scene search is carried out through the model page

    for searchResult in searchResults.xpath('//div[@class="content-box"]'):
        titleNoFormatting = searchResult.xpath('.//h2//span')[0].text_content().strip()
        sceneUrl = searchResult.xpath('.//a')[0].get('href')
        curID = sceneUrl.replace('/','_').replace('?','!')
        scenePage = HTML.ElementFromURL(sceneUrl) # geting releaseDate from scene page
        releaseDate = parse(scenePage.xpath('//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    pageURL = str(metadata.id).split("|")[0].replace('_', '/').replace('!','?')
    Log('scene url: ' + pageURL)
    detailsPageElements = HTML.ElementFromURL(pageURL)
    art = []
    # Summary
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.studio = siteName
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="description"]//p')[0].text_content().strip()
        metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    except:
        pass

    # Director
    metadata.directors.clear()
    director = metadata.directors.new()
    director.name = "Charles Dera"

    # Collections / Tagline
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Genres
    try:
        genres = detailsPageElements.xpath('//dd[2]')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip().lower()
                Log("Genre for >" + metadata.title + "<: " + genreName)
                movieGenres.addGenre('All Sex')
    except:
        pass

    # Release Date
    try:
        date = detailsPageElements.xpath('//span[@class="date"]')
        if len(date) > 0:
            date = date[0].text_content().strip()
            date_object = parse(date)
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
    except:
        pass

    # Actors
    movieActors.clearActors()

    actors = detailsPageElements.xpath('//dd[1]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.xpath('.//a[1]')[0].text_content().strip()
            actorPhotoURL = actorLink.xpath('.//a[2]//img')[0].get('src')
            movieActors.addActor(actorName,actorPhotoURL)
            try:
                actorName = actorLink.xpath('.//a[3]')[0].text_content().strip()
                actorPhotoURL = actorLink.xpath('.//a[4]//img')[0].get('src')
                movieActors.addActor(actorName, actorPhotoURL)
            except:
                pass

    # Posters/Background
    posters = HTML.ElementFromURL(detailsPageElements.xpath('//dd[1]//a')[0].get('href'))

    for poster in posters.xpath('//a[contains(@href,"' + pageURL + '")]//img'):
        posterUrl = poster.get('src')
        Log("DownLoad Posters/Arts: " + posterUrl)
        if len(posterUrl) > 0:
            art.append(posterUrl)

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