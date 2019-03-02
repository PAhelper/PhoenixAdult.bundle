import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    if unicode(searchTitle, 'utf-8').isnumeric():
        url = PAsearchSites.getSearchBaseURL(siteNum) + "/video/" + searchTitle.lower().replace(" ","-").replace("'","-")
        searchResults = HTML.ElementFromURL(url)

        searchResult = searchResults.xpath('//div[@class="video-details"]')[0]
        titleNoFormatting = searchResult.xpath('//h2[@class="h2 m-0"]')[0].text_content()
        curID = searchTitle.lower().replace(" ","-").replace("'","-")
        releaseDate = parse(searchResult.xpath('//div[@class="mb-1"]//span')[1].text_content().strip()).strftime('%b %y')

        score = 100
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results
    return results

def update(metadata,siteID,movieGenres,movieActors):
    detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + '/video/' + str(metadata.id).split("|")[0])
    art = []

    # Title
    metadata.title = detailsPageElements.xpath('//h2[@class="h2 m-0"]')[0].text_content().strip()

    # Studio
    metadata.studio = "ManyVids"

    # Summary
    try:
        paragraphs = detailsPageElements.xpath('//div[@class="desc-text"]')
        pNum = 0
        summary = ""
        for paragraph in paragraphs:
            if pNum >= 0 and pNum < (len(paragraphs)):
                summary = summary + '\n\n' + paragraph.text_content()
            pNum += 1
    except:
        pass
    if summary == '':
        try:
            summary = detailsPageElements.xpath('//div[@class="desc-text"]')[0].text_content().strip()
        except:
            pass
    metadata.summary = summary.strip()

    # Collections / Tagline
    siteName = "ManyVids"
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Date
    date = detailsPageElements.xpath('//div[@class="video-details"]//div[@class="mb-1"]//span')[1].text_content().strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[contains(@class,"username ")]')[0].text_content()
    #if len(actors) > 0:
     #   for actorLink in actors:
    actorName = actors
       #     actorPageURL = actorLink.get("href")
        #    actorPage = HTML.ElementFromURL((PAsearchSites.getSearchBaseURL(siteID)+actorPageURL))
    actorPhotoURL = detailsPageElements.xpath('//div[@class="pr-2"]/a/img')[0].get('src')
    movieActors.addActor(actorName,actorPhotoURL)


    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="tags"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Posters
    background =  detailsPageElements.xpath('//div[@id="rmpPlayer"]')[0].get('data-video-screenshot')
    Log("Background:" + background)
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    #try:
     #   photoPageURL = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//a[@class="btn btn-primary btn-xs wptag " and contains(text(),"Pics")]')[0].get('href')
     #   Log("photoPageURL: " + str(photoPageURL))
      #  photoPageElements = HTML.ElementFromURL(photoPageURL)
       # for posterUrl in photoPageElements.xpath('//figure[@class="photo-thumbnail"]//img'):
        #    art.append("http:" + posterUrl.get('src').replace('/tn',''))
    #except:
     #   pass

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                j = j + 1
            except:
                pass

    return metadata