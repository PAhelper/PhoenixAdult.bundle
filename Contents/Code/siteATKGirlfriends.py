import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    modelID = encodedTitle.split('%20', 1)[0].lower()
    Log("modelID: " + modelID)
    try:
        sceneTitle = encodedTitle.split('%20', 1)[1].replace('%20',' ')
    except:
        sceneTitle = ''
    Log("Scene Title: " + sceneTitle)

    url = PAsearchSites.getSearchSearchURL(siteNum) + modelID
    searchResults = HTML.ElementFromURL(url)
    for searchResult in searchResults.xpath('//div[@class="movie-wrap-index img-polaroid left"]'):
        titleNoFormatting = searchResult.xpath('.//h1[@class="video-title-model"]')[0].text_content().strip()
        titleNoFormatting = titleNoFormatting.replace('/', '$').replace('?', '+')
        summary = searchResult.xpath('.//div[@class="col-lg-7"]')[0].text_content().split('Description:')[1].strip()
        summary = summary.replace('/', '$').replace('?', '+')
        actor = searchResult.xpath('//h1[@class="page-title col-lg-12"]')[0].text_content().strip()
        videoBG = searchResult.xpath('.//img[@class="img-responsive"]')[0].get('src')
        Log(videoBG)
        videoBG = videoBG.replace('/', '$').replace('?', '+')
        if searchDate:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d')
        else:
            releaseDate = ''
        curID = searchResult.xpath('.//a[@class="thumbnail left"]')[0].get('href')
        curID = curID.replace('/','$').replace('?','+')
        score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + titleNoFormatting + "|" + summary + "|" + releaseDate  + "|" + actor + "|" + videoBG, name = titleNoFormatting + " [ATKGirlfriends] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    ### Pull Data from Actor Page
    # Studio
    metadata.studio = 'ATK'

    # Title
    metadata.title = str(metadata.id).split("|")[2]
    metadata.title = metadata.title.replace('$', '/').replace('+', '?')

    # Summary
    metadata.summary = str(metadata.id).split("|")[3]
    metadata.summary = metadata.summary.replace('$', '/').replace('+', '?')

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    try:
        date = str(metadata.id).split("|")[4]
        if len(date) > 0:
            date_object = parse(date)
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
            Log("Date from file")
    except:
        pass

    # Actors
    actorName = str(metadata.id).split("|")[5]
    actorPhotoURL = ''
    movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.addGenre("Girlfriend Experience")
    # If scenePage is valid, try to load it to scrape genres
    try:
        url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('$','/').replace('+','?')
        detailsPageElements = HTML.ElementFromURL(url)

        # Genres
        genreText = detailsPageElements.xpath('//div[@class="movie-wrap img-polaroid"]')[0].text_content().split('Tags :')[1].strip()
        genres = genreText.split(',')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.strip().lower()
                movieGenres.addGenre(genreName)
    except:
        pass

    # Video trailer background images
    twitterBG = str(metadata.id).split("|")[6]
    twitterBG = twitterBG.replace('$', '/').replace('+', '?').replace('sm_','').split('1.jpg')[0]
    photoList = [1, 2, 3, 4, 5, 6, 7]
    for photoNum in photoList:
        photo = twitterBG + str(photoNum) + ".jpg"
        art.append(photo)

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            j = j + 1

    return metadata