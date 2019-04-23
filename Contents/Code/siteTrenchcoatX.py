import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchPageNum = 1
    while searchPageNum <= 3:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "&page=" + str(searchPageNum))
        for searchResult in searchResults.xpath('//div[@class="list-group-item"]'):
            if len(searchResult.xpath('//div[@class="list-group-item"]')) > 0:
                titleNoFormatting = searchResult.xpath('.//h3')[0].text_content().strip()
                Log("Result Title: " + titleNoFormatting)
                curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
                Log("curID: " + curID)
                releaseDate = parse(searchResult.xpath('.//ul//li[1]')[0].text_content().replace('Added On :','').strip()).strftime('%Y-%m-%d')
                Log("releaseDate: " + releaseDate)
                actors = searchResult.xpath('.//ul//li[2]//a')
                Log("# actors: " + str(len(actors)))
                firstActor = actors[0].text_content().strip()
                Log("firstActor: " + firstActor)
                seriesName = searchResult.xpath('.//h4//a')[0].text_content()
                Log("Series Name: " + seriesName)
                if searchDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = seriesName + ": " + titleNoFormatting + " [TrenchcoatX] " + releaseDate, score = score, lang = lang))
        searchPageNum += 1
    return results

def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Series Name
    seriesName = detailsPageElements.xpath('//h4//a')[0].text_content().strip()
    Log("seriesName: " + seriesName)

    # Title
    title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    metadata.title = title + " (" + seriesName + ")"
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "TrenchcoatX"
    metadata.tagline = seriesName
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)
    metadata.collections.add(metadata.studio)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="col-sm-8 pad-md-bottom"]//p[2]')[0].text_content().strip()
    except:
        metadata.summary = ''
        Log('No summary found')

    # Date
    date = detailsPageElements.xpath('//div[@class="col-sm-8 pad-md-bottom"]//ul//li[1]')[0].text_content().replace('Added On :','').strip()
    Log("date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="col-sm-8 pad-md-bottom"]//ul//li[2]//a')
    Log("actors #: " + str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            Log("Actor: " + actorName)
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="col-sm-8 pad-md-bottom"]//ul[2]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genre = genreLink.text_content()
            movieGenres.addGenre(genre)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    try:
        background = detailsPageElements.xpath('//img[contains(@class,"update_thumb")]')[0].get("src0_1x")
    except:
        background = detailsPageElements.xpath('//img[contains(@class,"update_thumb")]')[0].get("src")

    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    Log("BG URL: " + background)

    posterURL = detailsPageElements.xpath('//img[contains(@class,"img-full-width")]')[0].get("src0_1x")
    metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata