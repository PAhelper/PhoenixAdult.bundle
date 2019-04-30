import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    Log("Results: " + str(len(searchResults.xpath('//div[contains(@class,"card card-simple")]'))))
    for searchResult in searchResults.xpath('//div[contains(@class,"card card-simple")]'):
        titleNoFormatting = searchResult.xpath('.//h5//a')[0].text_content().strip()
        Log("title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','+').replace('?','!')
        Log("curID: " + curID)
        actors = searchResult.xpath('.//a[contains(@href,"/models/")]')
        Log("# actors: " + str(len(actors)))
        firstActor = actors[0].text_content().strip()
        Log("firstActor: " + firstActor)
        releaseDate = parse(searchResult.xpath('.//span[@class="ml-auto"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log("date: " + releaseDate)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [StepSecrets] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    urlBase = PAsearchSites.getSearchBaseURL(siteID)
    url = urlBase + str(metadata.id).split("|")[0].replace('+','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Joymii'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="color-title"]')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = "Step Secrets"
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = ["European","Taboo","Glamcore"]
    for genre in genres:
        movieGenres.addGenre(genre)

    metadata.summary = detailsPageElements.xpath('//div[@class="descripton"]//p')[0].text_content().strip()

    # Release Date
    date = detailsPageElements.xpath('//div[@class="text-muted small"]')[0].text_content().strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//p[@class="mb-2"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPageURL = urlBase + actorLink.get("href")
            try:
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//img[contains(@class,"mw-100")]')[0].get("src")
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###
    background = detailsPageElements.xpath('//video[@id="videoPlayer"]')[0].get("poster")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Possible extra posters
    posterNum = 2
    posters = detailsPageElements.xpath('//div[contains(@class,"carousel")]//img')
    Log("num posters: " + str(len(posters)))
    try:
        for poster in posters:
            posterURL = poster.get("src")
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            posterNum += 1
    except:
        pass

    return metadata
