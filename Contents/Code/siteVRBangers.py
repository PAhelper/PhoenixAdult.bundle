import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//article'):
        titleNoFormatting = searchResult.xpath('.//a[@rel="bookmark"]')[0].text_content().strip()
        detailsPageElements = HTML.ElementFromURL(searchResult.xpath('.//a[@rel="bookmark"]')[0].get('href'))
        releaseDate = parse(detailsPageElements.xpath('//p[@class="pull-right dates invisible"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        curID = searchResult.xpath('.//a[@rel="bookmark"]')[0].get('href').replace('/','_').replace('?','!')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        if len(titleNoFormatting) > 29:
            titleNoFormatting = titleNoFormatting[:32] + "..."

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Studio
    metadata.studio = "VR Bangers"

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="video-info-title"]//h1[@class="pull-left page-title"]//span')[0].text_content()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="mainContent"]/p')[0].text_content().strip()

    # Tagline and Collection
    tagline = "VR Bangers"
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//p[@class="pull-right dates invisible"]')[0].text_content()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="video-tags"]//a[@class="tags-item"]')
    if len(genres) > 0:
        for genre in genres:
            Log('genre: ' + genre.text_content())
            movieGenres.addGenre(genre.text_content())

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="girls-name"]//div[@class="girls-name-video-space"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().replace(", ","")
            Log('actor: ' + actorName)
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="single-model-featured"]//img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//*[@id="single-video-gallery-free"]//a')
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get("href")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1

    # backgroundURL = detailsPageElements.xpath('//img[@class="video-image"]')[0].get("src").split('?')
    # metadata.art[backgroundURL[0]] = Proxy.Preview(HTTP.Request(backgroundURL[0], headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata
