import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):

    url = PAsearchSites.getSearchSearchURL(searchSiteID) + searchTitle.lower().replace(" ","-")
    searchPage = HTML.ElementFromURL(url)

    titleNoFormatting = searchPage.xpath('//h1')[0].text_content().replace("VR Porn video","").strip()
    Log("Result Title: " + titleNoFormatting)
    curID = searchPage.xpath('//link[@rel="canonical"]')[0].get("href").replace('/','_').replace('?','!')
    Log("curID: " + curID)
    actors = searchPage.xpath('//div[@class="w-portfolio-item-image modelBox"]//img')
    firstActor = actors[0].get('alt')

    script_text = searchPage.xpath('//script[@type="application/ld+json"]')[1].text_content()
    alpha = script_text.find('datePublished')
    omega = script_text.find('"',alpha+16)
    script_date = script_text[alpha+16:omega]
    releaseDate = parse(script_date).strftime('%Y-%m-%d')
    Log("releaseDate:" + releaseDate)
    resultTitle = firstActor + " - " + titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(searchSiteID) + "] " + releaseDate
    if searchDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = resultTitle, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):

    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    Log('url: ' + url)
    detailsPageElements = HTML.ElementFromURL(url)


    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().replace("VR Porn video","").strip()
    Log('Title: ' + metadata.title)

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    Log('Studio: ' + metadata.studio)

    # Summary
    description = detailsPageElements.xpath('//div[@class="g-cols onlydesktop"]')
    if description:
        metadata.summary = description[0].text_content()

    # Tagline and Collection
    metadata.collections.clear()
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.add(metadata.studio)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@class="g-btn type_default"]//span')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="w-portfolio-item-image modelBox"]//img')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.get("alt")
            actorPhotoURL = actorLink.get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//a[contains(@class,"w-gallery-tnail")]')
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get("href")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1

    backgroundURL = detailsPageElements.xpath('//dl8-video')[0].get("poster")
    metadata.art[backgroundURL] = Proxy.Preview(HTTP.Request(backgroundURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Date
    script_text = detailsPageElements.xpath('//script[@type="application/ld+json"]')[1].text_content()
    alpha = script_text.find('datePublished')
    omega = script_text.find('"',alpha+16)
    date = script_text[alpha+16:omega]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    return metadata
