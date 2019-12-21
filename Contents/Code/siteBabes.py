import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    # Use encodedTitle as sceneID, if provided
    sceneID = encodedTitle.split('%20', 1)[0]
    Log("SceneID: " + sceneID)
    try:
        sceneTitle = encodedTitle.split('%20', 1)[1].replace('%20',' ')
    except:
        sceneTitle = ''
    Log("Scene Title: " + sceneTitle)
    url = PAsearchSites.getSearchBaseURL(siteNum) + "/scene/" + sceneID + "/1"
    searchResults = HTML.ElementFromURL(url)
    for searchResult in searchResults.xpath('//div[@class="wxt7nk-0 btKUEO"]'):
        titleNoFormatting = searchResult.xpath('.//div[1]/h1')[0].text_content().replace("SML-","").replace("Trailer","").strip()
        curID = url.replace('/','_').replace('?','!')
        subSite = searchResult.xpath('.//div[2]/a/div[2]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//div[@class="tjb798-2 flgKJM"]/span[position()=last()]')[0].text_content().strip().replace('Release Date:','')).strftime('%Y-%m-%d')
        score = 100
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Babes/" + subSite + "] " + releaseDate, score = score, lang = lang))

    if len(results) > 0:
        return results

    # Use search on site
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="dtkdna-1 cPNxux"]'):
        titleNoFormatting = searchResult.xpath('.//a[1]')[0].get('title')
        curID = (PAsearchSites.getSearchBaseURL(int(siteNum)) + searchResult.xpath('.//a[1]')[0].get('href')).replace('/','_').replace('?','!')
        subSite = searchResult.xpath('.//div[2]/div[4]/a/div[2]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//div[2]/div[3]/div[1]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Babes/" + subSite + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Babes'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="wxt7nk-4 fSsARZ"]')[0].text_content().replace("SML-","").replace("Trailer","").strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="tjb798-2 flgKJM"]/span[position()=last()-1]/div[2]')[0].text_content().strip()
    except:
        pass

    # Tagline and Collection(s)
    tagline = detailsPageElements.xpath('//div[@class="sc-11m21lp-2 fOadtn"]')[0].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="tjb798-2 flgKJM"]/span[1]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().replace(',','').strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="tjb798-2 flgKJM"]/span[last()]')
    if len(date) > 0:
        date = date[0].text_content().strip().replace('Release Date:','')
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    try:
        actors = detailsPageElements.xpath('//a[@class="wxt7nk-6 czvZQW"]')
        if len(actors) > 0:
            if len(actors) == 3:
                movieGenres.addGenre("Threesome")
            if len(actors) == 4:
                movieGenres.addGenre("Foursome")
            if len(actors) > 4:
                movieGenres.addGenre("Orgy")
            for actorLink in actors:
                actorName = str(actorLink.text_content().strip())
                actorPhotoURL = ''
                movieActors.addActor(actorName, actorPhotoURL)
    except:
        pass

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//div[@class="tg5e7m-2 evtSOm"]/img')[0].get('src')
        art.append(twitterBG)
    except:
        pass

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
