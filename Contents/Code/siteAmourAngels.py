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
    url = PAsearchSites.getSearchSearchURL(siteNum) + sceneID + ".html"
    searchResult = HTML.ElementFromURL(url)

    titleNoFormatting = searchResult.xpath('//td[@class="blox-bg"]//td[2]//b')[0].text_content().title().replace("Video","").strip()
    curID = url.replace('/','+').replace('?','!')
    releaseDate = searchResult.xpath('//td[@class="blox-bg"]//td[2]')[0].text_content().split('Added')[1].strip()[:10]
    releaseDate = parse(releaseDate).strftime('%Y-%m-%d')
    if sceneTitle:
        score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
    else:
        score = 90
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [AmourAngels] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('+','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'AmourAngels'

    # Title
    metadata.title = detailsPageElements.xpath('//td[@class="blox-bg"]//td[2]//b')[0].text_content().title().replace("Video","").strip()

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.addGenre("Softcore")
    movieGenres.addGenre("European Girls")

    # Release Date
    date = detailsPageElements.xpath('//td[@class="blox-bg"]//td[2]')[0].text_content().split('Added')[1].strip()[:10]
    if len(date) > 0:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//td[@class="modinfo"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().title().strip())
            try:
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//td[@class="modelinfo-bg"]//td[1]//img')[0].get("src")
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//td[@class="noisebg"]//div//img')[0].get('src')
        art.append(twitterBG)
    except:
        pass

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            j = j + 1

    return metadata