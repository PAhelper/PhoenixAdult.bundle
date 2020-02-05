import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    shootID = None
    for splited in searchTitle.split(' '):
        if unicode(splited, 'utf8').isdigit():
            shootID = splited
            break

    if shootID:
        url = '/shoot/' + shootID
        detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + url, headers={'Cookie': 'viewing-preferences=straight%2Cgay'})

        titleNoFormatting = detailsPageElements.xpath('//h1[@class="shoot-title"]')[0].text_content().strip()[:-1]
        releaseDate = parse(detailsPageElements.xpath('//div[@class="columns"]/div[@class="column"]/p')[0].text_content().strip()[6:]).strftime('%Y-%m-%d')
        curID = url.replace('/','_').replace('?','!')

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s [%s] %s' % (shootID, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=100, lang=lang))
    else:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
        for searchResult in searchResults.xpath('//div[@class="shoot-card scene"]'):
            titleNoFormatting = searchResult.xpath('.//img')[0].get('alt').strip()
            curID = searchResult.xpath('.//a[@class="shoot-link"]')[0].get('href').replace('/','_').replace('?','!')
            releaseDate = parse(searchResult.xpath('.//div[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            shootID = searchResult.xpath('.//span[@class="favorite-button"]')[0].get('data-id')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s [%s] %s' % (shootID, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url, headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
    art = []

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="description"]')[1].text_content().strip().replace('\n',' ')
    
    # Tagline
    channel = detailsPageElements.xpath('//div[contains(@class,"shoot-logo")]')[0].text_content().strip()
    if "boundgangbangs" in channel:
        tagline = "Bound Gangbangs"
    elif "brutalsessions" in channel:
        tagline = "Brutal Sessions"
    elif "devicebondage" in channel:
        tagline = "Device Bondage"
    elif "familiestied" in channel:
        tagline = "Families Tied"
    elif "hardcoregangbang" in channel:
        tagline = "Hardcore Gangbang"
    elif "hogtied" in channel:
        tagline = "Hogtied"
    elif "kinkfeatures" in channel:
        tagline = "Kink Features"
    elif "kinkuniversity" in channel:
        tagline = "Kink University"
    elif "publicdisgrace" in channel:
        tagline = "Public Disgrace"
    elif "sadisticrope" in channel:
        tagline = "Sadistic Rope"
    elif "sexandsubmission" in channel:
        tagline = "Sex and Submission"
    elif "thetrainingofo" in channel:
        tagline = "The Training of O"
    elif "theupperfloor" in channel:
        tagline = "The Upper Floor"
    elif "waterbondage" in channel:
        tagline = "Water Bondage"
    elif "everythingbutt" in channel:
        tagline = "Everything Butt"
    elif "footworship" in channel:
        tagline = "Foot Worship"
    elif "fuckingmachines" in channel:
        tagline = "Fucking Machines"
    elif "tspussyhunters" in channel:
        tagline = "TS Pussy Hunters"
    elif "tsseduction" in channel:
        tagline = "TS Seduction"
    elif "ultimatesurrender" in channel:
        tagline = "Ultimate Surrender"
    elif "30minutesoftorment" in channel:
        tagline = "30 Minutes of Torment"
    elif "boundgods" in channel:
        tagline = "Bound Gods"
    elif "boundinpublic" in channel:
        tagline = "Bound in Public"
    elif "buttmachineboys" in channel:
        tagline = "Butt Machine Boys"
    elif "menonedge" in channel:
        tagline = "Men on Edge"
    elif "nakedkombat" in channel:
        tagline = "Naked Kombat"
    elif "divinebitches" in channel:
        tagline = "Divine Bitches"
    elif "electrosluts" in channel:
        tagline = "Electrosluts"
    elif "meninpain" in channel:
        tagline = "Men in Pain"
    elif "whippedass" in channel:
        tagline = "Whipped Ass"
    elif "wiredpussy" in channel:
        tagline = "Wired Pussy"
    elif "chantasbitches" in channel:
        tagline = "Chantas Bitches"
    elif "fuckedandbound" in channel:
        tagline = "Fucked and Bound"
    elif "captivemale" in channel:
        tagline = "Captive Male"
    else:
        tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Studio
    if tagline == "Chantas Bitches" or tagline == "Fucked and Bound" or tagline == "Captive Male":
        metadata.studio = 'Twisted Factory'
    else:
        metadata.studio = 'Kink'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="shoot-title"]')[0].text_content().strip()[:-1]

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//p[@class="tag-list category-tag-list"]//a')
    for genreLink in genres:
        genreName = genreLink.text_content().strip().title()
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//p[@class="starring" and contains(text(),"With:")]//a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
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
    date = detailsPageElements.xpath('//div[@class="columns"]/div[@class="column"]/p')[0].text_content().strip()
    date = date[6:]
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    #Posters
    xpaths = [
        '//video/@poster',
        '//div[@class="player"]//img/@src',
        '//div[@id="previewImages"]//img/@data-image-file'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if(width > 100 and idx > 1):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
