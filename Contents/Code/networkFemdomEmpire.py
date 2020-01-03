import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    # Advanced Search
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="item-info clear"]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].text_content().strip()
        scenePage = searchResult.xpath('.//a')[0].get('href')
        curID = scenePage.replace('/', '_').replace('?', '!')
        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Femdom Empire] " + releaseDate, score = score, lang = lang))

    # Difficult Scenes
    if searchTitle == "Extreme Strap on Training":
        Log("Manual Search Match")
        curID = ("https://femdomempire.com/tour/trailers/EXTREMEStrap-OnTraining.html").replace('/','_')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "EXTREME Strap-On Training" + " [Femdom Empire] " + "2012.04.11", score = 101, lang = lang))
    if searchTitle == "Tease  Stroke":
        Log("Manual Search Match")
        curID = ("https://femdomempire.com/tour/trailers/TeaseStroke.html").replace('/','_')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Tease & Stroke" + " [Femdom Empire] " + "2012.12.05", score = 101, lang = lang))
    if searchTitle == "Cock Locked":
        Log("Manual Search Match")
        curID = ("https://femdomempire.com/tour/trailers/CockLocked.html").replace('/','_')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Cock Locked" + " [Femdom Empire] " + "2012.04.20", score = 101, lang = lang))
    if searchTitle == "Oral Servitude":
        Log("Manual Search Match")
        curID = ("https://femdomempire.com/tour/trailers/OralServitude.html").replace('/','_')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Oral Servitude" + " [Femdom Empire] " + "2012.04.08", score = 101, lang = lang))

    if len(results) > 0:
        return results

    # Standard Search
    else:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + "/tour/search.php?query=" + encodedTitle)
        for searchResult in searchResults.xpath('//div[@class="item-info clear"]'):
            titleNoFormatting = searchResult.xpath('.//a')[0].text_content().strip()
            scenePage = searchResult.xpath('.//a')[0].get('href')
            curID = scenePage.replace('/', '_').replace('?', '!')
            releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Femdom Empire] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    url = str(metadata.id).split("|")[0].replace('_','/')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    #Studio
    metadata.studio = "Femdom Empire"

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="videoDetails clear"]//h3')[0].text_content().strip()
    Log("Scene Title: " + metadata.title)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="videoDetails clear"]//p')[0].text_content().strip()
    except:
        pass

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="featuring clear"][2]//ul//li')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower().replace('categories:', '').replace('tags:', '')
            movieGenres.addGenre(genreName)
    movieGenres.addGenre("Femdom")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="videoInfo clear"]//p')[0].text_content().replace('Date Added:', '').strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="featuring clear"][1]/ul/li')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip().replace('Featuring:', '')
            actorPhotoURL = ''
            movieActors.addActor(actorName, actorPhotoURL)

    if metadata.title == "Owned by Alexis":
        actorName = "Alexis Monroe"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//a[@class="fake_trailer"]//img')[0].get('src0_1x')
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