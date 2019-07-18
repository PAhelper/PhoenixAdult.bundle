import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    if searchDate:
        url = PAsearchSites.getSearchSearchURL(siteNum) + "date/" + searchDate + "/" + searchDate
        searchResults = HTML.ElementFromURL(url)
        for searchResult in searchResults.xpath('//div[contains(@class, "content-grid-item")]'):
            titleNoFormatting = searchResult.xpath('//a[@class= "title"]')[0].text_content().strip()
            curID = searchResult.xpath('//a[@class="title"]')[0].get('href').split("/")[3]
            Log('curID: ' + str(curID))
            releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))

    if unicode(searchTitle, 'utf-8').isnumeric():
        url = PAsearchSites.getSearchBaseURL(siteNum) + "/video/watch/" + searchTitle.lower().replace(" ","-").replace("'","-")
        searchResults = HTML.ElementFromURL(url)

        searchResult = searchResults.xpath('//div[contains(@class, "content-pane-title")]')[0]
        titleNoFormatting = searchResult.xpath('//h2')[0].text_content()
        curID = searchTitle.lower().replace(" ","-").replace("'","-")
        releaseDate = parse(searchResult.xpath('//span[@class= "date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        score = 100
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + '/video/watch/' + str(metadata.id).split("|")[0])
    art = []

    # Title
    title = detailsPageElements.xpath('//div[contains(@class, "content-pane-title")]/h2')[0].text_content().strip()
    metadata.title = title
    #episode = title.split(' - ')[-1].strip()
    #Log("Sort Title: "+episode + " - " + title[:title.rfind('-')])
    #metadata.sort_title = episode + " - " + title[:title.rfind('-')]

    # Studio
    metadata.studio = "Nubiles"

    # Summary
    try:
        paragraphs = detailsPageElements.xpath('//div[contains(@class, "content-pane-container")]//p')
        pNum = 0
        summary = ""
        for paragraph in paragraphs:
            if pNum >= 0 and pNum < (len(paragraphs)):
                summary = summary + '\n\n' + paragraph.text_content()
            pNum += 1
    except:
        pass
    if summary == '':
        try:
            summary = detailsPageElements.xpath('//div[@class="video-description"]/article')[0].text_content().strip()
        except:
            pass
    metadata.summary = summary.strip()

    # Collections / Tagline
    siteName = detailsPageElements.xpath('//div[contains(@class, "content-pane")]//a[@class= "site-link"]')[0].text_content().strip().replace(".com", "")
    if "stepsiblingscaught" in siteName.lower():
        tagline = "Step Siblings Caught"
    elif "momsteachsex" in siteName.lower():
        tagline = "Moms Teach Sex"
    elif "badteenspunished" in siteName.lower():
        tagline = "Bad Teens Punished"
    elif "princesscum" in siteName.lower():
        tagline = "Princess Cum"
    elif "nubilesunscripted" in siteName.lower():
        tagline = "Nubiles Unscripted"
    elif "nubilescasting" in siteName.lower():
        tagline = "Nubiles Casting"
    elif "petitehdporn" in siteName.lower():
        tagline = "Petite HD Porn"
    elif "driverxxx" in siteName.lower():
        tagline = "Driver XXX"
    elif "petiteballerinasfucked" in siteName.lower():
        tagline = "Petite Ballerinas Fucked"
    elif "teacherfucksteens" in siteName.lower():
        tagline = "Teacher Fucks Teens"
    elif "bountyhunterporn" in siteName.lower():
        tagline = "Bountyhunter Porn"
    elif "daddyslilangel" in siteName.lower():
        tagline = "Daddy's Lil Angel"
    elif "myfamilypies" in siteName.lower():
        tagline = "My Family Pies"
    elif "nubiles.net" in siteName.lower():
        tagline = "Nubiles"
    elif "brattysis" in siteName.lower():
        tagline = "Bratty Sis"
    elif "anilos" in siteName.lower():
        tagline = "Anilos"
    elif "hotcrazymess" in siteName.lower():
        tagline = "Hot Crazy Mess"
    elif "nfbusty" in siteName.lower():
        tagline = "NF Busty"
    elif "thatsitcomporn" in siteName.lower():
        tagline = "That Sitcom Show"
    elif "detentiongirls" in siteName.lower():
        tagline = "Detention Girls"
    elif "nubileset" in siteName.lower():
        tagline = "Nubiles ET"
    else:
        tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Date
    date = detailsPageElements.xpath('//div[contains(@class, "content-pane")]//span[@class= "date"]')[0].text_content().strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class, "content-pane-performers")]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL((PAsearchSites.getSearchBaseURL(siteID)+actorPageURL))
            actorPhotoURL = "http:"+actorPage.xpath('//div[contains(@class, "model-profile")]//img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)
    if "Logan Long" in summary:
        movieActors.addActor('Logan Long','')
    elif "Patrick Delphia" in summary:
        movieActors.addActor('Patrick Delphia','')
    elif "Seth Gamble" in summary:
        movieActors.addActor('Seth Gamble','')
    elif "Alex D." in summary:
        movieActors.addActor('Alex D.','')
    elif "Lucas Frost" in summary:
        movieActors.addActor('Lucas Frost','')
    elif "Van Wylde" in summary:
        movieActors.addActor('Van Wylde','')
    elif "Tyler Nixon" in summary:
        movieActors.addActor('Tyler Nixon','')
    elif "Logan Pierce" in summary:
        movieActors.addActor('Logan Pierce','')
    elif "Johnny Castle" in summary:
        movieActors.addActor('Johnny Castle','')
    elif "Damon Dice" in summary:
        movieActors.addActor('Damon Dice','')
    elif "Scott Carousel" in summary:
        movieActors.addActor('Scott Carousel','')
    elif "Dylan Snow" in summary:
        movieActors.addActor('Dylan Snow','')
    elif "Michael Vegas" in summary:
        movieActors.addActor('Michael Vegas','')
    elif "Xander Corvus" in summary:
        movieActors.addActor('Xander Corvus','')
    elif "Chad White" in summary:
        movieActors.addActor('Chad White','')

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="categories"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Posters
    background = "http:" + detailsPageElements.xpath('//video')[0].get('poster')
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Scene cover from related photosets
    try:
        posters = detailsPageElements.xpath('//figure[@class=" "]')
        for poster in posters:
            posterName = poster.xpath('//a[@class= "title"]/text()')
            if posterName == title:
                Log('Cover image found')
                posterLink = "http:" + poster.xpath('//img').get("src")
                metadata.posters[posterLink] = Proxy.Preview(HTTP.Request(posterLink, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    try:
        photoPageURL = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//div[contains(@class, "content-pane-related-links")] " and contains(text(),"Pics")]')[0].get('href')
        Log("photoPageURL: " + str(photoPageURL))
        photoPageElements = HTML.ElementFromURL(photoPageURL)
        for posterUrl in photoPageElements.xpath('//div[@class= "content-grid masonry "]//img'):
            art.append("http:" + posterUrl.get('src'))
    except:
        pass
    
    if len(art)is 0:
        try:
            photoPageURL = "https://nubiles-porn.com/photo/gallery/" + str(metadata.id).split("|")[0]
            Log("photoPageURL: " + str(photoPageURL))
            photoPageElements = HTML.ElementFromURL(photoPageURL)
            for posterUrl in photoPageElements.xpath('//div[@class= "content-grid masonry "]//img'):
                art.append("https:" + posterUrl.get('src'))
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
