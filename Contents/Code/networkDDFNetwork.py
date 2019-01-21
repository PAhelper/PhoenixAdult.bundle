import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    i = 0
    for searchResult in searchResults.xpath('//div[@class="card m-1"]/a'):
        Log('Url : ' + str(searchResult.get('href')))
        titleNoFormatting = searchResult.get("title")
        Log('Titre ' + str(titleNoFormatting))
        releaseDate = searchResults.xpath('//div[@class="card-footer d-flex justify-content-between"]//small')[i].text_content().strip()
        #coverURL = searchResults.xpath('//div[@class="card m-1"]/a/img')[i].get('data-src')
        #Log('CoverUrl : ' + str(coverURL) )
        curID = searchResult.get('href').replace('/','_')
        Log('CurID : ' + curID )
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID) + "|" + str(i) + "|" + str(encodedTitle) , name = titleNoFormatting + " [DDFNetwork] " + releaseDate , score = score, lang = lang ))
        i = i + 1
    return results



def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('_','/')
    Log('temp :' + temp)
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    Log('Url : ' + url)
    detailsPageElements = HTML.ElementFromURL(url)
    indice = str(metadata.id).split("|")[2]
    titre_search=str(metadata.id).split("|")[3]
    siteNum = str(metadata.id).split("|")[1]
    searchcovers = HTML.ElementFromURL('https://ddfnetwork.com/videos/freeword/' + titre_search )
    j = int(indice)
    k=0
    for searchcover in searchcovers.xpath('//div[@class="card m-1"]/a') :
        coverURL = searchcover.xpath('//div[@class="card m-1"]/a/img')[k].get('data-src')
        if k == j:
            Good_CoverURL = coverURL
        k = k + 1
    Log('Good Cover URL ' + Good_CoverURL )
    paragraph = detailsPageElements.xpath('//p[@class="box-container"]')[0].text_content()
    metadata.summary = paragraph.strip()

    metadata.studio="DDFNetwork"
    tagline = "DDFNetwork"
    tagline = tagline.strip()
    metadata.tagline = tagline

    metadata.collections.clear()
    collection = str(PAsearchSites.getSearchSiteName(siteID))
    metadata.collections.add(collection)

    metadata.title = detailsPageElements.xpath('//div[@class="px-2 col-12 col-md-7 video-titles "]/h1')[0].text_content()
    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@class="btn btn-light-tag"]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//time')[0].text_content()
    if len(date) > 0:
        date = date.strip()
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h5[@class="card-title mb-1 text-center"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = str(actorLink.text_content().strip())
            actorName = actorName.replace("\xc2\xa0", " ")
            role.name = actorName
            actorPageURL = actorLink.get("href")
            Log('acteur page : ' + actorPageURL)
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + actorPageURL)
            actorPhoto = actorPage.xpath('//div[@class="col-6 col-sm-4 col-md-6 col-xl-5 px-0 card border-0"]/img')[0].get("data-src")
            actorPhotoURL= 'http:' + actorPhoto
            Log('acteur URL img: ' + str(actorPhotoURL))
            movieActors.addActor(actorName,actorPhotoURL)
            role.photo = actorPhotoURL
    #Posters
        background = detailsPageElements.xpath('//div[@class="video-join-box after_video_join"]/a/img')[0].get("src")
        Log("BG DL: " + str(background))
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
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