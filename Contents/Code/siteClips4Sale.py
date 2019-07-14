import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    userID = encodedTitle.split('%20', 1)[0]
    Log("userID: " + userID)
    encodedSceneTitle = encodedTitle.split('%20', 1)[1]
    sceneTitle = encodedSceneTitle.replace('%20', ' ')
    Log("Scene Title: " + sceneTitle)
    url = PAsearchSites.getSearchSearchURL(siteNum) + userID + "/1/Cat0-AllCategories/Page1/SortBy-bestmatch/Limit50/search/" + encodedSceneTitle
    searchResults = HTML.ElementFromURL(url)
    for searchResult in searchResults.xpath('//div[@class="clipWrapper"]'):
        titleNoFormatting = searchResult.xpath('.//a[@class="clipTitleLink"]')[0].text_content().replace('(HD MP4)','').replace('(WMV)','').strip()
        curID = searchResult.xpath('.//a[@class="clipTitleLink"]')[0].get('href').replace('/','_').replace('?','!')
        subSite = searchResult.xpath('//title')[0].text_content().strip()
        score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Clips4Sale/" + subSite + "] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    userID = url.split('/')[-3]
    Log("userID:" + userID)
    sceneID = url.split('/')[-2]
    Log("sceneID:" + sceneID)

    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Clips4Sale'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="clipTitle"]')[0].text_content().replace('(HD MP4)','').replace('(WMV)','').strip()

    # Summary
    summary = detailsPageElements.xpath('//div[contains(@class, "dtext dheight")]/p[last()]')[0].text_content().strip()
    summary = summary.split("--SCREEN SIZE")[0] #K Klixen
    metadata.summary = summary

    #Tagline and Collection(s)
    tagline = detailsPageElements.xpath('//title')[0].text_content().split('-')[0].strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    # Category
    cat = detailsPageElements.xpath('//div[@class="clipInfo clip_details"]/div[1]/a')[0].text_content().strip().lower()
    movieGenres.addGenre(cat)
    # Related Categories / Keywords
    genreList =[]
    genres = detailsPageElements.xpath('//span[@class="relatedCatLinks"]/span/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            genreList.append(genreName)
            movieGenres.addGenre(genreName)
    Log(str(genreList))

    # Release Date
    date = detailsPageElements.xpath('//div[@class="clearfix infoRow2 clip_details"]/div/div[2]/div[3]/span/span')[0].text_content().strip()[:-8]
    Log("Date: " + date)
    if len(date) > 0:
        date_object = datetime.strptime(date, '%m/%d/%y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    if "MARKS HEAD BOBBERS" in tagline:
        movieActors.addActor("Mark Rockwell", "")
        if "Alexa Grace" in metadata.summary:
            movieActors.addActor("Alexa Grace","")
        if "Remy LaCroix" in metadata.summary:
            movieActors.addActor("Remy LaCroix","")
        if "jade indica" in genreList:
                movieActors.addActor("Jade Indica","")
    else:
        actorName = tagline
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    twitterBG = "http://imagecdn.clips4sale.com/accounts99/" + userID + "/clip_images/previewlg_" + sceneID + ".jpg"
    art.append(twitterBG)

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
            j = j + 1

    return metadata