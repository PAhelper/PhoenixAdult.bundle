import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    i = 0
    for searchResult in searchResults.xpath('//div[@class="card text-white bg-dark m-1"]/a'):
        Log('Url : ' + str(searchResult.get('href')))
        titleNoFormatting = searchResult.get("title")
        Log('Titre ' + str(titleNoFormatting))
        releaseDate = parse(searchResult.xpath('//div[@class="d-flex p-0 m-0 lh-1 pb-1"]//small')[i].text_content().strip()).strftime('%Y-%m-%d')
        #coverURL = searchResults.xpath('//div[@class="card m-1"]/a/img')[i].get('data-src')
        #Log('CoverUrl : ' + str(coverURL) )
        curID = searchResult.get('href').replace('/','_').replace('?','!')
        Log('CurID : ' + curID )
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + str(i) + "|" + str(encodedTitle) , name = titleNoFormatting + " [DDFNetwork] " + releaseDate , score = score, lang = lang ))
        i = i + 1
    return results



def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?'))
    indice = str(metadata.id).split("|")[2]
    titre_search=str(metadata.id).split("|")[3]
    siteNum = str(metadata.id).split("|")[1]
    searchcovers = HTML.ElementFromURL('https://ddfnetwork.com/videos/freeword/' + titre_search )
    j = int(indice)
    k=0
    for searchcover in searchcovers.xpath('//div[@class="card text-white bg-dark m-1"]/a') :
        coverURL = searchcover.xpath('//div[@class="card text-white bg-dark m-1"]/a/img')[k].get('data-src')
        if k == j:
            Good_CoverURL = coverURL
        k = k + 1
    Log('Good Cover URL ' + Good_CoverURL )

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="px-2 col-12 col-md-7 video-titles "]/h1')[0].text_content()

    # Summary
    try:
        summaryp1 = detailsPageElements.xpath('//div[@id="descriptionBox"]/p[2]')[0].text_content().strip()
        summaryp2 = detailsPageElements.xpath('//div[@id="descriptionBox"]/p[3]')[0].text_content().strip()
        summaryp3 = detailsPageElements.xpath('//div[@id="descriptionBox"]/p[4]')[0].text_content().strip()
        summary = summaryp1 + '\n' + summaryp2 + '\n' + summaryp3
    except:
        try:
            summary = detailsPageElements.xpath('//div[@id="descriptionBox"]//p[2]')[0].text_content().strip()
        except:
            try:
                summary = detailsPageElements.xpath('//p[@class="box-container"]')[0].text_content().strip()
            except:
                pass
    metadata.summary = summary


    # Studio
    metadata.studio = "DDFProd"

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
    date = detailsPageElements.xpath('//time')[0].text_content().strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h2[@class="actors mb-2"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + actorPageURL)
            actorPhotoURL = 'http:' + actorPage.xpath('//div[@class="card nomargin"]/img')[0].get("data-src")
            movieActors.addActor(actorName,actorPhotoURL)

    #Posters
        try:
            background = detailsPageElements.xpath('//div[@class="video-join-box after_video_join"]/a/img')[0].get("src")
            Log("BG DL: " + str(background))
            metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
        except:
            pass
    i = 1
    #Searchposter = detailsPageElements.xpath('//div[@class="cell content_tab"]/a')[0].get("href")
    for posterUrls in detailsPageElements.xpath('//img[@class="card-img-top"]'):
        posterUrl = posterUrls.get("src")
        Log('Url poster ' + str(posterUrl))
            #Download image file for analysis
        try:
            if i == 1:
                posterUrl = Good_CoverURL
            img_file = urllib.urlopen(posterUrl)
            im = StringIO(img_file.read())
            resized_image = Image.open(im)
            width, height = resized_image.size
            #posterUrl = posterUrl[:-6] + "01.jpg"
            #Add the image proxy items to the collection
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i)
            i = i + 1
            if i>10:
                break


        except:
            pass


    return metadata