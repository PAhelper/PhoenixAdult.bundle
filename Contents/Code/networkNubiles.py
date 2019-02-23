import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.lower().replace(" ","-").replace("'","-")
    searchResults = HTML.ElementFromURL(url)

    searchResult = searchResults.xpath('//div[@class="descrips"]')[0]
    titleNoFormatting = searchResult.xpath('//span[@class="wp-title videotitle"]')[0].text_content()
    curID = searchTitle.lower().replace(" ","-").replace("'","-")
    releaseDate = parse(searchResult.xpath('.//div[@class="row"]//div[@class="col-lg-6 col-sm-6"]//span')[0].text_content().strip()).strftime('%Y-%m-%d')

    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0]

    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//span[contains(@class,"wp-title")]')[0].text_content().strip()

    # Studio
    metadata.studio = "Nubiles"

    # Summary
    try:
        paragraphs = detailsPageElements.xpath('//div[@class="video-description"]/article/p')
        pNum = 0
        summary = ""
        for paragraph in paragraphs:
            if pNum >= 0 and pNum < (len(paragraphs)):
                summary = summary + '\n\n' + paragraph.text_content()
            pNum += 1
    except:
        summary = detailsPageElements.xpath('//div[@class="video-description"]/article')[0].text_content().strip()
    metadata.summary = summary.strip()

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Date
    date = detailsPageElements.xpath('//div[@class="descrips"]//div[@class="row"]//div[@class="col-lg-6 col-sm-6"]//span')[10].text_content().strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//span[@class="featuring-modelname model"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL((PAsearchSites.getSearchBaseURL(siteID)+actorPageURL))
            actorPhotoURL = "http:"+actorPage.xpath('//img[@class="img-responsive"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="tags categories"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Posters
    background = "http:" + detailsPageElements.xpath('//div[@id="watchpagevideo"]//div[@class="edgeCMSVideoPlayer"]//video')[0].get('poster')
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata