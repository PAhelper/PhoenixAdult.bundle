import PAsearchSites
import PAgenres

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
    searchResults = HTML.ElementFromURL('https://gloryholeswallow.com/newtour/search.php?query=' + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="update_details"]'):
        detailsPage = searchResult.xpath('./a[2]')[0].get('href')
        Log(str(detailsPage))
        titleNoFormatting = searchResult.xpath('./a[2]')[0].text_content().strip()
        if titleNoFormatting[0].isdigit():
            titleNoFormatting = searchResult.xpath('./span[@class="update_models"]/a[1]')[0].text_content().strip() + " (" + titleNoFormatting + ")"
        try:
            titleNoFormatting = titleNoFormatting + " w/" +searchResult.xpath('./span[@class="update_models"]/a[2]')[0].text_content().strip()
        except:
            pass
        Log(str(titleNoFormatting))
        releaseDate = parse(searchResult.xpath('.//div[@class="cell update_date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log(str(releaseDate))
        curID = detailsPage.replace('/','_').replace('?','!')
        Log(curID + "|" + str(siteNum))
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [GloryHoleSwallow] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'GloryHoleSwallow'
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[@class="latest_update_description"]')[0].text_content().strip()
    tagline = 'GloryHoleSwallow'
    metadata.collections.clear()
    tagline = tagline.strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    # Unfortunately the information just isn't there to make or even build a title:
    # https://gloryholeswallow.com/newtour/index.php?id=713
    # In that example, the girl doesn't even have a name in the image URLs. There's no description, there's nothing to use. Unfortunately I don't see how this site is possible to add :(
    #metadata.title = detailsPageElements.xpath('//h2[@class="H_underline"]')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//span[@class="tour_update_tags"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//span[@class="update_date"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h5[@class="featuring_model"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            sceneImg = detailsPageElements.xpath('//div[@class="grid_10 alpha"]/a/img')[0].get('src')
            actorFullName = sceneImg.split('/')[4]
            actorFirstName = actorName.split(' ')[0]
            if actorFirstName.lower() == actorFullName[:len(actorFirstName)].lower() and len(actorFullName) > len(actorName):
                actorLastName = actorFullName[len(actorFirstName):].capitalize()
                actorName = actorFirstName + " " + actorLastName
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL('http://www.gloryholesecrets.com/tour/'+actorPageURL)
            actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPage.xpath('//img[@class="thumbs"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    #Posters
    i = 1
    try:
        background = "http://www.gloryholesecrets.com" + detailsPageElements.xpath('//div[@class="grid_10 alpha"]/a/img')[0].get('src')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    for poster in detailsPageElements.xpath('//div[@class="grid_4"]//img'):
        posterUrl = "http://gloryholesecrets.com" + poster.get('src')
        Log("posterURL: " + posterUrl)
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

