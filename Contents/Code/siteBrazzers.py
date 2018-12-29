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
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="scene-card-info"]'):
        titleNoFormatting = searchResult.xpath('.//a[1]')[0].get('title')
        curID = (PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a[1]')[0].get('href')).replace('/','_').replace('?','!')
        Log("curID: "+curID)
        subSite = searchResult.xpath('.//span[@class="label-text"]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//time')[0].text_content().strip()).strftime('%Y-%m-%d')
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Brazzers/" + subSite + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Brazzers'
    url = str(metadata.id).split("|")[0].replace('_','/')
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//p[@itemprop="description"]')[0].text_content()
    paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = paragraph[:-10]
    tagline = detailsPageElements.xpath('//span[@class="label-text"]')[0].text_content()
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[contains(@class,"tag-card-container")]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            # If it's part of a series, add an extra Collection tag with the series name... Trouble is there's no standard for locating the series name, so this might not work 100% of the time
            if "series" in genreName or "800 Phone Sex: Line " in metadata.title:
                seriesName = metadata.title
                k = seriesName.rfind(':')
                if (k != -1):
                    metadata.collections.add(seriesName[:k])
                else:
                    metadata.collections.add(seriesName.rstrip('1234567890 '))
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//aside[contains(@class,"scene-date")]')
    if len(date) > 0:
        date = date[0].text_content()
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    
    # Actors
    movieActors.clearActors()
    #starring = detailsPageElements.xpath('//p[contains(@class,"related-model")]//a')
    actors = detailsPageElements.xpath('//div[@class="model-card"]/div[@class="card-image"]/a/img[@class="lazy card-main-img"]')
    if len(actors) > 0:
        # Check if member exists in the maleActors list as either a string or substring
        #if any(member.text_content().strip() in m for m in maleActors) == False:
        for actorLink in actors:
            actorName = actorLink.get('alt')
            actorPhotoURL = "http:" + actorLink.get('data-src').replace("model-medium.jpg","model-small.jpg")
            movieActors.addActor(actorName,actorPhotoURL)
    
    #Posters
    i = 1
    try:
        background = "http:" + detailsPageElements.xpath('//*[@id="trailer-player"]/img')[0].get('src')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass
    for poster in detailsPageElements.xpath('//a[@rel="preview"]'):
        posterUrl = "http:" + poster.get('href').strip()
        thumbUrl = "http:" + detailsPageElements.xpath('//img[contains(@data-src,"thm")]')[i-1].get('data-src')
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