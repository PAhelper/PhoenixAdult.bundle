import PAsearchSites
import PAgenres
import PAactors
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//li[@class="thumb"]'):
        titleNoFormatting = searchResult.xpath('.//span[@class="thumb-title"]')[0].text_content().strip()
        curID = searchResult.xpath('.//a[@class="thumb-img"]')[0].get('href').replace('/','_').replace('?','!')
        Log("curID: "+curID)
        releaseDate = parse(searchResult.xpath('.//span[@class="thumb-added"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Pioneer'
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    movieGenres.clearGenres()
    movieActors.clearActors()
    metadata.directors.clear()
    director = metadata.directors.new()
    art = []

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="text-desc"]')[0].text_content().strip()
    
    # Tagline
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="container content"]/div[@class="page-header"]/span[@class="title"]')[0].text_content().strip()

    # Genres
    genres = detailsPageElements.xpath('//div[@class="media-body"]/ul[3]/li/a')
    if len(genres) > 0:
        for genreLink in genres:
            genre = genreLink.text_content()
            movieGenres.addGenre(genre)

    # Actors
    actors = detailsPageElements.xpath('//ul[contains(text(),"Models:")]/li/a')
    if len(actors) > 0:
        if "porn-movie" not in url and len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if "porn-movie" not in url and len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if "porn-movie" not in url and len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="model-box"]/img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Release Date
    date = str(metadata.id).split("|")[2]
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Artwork
    art.append(detailsPageElements.xpath('//img[@class="player-preview"]')[0].get('src'))
    for poster in detailsPageElements.xpath('//a[@class="fancybox img-album"] | //a[@data-fancybox-group="gallery"]'):
        art.append(poster.get('href'))

    j = 1
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
            except Exception as e:
                Log("Error: " + str(e))

    return metadata
