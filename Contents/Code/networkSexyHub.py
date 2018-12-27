import PAsearchSites
import PAgenres

#SexyHub sites:
#MassageRooms
#MomXXX
#DaneJones
#Lesbea
#Girlfriends
#FitnessRooms

#FakeHub sites:
#FakeAgent
#FakeAgentUK
#FakeCop
#FakeTaxi
#FakeHospital
#FemaleAgent
#PublicAgent
#FemaleFakeTaxi
#FakeDrivingSchool


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
    for searchResult in searchResults.xpath('//article[@class="release-card scene"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="card-title"]/a')[0].get('title')
        curID = (PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//div[@class="card-title"]/a')[0].get('href')).replace('/','_').replace('?','!')
        subSite = searchResult.xpath('.//div[@class="site-domain"]')[0].text_content().strip().replace(' ','')
        releaseDate = parse(searchResult.xpath('.//div[@class="release-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [SexyHub/"+subSite+"] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'SexyHub'
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.summary  = detailsPageElements.xpath('//div[@class="overview"]/p')[0].text_content().strip()
    metadata.collections.clear()
    subSite = detailsPageElements.xpath('//div[@class="collection-logo"]/img')[0].get('alt')
    if "danejones" in subSite:
        tagline = "DaneJones"
    elif "lesbea" in subSite:
        tagline = "Lesbea"
    elif "momxxx" in subSite:
        tagline = "MomXXX"
    elif "fitnessrooms" in subSite:
        tagline = "FitnessRooms"
    elif "girlfriends" in subSite:
        tagline = "Girlfriends"
    elif "massagerooms" in subSite:
        tagline = "MassageRooms"
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="col-tags"]//a[@rel="nofollow"]')
    Log("Genres found: "+str(len(genres)))
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//time')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="tag-group"]//a')
    Log("Actors found: "+str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID)+actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = "http:" + actorPage.xpath('//img[@class="card-image load"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    #Posters
    i = 1
    try:
        tmp = detailsPageElements.xpath('//div[@id="player"]')[0].get('style')
        k = tmp.find("url(")
        j = tmp.rfind(")")
        background = "http:" + tmp[k+4:j]
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    return metadata
