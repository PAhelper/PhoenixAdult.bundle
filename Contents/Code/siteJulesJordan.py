import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    i = 0
    for searchResult in searchResults.xpath('//div[@class="update_details"]/a[2]'):
        Log(str(searchResult.get('href')))
        titleNoFormatting = searchResults.xpath('//div[@class="update_details"]/a[2]')[i].text_content()
        Log(str(titleNoFormatting))
        releaseDate = searchResults.xpath('//div[@class="update_details"]//div[@class="cell update_date"]')[i].text_content().strip()
        curID = searchResult.get('href').replace('/','_')
        Log('CurID : ' + curID )
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [JulesJordan] " + releaseDate , score = score, lang = lang))
        i = i + 1
    return results



def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Jules Jordan'
    temp = str(metadata.id).split("|")[0].replace('_','/').replace('/vids.html','_vids.html')
    Log('temp :' + temp)
    url = temp
    Log('Url : ' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    paragraph = detailsPageElements.xpath('//span[@class="update_description"]')[0].text_content()
    #paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = paragraph.strip()
    tagline = "JulesJordan"
    metadata.collections.clear()
    tagline = tagline.strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//span[@class="title_bar_hilite"]')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//span[@class="update_tags"]')

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
    try:
        background = detailsPageElements.xpath('//div[@class="mejs-poster mejs-layer"]')[0].get("style")
        Log("BG DL: " + str(background))
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
    	pass
    i = 1
    page = detailsPageElements.xpath('//div[@class="cell content_tab"]/a')[0].get("href")
    Log(page)
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
