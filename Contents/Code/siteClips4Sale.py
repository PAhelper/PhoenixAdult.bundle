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
    summary = detailsPageElements.xpath('//div[contains(@class, "dtext dheight")]')[0].text_content().strip()
    summary = summary.split("--SCREEN SIZE")[0].strip() #K Klixen
    summary = summary.split("Description:")[1].split("window.NREUM")[0].replace("**TOP 50 CLIP**","").replace("1920x1080 (HD1080)","").strip() # MHBHJ
    metadata.summary = summary

    #Tagline and Collection(s)
    tagline = detailsPageElements.xpath('//title')[0].text_content().split('-')[0].strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Actors / Genres
    # Main Category
    cat = detailsPageElements.xpath('//div[@class="clipInfo clip_details"]/div[1]/a')[0].text_content().strip().lower()
    movieGenres.addGenre(cat)
    # Related Categories / Keywords
    genreList =[]
    genres = detailsPageElements.xpath('//span[@class="relatedCatLinks"]/span/a')
    if len(genres) > 0:
        for genre in genres:
            genreName = genre.text_content().strip().lower()
            genreList.append(genreName)
    Log(str(genreList))
    # Add Actors
    if "My cherry crush" in tagline:
        genreList.remove("cherry")
        genreList.remove("cherrycrush")
    elif "MARKS HEAD BOBBERS" in tagline:
        movieActors.addActor("Mark Rockwell", "")
        if "mark rockwell" in genreList:
            genreList.remove("mark rockwell")
        if "Alexa Grace" in metadata.summary or "alexa grace" in genreList:
            movieActors.addActor("Alexa Grace","")
            genreList.remove("alexa grace")
        if "Remy LaCroix" in metadata.summary or "alexa grace" in genreList:
            movieActors.addActor("Remy LaCroix","")
            genreList.remove("remy lacroix")
        if "Jade Indica" in metadata.summary or "jade indica" in genreList:
            movieActors.addActor("Jade Indica","")
            genreList.remove("jade indica")
        if "Dillion Carter" in metadata.summary or "dillion carter" in genreList:
            movieActors.addActor("Dillion Carter","")
            genreList.remove("dillion carter")
        if "Sierra Cure" in metadata.summary or "sierra cure" in genreList:
            movieActors.addActor("Sierra Cure","")
            genreList.remove("sierra cure")
        if "Britney Stevens" in metadata.summary or "britney stevens" in genreList:
            movieActors.addActor("Britney Stevens","")
            genreList.remove("britney stevens")
        if "Megan Piper" in metadata.summary or "megan piper" in genreList:
            movieActors.addActor("Megan Piper","")
            genreList.remove("megan piper")
        if "Alexis Venton" in metadata.summary or "alexis venton" in genreList:
            movieActors.addActor("Alexis Venton","")
            genreList.remove("alexis venton")
        if "Jessica Rayne" in metadata.summary or "jessica rayne" in genreList:
            movieActors.addActor("Jessica Rayne","")
            genreList.remove("jessica rayne")
        if "Mandy Haze" in metadata.summary or "mandy haze" in genreList:
            movieActors.addActor("Mandy Haze","")
            genreList.remove("mandy haze")
    elif "KLIXEN" in tagline:
        actors = detailsPageElements.xpath('//div[@class="clipInfo clip_details"]/div[3]/span[2]/span/a')
        for actor in actors:
            actorName = str(actor.text_content().strip())
            actorPhotoURL = ''
            genreList.remove(actorName)
            movieActors.addActor(actorName, actorPhotoURL)
    else:
        actorName = tagline
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    # Add Genres
    for genre in genreList:
        movieGenres.addGenre(genre)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="clearfix infoRow2 clip_details"]/div/div[2]/div[3]/span/span')[0].text_content().strip()[:-8]
    Log("Date: " + date)
    if len(date) > 0:
        date_object = datetime.strptime(date, '%m/%d/%y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = "http://imagecdn.clips4sale.com/accounts99/" + userID + "/clip_images/previewlg_" + sceneID + ".jpg"
        art.append(twitterBG)
    except:
        pass

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
            j = j + 1

    return metadata