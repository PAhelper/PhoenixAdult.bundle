import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    i = 0
    for searchResult in searchResults.xpath('//div[@class="card text-white bg-dark m-1"]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].get("title")
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//div[@class="d-flex p-0 m-0 lh-1 pb-1"]//small')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + str(i) + "|" + str(encodedTitle), name = titleNoFormatting + " [DDFNetwork] " + releaseDate, score = score, lang = lang ))
        i = i + 1
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?'))
    indice = str(metadata.id).split("|")[2]
    titre_search=str(metadata.id).split("|")[3]
    # siteNum = str(metadata.id).split("|")[1]
    art = []
    searchcovers = HTML.ElementFromURL('https://ddfnetwork.com/videos/freeword/' + titre_search )
    j = int(indice)
    k=0
    for searchcover in searchcovers.xpath('//div[@class="card text-white bg-dark m-1"]/a') :
        coverURL = searchcover.xpath('//div[@class="card text-white bg-dark m-1"]/a/img')[k].get('data-src')
        if k == j:
            Good_CoverURL = coverURL
        k = k + 1
    Log('Good Cover URL ' + Good_CoverURL)

    # Studio
    metadata.studio = "DDFProd"

    # Title
    try:
        metadata.title = detailsPageElements.xpath('//div[@id="video-specs"]/h1')[0].text_content()
    except:
        pass

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@id="descriptionBoxMobile"]/p')[0].text_content().strip()
    except:
        pass

    # Tagline / Collection
    try:
        itempropURL = detailsPageElements.xpath('//meta[@itemprop="url"]')[0].get('content').strip()
        if "ddfhardcore" in itempropURL:
            tagline = "DDF Hardcore"
        elif "ddfbusty" in itempropURL:
            tagline = "DDFBusty"
        elif "ddfxtreme" in itempropURL:
            tagline = "DDF Xtreme"
        elif "handsonhardcore" in itempropURL:
            tagline = "Hands on Hardcore"
        elif "houseoftaboo" in itempropURL:
            tagline = "House of Taboo"
        elif "onlyblowjob" in itempropURL:
            tagline = "Only Blowjob"
        elif "hotlegsandfeet" in itempropURL:
            tagline = "Hot Legs & Feet"
        elif "eurogirlsongirls" in itempropURL:
            tagline = "Euro Girls on Girls"
        elif "1by-day" in itempropURL:
            tagline = "1By-Day"
        elif "cherryjul" in itempropURL:
            tagline = "Cherry Jul"
        elif "ddfnetworkvr" in itempropURL:
            tagline = "DDF Network VR"
        elif "euroteenerotica" in itempropURL:
            tagline = "Euro Teen Erotica"
        elif "sandysfantasies" in itempropURL:
            tagline = "Sandy's Fantasies"
        elif "eveangelofficial" in itempropURL:
            tagline = "Eve Angel Official"
        elif "sexvideocasting" in itempropURL:
            tagline = "Sex Video Casting"
        elif "hairytwatter" in itempropURL:
            tagline = "Hairy Twatter"
        else:
            tagline = str(PAsearchSites.getSearchSiteName(siteID).strip())
    except:
        tagline = str(PAsearchSites.getSearchSiteName(siteID).strip())

    metadata.tagline = tagline
    metadata.collections.clear()
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@class="btn btn-light-tag"]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="d-flex col-12 col-md-8"]//div[2]//p')[0].text_content().strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h5[@class="card-title mb-0"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = actorLink.get("href")
                actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + actorPageURL)
                actorPhotoURL = 'http:' + actorPage.xpath('//div[@class="card nomargin"]/img')[0].get("data-src")
            except:
                actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Artwork
    # Posters

    posters = detailsPageElements.xpath('//img[@class="card-img-top"]')
    for poster in posters:
        artURL = poster.get("src").replace("/thu/", "/fulm/")
        art.append(artURL)
        Log('art.append: ' + artURL)


    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if (width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(
                        HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
                if (width > 100):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(
                        HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
                j = j + 1
            except:
                pass

    return metadata