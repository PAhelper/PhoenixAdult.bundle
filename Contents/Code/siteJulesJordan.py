import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    i = 0
    for searchResult in searchResults.xpath('//div[@class="update_details"]/a[2]'):
        Log(str(searchResult.get('href')))
        titleNoFormatting = searchResults.xpath('//div[@class="update_details"]/a[2]')[i].text_content()
        Log(str(titleNoFormatting))
        releaseDate = parse(searchResult.xpath('//div[@class="update_details"]//div[@class="cell update_date"]')[i].text_content().strip()).strftime('%Y-%m-%d')
        curID = searchResult.get('href').replace('/','_').replace('?','!')
        Log('CurID : ' + curID )
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + str(i) + "|" + str(encodedTitle) , name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate , score = score, lang = lang))
        i = i + 1
    return results



def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Jules Jordan'
    temp = str(metadata.id).split("|")[0].replace('_','/').replace('?','!').replace('/vids.html','_vids.html')
    Log('temp :' + temp)
    url = temp
    Log('Url : ' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    indice = str(metadata.id).split("|")[2]
    titre_search=str(metadata.id).split("|")[3]
    siteNum = str(metadata.id).split("|")[1]
    Log('Indice ' + indice)
    paragraph = detailsPageElements.xpath('//span[@class="update_description"]')[0].text_content()
    metadata.summary = paragraph.strip()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    tagline = tagline.strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//span[@class="title_bar_hilite"]')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//span[@class="update_tags"]/a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//div[@class="cell update_date"]')[0].text_content()
    if len(date) > 0:
        date = date.strip()
        date_object = datetime.strptime(date, '%m/%d/%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="backgroundcolor_info"]/span[@class="update_models"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = str(actorLink.text_content().strip())
            actorName = actorName.replace("\xc2\xa0", " ")
            role.name = actorName
            actorPageURL = actorLink.get("href")
            Log('acteur page : ' + actorPageURL)
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="model_bio_thumb stdimage thumbs target"]')[0].get("src0_1x")
            if (str(actorPhotoURL) == 'None' ) :
                actorPhotoURL = actorPage.xpath('//img[@class="model_bio_thumb stdimage thumbs target"]')[0].get("src0")

            Log('acteur URL img: ' + str(actorPhotoURL))
            movieActors.addActor(actorName,actorPhotoURL)
            role.photo = actorPhotoURL
    #Posters
    searchbckgs = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteID) + titre_search )
    j = int(indice)
    k=0
    for searchbckg in searchbckgs.xpath('//div[@class="category_listing_wrapper_updates"]/div[@class="update_details"]' ):
        if k == j:
            try:
                for l in range (0,6):
                    m = 1
                    srcbckgrd=str("src" + str(l) + "_1x")
                    background = searchbckg.xpath('./a/img')[0].get(srcbckgrd)
                    Log('Url BG ' + str(background))
                    try:
                        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = m)
                    except:
                        pass
                    l = l + 1
                    m = m + 1

            except: 
                background = searchbckg.get("src")
                metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)       
            break   
        k = k + 1

    i = 1
    page = detailsPageElements.xpath('//div[@class="cell content_tab"]/a')[0].get("href")

    Searchposter = HTML.ElementFromURL(page)
    for posterUrls in Searchposter.xpath('//div[@class="photo_gallery_thumbnail_wrapper"]/a/img'):
        posterUrl = posterUrls.get("src")
        Log(str(posterUrl))
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

            i = i + 1
            if i>10:
                break


        except:
            pass


    return metadata