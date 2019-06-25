import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchString = searchTitle.replace(' ','-').replace("'","-")
    actressSearchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString + "/")
    actressPageUrl = actressSearchResults.xpath('//div[@class="item-inside"]//a')[0].get('href')
    searchResults = HTML.ElementFromURL(actressPageUrl)
    for searchResult in searchResults.xpath('//div[contains(@class,"listing-videos")]//div[@class="item"]'):
        titleNoFormatting = searchResult.xpath('.//span[@class="title"]')[0].text_content()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().replace("th","").replace('st','').strip()).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        subSiteRaw = searchResult.xpath('.//div[@class="meta"]//span[@class="date-and-site"]//span')[0].text_content()
        Log("subSite: " + releaseDate)
        if subSiteRaw == 'kha':
            subSite = 'KarupsHA'
        elif subSiteRaw == 'kow':
            subSite = 'KarupsOW'
        elif subSiteRaw == 'kpc':
            subSite = 'KarupsPC'
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            searchSubSite = PAsearchSites.getSearchFilter(siteNum)
            score = 100 - Util.LevenshteinDistance(searchSubSite.lower(), subSite.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + subSite + "] " + releaseDate, score = score, lang = lang))
    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//h1//span[@class="title"]')[0].text_content().strip()
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "Karups"
    subSite = detailsPageElements.xpath('//h1//span[@class="sup-title"]//span')[0].text_content().strip()
    metadata.tagline = subSite
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)


    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="content-information-description"]//p')[0].text_content()
    except:
        Log('No summary found')

    # Date
    date = detailsPageElements.xpath('//span[@class="date"]/span[@class="content"]')[0].text_content().replace(subSite,"").replace('Video added on','').strip()
    Log("date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//span[@class="models"]//a')
    Log("actors #: " + str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            Log("Actor: " + actorName)
            actorPageURL = actorLink.get('href')
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPageElements.xpath('//div[@class="model-thumb"]//img')[0].get("src")
            Log("ActorPhotoURL: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    if subSite == 'KarupsHA':
        genres = ["Amateur"]
    if subSite == 'KarupsPC':
        genres = []
    if subSite == 'KarupsOW':
        genres = ["MILF"]
    for genre in genres:
        movieGenres.addGenre(genre)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    try:
        background = detailsPageElements.xpath('//div[@class="video-player"]//video')[0].get("poster")
        metadata.art[background] = Proxy.Preview(
            HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
        metadata.posters[background] = Proxy.Preview(
            HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
        Log("BG URL: " + background)
    except:
        pass
    try:
        background = detailsPageElements.xpath('//img[@class="poster"]')[0].get("src")
        metadata.art[background] = Proxy.Preview(
            HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
        metadata.posters[background] = Proxy.Preview(
            HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
        Log("BG URL: " + background)
    except:
        pass


    posters = detailsPageElements.xpath('//div[@class="video-thumbs"]//img')
    Log(str(len(posters)) + " thumbs found.")
    posterNum = 2
    for posterCur in posters:
        posterURL = posterCur.get("src")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum += 1




    return metadata
