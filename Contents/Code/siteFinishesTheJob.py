import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="scene"]'):
        titleNoFormatting = searchResult.xpath('.//h4[@itemprop="name"]//a')[0].text_content()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//small[@class="date"]')[0].text_content().replace("Added:","").strip()).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        subSite = searchResult.xpath('.//small[@class="shadow"]//a')[0].text_content().strip()
        Log("subSite: " + subSite)
        if subSite.lower().replace(".com","").replace(" ","") == PAsearchSites.getSearchSiteName(siteNum).lower().replace(" ",""):
            siteScore = 10
            Log("subSite Match")
        else:
            siteScore = 0
            Log("subSite mismatch")
        if searchDate:
            score = siteScore + 90 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = siteScore + 90 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + subSite + "] " + releaseDate, score = score, lang = lang))

    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    sceneTitle = detailsPageElements.xpath('//h1[@itemprop="name"]')[0].text_content().strip()
    metadata.title = sceneTitle
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "Finishes The Job"
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Summary
    metadata.summary = detailsPageElements.xpath('//section[@class="scene-content"]//p[@itemprop="description"]')[0].text_content().strip()
    Log("Scene Summary: " + metadata.summary[:20])

    # Date
    date = detailsPageElements.xpath('//section[@class="scene-content"]//p[2]')[0].text_content().replace("Added:","").strip()
    Log("Scene Date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//section[@class="scene-content"]//h4//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            Log("Actress: " + actorName)
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//section[@class="scene-content"]//p[1]//a')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())
            Log("Genre: " + genre.text_content())

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posterNum = 1

    # Poster
    posters = detailsPageElements.xpath('//section[contains(@class,"featured-set-a")]//a//img')
    for posterCur in posters:
        sceneName = posterCur.get("alt")
        if sceneName.lower() == sceneTitle.lower():
            posterURL = posterCur.get("src")
            Log("Found poster: " + posterURL)
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            posterNum += 1

    # Background
    try:
        backgroundURL = detailsPageElements.xpath('//aside[@class="scene-aside"]//link[@itemprop="thumbnailUrl"]')[0].get("href")
    except:
        try:
            backgroundURL = detailsPageElements.xpath('//aside[@class="scene-aside"]//img')[0].get("src")
        except:
            backgroundURL = ''
            Log("background not found")
    metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)

    return metadata
