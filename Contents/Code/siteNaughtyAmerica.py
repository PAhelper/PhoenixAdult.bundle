import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@id="ajax-results"]/div/div'):
        titleNoFormatting = searchResult.xpath('./a')[0].get("title")
        curID = searchResult.xpath('./a')[0].get('href')
        curID = curID[:-26]
        curID = curID.replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('./p[@class="entry-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [NA] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = "Naughty America"

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="synopsis grey-text"]')[0].text_content().replace('Synopsis','').strip()

    # Tagline and Collection(s)
    subSite = detailsPageElements.xpath('//div[@class="scene-info"]/a[@class="site-title grey-text link"]')[0].text_content().strip()
    metadata.tagline = subSite
    metadata.collections.add(metadata.tagline)

    # Genres
    genres = detailsPageElements.xpath('//a[@class="cat-tag"]')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="entry-date light-grey-text"]')[0].text_content().strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
        
    # Actors
    actors = detailsPageElements.xpath('//a[contains(@class,"scene-title grey-text")]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            try:
                actorPageURL = actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = "http:" + actorPage.xpath('//img[@class="performer-pic"]')[0].get("src")
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)


    ### Posters and artwork ###

    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    # Video trailer background image
    try:
        background = "http:" + detailsPageElements.xpath('//video')[0].get("poster")
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    try:
        background = "http:" + detailsPageElements.xpath('//img[@class="start-card"]')[0].get("src")
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    # Photos
    posters = detailsPageElements.xpath('//a[contains(@class,"scene-image")]')
    posterNum = 1
    for posterCur in posters:
        posterURL = "http:" + posterCur.get("href")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1
    return metadata
