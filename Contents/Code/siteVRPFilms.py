import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchString = encodedTitle.replace(" ","+")
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchString)
    Log("Results found: " + str(len(searchResults.xpath('//h3[contains(@data-mh,"movie-column-title")]'))))
    i = 0
    for searchResult in searchResults.xpath('//h3[contains(@data-mh,"movie-column-title")]'):
        titleNoFormatting = searchResult.xpath('//h3[contains(@data-mh,"movie-column-title")]')[i].text_content().title().strip()
        Log ("Title: " +titleNoFormatting)
        curID = PAutils.Encode(searchResult.xpath('//div[contains(@class,"overlay")]/a')[i].get('href'))
        Log("curID: " +curID)
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        Log("Score: " + str(score))
        releaseDate=""
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
    title = detailsPageElements.xpath('//h3[contains(@class,"release-title")]/span')[0].text_content().strip()
    metadata.title = title
    Log('Title: ' +  metadata.title)

    # Summary
    summary = detailsPageElements.xpath('//div[contains(@class,"movie-content")]/p')
    summary2 = ""
    for summaryCur in summary:
		summary2 = summary2 + summaryCur.text_content().strip() + "\n"
    metadata.summary = summary2
    Log('summary: ' +  metadata.summary)
	
    # Release Date
    script_text = detailsPageElements.xpath('//script[@type="application/ld+json"][1]')[0].text_content()
    alpha = script_text.find('datePublished')
    omega = script_text.find('"',alpha+16)
    date = script_text[alpha+16:omega]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
		
    # Rating
    rating = detailsPageElements.xpath('//div[contains(@class,"gdrts-rating-text")]/strong')[0].text_content().strip()
    metadata.rating = ((float(rating))*2)
    Log('rating: ' +  rating + '*2')

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//div[contains(@class,"movies-gallery")]/div/div/a')
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get('href')
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum = posterNum + 1			
    backgroundURL = detailsPageElements.xpath('//meta[@property="og:image"]')[0].get('content').split('?')
    metadata.art[backgroundURL[0]] = Proxy.Preview(HTTP.Request(backgroundURL[0], headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Actors
    actors = detailsPageElements.xpath('//div[@class="detail"][2]//p')[0].text_content().strip()
    actorName = actors[10:].strip()
    actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + "/pornstar/" + actorName.replace(" ","-")
    actorPage = HTML.ElementFromURL(actorPageURL)
    actorPhotoURL = actorPage.xpath('//section[contains(@id,"pornstar-profile")]/div/div/div/img/@src')
    movieActors.addActor(actorName,actorPhotoURL[0])

    # Genres
    genres = detailsPageElements.xpath('//div[@class="movies-description"]//div[3]//p[1]')[0].text_content().strip().split(":")[1].split(",")
    for genre in genres:
        genreName = genre
        movieGenres.addGenre(genreName)

    return metadata
