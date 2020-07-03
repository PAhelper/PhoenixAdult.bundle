import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchString = searchTitle.replace(" ","-").replace(",","").replace("'","").replace("?","")
    Log("searchString: " + searchString)
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchString
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    titleNoFormatting = searchResults.xpath('//h3[@class="release-title"]//span')[0].text_content().strip()
    Log("titleNoFormatting: " + titleNoFormatting)
    curID = url.replace('/','+').replace('?','!')
    Log("curID: " + curID)
    
    script_text = searchResults.xpath('//script[@type="application/ld+json"][1]')[0].text_content()
    alpha = script_text.find('datePublished')
    omega = script_text.find('"',alpha+16)
    script_date = script_text[alpha+16:omega]
    releaseDate = parse(script_date).strftime('%Y-%m-%d')
    Log("releaseDate:" + releaseDate)
    
    if searchDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 95

    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) , name = titleNoFormatting + " [VRP Films] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('+','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()
    urlBase = PAsearchSites.getSearchBaseURL(siteID)

    # Title
    metadata.title = detailsPageElements.xpath('//h3[@class="release-title"]//span')[0].text_content().strip()
    Log("title: " + metadata.title)

    #Tagline and Collection(s)
    siteName = "VRP Films"
    metadata.studio = siteName
    metadata.tagline = siteName
    metadata.collections.add(siteName)
    Log("siteName: " + siteName)

    # Summary
    paragraph = detailsPageElements.xpath('//meta[@property="og:description"]')[0].get('content')
    metadata.summary = paragraph
    
    # Release Date
    script_text = detailsPageElements.xpath('//script[@type="application/ld+json"][1]')[0].text_content()
    alpha = script_text.find('datePublished')
    omega = script_text.find('"',alpha+16)
    date = script_text[alpha+16:omega]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Video trailer background image
    previewBG = detailsPageElements.xpath('//div[@class="hero-img"]')[0].get("style").replace("background-image: url(","").replace(")","")
    # previewBG = "https:" + previewBG
    metadata.art[previewBG] = Proxy.Preview(HTTP.Request(previewBG, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    Log('previewBG: ' + previewBG)

    # Posters
    posterNum = 1
    posters = detailsPageElements.xpath('//a[@class="vrp-lightbox"]')
    for poster in posters:
        posterURL = poster.get("href")
        posterURL = posterURL
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum += 1
        Log('posterURL: ' + posterURL)

    # Actors
    actors = detailsPageElements.xpath('//div[@class="detail"][2]//p')[0].text_content().strip()
    actorName = actors[10:].strip()
    actorPhotoURL = ""
    movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="movies-description"]//div[3]//p[1]')
    for genre in genres:
        genreName = genre.text_content().strip()
        movieGenres.addGenre(genreName)

    return metadata
