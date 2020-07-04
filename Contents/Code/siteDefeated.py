import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchString = encodedTitle.replace(" ","+")
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    Log("Results found: " + str(len(searchResults.xpath('//h2[contains(@class,"post-title") and contains(@class,"entry-title")]'))))
    i = 0
    for searchResult in searchResults.xpath('//h2[contains(@class,"post-title") and contains(@class,"entry-title")]'):
        titleNoFormatting = searchResult.xpath('//h2[contains(@class,"post-title") and contains(@class,"entry-title")]')[i].text_content().title().strip()
        Log ("Title: " +titleNoFormatting)
        curID = PAutils.Encode(searchResult.xpath('//h2[contains(@class,"post-title") and contains(@class,"entry-title")]/a')[i].get('href'))
        Log("curID: " +curID)
        try:
            releaseDate3 = searchResult.xpath('//meta[@itemprop="datePublished"]')[i].get('content').split("T")
            releaseDate = releaseDate3[0].strip()
            Log("releaseDate: " +releaseDate)
        except:
            releaseDate = ""
            Log("No date found (Defeated)")
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        Log("Score: " + str(score))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
        i = i +1
		
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    path = PAutils.Decode(str(metadata.id).split("|")[0])
    url = PAsearchSites.getSearchBaseURL(siteID) + path
    detailsPageElements = HTML.ElementFromURL(path)
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
    title = detailsPageElements.xpath('//meta[@property="og:title"]')[0].get('content').split("|")
    titleFixed = title[0].strip()
    metadata.title = titleFixed
    Log('Title: ' +  metadata.title)

    # Summary
    metadata.summary = ((detailsPageElements.xpath('//meta[@property="og:description"]')[0].get('content')) + ("..."))
    Log('summary: ' +  metadata.summary)
	
    # Rating
    rating = detailsPageElements.xpath('//div[(contains(@class,"gdrts-rating-text"))]/strong')[0].text_content().strip()
    metadata.rating = ((float(rating))*2)
    Log('rating: ' +  rating + '*2')

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//img[(contains(@class,"alignnone") and ((contains(@class,"size-full")) or (contains(@class,"size-medium")))) and not(contains(@class,"wp-image-4512"))]')
    posters2 = detailsPageElements.xpath('//div[(contains(@class,"iehand"))]/a')
    posters3 = detailsPageElements.xpath('//a[contains(@class,"colorbox-cats")]')
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get('src')
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1	
    for posterCur2 in posters2:
        posterURL = posterCur2.get('href')
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1	
    for posterCur3 in posters3:
        posterURL = posterCur3.get('href')
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1		
    backgroundURL = detailsPageElements.xpath('//meta[@property="og:image"]')[0].get('content').split('?')
    metadata.art[backgroundURL[0]] = Proxy.Preview(HTTP.Request(backgroundURL[0], headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Date
    try:
        date = detailsPageElements.xpath('//meta[@property="article:published_time"]')[0].get('content').split("T")
        dateFixed = date[0].strip()
        Log('DateFixed: ' + dateFixed)
        date_object = datetime.strptime(dateFixed, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    except:
        Log("No date found")

    return metadata
