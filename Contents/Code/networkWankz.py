import PAsearchSites
import PAgenres


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="scene"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="title-wrapper"]//a[@class="title"]')[0].text_content()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        Log("curID: " + curID)
        # No releaseDate available on search page
        # releaseDate = parse(searchResult.xpath('.//small[@class="date"]')[0].text_content().replace("Added:","").strip()).strftime('%Y-%m-%d')
        # Log("releaseDate: " + releaseDate)
        subSite = searchResult.xpath('.//div[@class="series-container"]//a[@class="sitename"]')[0].text_content()
        Log("subSite: " + subSite)
        siteScore = 80 - (Util.LevenshteinDistance(subSite.lower(), PAsearchSites.getSearchSiteName(siteNum).lower())*8/10)
        Log("siteScore: " + str(siteScore))
        titleScore = 20 - (Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())*2/10)
        Log("titleScore: " + str(titleScore))
        score = siteScore + titleScore
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + subSite + "]", score = score, lang = lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    sceneTitle = detailsPageElements.xpath('//div[@class="title"]//h1')[0].text_content().replace('HD','').strip()
    metadata.title = sceneTitle
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "Wankz"
    metadata.tagline = detailsPageElements.xpath('//div[@class="bc"]/a[3]')[0].text_content().strip()
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="description"]//p')[0].text_content()
    Log("Scene Summary: " + metadata.summary[:20])

    # Date
    date = detailsPageElements.xpath('//div[@class="views"]//span')[0].text_content().replace("Added","").strip()
    Log("Scene Date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[@class="model"]')
    if len(actors) > 0:
        for actor in actors:
            actorName = actor.xpath('.//span')[0].text_content().strip()
            Log("Actor: " + actorName)
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@class="cat"]')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())
            Log("Genre: " + genre.text_content())

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    try:
        backgroundURL = detailsPageElements.xpath('//a[contains(@class,"noplayer")]//img')[0].get("src")
    except:
        backgroundURL = ''
    metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata
