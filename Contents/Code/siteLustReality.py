import PAsearchSites
import PAgenres


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.lower().replace(" ","-", 1).replace(" ","-")
    searchResults = HTML.ElementFromURL(url)

    titleNoFormatting = searchResults.xpath('//h1')[0].text_content().strip()
    curID = searchTitle.lower().replace(" ","-", 1).replace(" ","-")
    releaseDate = parse(searchResults.xpath('//span[@class="date-display-single"] | //span[@class="u-inline-block u-mr--nine"] | //div[@class="video-meta-date"] | //div[@class="date"]')[0].text_content().strip()).strftime('%b %d, %Y')

    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+ PAsearchSites.getSearchSiteName(siteNum) +"] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0]
    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Studio
    metadata.studio = "Lust Reality"

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="u-mb--six u-fs--fo u-lh--normal"]')[0].text_content().strip()

    # Date
    date_object = parse(detailsPageElements.xpath('//span[@class="date-display-single"] | //span[@class="u-inline-block u-mr--nine"] | //div[@class="video-meta-date"] | //div[@class="date"]')[0].text_content().strip())
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year
	
    # Studio/Tagline/Collection
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)
	
    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[@class="u-list u-list--inline u-fs--th u-ff--alt"]/li/a')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content().lower())

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="video-actress-name"]//a | //div[@class="u-mt--three u-mb--three"]//a | //div[@class="model-one-inner js-trigger-lazy-item"]//a | //div[@class="featuring commed"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[contains(@class,"u-ratio--model-poster")]//img/@data-src')
            movieActors.addActor(actorName,actorPhotoURL[0])

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//a[@class="u-block u-ratio u-ratio--lightbox u-bgc--bg-opt u-z--zero"]')
    posterNum = 1
    for posterCur in posters:
        posterURLfull = posterCur.get("href").split('?')
        posterURL = posterURLfull[0]
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.bing.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1

    backgroundStyle = detailsPageElements.xpath('//div[@class="splash-screen fullscreen-message is-visible"]')[0].get("style")
    alpha = backgroundStyle.find('url(')+4
    omega = backgroundStyle.find('.jpg')+4
    background = backgroundStyle[alpha:omega]
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata
