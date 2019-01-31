import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchResults = HTML.ElementFromURL('https://www.spizoo.com/search.php?query=' + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="category_listing_wrapper_updates"]'):

        titleNoFormatting = searchResult.xpath('.//div[@class="model-update row"]//div[@class="col-sm-6"]')[1].xpath('.//a[@class="ampLink"]//h3')[0].text_content().strip()
        if titleNoFormatting[-3:] == " 4k":
            titleNoFormatting = titleNoFormatting[:-3].strip()
        curID = searchResult.xpath('.//div[@class="model-update row"]//div[@class="col-sm-6"]')[1].xpath('.//a[@class="ampLink"]')[0].get('href').replace('/','_').replace('?','!')

        releaseDate = parse(searchResult.xpath('.//div[@class="model-update row"]//div[@class="col-sm-6"]')[1].xpath('.//div[@class="row model-update-data"]//div[@class="col-5 col-md-5"]//div[@class="date-label"]')[0].text_content()[22:].strip()).strftime('%Y-%m-%d')

        girlName = searchResult.xpath('.//div[@class="model-update row"]//div[@class="col-sm-6"]')[1].xpath('.//div[@class="row model-update-data"]//div[@class="col-5 col-md-5"]//div[@class="model-labels"]//span[@class="update_models"]//a')[0].get('title').strip()

        Log("CurID" + str(curID))
        
        titleNoFormatting = girlName + " - " + titleNoFormatting + " [Spizoo] " + releaseDate
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0].replace('_', '/').replace('!','?')

    url = temp
    Log('url :' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    metadata.studio = "Spizoo"

    # Summary
    paragraph = detailsPageElements.xpath('//p[@class="description"]')[0].text_content().strip()
    metadata.summary = paragraph
    metadata.collections.clear()
    try:
        tagline = detailsPageElements.xpath('//i[@id="site"]')[0].get('value').strip()
    except:
        tagline = "Spizoo"
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    if title[-3:] == " 4k":
        title = title[:-3].strip()
    metadata.title = title

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@id="trailer-data"]//div[@class="col-12 col-md-6"]//div[@class="row"]//div[@class="col-12"]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().lower().strip()
            movieGenres.addGenre(genreName)

    # Date
    date = detailsPageElements.xpath('//p[@class="date"]')
    if len(date) > 0:
        date = date[0].text_content()[:10]
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    titleActors = ""
    actors = detailsPageElements.xpath('//div[@id="trailer-data"]//div[@class="col-12 col-md-6"]//div[@class="row line"]//div[@class="col-3"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorPageURL = 'https://www.spizoo.com' + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorName = actorPage.xpath('//div[@class="model-titular col-12"]//h1')[0].text_content()
            titleActors = titleActors + actorName + " & "
            actorPhotoURL = "https://www.spizoo.com" + actorPage.xpath('//div[@class="model-bio-pic"]//img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)
        titleActors = titleActors[:-3]
        metadata.title = metadata.title


    # Posters
    background = "https://www.spizoo.com/" + detailsPageElements.xpath('//img[@class="update_thumb thumbs"]')[0].get('src')
    Log("BG DL: " + background)
    posterURL = background[:-5]
    Log("Poster: " + posterURL)
    for i in range(1, 8):
        metadata.art[posterURL + str(i) + ".jpg"] = Proxy.Preview(HTTP.Request(posterURL + str(i) + ".jpg", headers={'Referer': 'http://www.google.com'}).content, sort_order = 8-i)
        metadata.posters[posterURL + str(i) + ".jpg"] = Proxy.Preview(HTTP.Request(posterURL + str(i) + ".jpg", headers={'Referer': 'http://www.google.com'}).content, sort_order = i)

    return metadata
