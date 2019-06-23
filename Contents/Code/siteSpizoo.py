import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="category_listing_wrapper_updates"]'):

        titleNoFormatting = searchResult.xpath('.//h3')[0].text_content().strip()
        if titleNoFormatting[-3:] == " 4k":
            titleNoFormatting = titleNoFormatting[:-3].strip()
        curID = searchResult.xpath('.//a[@class="ampLink"]')[0].get('href').replace('/','_').replace('?','!')
        try:
            releaseDate = parse(searchResult.xpath('.//div[@class="date-label"]')[0].text_content()[22:].strip()).strftime('%Y-%m-%d')
        except:
            releaseDate = ''

        if searchDate and releaseDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Spizoo] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0].replace('_', '/').replace('!','?')

    url = temp
    detailsPageElements = HTML.ElementFromURL(url)

    metadata.studio = "Spizoo"

    # Summary
    paragraph = detailsPageElements.xpath('//p[@class="description"] | //p[@class="description-scene"]')[0].text_content().strip()
    metadata.summary = paragraph
    metadata.collections.clear()
    try:
        tagline = detailsPageElements.xpath('//i[@id="site"]')[0].get('value').strip()
    except:
        if 'rawattack' in url:
            tagline = "RawAttack"
        else:
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
    else: #Manual genres for Rawattack
        if siteID == 577:
            movieGenres.addGenre('Unscripted')
            movieGenres.addGenre('Raw')
            movieGenres.addGenre('Hardcore')

    # Date
    date = detailsPageElements.xpath('//p[@class="date"]')
    if len(date) > 0:
        date = date[0].text_content()[:10]
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@id="trailer-data"]//div[@class="col-12 col-md-6"]//div[@class="row line"]//div[@class="col-3"]//a | //p[@class="featuring"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().replace('.','').strip()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            try:
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPage.xpath('//div[@class="model-bio-pic"]//img')[0].get("src")
            except:
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPage.xpath('//div[@class="model-bio-pic"]//img')[0].get("src0_1x")
            movieActors.addActor(actorName,actorPhotoURL)


    # Posters
    try:
        background = PAsearchSites.getSearchBaseURL(siteID) + "/" + detailsPageElements.xpath('//img[contains(@class,"update_thumb thumbs")]')[0].get('src')
        Log("Background: " + background)
    except:
        pass

    posterURL = background[:-5]
    Log("Poster: " + posterURL)
    for i in range(1, 8):
        try:
            metadata.art[posterURL + str(i) + ".jpg"] = Proxy.Preview(HTTP.Request(posterURL + str(i) + ".jpg", headers={'Referer': 'http://www.google.com'}).content, sort_order = 8-i)
            metadata.posters[posterURL + str(i) + ".jpg"] = Proxy.Preview(HTTP.Request(posterURL + str(i) + ".jpg", headers={'Referer': 'http://www.google.com'}).content, sort_order = i)
        except:
            pass

    return metadata
