import PAsearchSites
import PAgenres
def tagAleadyExists(tag,metadata):
    for t in metadata.genres:
        if t.lower() == tag.lower():
            return True
    return False

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
    for searchResult in searchResults.xpath('//div[@data-itemtype="scenes"]//a'):
        Log(str(searchResult.get('href')))
        titleNoFormatting = searchResult.text_content()
        curID = searchResult.get('href').replace('/','_')
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Evil Angel]", score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Evil Angel'
    temp = str(metadata.id).split("|")[0].replace('_','/')
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//div[@class="sceneDesc bioToRight showMore"]')[0].text_content().strip()
    #paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    paragraph = paragraph[14:]
    metadata.summary = paragraph.strip()
    tagline = detailsPageElements.xpath('//a[@class="dvdLink  "]')[0].get('title')
    metadata.collections.clear()
    tagline = tagline.strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Director
    try:
        directedBy = detailsPageElements.xpath('//div[@class="sceneCol sceneColDirectors"]//a')[0].text_content().strip()
        metadata.directors.clear()
        metadata.directors.add(directedBy)
    except:
        pass

    # director  
    #try:
    #  htmldirector = html.xpath('//p[@class="director"]/a')
    #  metadata.directors.clear()
    #  for member in htmldirector:
    #    dirname = member.text_content().strip()
    #  try:
    #    director = metadata.directors.new()
    #    director.name = dirname
    #  except:
    #    try:
    #      director = metadata.directors.new()
    #      metadata.directors.add(dirname)
    #    except: pass
    #except: pass



    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="sceneCol sceneColCategories"]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//div[@class="updatedDate"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="sceneCol sceneColActors"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    #Posters
    #i = 1
    #try:
    #    background = "http:" + detailsPageElements.xpath('//*[@class="player-video"]/img')[0].get('src')
    #    Log("BG DL: " + background)
    #    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    #except:
    #    pass

    return metadata
