import PAsearchSites
import PAgenres
def tagAleadyExists(tag,metadata):
    for t in metadata.genres:
        if t.lower() == tag.lower():
            return True
    return False

def posterAlreadyExists(posterUrl,metadata):
    for p in metadata.posters.keys():
        Log(p.lower())
        if p.lower() == posterUrl.lower():
            Log("Found " + posterUrl + " in posters collection")
            return True

    for p in metadata.art.keys():
        if p.lower() == posterUrl.lower():
            return True
    return False

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID):
    encodedTitle = encodedTitle.replace('%20a%20','%20')
    i=0
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//a[@class="scene-title notracking"]'):
        Log(str(searchResult.get('href')))
        titleNoFormatting = searchResult.text_content()
        curID = searchResult.get('href').replace('/','_')
        lowerResultTitle = str(titleNoFormatting).lower()
        releaseDate = searchResult.xpath('//time[@class="release-date"]')[i].text_content()
        subSite = searchResult.xpath('//a[@class="release-site notracking"]')[i].text_content().strip()
        site = " [Babes"
        if len(subSite) > 0 and subSite != "Babes":
            site = site + "/" + subSite
        site = site + "] "
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + site + releaseDate, score = score, lang = lang))
        i = i + 1
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Babes'
    temp = str(metadata.id).split("|")[0].replace('_','/')
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//p[@class="section-detail section-detail--description"]')[0].text_content()
    #paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = paragraph.strip()
    tagline = detailsPageElements.xpath('//a[@class="video-bar__release-site"]')[0].text_content()
    metadata.collections.clear()
    tagline = tagline.strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//p[@class="section-detail section-detail--tags last"]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//span[@class="video-info__date"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h2[@class="video-bar__models"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
            actorPhotoURL = "http:" + actorPage.xpath('//img[@class="profile-picture"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    #Posters
    sceneID = detailsPageElements.xpath('//input[@id="sceneid"]')[0].get("value")
    try:
        background = "https://static-hw.babescontent.com/scenes/" + str(sceneID) + "/s970x545.jpg"
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    i = 1
    for i in range(1,10):
        posterUrl = "https://static-hw.babescontent.com/scenes/" + str(sceneID) + "/s310x161_" + str(i) + ".jpg"
        Log("Poster URL: " + posterUrl)
        if not posterAlreadyExists(posterUrl,metadata):
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #posterUrl = posterUrl[:-6] + "01.jpg"
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster

                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i)
                if(width > 100):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i+1)
                i = i + 1

            except:
                pass

    return metadata
