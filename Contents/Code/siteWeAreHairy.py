import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="results"]/ul/li'):
        titleNoFormatting = searchResult.xpath('.//p[@class="title"]/a')[0].text_content().strip()
        curID = searchResult.xpath('.//div[@class="top"]/p/a')[0].get('href').replace('_','-').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//p[@class="short"]')[0].text_content().replace('Added:', '').strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [We Are Hairy] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('?','!').replace('-','_')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'We Are Hairy'

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="desc"]/div[1]/p')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="tagline"]/p/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)
    movieGenres.addGenre("Hairy Girls")
    movieGenres.addGenre("Hairy Pussy")

    # Release Date
    date = detailsPageElements.xpath('//span[@class="added"]/time')[0].text_content().strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="meet"]/a/img')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.get('alt').replace('WeAreHairy.com','').strip())
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Director
    director = metadata.directors.new()
    try:
        directors = detailsPageElements.xpath('//div[@class="desc"]/div[2]/p')
        for dirname in directors:
            director.name = dirname.text_content().strip()
    except:
        pass

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = "http:" + detailsPageElements.xpath('//div[@class="moviemain"]/div[1]/a/img')[0].get('src')
        art.append(twitterBG)
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