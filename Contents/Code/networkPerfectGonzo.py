import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    Log('searchtitle ' + searchTitle) 
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle )
    for searchResult in searchResults.xpath('//div[@class="itemm"]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].get("title")
        releaseDate = parse(searchResult.xpath('.//span[@class="nm-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        subSite = searchResult.xpath('.//img[@class="domain-label"]')[0].get('src')
        if 'allinternal' in subSite:
            subSite = '/AllInternal'
        elif 'asstraffic' in subSite:
            subSite = '/AssTraffic'
        elif 'givemepink' in subSite:
            subSite = '/GiveMePink'
        elif 'primecups' in subSite:
            subSite = '/PrimeCups'
        elif 'fistflush' in subSite:
            subSite = '/FistFlush'
        elif 'cumforcover' in subSite:
            subSite = '/CumForCover'
        elif 'tamedteens' in subSite:
            subSite = '/TamedTeens'
        elif 'spermswap' in subSite:
            subSite = '/SpermSwap'
        elif 'milfthing' in subSite:
            subSite = '/MilfThing'
        elif 'interview' in subSite:
            subSite = '/Interview'
        else:
            subSite = PAsearchSites.getSearchSiteName(siteNum)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Perfect Gonzo"+subSite+"] " + releaseDate , score = score, lang = lang ))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    #Studio
    metadata.studio = "Perfect Gonzo"

    # Title
    metadata.title = detailsPageElements.xpath('//h2')[0].text_content().strip()

    # Summary
    paragraph = detailsPageElements.xpath('//div[@class="col-sm-8 col-md-8 no-padding-side"]/p')[0].text_content().strip()
    metadata.summary = paragraph

    # Tagline and Collection(s)
    subSite = detailsPageElements.xpath('.//img[@class="domain-label"]')[0].get('src')
    if 'allinternal' in subSite:
        tagline = 'All Internal'
    elif 'asstraffic' in subSite:
        tagline = 'Ass Traffic'
    elif 'givemepink' in subSite:
        tagline = 'Give Me Pink'
    elif 'primecups' in subSite:
        tagline = 'Prime Cups'
    elif 'fistflush' in subSite:
        tagline = 'Fist Flush'
    elif 'cumforcover' in subSite:
        tagline = 'Cum For Cover'
    elif 'tamedteens' in subSite:
        tagline = 'Tamed Teens'
    elif 'spermswap' in subSite:
        tagline = 'Sperm Swap'
    elif 'milfthing' in subSite:
        tagline = 'Milf Thing'
    elif 'interview' in subSite:
        tagline = 'Perfect Gonzo Interview'
    else:
        tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="col-sm-8 col-md-8 no-padding-side tag-container"]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="col-sm-6 col-md-6 no-padding-left no-padding-right text-right"]/span')[0].text_content().replace('Added','').strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="col-sm-3 col-md-3 col-md-offset-1 no-padding-side"]/p/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get('href')
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="col-md-8 bigmodelpic"]/img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    ### Artwork ###

    # Background
    art.append(detailsPageElements.xpath('//video')[0].get("poster"))

    # Photos
    photos = []
    for poster in detailsPageElements.xpath('//ul[@class="bxslider_screenshots"]//img'):
        try:
            photos.append(poster.get('src'))
        except:
            photos.append(poster.get('data-original'))
    for x in range(10):
        art.append(photos[random.randint(1,len(photos))])

    # Screencaps
    vidcaps = []
    for poster in detailsPageElements.xpath('//ul[@class="bxslider_screenshots"]//img'):
        try:
            vidcaps.append(poster.get('src'))
        except:
            vidcaps.append(poster.get('data-original'))
    for x in range(10):
        art.append(vidcaps[random.randint(1,len(vidcaps))])

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
