import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchString = encodedTitle.replace(" ","+")
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    Log("Results found: " + str(len(searchResults.xpath('//div[contains(@class,"episode__preview")]'))))
    i = 0
    for searchResult in searchResults.xpath('//div[contains(@class,"episode__preview")]/div[contains(@class,"episode__title")]/a/h2'):
        titleNoFormatting = searchResult.xpath('//div[contains(@class,"episode__preview")]/div[contains(@class,"episode__title")]/a/h2')[i].text_content().title().strip()
        Log ("Title: " +titleNoFormatting)
        curID = PAutils.Encode(searchResult.xpath('//div[contains(@class,"episode__preview")]/div[contains(@class,"episode__title")]/a')[i].get('href'))
        Log("curID: " +curID)
        releaseDate = ""
        Log("No date available (XVirtual)")
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        Log("Score: " + str(score))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
        i = i +1
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    path = PAutils.Decode(str(metadata.id).split("|")[0])
    url = PAsearchSites.getSearchBaseURL(siteID) + path
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio/Tagline/Collection
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # TITLE
    title = detailsPageElements.xpath('//div[contains(@class,"title")]/h2')[0].text_content().strip()
    metadata.title = title
    Log('Title: ' +  metadata.title)
	
    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[contains(@class,"tags")]//a')
    for genreLink in genres:
        genreName = genreLink.text_content().strip().lower()
        movieGenres.addGenre(genreName)
	
    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class,"description")]/div[contains(@class,"desc-text")]/p')[0].text_content().strip()
    Log('summary: ' +  metadata.summary)
	
    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//div[contains(@class,"thumbnails small-block-grid-2 medium-block-grid-3")]/a/img')
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get('src')
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1
    backgroundURL = detailsPageElements.xpath('//meta[@property="og:image"]')[0].get('content').split('?')
    metadata.art[backgroundURL[0]] = Proxy.Preview(HTTP.Request(backgroundURL[0], headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
	
    return metadata
