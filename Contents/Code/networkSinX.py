import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="view_grid--container"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="video_item--content with-badge"]/a')[0].get('title')
        curID = searchResult.xpath('.//div[@class="video_item--content with-badge"]/a')[0].get('href').replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Pissing in Action] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    temp = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    url = 'https://www.sinx.com' + temp
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'SinX'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="title--3"]')[0].text_content().strip()

    # Summary
    summary = detailsPageElements.xpath('//div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/p')[0].text_content().strip()
    metadata.summary = summary
    # Log("Summary:" + metadata.summary)
    
    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div/section[4]/div/p/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[2]/div[1]/div[3]/div[1]/ul/li[1]')[0].text_content().strip()
    #Log("Date:" + date)
    if len(date) > 0:
        date_object = datetime.strptime(date, '%d %b %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div/figure/figcaption/h4')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            if len(actors) == 1:
                actorPhotoURL = detailsPageElements.xpath('//div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div/figure/div/img')[0].get("src")
            if len(actors) > 1:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    # Director

    ### Posters and artwork ###
    # Posters
    posters = detailsPageElements.xpath('//div[2]/div[1]/div[1]/a/div[1]/img')
    posterNum = 1
    Log(str(len(posters)))
    for poster in posters:
        posterURL = poster.get("src")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum += 1
    
#    j = 1
#    Log("Artwork found: " + str(len(art)))
#    for posterUrl in art:
#        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
#            #Download image file for analysis
#            try:
#                img_file = urllib.urlopen(posterUrl)
#                im = StringIO(img_file.read())
#                resized_image = Image.open(im)
#                width, height = resized_image.size
#                #Add the image proxy items to the collection
#                if width > 1 or height > width:
#                    # Item is a poster
#                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
#                if width > 100 and width > height:
#                    # Item is an art item
#                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
#                    # and Item is a poster
#                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
#                j = j + 1
#            except:
#                pass

    return metadata