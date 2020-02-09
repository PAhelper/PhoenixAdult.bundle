import PAsearchSites
import PAgenres
import PAactors
import googlesearch


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchResultsURLs = []
    shootID = None
    for search in searchTitle.split(' '):
        if unicode(search, 'utf8').isdigit():
            shootID = search
            break

    if shootID:
        sitemapURL = PAsearchSites.getSearchBaseURL(siteNum) + '/sitemap.xml'

        searchResults = HTML.ElementFromURL(sitemapURL)
        for searchResult in searchResults.xpath('//url'):
            sceneURL = searchResult.xpath('.//loc')[0].text_content().strip()
            if ('/movies/' in sceneURL) and (shootID in sceneURL):
                searchResultsURLs.append(sceneURL)
                break

    if not searchResultsURLs:
        domain = PAsearchSites.getSearchBaseURL(siteNum).split('://')[1]

        for sceneURL in googlesearch.search('site:%s %s' % (domain, searchTitle), stop=10):
            sceneURL = sceneURL.rsplit('?', 1)[0]
            if ('/movies/' in sceneURL):
                searchResultsURLs.append(sceneURL)

    for sceneURL in searchResultsURLs:
        detailsPageElements = HTML.ElementFromURL(sceneURL)

        titleNoFormatting = detailsPageElements.xpath('//span[contains(@class, "m_scenetitle")]')[0].text_content().strip()
        sceneID = sceneURL.rsplit('/', 2)[1]
        curID = sceneURL.replace('/', '_').replace('?', '!')
        if "mylfdom" in curID:
            subSite = "MylfDom"
        else:
            subSite = detailsPageElements.xpath('//img[@class="lazy img-fluid"]/@data-original')[0].split('/')[-1].replace('_logo.png', '').title()
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
        if shootID:
            score = 100 - Util.LevenshteinDistance(shootID, sceneID)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [Mylf/%s]' % (titleNoFormatting, subSite), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!').replace('+',',')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Mylf'

    # Title
    metadata.title = detailsPageElements.xpath('//span[contains(@class,"m_scenetitle")]')[0].text_content().strip()

    # Summary
    summary = detailsPageElements.xpath('//div[contains(@class,"text-light")]')[0].text_content().strip()
    metadata.summary = summary.replace('See full video here >', '')

    #Tagline and Collection(s)
    subSite = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = subSite
    metadata.collections.add(subSite)

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
            actorPageURL = actor.get("href")
            if 'http' not in actorPageURL:
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorPageURL
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[contains(@class,"girlthumb")]')[0].get("data-original")
            movieActors.addActor(actorName,actorPhotoURL)

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
    elif subSite.lower() == "MylfDom".lower():
        for genreName in ['BDSM']:
            movieGenres.addGenre(genreName)
    if (len(actors) > 1) and subSite != "Mylfed":
        genres.append("Threesome")
    for genre in genres:
        movieGenres.addGenre(genre)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//video[@id="main-movie-player"]')[0].get('poster')
        art.append(twitterBG)
    except:
        pass

    # Photos
    photos = detailsPageElements.xpath('//div[contains(@class,"trailer-small-images")]//a')
    if len(photos) > 0:
        for photoLink in photos:
            photo = photoLink.get('href')
            if 'http' not in photo:
                photo = PAsearchSites.getSearchBaseURL(siteID) + photo
            art.append(photo)

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            j = j + 1

    return metadata
