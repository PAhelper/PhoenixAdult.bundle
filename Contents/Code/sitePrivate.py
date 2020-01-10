import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    searchResults = HTML.ElementFromURL('https://www.private.com/search.php?query=' + encodedTitle)
    for searchResult in searchResults.xpath('//ul[@id="search_results"]//li[contains(@class, "col-sm-6")]'):
        #Log(searchResult.get('class'))
        titleNoFormatting = searchResult.xpath('.//div[@class="scene"]//div//h3//a')[0].text_content()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//div[@class="scene"]//div//h3//a')[0].get('href').replace('/','_').replace('?','!')
        Log("ID: " + curID)
        # releaseDate = searchResult.xpath('.//div[@class="release-info"]//div[@class="views-date-box"]//span[@class="date-added"]')[0].text_content()

        #girlName = searchResult.xpath('.//div[@class="scene"]//div//p[@class="scene-models"]//a')[0].text_content()

        #Log("CurID" + str(curID))
        #lowerResultTitle = str(titleNoFormatting).lower()
        #titleNoFormatting = girlName + " - " + titleNoFormatting + " [Private]"
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Private]", score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0].replace('_', '/').replace('!','?')

    url = temp
    Log('url :' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    metadata.studio = "Private"

    # Summary
    paragraph = detailsPageElements.xpath('//meta[@itemprop="description"]')[0].get('content')
    # paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n', '').replace('  ', '') + "\n\n"
    metadata.summary = paragraph
    try:
        tagline = detailsPageElements.xpath('//span[@class="title-site"]')[0].text_content()
        metadata.collections.clear()
        metadata.tagline = tagline
        metadata.collections.add(tagline)
    except:
        tagline = PAsearchSites.getSearchSiteName(siteID).strip()
        metadata.collections.clear()
        metadata.tagline = tagline
        metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[contains(@class,"scene-tags")]//li')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.xpath('.//a')[0].text_content().lower()
            movieGenres.addGenre(genreName)

    # Date
    date = detailsPageElements.xpath('//meta[@itemprop="uploadDate"]')[0].get('content')
    if len(date) > 0:
        date_object = datetime.strptime(date, '%m/%d/%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    titleActors = ""
    actors = detailsPageElements.xpath('//ul[@id="featured_pornstars"]//li[contains(@class, "featuring")]')
    if len(actors) > 0:
        for actorPage in actors:
            actorName = actorPage.xpath('.//div[@class="model"]//a')[0].get("title")
            titleActors = titleActors + actorName + " & "
            actorPhotoURL = actorPage.xpath('.//div[@class="model"]//a//picture//img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)
        titleActors = titleActors[:-3]
        metadata.title = metadata.title


    # Posters
    art = detailsPageElements.xpath('//meta[@itemprop="thumbnailUrl"]')[0].get('content')
    Log("posters DL: " + art)
    metadata.posters[art] = Proxy.Preview(HTTP.Request(art, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
    metadata.art[art] = Proxy.Preview(HTTP.Request(art, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)

    #backgrounds = detailsPageElements.xpath('//div[@class="slick-slide"]')
    posterNum = 1
    backgrounds = detailsPageElements.xpath('//meta[@itemprop="contentURL"]')[0].get('content')
    i = 1
    j = backgrounds.rfind("upload/")
    k = backgrounds.rfind("trailers/")
    sceneID = backgrounds[j+7:k-1]
    backgrounds = backgrounds[:k] + "Fullwatermarked/"
    Log('Backgrounds Base URL: ' + backgrounds)
    for i in range(1,10):
        posterUrl = backgrounds + sceneID.lower() + "_" + "{0:0=3d}".format(i*5) + ".jpg"
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

            except:
                pass

        #Log('Background: ' + img)
        #metadata.art[img] = Proxy.Preview(HTTP.Request(img, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        #metadata.posters[img] = Proxy.Preview(HTTP.Request(img, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)

    return metadata
