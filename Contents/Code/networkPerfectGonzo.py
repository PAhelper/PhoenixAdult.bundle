import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    Log('searchtitle ' + searchTitle) 
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle )
    i = 0
    for searchResult in searchResults.xpath('//div[@class="itemm"]/a'):
        titleNoFormatting = searchResult.get("title")
        releaseDate = parse(searchResult.xpath('//div[@class="itemm"]//span[@class="nm-date"]')[i].text_content().strip()).strftime('%Y-%m-%d')
        curID = searchResult.get('href').replace('/','_').replace('?','!')
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = titleNoFormatting + " [Primecups] " + releaseDate , score = score, lang = lang ))
        i = i + 1
    return results



def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    Log('temp :' + temp)
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    Log('Url : ' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    paragraph = detailsPageElements.xpath('//div[@class="col-sm-8 col-md-8 no-padding-side"]/p')[0].text_content()
    metadata.summary = paragraph.strip()

    metadata.studio="Perfect Gonzo"
    tagline = "Primecups"
    tagline = tagline.strip()
    metadata.tagline = tagline

    metadata.collections.clear()
    collection = str(PAsearchSites.getSearchSiteName(siteID))
    metadata.collections.add(collection)

    metadata.title = detailsPageElements.xpath('//title')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="col-sm-8 col-md-8 no-padding-side tag-container"]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//div[@class="col-sm-6 col-md-6 no-padding-left no-padding-right text-right"]/span')[0].text_content()
    if len(date) > 0:
        date = date.strip('Added').strip()
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="col-sm-6 col-md-6 no-padding-left no-padding-right"]/h2')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = str(actorLink.text_content().strip())
            actorName = actorName.replace("\xc2\xa0", " ")
            role.name = actorName
            actorPageURL = "https://www.primecups.com/models/" + str(actorName.strip().lower().replace(" ","-"))
            Log('acteur page : ' + str(actorPageURL))
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="col-md-8 bigmodelpic"]/img')[0].get("src")
            #actorPhotoURL= 'http:' + actorPhoto
            #Log('acteur URL img: ' + str(actorPhotoURL))
            movieActors.addActor(actorName,actorPhotoURL)
            role.photo = actorPhotoURL
    #Posters
        background = detailsPageElements.xpath('//video[@class="video-js vjs-default-skin"]')[0].get("poster")
        Log("BG DL: " + str(background))
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    i = 1
    #Searchposter = detailsPageElements.xpath('//div[@class="cell content_tab"]/a')[0].get("href")
    for posterUrls in detailsPageElements.xpath('//ul[@class="bxslider_pics "]//img'):
        if i < 5:
            posterUrl = posterUrls.get("src")
        else:
            posterUrl = posterUrls.get("data-original")
        Log('Url poster ' + str(posterUrl))
            #Download image file for analysis
        try:
            img_file = urllib.urlopen(posterUrl)
            im = StringIO(img_file.read())
            resized_image = Image.open(im)
            width, height = resized_image.size
            #posterUrl = posterUrl[:-6] + "01.jpg"
            #Add the image proxy items to the collection
            if i == 1:
                metadata.posters[background] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i)
            i = i + 1
            if i>10:
                break


        except:
            pass


    return metadata