import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchString = searchTitle.replace(" ","-").replace(",","").replace("'","").replace("?","").replace('html','').strip()
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString + ".html")

    titleNoFormatting = searchResults.xpath('//title')[0].text_content().strip()
    curID = (PAsearchSites.getSearchSearchURL(siteNum) + searchString + ".html").replace('/','_').replace('?','!')
    if 'upherasshole' in searchResults.xpath('meta[@name="keywords"]')[0].get('content').lower()
        subSite = 'Up Her Asshole'
    elif 'oraloverdose' in searchResults.xpath('meta[@name="keywords"]')[0].get('content').lower()
        subSite = 'Oral Overdose'
    elif 'analoverdose' in searchResults.xpath('meta[@name="keywords"]')[0].get('content').lower()
        subSite = 'Anal Overdose'
    elif 'chocolatebjs' in searchResults.xpath('meta[@name="keywords"]')[0].get('content').lower()
        subSite = 'Chocolate BJs'
    elif 'bangingbeauties' in searchResults.xpath('meta[@name="keywords"]')[0].get('content').lower()
        subSite = 'Banging Beauties'
    else:
        subSite = PAsearchSites.getSearchSiteName(siteNum)
    if searchDate:
        releaseDate = parse(searchDate).strftime('%Y-%m-%d')
    else:
        releaseDate = ''

    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate , name = titleNoFormatting + " [Mylf/"+subSite+"] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    # art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()
    urlBase = PAsearchSites.getSearchBaseURL(siteID)
    # Studio
    metadata.studio = 'Mylf'

    # Title
    metadata.title = detailsPageElements.xpath('//span[contains(@class,"m_scenetitle")]')[0].text_content().strip()
    Log("title: " + metadata.title)

    #Tagline and Collection(s)
    subSite = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = subSite
    metadata.collections.add(subSite)
    Log("subSite: " + subSite)

    # Summary
    summary = detailsPageElements.xpath('//div[contains(@class,"text-light")]')[0].text_content().strip()
    metadata.summary = summary.replace('See full video here >', '')


    # Release Date
    date = str(metadata.id).split("|")[2]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
        Log("Date from file")

    # Actors
    actors = detailsPageElements.xpath('//div[@class="col-12 col-md-8"]//a')
    if len(actors) > 0:
        for actor in actors:
            actorName = actor.xpath('./span')[0].text_content().strip()
            actorPageURL = urlBase + actor.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[contains(@class,"girlthumb")]')[0].get("data-original")
            movieActors.addActor(actorName,actorPhotoURL)
            Log('actor: ' + actorName + ", " + actorPhotoURL)

    ### Posters and artwork ###
    posterNum = 1
    posters = detailsPageElements.xpath('//div[contains(@class,"trailer-small-images")]//a')
    for poster in posters:
        posterURL = poster.get("href")
        if posterURL != "/join":
            if 'http' not in posterURL:
                posterURL = urlBase + posterURL
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            posterNum += 1
            Log('posterURL: ' + posterURL)

    # Video trailer background image
    previewBG = detailsPageElements.xpath('//video[@id="my-video"]')[0].get('poster')
    if 'http' not in previewBG:
        previewBG = urlBase + previewBG
    metadata.art[previewBG] = Proxy.Preview(HTTP.Request(previewBG, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
    Log('previewIMG: ' + previewBG)

    # Genres
    movieGenres.clearGenres()
    genres = ["MILF", "Mature"]
        # Based on site
    if subSite.lower() == "MylfBoss".lower():
        for genreName in ['Office', 'Boss']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "MylfBlows".lower():
        for genreName in ['Blowjob']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "Milfty".lower():
        for genreName in ['Cheating']:
            movieGenres.addGenre(genreName)
    # elif subSite.lower() == "Got Mylf".lower():
    #     for genreName in []:
    #         movieGenres.addGenre(genreName)
    elif subSite.lower() == "Mom Drips".lower():
        for genreName in ['Creampie']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "Milf Body".lower():
        for genreName in ['Gym', 'Fitness']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "Lone Milf".lower():
        for genreName in ['Solo']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "Full Of JOI".lower():
        for genreName in ['JOI']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == "Mylfed".lower():
        for genreName in ['Lesbian', 'Girl on Girl', 'GG']:
            movieGenres.addGenre(genreName)
    if (len(actors) > 1) and subSite != "Mylfed":
        genres.append("Threesome")
    for genre in genres:
        movieGenres.addGenre(genre)

    return metadata
