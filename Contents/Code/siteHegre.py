import PAsearchSites
import PAgenres


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    if searchDate:
        searchYear = '&year='+parse(searchDate).strftime('%Y')
    else:
        searchYear = ''
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + searchYear)
    for searchResult in searchResults.xpath('//div[contains(@class,"item")]'):
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        if "_films_" in curID or "_massage_" in curID:
            titleNoFormatting = searchResult.xpath('.//img')[0].get('alt').strip()
            releaseDate = parse(searchResult.xpath('.//div[@class="details"]/span[last()]')[0].text_content().strip()).strftime('%Y-%m-%d')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Hegre'
    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Title
    try:
        metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    except:
        try:
            metadata.title = detailsPageElements.xpath('//meta[@property="og:title"]')[0].text_content().strip()
        except:
            try:
                metadata.title = detailsPageElements.xpath('//meta[@name="twitter:title"]')[0].text_content().strip()
            except:
                pass

    # Summary
    summary = detailsPageElements.xpath('//div[@class="record-description-content record-box-content"]')[0].text_content().strip()
    metadata.summary = summary[:summary.find('Runtime')].strip()

    # Tagline
    tagline = "Hegre"
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@class="tag"]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[@class="record-model"]')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.get('title').strip())
            actorPhotoURL = actorLink.xpath('.//img')[0].get('src').replace('240x','480x')
            movieActors.addActor(actorName,actorPhotoURL)

    # Director
    director = metadata.directors.new()
    director.name = 'Petter Hegre'
    director.photo = 'https://img.discogs.com/TafxhnwJE2nhLodoB6UktY6m0xM=/fit-in/180x264/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-2236724-1305622884.jpeg.jpg'

    # Release Date
    date = detailsPageElements.xpath('//span[@class="date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    #Posters
    try:
        art.append(detailsPageElements.xpath('//meta[@name="twitter:image"]')[0].get('content').replace('board-image','poster-image').replace('1600x','640x'))
    except:
        pass

    try:
        art.append(detailsPageElements.xpath('//meta[@name="twitter:image"]')[0].get('content').replace('1600x','1920x'))
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
