import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    if siteNum != 670: # If it's any of the sites besides TushyRaw that have a search function, let's use that
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
        for searchResult in searchResults.xpath('//article[@class="videolist-item"]'):
            titleNoFormatting = searchResult.xpath('.//h4[@class="videolist-caption-title"]')[0].text_content()
            curID = searchResult.xpath('.//a[contains(@class,"videolist-link")]')[0].get('href')
            curID = curID.replace('/','_').replace('?','!')
            releaseDate = parse(searchResult.xpath('.//div[@class="videolist-caption-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))

        # I'm getting redirected to https://beta.blacked.com for searches, unsure if everybody else is; this should pull results from the beta search:
        for searchResult in searchResults.xpath('//div[@class="pb6v16-1 fNpwyc"]'):
            titleNoFormatting = searchResult.xpath('.//img')[0].get('alt')
            curID = searchResult.xpath('.//a')[0].get('href')
            curID = curID.replace('/','_').replace('?','!')
            score = 102 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            titleNoFormatting = titleNoFormatting + " [" + PAsearchSites.searchSites[siteNum][1] + "]"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    else: # Special parsing for TushyRaw exact match until they get a search function put in
        encodedTitle = searchTitle.lower().strip().replace(' ','-')
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + '/' + encodedTitle)
        titleNoFormatting = searchResults.xpath('//h1[@data-test-component="VideoTitle"]')[0].text_content()
        curID = ("/"+encodedTitle).replace('/','_').replace('?','!')
        bigScript = searchResults.xpath('//footer/following::script[1]')[0].text_content()
        alpha = bigScript.find('"releaseDate":"')+15
        omega = bigScript.find('"',alpha)
        date = bigScript[alpha:omega]
        releaseDate = parse(date).strftime('%Y-%m-%d')
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Studio
    metadata.studio = "Strike 3"

    # Tagline (Site)
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)

    # Collections (Site and sometimes others like DVD name or series name)
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Summary
    try:
        paragraph = detailsPageElements.xpath('//span[@class="moreless js-readmore"]')[0].text_content().strip()
    except:
        paragraph = detailsPageElements.xpath('//meta[@name="description"]')[0].get('content').strip()
    metadata.summary = paragraph

    # Title
    metadata.title = detailsPageElements.xpath('//*[@id="castme-title"] | //h1[@data-test-component="VideoTitle"]')[0].text_content().strip()

    # Release Date
    try:
        date = detailsPageElements.xpath('//span[@class="right"]/span[@class="info"] | //span[@class="player-description-detail"]/span[@class="info"]')[0].text_content()
        date_object = datetime.strptime(date, '%B %d, %Y')
    except:
        bigScript = detailsPageElements.xpath('//footer/following::script[1]')[0].text_content()
        alpha = bigScript.find('"releaseDate":"')+15
        omega = bigScript.find('"',alpha)
        date = bigScript[alpha:omega]
        date_object = parse(date)
        Log("Must be beta...")
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year    

    # Genres
    movieGenres.clearGenres()
    try:
        alpha = bigScript.find('"tags":[')+8
        omega = bigScript.find(']',alpha)
        genres = bigScript[alpha:omega].strip('"').split(',')
        for genre in genres:
            movieGenres.addGenre(genre.replace('"','').lower())
    except:
        # No Source for Genres, add manual
        if 'Blacked' in metadata.tagline:
            movieGenres.addGenre("Interracial")
        if 'Tushy' in metadata.tagline:
            movieGenres.addGenre("Anal")
        if 'Vixen' in metadata.tagline:
            movieGenres.addGenre("Boy Girl")
            movieGenres.addGenre("Caucasian Men")
            movieGenres.addGenre("Glamcore")
        movieGenres.addGenre("Hardcore")
        movieGenres.addGenre("Heterosexual")

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//p[@id="castme-subtitle"]/a | //span[@id="castme-subtitle"]/a | //div[@data-test-component="VideoModels"]/a')

    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
            try:
                actorPhotoURL = actorPage.xpath('//img[@class="thumb-img"]')[0].get("src")
            except:
                actorBigScript = actorPage.xpath('//footer/following::script[1]')[0].text_content()
                alpha = actorBigScript.find('"src":"')+7
                omega = actorBigScript.find('"',alpha)
                actorPhotoURL = actorBigScript[alpha:omega].decode('unicode_escape')
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID)+actorPhotoURL
            movieActors.addActor(actorName,actorPhotoURL)

    # Director
    metadata.directors.clear()
    director = metadata.directors.new()
    director.name = 'Greg Lansky'

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    try:
        art.append(detailsPageElements.xpath('//img[contains(@class,"player-img")]')[0].get("src"))
    except:
        # This is where beta.*.com code will go
        alpha = bigScript.find('"width":1200,"height":800,"src"')+33
        omega = bigScript.find('"',alpha)
        background = bigScript[alpha:omega].decode('unicode_escape')
        if 'http' not in background:
            background = PAsearchSites.getSearchBaseURL(siteID)+background
        Log("background: "+background)
        art.append(background)

    try:
        posters = detailsPageElements.xpath('//div[@class="swiper-slide"]')
        posterNum = 1
        for posterCur in posters:
            posterURL = posterCur.xpath('.//img[@class="swiper-content-img"]')[0].get("src")
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            posterNum = posterNum + 1
    except:
        # This is where beta.*.com code will go
        i = 1
        alpha = 0
        omega = 0
        imageCount = bigScript.count('"width":1200,"height":800,"src"')
        while i <= imageCount:
            alpha = bigScript.find('"width":1200,"height":800,"src"',omega)+33
            omega = bigScript.find('"',alpha)
            posterUrl = bigScript[alpha:omega].decode('unicode_escape')
            if 'http' not in posterUrl:
                posterUrl = PAsearchSites.getSearchBaseURL(siteID)+posterUrl
            Log("artwork: "+posterUrl)
            art.append(posterUrl)
            i = i + 1

    # Posters
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
            except:
                pass


    return metadata
