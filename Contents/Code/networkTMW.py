import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchPageNum = 1
    while searchPageNum <= 5:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "&page=" + str(searchPageNum))
        for searchResult in searchResults.xpath('//article'):
            if len(searchResult.xpath('//article')) > 0:
                titleNoFormatting = searchResult.xpath('.//h1')[0].text_content().strip()
                curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
                releaseDate = parse(searchResult.xpath('.//time')[0].text_content()).strftime('%Y-%m-%d')
                subSite = searchResult.xpath('.//div[@class="site"]/a')[0].text_content().replace('.com','').strip()
                if searchDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [TMW/" + subSite + "] " + releaseDate, score = score, lang = lang))
        searchPageNum += 1
    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="title-line"]/h1')[0].text_content().strip()

    # Studio/Tagline/Collection
    metadata.studio = "Teen Mega World"
    subSite = detailsPageElements.xpath('//div[@class="site"]/a')[0].text_content().replace('.com','').strip()
    metadata.tagline = subSite
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="text"]//p')[0].text_content().strip()

    # Date
    date = detailsPageElements.xpath('//div[@class="date"]//time')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="video"]//div[@class="site"]//a[position()>1]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPageURL = actorLink.get('href')
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPageElements.xpath('//div[@class="photo"]//img')[0].get("data-src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[@class="tag-list"]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genre = genreLink.text_content()
            movieGenres.addGenre(genre)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//video')[0].get('poster')
        art.append(twitterBG)
    except:
        twitterBG = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//deo-video')[0].get('cover-image')
        art.append(twitterBG)

    j = 1
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            j = j + 1

    return metadata