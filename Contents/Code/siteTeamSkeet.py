import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="info"]'):
        sceneURL = searchResult.xpath('.//span//a')[0].get("href").split("?", 1)[0]
        if 'http' not in sceneURL:
            sceneURL = 'https' + str(sceneURL)
        scenePage = HTML.ElementFromURL(sceneURL)
        titleNoFormatting = scenePage.xpath('//title')[0].text_content().split(" | ")[1]
        curID = sceneURL.replace('/','+').replace('?','!')
        actors = scenePage.xpath('//a[contains(@href,"/profile/")]')[0].text_content()
        releaseDate = parse(scenePage.xpath('//div[contains(text(),"Date Added:")]')[0].text_content().replace('Date Added:','').strip()).strftime('%Y-%m-%d')
        if searchDate and releaseDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " w/ " + actors + " [TeamSkeet] " + releaseDate, score = score, lang = lang))

    if searchTitle == "Eavesdropping And Pussy Popping":
        Log("Manual Search Match")
        curID = ("www.teamskeet.com/t1/trailer/view/55019").replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Eavesdropping And Pussy Popping" + " [TeamSkeet/TeenPies] " + "2019-02-27", score = 101, lang = lang))
    if searchTitle == "Zoe's Fantasy":
        Log("Manual Search Match")
        curID = ("www.teamskeet.com/t1/trailer/view/47562").replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Zoe's Fantasy" + " [TeamSkeet/She's New] " + "2016-06-12", score = 101, lang = lang))
    if searchTitle == "She Has Her Ways":
        Log("Manual Search Match")
        curID = ("www.teamskeet.com/t1/trailer/view/43061").replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "She Has Her Ways" + " [TeamSkeet/TeamSkeet Extras] " + "2014-08-28", score = 101, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    url = str(metadata.id).split("|")[0].replace('+','/')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = "TeamSkeet"

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().split(" | ")[1]

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="gray"]')[1].text_content()

    # Release Date
    releaseDate = detailsPageElements.xpath('//div[@style="width:430px;text-align:left;margin:8px;border-right:3px dotted #bbbbbb;position:relative;"]//div[@class="gray"]')[0].text_content()[12:].replace("th,",",").replace("st,",",").replace("nd,",",").replace("rd,",",")
    date_object = datetime.strptime(releaseDate, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    #Tagline and Collection(s)
    tagline = detailsPageElements.xpath('//div[@style="white-space:nowrap;"]')[0].text_content()[6:].strip()
    endofsubsite = tagline.find('.com')
    tagline = tagline[:endofsubsite].strip()
    metadata.tagline = tagline
    metadata.collections.add(metadata.tagline)

    # Genres
    genres = detailsPageElements.xpath('//a[contains(@href,"?tags=")]')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors

    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[contains(@href,"/profile/")]')
    try:
        if len(actors) > 0:
            for actorLink in actors:
                actorName = actorLink.text_content()
                actorPage = actorLink.get("href")

                try:
                    detailsActorPage = HTML.ElementFromURL(actorPage)
                except:
                    request = urllib.Request(actorPageURL, headers=headers)
                    response = urllib.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
                    htmlstring = response.read()
                    detailsActorPage = fromstring(htmlstring)

                try:
                    actorPhotoURL = detailsActorPage.xpath('//img[@id="profile_image"]')[0].get('src')
                except:
                    actorPhotoURL = ''

                movieActors.addActor(actorName, actorPhotoURL)
    except:
        pass

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//video')[0].get("poster")
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
