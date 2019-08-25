import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    searchResults = HTML.ElementFromURL('http://www.gloryholesecrets.com/tour/search.php?query=' + encodedTitle)
    for searchResult in searchResults.xpath('//li[@class="featured-video morestdimage grid_4 mb"]'):
        detailsPage = searchResult.xpath('./a')[0].get('href')
        titleNoFormatting = searchResult.xpath('./div[@class="details"]//h5')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('./div[@class="details"]/p/strong')[0].text_content().strip()).strftime('%Y-%m-%d')
        curID = detailsPage.replace('/','_').replace('?','!')
        Log(curID + "|" + str(siteNum))
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " [GloryHoleSecrets] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Aziani'
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    #url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//div[@class="desc"]')[0].text_content().strip()
    metadata.summary = paragraph.strip()
    tagline = 'GloryHoleSecrets'
    metadata.collections.clear()
    tagline = tagline.strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h2[@class="H_underline"]')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//h5[@class="video_categories"]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            if "cumshots" not in genreName:
                movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//p[@class="mb0"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = datetime.strptime(date[12:], '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    else:
        date = str(metadata.id).split("|")[2]
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="video_details mb mt0"]/h5[1]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            sceneImg = detailsPageElements.xpath('//meta[@property="og:image"]')[0].get('content')
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
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):
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

