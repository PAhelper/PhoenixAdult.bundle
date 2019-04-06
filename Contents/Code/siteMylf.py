import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchString = searchTitle
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)

    titleNoFormatting = searchResults.xpath('//div[@class="col-12 col-md-7"]//span[contains(@class,"text-lightgray")]')[0].text_content().strip()
    Log("titleNoFormatting: " + titleNoFormatting)
    curID = searchResults.xpath('//link[@rel="canonical"]')[0].get('href').replace('/','_').replace('?','!')
    Log("curID: " + curID)
    actors = searchResults.xpath('//div[@class="col-12 col-md-8"]//a//span')
    Log("# actors: " + str(len(actors)))
    firstActor = actors[0].text_content()
    Log("firstActor: " + firstActor)
    subSite = searchResults.xpath('//img[@class="lazy img-fluid"]')[0].get("data-original").split('/')[-1].replace('_logo.png','').title()
    Log("subSite: " + subSite)

    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Mylf/"+subSite+"] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    # art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Mylf'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="col-12 col-md-7"]//span[contains(@class,"text-lightgray")]')[0].text_content().strip()
    Log("title: " + metadata.title)

    #Tagline and Collection(s)
    subSite = detailsPageElements.xpath('//img[@class="lazy img-fluid"]')[0].get("data-original").split('/')[-1].replace('_logo.png','').strip().title()
    metadata.tagline = subSite
    metadata.collections.add(subSite)
    Log("subSite: " + subSite)

    # Genres
    # genres = detailsPageElements.xpath('//span[@class="update_tags"]/a')
    # if len(genres) > 0:
    #     for genreLink in genres:
    #         genreName = genreLink.text_content().strip().lower()
    #         movieGenres.addGenre(genreName)

    # Release Date
    # date = detailsPageElements.xpath('//div[@class="cell update_date"]')[0].text_content().strip()
    # if len(date) > 0:
    #     date_object = parse(date)
    #     metadata.originally_available_at = date_object
    #     metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="col-12 col-md-8"]//a')
    if len(actors) > 0:
        for actor in actors:
            actorName = actor.xpath('./span').text_content().strip()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPage.xpath('//img[contains(@class,"girlthumb")]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)
            Log('actor: ' + actorName + ", " + actorPhotoURL)



    ### Posters and artwork ###
    posterNum = 1
    posters = detailsPageElements.xpath('//div[contains(@class,"trailer-small-images")]//a')
    for poster in posters:
        posterLink = poster.get("href")
        if posterLink != "/join":
            posterURL = poster.xpath('.//img')[0].get('data-original')
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            Log('posterURL: ' + posterURL)

    # Video trailer background image
    preview = detailsPageElements.xpath('//video[@id="my-video"]')[0].get('poster')
    metadata.art[preview] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
    Log('previewIMG: ' + preview)



    return metadata
