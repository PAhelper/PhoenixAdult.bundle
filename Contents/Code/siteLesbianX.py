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

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchsiteID):
    searchResults = HTML.ElementFromURL('https://www.lesbianx.com/en/search/' + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="tlcTitle"]//a'):
        Log(str(searchResult.get('href')))
        titleNoFormatting = searchResult.text_content()
        curID = searchResult.get('href').replace('/','_')
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Lesbian X]", score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'XEmpire'
    temp = str(metadata.id).split("|")[0].replace('_','/')
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//div[@class="sceneDesc bioToRight showMore"]')[0].text_content().strip()
    #paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    paragraph = paragraph[20:]
    metadata.summary = paragraph.strip()
    metadata.collections.clear()
    tagline = "LesbianX"
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="sceneCol sceneColCategories"]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//div[@class="updatedDate"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = datetime.strptime(date, '%m-%d-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    actors = detailsPageElements.xpath('//div[@class="sceneCol sceneColActors"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = str(actorLink.text_content().strip())
            #actorName = actorName.replace("\xc2\xa0", " ")
            role.name = actorName
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]')[0].get("src")
            role.photo = actorPhotoURL

    #Posters
    i = 1
    try:
        background = detailsPageElements.xpath('//meta[@name="twitter:image"]')[0].get('content').replace("https:","http:")
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    photoPageUrl = PAsearchSites.getSearchBaseURL(siteID)+detailsPageElements.xpath('//a[@class="controlButton GA_Track GA_Track_Action_Pictures GA_Track_Category_Player GA GA_Click GA_Id_ScenePlayer_Pictures"]')[0].get('href')
    photoPage = HTML.ElementFromURL(photoPageUrl)
    unlockedPhotos = photoPage.xpath('//a[@class="imgLink"]')
    for unlockedPhoto in unlockedPhotos:
        posterUrl = unlockedPhoto.get('href').replace("https:","http:")
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
