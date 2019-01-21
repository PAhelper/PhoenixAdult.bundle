import PAsearchSites
import PAgenres

def posterAlreadyExists(posterUrl,metadata):
    for p in metadata.posters.keys():
        #Log(p.lower())
        if p.lower().split('?')[0] == posterUrl.lower().split('?')[0]:
            Log("Found " + posterUrl.split('?')[0] + " in posters collection")
            return True

    for p in metadata.art.keys():
        if p.lower() == posterUrl.lower():
            return True
    return False

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    encodedTitle = encodedTitle.replace('%20a%20','%20')
    i=0
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    Log("resultat" + str(searchResults) )
    for searchResult in searchResults.xpath('//a[@class="thumbnail clearfix"]'):
        Log(str(searchResult.get('href')))
        titleNoFormatting = searchResult.xpath('//div/h3[@class="scene-title"]')[i].text_content()
        Log(titleNoFormatting)
        curID = searchResult.get('href').replace("_","$").replace("/","_").split("?")[0]
        Log(curID)
        lowerResultTitle = str(titleNoFormatting).lower()
        subSite = searchResult.xpath('//div/p[@class="help-block"]')[i].text_content()
        Log("subsite: "+ subSite)

        site = " [Dogfart"
        if len(subSite) > 0 and subSite != "Dogfart":
            site = site + " / " + subSite
        site = site + "] "
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(searchSiteID), name = titleNoFormatting + site , score = score, lang = lang))
        i = i + 1
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Dogfart'
    temp = str(metadata.id).split("|")[0].replace('_','/').replace("$","_")
    Log(temp)
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    Log(url)
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//div[@class="description shorten"]')[0].text_content().strip()

    metadata.summary = paragraph.strip()
    tagline = detailsPageElements.xpath('//h3 [@class="site-name"]')[0].text_content()
    tagline = tagline.strip()
    metadata.tagline = tagline

    metadata.collections.clear()
    collection = str(PAsearchSites.getSearchSiteName(siteID))
    metadata.collections.add(collection)
    metadata.title = detailsPageElements.xpath('//div[@class="icon-container"]/a')[0].get("title")
    metadata.studio = "Dofgart Network"

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="categories"]/p/a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)


    # Release Date
    try:
        date = " "
        if len(date) > 0:
            date = date[0].text_content().strip()
            date_object = datetime.strptime(date, '%b %d, %Y')
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year

    except:
        pass
    # Actors
    metadata.roles.clear()
    actors = detailsPageElements.xpath('//h4[@class="more-scenes"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = str(actorLink.text_content().strip())
            actorName = actorName.replace("\xc2\xa0", " ")
            role.name = actorName
            actorsearch = HTML.ElementFromURL("https://www.adultdvdempire.com/performer/search?q=" + actorName.replace(' ','%20'))
            actropageURL = actorsearch.xpath('//div[@class="col-xs-6 col-sm-3 grid-item grid-item-performer grid-item-performer-145"]/a')[0].get("href")
            actropageURL = "https://www.adultdvdempire.com" + actropageURL
            actropage = HTML.ElementFromURL(actropageURL)
            actorPhotoURL = actropage.xpath('//a[@class="fancy headshot"]')[0].get("href")
            role.photo = actorPhotoURL

    #Posters
    try:
        background = "https:" + detailsPageElements.xpath('//div[@class="icon-container"]//img')[0].get('src')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass
    i=0
    for posterUrls in detailsPageElements.xpath('//div[@class="preview-image-container col-xs-6 col-md-2 clearfix"]//a'):
        page = PAsearchSites.getSearchBaseURL(siteID) + posterUrls.get("href")
        posterpage = HTML.ElementFromURL(page)
        posterUrl = posterpage.xpath('//div[@class="col-xs-12 remove-bs-padding"]/img')[0].get('src')
            #Download image file for analysis
        try:
            if not posterAlreadyExists(posterUrl,metadata):
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size

                metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i)
                if width > height and i > 1:
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i )
                i = i + 1
                if i>15:
                    break


        except:
            pass

    return metadata