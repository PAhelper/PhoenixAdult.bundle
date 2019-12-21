import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    sceneID = encodedTitle.split('%20', 1)[0]
    Log("SceneID: " + sceneID)
    try:
        sceneTitle = encodedTitle.split('%20', 1)[1].replace('%20',' ')
    except:
        sceneTitle = ''
    Log("Scene Title: " + sceneTitle)
    url = PAsearchSites.getSearchSearchURL(siteNum) + sceneID
    searchResult = HTML.ElementFromURL(url)
    titleNoFormatting = searchResult.xpath('//div[@class="titleBar"]/h1')[0].text_content().strip()
    curID = url.replace('/', '_').replace('?', '!')
    subSite = searchResult.xpath('//div[@class="siteLink"]/a')[0].get('title').strip()
    releaseDate = parse(searchResult.xpath('//div[@class="updatedDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')
    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [GirlsWay/" + subSite + "] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'GirlsWay'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="titleBar"]/h1')[0].text_content().strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="sceneDesc bioToRight showMore"]')[0].text_content().replace('Video Description:','').strip()
    except:
        pass

    # Tagline and Collection(s)
    tagline = detailsPageElements.xpath('//div[@class ="siteLink"]/a')[0].get('title').strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="sceneCol sceneColCategories"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)
    movieGenres.addGenre('Lesbian')

    # Release Date
    date = detailsPageElements.xpath('//div[@class="updatedDate"]')[0].text_content().strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="sceneCol sceneColActors"]/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = actorLink.get("href")
                if 'http' not in actorPageURL:
                    actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorPageURL
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]')[0].get("src")
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//meta[@name="twitter:image"]')[0].get('content')
        art.append(twitterBG)
    except:
        pass

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
        metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
        j = j + 1

    return metadata