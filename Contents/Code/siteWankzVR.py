import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    searchString = searchTitle.replace(" ","+")
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(searchSiteID) + searchString)
    for searchResult in searchResults.xpath('//section[@class="compact wrap"]//article'):
        titleNoFormatting = searchResult.xpath('.//a//h3')[0].get("title")
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href')
        curID = curID.replace('/preview','').replace('/','_').replace('?','!')
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//div[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate.strip())

        searchString = searchString.replace("+"," ")
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))

    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Studio/Tagline/Collection
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="description"]')[0].text_content().strip()

    # Date
    date = detailsPageElements.xpath('//div[@class="date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors / possible posters
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//header//h4//a')
    if len(actors) > 0:
        posterNum = 2
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
            Log(actorName + ": " + actorPageURL)
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="profile"]//img')[0].get("src")
            Log('actorPhotoURL: ' + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)
            # Actor profile pic as possible poster
            metadata.posters[actorPhotoURL] = Proxy.Preview(HTTP.Request(actorPhotoURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            posterNum += 1

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('.//div[@class="tags"]//a')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())

    # Posters and artwork
    art = []

    # Background
    try:
        art.append(detailsPageElements.xpath('//meta[@property="og:image"]')[0].get('content').replace('medium.jpg','large.jpg'))
    except:
        pass

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                j = j + 1
            except:
                pass

    return metadata
