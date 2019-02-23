import PAsearchSites
import PAgenres

def searchSwallowed(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.lower())
    for searchResult in searchResults.xpath('//div[@class="info-wrap"]'):
        titleNoFormatting = searchResult.xpath('./div/div/h3[@class="title"]/a')[0].text_content().strip()
        curID = searchResult.xpath('./div/div/h3[@class="title"]/a')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//time')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))
    return results

def searchTrueAnal(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.lower())
    for searchResult in searchResults.xpath('//div[@class="content-meta"]'):
        titleNoFormatting = searchResult.xpath('./h3[@class="title"]/a')[0].text_content().strip()
        curID = searchResult.xpath('./h3[@class="title"]/a')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))
    return results

def searchNympho(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.lower())
    for searchResult in searchResults.xpath('//div[@class="content-card-info"]'):
        titleNoFormatting = searchResult.xpath('./h4[@class="content-title-wrap"]/a')[0].text_content().strip()
        curID = searchResult.xpath('./h4[@class="content-title-wrap"]/a')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//span[@class="date hidden-xs"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Stepped Up Media'
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class,"desc")]')[0].text_content().strip()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h2[@class="title"]')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('hardcore')
    movieGenres.addGenre('heterosexual')
    if tagline == "Swallowed":
        movieGenres.addGenre('blowjob')
        movieGenres.addGenre('cum swallow')
    elif tagline == "TrueAnal":
        movieGenres.addGenre('anal')
        movieGenres.addGenre('gaping')
    elif tagline == "Nympho":
        movieGenres.addGenre('nympho')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('(//h4[@class="models"])[1]//a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[contains(@class,"model")]/img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)
    movieActors.addActor('Mike Adriano','https://imgs1cdn.adultempire.com/actors/470003.jpg')

    # Release Date
    date = detailsPageElements.xpath('//span[contains(@class,"date")]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    #Posters
    try:
        art.append(detailsPageElements.xpath('//div[@id="trailer-player"]')[0].get('data-screencap'))
    except:
        art.append(detailsPageElements.xpath('//video[@id="ypp-player"]')[0].get('poster'))

    for poster in actorPage.xpath('//a[@href="' + url + '"]//img'):
        art.append(poster.get('src'))
    for poster in actorPage.xpath('//div[@class="thumb-mouseover"]'):
        theStyle = poster.get('style')
        alpha = theStyle.find('http')
        omega = theStyle.find(');',alpha)
        art.append(theStyle[alpha:omega].strip())

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
