import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="item-info clear"]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].text_content().strip()
        scenePage = searchResult.xpath('.//a')[0].get('href')
        curID = scenePage.replace('/', '_').replace('?', '!')
        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Femdom Empire] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    url = str(metadata.id).split("|")[0].replace('_','/')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    #Studio
    metadata.studio = "Femdom Empire"

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="videoDetails clear"]//h3')[0].text_content().strip()
    Log("Scene Title: " + metadata.title)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="videoDetails clear"]//p')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="featuring clear"][2]//ul//li')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower().replace('categories:', '').replace('tags:', '')
            movieGenres.addGenre(genreName)
    movieGenres.addGenre("Femdom")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="videoInfo clear"]//p')[0].text_content().replace('Date Added:', '').strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="featuring clear"][1]//ul//li')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip().replace('Featuring:', '')
            actorPhotoURL = ''
            movieActors.addActor(actorName, actorPhotoURL)

    ### Posters and artwork ###
    # Video trailer background image

    return metadata