import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//tr[@style="width:px;height:190px;"]/td'):
        titleNoFormatting = searchResult.xpath('./span[1]/a')[0].text_content().strip()
        curID = searchResult.xpath('./span[1]/a')[0].get('href').replace('/','_').replace('?','!')
        subSite = searchResult.xpath('./span[3]')[0].text_content().split('.com')[0].strip().title()
        Log(subSite)
        releaseDate = parse(searchResult.xpath('./span[3]')[0].text_content().split('-', 1)[1].strip()).strftime('%Y-%m-%d')
        actress = searchResult.xpath('./span[2]')[0].text_content().strip()
        Log(actress)
        scenePoster = searchResult.xpath('./a/img')[0].get('src').replace('/','+').replace('?','!')
        if subSite == PAsearchSites.getSearchSiteName(siteNum):
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            elif searchTitle in actress:
                score = 80
        else:
            if searchDate:
                score = 60 - Util.LevenshteinDistance(searchDate, releaseDate)
            elif searchTitle in actress:
                score = 60 - Util.LevenshteinDistance(searchTitle.lower(), actress.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + scenePoster, name = titleNoFormatting + " [Insex/"+subSite+"] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = PAsearchSites.getSearchBaseURL(siteID) + "/iod/" + str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Insex'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@style="width:934px;font-size:14px;background-color:#333333;"][1]/div[1]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@style="width:934px;font-size:14px;background-color:#333333;"][1]/div[5]')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.addGenre("BDSM")

    # Release Date
    dateText = detailsPageElements.xpath('//div[@style="width:934px;font-size:14px;background-color:#333333;"][1]/div[3]')[0].text_content().strip()
    date = dateText.split(",")[0]
    if len(date) > 0:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@style="width:934px;font-size:14px;background-color:#333333;"][1]/div[2]/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//div[@class="video-js vjs-paused my-video-dimensions vjs-controls-enabled vjs-workinghover vjs-v7 vjs-user-active"]')[0].get('poster')
        Log(twitterBG)
        art.append(twitterBG)
    except:
        pass

    # Scene Poster
    scenePoster = str(metadata.id).split("|")[2].replace('+', '/').replace('!', '?')
    Log(scenePoster)
    art.append(scenePoster)

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