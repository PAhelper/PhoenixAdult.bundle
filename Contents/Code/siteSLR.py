import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.lower().replace(" ","-")
    searchResults = HTML.ElementFromURL(url)

    titleNoFormatting = searchResults.xpath('//h1')[0].text_content().strip()
    curID = searchTitle.lower().replace(" ","-", 1).replace(" ","-")
    Log('CURID: ' +  curID)
    releaseDate = parse(searchResults.xpath('//time')[0].get('datetime')).strftime('%Y-%m-%d')

    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+ PAsearchSites.getSearchSiteName(siteNum) +"] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0]
    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
	
    # Studio/Tagline/Collection
    metadata.studio = detailsPageElements.xpath('//div[(contains(@class,"u-block"))]/span/a/span')[0].text_content().strip()
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@class="u-wh u-fs--fo hover:u-lw u-transition--base u-mr--one u-lh--opt"]')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content().lower())


    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[@class="u-wh u-fs--fo hover:u-lw u-transition--base u-mr--one"]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[(contains(@class,"u-ratio u-ratio--top u-ratio--model u-radius--two"))]/img/@data-src')
            movieActors.addActor(actorName,actorPhotoURL[0])
		
    # TITLE
    title = detailsPageElements.xpath('//div[(contains(@class,"u-inline-block u-align-y--m desktop:u-ml--four"))]/h1')[0].text_content().strip()
    metadata.title = title
    Log('Title: ' +  metadata.title)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[(contains(@class,"u-mb--four u-lh--opt u-fs--fo u-fw--medium u-lw"))]')[0].text_content().strip()
    Log('summary: ' +  metadata.summary)
	
    # Date
    date_object = parse(detailsPageElements.xpath('//time[@class="u-inline-block u-align-y--m u-wh u-fw--bold"]')[0].text_content().strip())
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year
	
    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//a[(contains(@class,"u-block u-ratio u-ratio--lightbox u-bgc--bg-opt u-z--zero"))]')
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get('href')
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1		
    backgroundURL = detailsPageElements.xpath('//meta[@property="og:image"]')[0].get('content').split('?')
    metadata.art[backgroundURL[0]] = Proxy.Preview(HTTP.Request(backgroundURL[0], headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata
