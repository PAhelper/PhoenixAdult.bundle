import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="video_list"]//div[@style="position:relative;"]'):
        titleNoFormatting = searchResult.xpath('.//div/a[@class="title"]')[0].text_content().strip()
        curID = searchResult.xpath('.//a[@class="img"]')[0].get('href').replace('/','_').replace('?','!')
        if searchDate:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d')
        else:
            releaseDate = ''
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " [VIPissy" + "] ", score = score, lang = lang))

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
    metadata.studio = 'VIPissy'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="update_title"]/h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="con_left"]/p')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genreList = detailsPageElements.xpath('//div[@class="con_left"]/div')[0].text_content().strip()
    Log("Genres: " + genreList)
    genres = genreList.split('Tags:')[1].split('Rating:')[0].split(' - ')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.strip().lower()
            movieGenres.addGenre(genreName)
    movieGenres.addGenre("Piss Play")

    # Release Date
    date = str(metadata.id).split("|")[2]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
        Log("Date from file")

    # Actors
    actorList = genreList
    actors = actorList.split('Starring:')[1].split('Duration:')[0].split(' - ')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.strip())
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Director

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//div[@class="update_box"]/img')[0].get('src')
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