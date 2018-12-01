import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchSiteName = PAsearchSites.getSearchSiteName(searchSiteID)
    searchResults = HTML.ElementFromURL('https://www.private.com/search.php?query=' + encodedTitle)
    for searchResult in searchResults.xpath('//ul[@id="search_results"]//li[@class="col-lg-3 col-md-4 col-sm-6 col-xs-6"]'):
        Log(searchResult.get('class'))
        titleNoFormatting = searchResult.xpath('.//div[@class="scene"]//div//h3//a')[0].text_content()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//div[@class="scene"]//div//h3//a')[0].get('href').replace('/','_')
        Log("ID: " + curID)
        # releasedDate = searchResult.xpath('.//div[@class="release-info"]//div[@class="views-date-box"]//span[@class="date-added"]')[0].text_content()

        girlName = searchResult.xpath('.//div[@class="scene"]//div//p[@class="scene-models"]//a')[0].text_content()

        Log("CurID" + str(curID))
        lowerResultTitle = str(titleNoFormatting).lower()
        
        titleNoFormatting = girlName + " - " + titleNoFormatting + " [Private]"
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    return results


def update(metadata, siteID, movieGenres):
    temp = str(metadata.id).split("|")[0].replace('_', '/')

    url = temp
    Log('url :' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    metadata.studio = "Private"

    # Summary
    paragraph = detailsPageElements.xpath('//meta[@itemprop="description"]')[0].get('content')
    # paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n', '').replace('  ', '') + "\n\n"
    metadata.summary = paragraph[:-10]
    tagline = detailsPageElements.xpath('//span[@class="title-site"]')[0].text_content()
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[contains(@class,"scene-tags")]//li')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.xpath('//a')[0].text_content().lower()
            movieGenres.addGenre(genreName)

    # Date
    date = detailsPageElements.xpath('//meta[@itemprop="uploadDate"]')[0].get('content')
    if len(date) > 0:
        date_object = datetime.strptime(date, '%m/%d/%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    titleActors = ""
    actors = detailsPageElements.xpath('//ul[@id="featured_pornstars"]//li[@class=" col-md-4 col-sm-6 col-xs-6 featuring"]')
    if len(actors) > 0:
        for actorPage in actors:
            role = metadata.roles.new()

            actorName = actorPage.xpath('.//div[@class="model"]//a')[0].get("title")
            titleActors = titleActors + actorName + " & "
            role.name = actorName
            actorPhotoURL = actorPage.xpath('.//div[@class="model"]//a//picture//img')[0].get("src")
            role.photo = actorPhotoURL
        titleActors = titleActors[:-3]
        metadata.title = metadata.title


    # Posters
    art = detailsPageElements.xpath('//meta[@itemprop="thumbnailUrl"]')[0].get('content')
    Log("posters DL: " + art)
    metadata.posters[art] = Proxy.Preview(HTTP.Request(art, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)

    backgrounds = detailsPageElements.xpath('//div[@class="slick-slide"]')
    posterNum = 1
    Log('Len ' + str(len(backgrounds)))
    for background in backgrounds:
        Log(background.get("class"))
        img = background.xpath('.//a')[0].get("href")
        metadata.art[img] = Proxy.Preview(HTTP.Request(posterURL + str(i) + ".jpg", headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        metadata.posters[img] = Proxy.Preview(HTTP.Request(posterURL + str(i) + ".jpg", headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1

    return metadata
