import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    url = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.replace('%20','-') + ".html"
    searchResults = HTML.ElementFromURL(url)
    for searchResult in searchResults.xpath('//div[@class="card"]'):
        titleNoFormatting = searchResult.xpath('.//div[2]/div/div[1]/h1')[0].text_content().strip()
        curID = url.replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//div[2]/div/div[1]/p[2]/small')[0].text_content().replace('Posted on','').strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Straplezz" + "] " + releaseDate, score = score, lang = lang))

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
    metadata.studio = 'Straplezz'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="card"]/div[2]/div/div[1]/h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="card"]/div[2]/div/div[1]/p[3]')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//li[@class="list-inline-item tag"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)
    movieGenres.addGenre("Strap-On")
    movieGenres.addGenre("Lesbian")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="card"]/div[2]/div/div[1]/p[2]/small')[0].text_content().replace('Posted on','').strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="card model m-0"]/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorName = actorPage.xpath('//div[@class="row mb-3"]/div[2]/h1')[0].text_content().strip()
            actorPhotoURL = actorPage.xpath('//div[@class="row mb-3"]/div[1]/img')[0].get("src0_1x")
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Photos
    try:
        sceneID = detailsPageElements.xpath('//div[@class="col-md-12 col-lg-3 d-none d-md-block"]/div/div[1]/a/img')[0].get('alt')
        Log("SceneID: " + sceneID)
        photo = PAsearchSites.getSearchBaseURL(siteID) + "/content/" + sceneID + "/0" + ".jpg"
        art.append(photo)
        photo = PAsearchSites.getSearchBaseURL(siteID) + "/content/" + sceneID + "/1" + ".jpg"
        art.append(photo)
        photo = PAsearchSites.getSearchBaseURL(siteID) + "/content/" + sceneID + "/2" + ".jpg"
        art.append(photo)
        photo = PAsearchSites.getSearchBaseURL(siteID) + "/content/" + sceneID + "/3" + ".jpg"
        art.append(photo)
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