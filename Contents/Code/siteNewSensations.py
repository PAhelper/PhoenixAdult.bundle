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

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    searchResults = HTML.ElementFromURL('https://www.newsensations.com/tour_ns/search.php?query=' + encodedTitle)
    for searchResult in searchResults.xpath('//h4//a'):
        Log(str(searchResult.get('href')))
        titleNoFormatting = searchResult.text_content()
        curID = searchResult.get('href').replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [New Sensations]", score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'New Sensations'
    detailsPageElements = HTML.ElementFromURL(str(metadata.id).split("|")[0].replace('_','/').replace('!','?').replace('tour/ns','tour_ns'))

    # Summary
    paragraph = detailsPageElements.xpath('//div[@class="trailerInfo"]//p')[0].text_content().strip()
    metadata.summary = paragraph
    tagline = detailsPageElements.xpath('//div[@class="trailerInfo"]//ul//li[4]')[0].text_content().strip()
    metadata.collections.clear()
    tagline = tagline.strip()
    metadata.tagline = tagline
    #metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//div[@class="trailerVideos clear"]//div[@class="title clear"]//h3')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="trailerInfo"]//ul//li[3]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            Log("Genre Found: "+genreName)
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//div[@class="trailerInfo"]//ul//li[2]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date = date[10:20]
        date_object = datetime.strptime(date, '%m/%d/%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="trailerInfo"]//ul//li//span[@class="tour_update_models"]//a')
    Log("Actors found: "+str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="modelPicture"]//img')[0].get("src")
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
