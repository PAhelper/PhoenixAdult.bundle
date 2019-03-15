import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL('https://www.mofos.com/tour/search/?q=' + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="widget-release-card"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="title details-only"]//a')[0].text_content().strip()
        subSite = searchResult.xpath('.//a[@class="site-name"]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//span[@class="date-added"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Mofos/" + subSite + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Mofos'
    temp = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//p[@class="desc"]')[0].text_content()
    #paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = paragraph
    tagline = detailsPageElements.xpath('//a[@class="site-name"]')[0].text_content().strip()
    searchQuery = ''
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1[@class="title"]')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="categories"]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[@class="model-name"]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorName = actorName.replace("\xc2\xa0", " ")
            searchQuery = searchQuery + " " + actorName
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
            actorPhotoURL = "http:" + actorPage.xpath('//img[@class="model-pic"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Release Date
    searchQuery = searchQuery.replace(' ','+')
    searchPageElements = HTML.ElementFromURL('https://www.mofos.com/tour/search/?q=' + searchQuery)
    date = searchPageElements.xpath('//span[@class="date-added"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    #Posters
    background = "https:" + detailsPageElements.xpath('//*[@id="trailer-player"]/img')[0].get('src')
    Log("BG DL: " + background)
    posterURL = background[:-5]
    Log("Poster: " + posterURL)
    for i in range(1, 6):
        metadata.art[posterURL + str(i) + ".jpg"] = Proxy.Preview(HTTP.Request(posterURL + str(i) + ".jpg", headers={'Referer': 'http://www.google.com'}).content, sort_order = 6-i)
        metadata.posters[posterURL + str(i) + ".jpg"] = Proxy.Preview(HTTP.Request(posterURL + str(i) + ".jpg", headers={'Referer': 'http://www.google.com'}).content, sort_order = i)

    return metadata
