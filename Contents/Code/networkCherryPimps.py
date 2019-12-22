import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchPageNum = 1
    while searchPageNum <= 2:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + "%22" + encodedTitle + "%22" + "&page=" + str(searchPageNum))
        for searchResult in searchResults.xpath('//div[@class="video-thumb  "]'):
            titleNoFormatting = searchResult.xpath('.//p[@class="text-thumb"]/a[1]')[0].text_content().strip()
            curID = searchResult.xpath('.//p[@class="text-thumb"]/a[1]')[0].get('href').replace('/','_').replace('?','!')
            subSite = searchResult.xpath('.//p[@class="text-thumb"]//a[@class="badge"]')[0].text_content().strip()
            releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().split("|")[1].strip()).strftime('%Y-%m-%d')
            actorNames = ""
            actors = searchResult.xpath('.//span[@class="category"]//a')
            for actor in actors:
                actorName = actor.text_content()
                actorNames = actorNames + actorName + ", "
                Log("actorNames: " + actorNames)
            actorNames = actorNames[:-2]
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = actorNames + " in " + titleNoFormatting + " [CherryPimps/"+subSite+"] " + releaseDate, score = score, lang = lang))
        searchPageNum += 1

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Cherry Pimps'

    # Title
    metadata.title = detailsPageElements.xpath('//p[@class="trailer-block_title"] | //h1[@class="trailer-block_title"]')[0].text_content().strip()
    Log("Title: " + metadata.title)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="info-block"]//p[@class="text"]')[0].text_content().strip()
    Log("Summary: " + metadata.summary[:20])

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="info-block"]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="info-block_data"]//p[@class="text"]')[0].text_content().split('|')[0].replace("Added","").strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    ### Posters and artwork ###
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    # Video trailer background image
    try:
        background = detailsPageElements.xpath('//img[contains(@class,"update_thumb")]')[0].get("src")
    except:
        script_text = detailsPageElements.xpath('//div[@class="player"]//script')[0].text_content()
        alpha = script_text.find('poster="')
        omega = script_text.find('"', alpha + 8)
        backgroundURL = script_text[alpha + 8:omega]
        if 'http' in backgroundURL:
            background = backgroundURL
        else:
            background = ""
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)


    # Actors
    actors = detailsPageElements.xpath('//div[@class="info-block_data"]//a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            try:
                try:
                    actorPhotoURL = actorPage.xpath('//img[contains(@class,"model_bio_thumb")]')[0].get("src")
                except:
                    actorPhotoURL = actorPage.xpath('//img[contains(@class,"model_bio_thumb")]')[0].get("src0_1x")
                if actorPhotoURL != None:
                    if '//' == actorPhotoURL[:2]:
                        actorPhotoURL = "https:" + actorPhotoURL
                movieActors.addActor(actorName,actorPhotoURL)
                metadata.posters[actorPhotoURL] = Proxy.Preview(HTTP.Request(actorPhotoURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 2)
            except:
                actorPhotoURL = ""
                movieActors.addActor(actorName,actorPhotoURL)                

    return metadata
