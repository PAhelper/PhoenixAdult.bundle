import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="shoot search"]'):
        titleNoFormatting = searchResult.xpath('.//img')[0].get('alt').strip()
        curID = searchResult.xpath('.//a[@class="shoot-link"]')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//div[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Kink'
    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="description"]')[0].text_content().strip()
    
    # Tagline
    channel = detailsPageElements.xpath('//div[contains(@class,"shoot-logo")]')[0].text_content().strip()
    if "boundinpublic" in channel:
        tagline = "Bound in Public"
    elif "publicdisgrace" in channel:
        tagline = "Public Disgrace"
    else:
        tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1[@class="shoot-title"]')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//p[@class="starring" and contains(text(),"Tags:")]/a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//p[@class="starring" and contains(text(),"With:")]/a')
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
            actorPhotoURL = actorPage.xpath('//div[@class="model-image"]/img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Director
    director = metadata.directors.new()
    try:
        directors = detailsPageElements.xpath('//p[@class="director"]/a')
        for dirname in directors:
            director.name = dirname.text_content().strip()
    except:
        pass

    # Release Date
    date_object = parse(detailsPageElements.xpath('//div[@class="columns"]/div[@class="column"]/p')[6:].strip())
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    #Posters
    try:
        art.append(detailsPageElements.xpath('//video')[0].get('poster'))
    except:
        pass

    for poster in detailsPageElements.xpath('//div[@class="gallery"]//img'):
        #baseCDN = poster.get('src')[:poster.find(".com")+4]
        art.append("https://cdnp.kink.com"+poster.get('data-image-file'))

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
