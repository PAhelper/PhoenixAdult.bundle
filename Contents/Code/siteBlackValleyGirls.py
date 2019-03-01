import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum)) # There's one page that contains all the scenes as of this coding
    for searchResult in searchResults.xpath('//div[@id="scenes-card"]'):
        titleNoFormatting = searchResult.xpath('./a')[0].get('title').strip()
        curID = searchResult.xpath('./a')[0].get("href").replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//div[@class="date d-inline-block pull-right"]')[0].text_content()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [TeamSkeet/" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    sceneID = url.split("/")[3]
    actorID = url.split("/")[5]

    Log("sceneID: "+str(sceneID))
    Log("actorID: "+str(actorID))

    # Summary
    metadata.studio = "TeamSkeet"
    metadata.summary = detailsPageElements.xpath('//p[@class="scene-description-text light-gray2"]')[0].text_content().strip()
    metadata.title = detailsPageElements.xpath('//div[@class="girlname d-inline-block"]')[0].text_content().strip()
    releaseDate = detailsPageElements.xpath('//div[@class="d-inline-block light-gray"]')[0].text_content()
    date_object = parse(releaseDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year 
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Actors
    movieActors.clearActors()
    actors = actorID.lower().replace('-',' ').title().split('and')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink
            actorPageURL = "https://www.blackvalleygirls.com/girls"
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//a[@data-id="'+sceneID+'"]/img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre("Ebony")
    movieGenres.addGenre("Hardcore")
    movieGenres.addGenre("Interracial")
    movieGenres.addGenre("Teen")
    if len(actors) == 3:
        movieGenres.addGenre("Threesome")
    if len(actors) == 4:
        movieGenres.addGenre("Foursome")
    if len(actors) > 4:
        movieGenres.addGenre("Orgy")

    # Posters/Background
    art.append(detailsPageElements.xpath('//video')[0].get("poster"))
    art.append(detailsPageElements.xpath('//ul[@data-thumbnum="'+sceneID+'"]')[0].get("data-main"))
    for posterUrl in detailsPageElements.xpath('//li[@data-thumbnum="'+sceneID+'"]'):
        art.append(posterUrl.get('data-image'))

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
            except Exception as e:
                Log("posterUrl: "+ posterUrl)
                Log("Error: " + str(e))

    return metadata