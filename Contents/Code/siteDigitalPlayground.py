import PAsearchSites
import PAgenres

def posterAlreadyExists(posterUrl,metadata):
    for p in metadata.posters.keys():
        Log(p.lower())
        if p.lower() == posterUrl.lower():
            Log("Found " + posterUrl + " in posters collection")
            return True

    for p in metadata.art.keys():
        if p.lower() == posterUrl.lower():
            return True
    return False

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="box-card scene"]'):
        titleNoFormatting = searchResult.xpath('.//img[@class=" lazyload"]')[0].get('alt')
        Log("Result Title: " + titleNoFormatting)
        curID = PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a[@class="track"]')[0].get('href')
        curID = curID.replace('/','_')
        Log("ID: " + curID)
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [DigitalPlayground]", score = score, lang = lang))
    return results


def update(metadata, siteID, movieGenres):
    detailsPageElements = HTML.ElementFromURL(str(metadata.id).split("|")[0].replace('_', '/'))

    metadata.studio = "Digital Playground"

    # Tagline
    try:
        tagline = detailsPageElements.xpath('//a[@class="full-scene-button "]')[0].text_content().strip()
    except:
        pass

    # Summary
    try:
        #Typical summary for Flixxx and Raw Cuts, etc.
        summary = detailsPageElements.xpath('//span[text()="SYNOPSIS"]/following::span')[0].text_content().strip()
    except:
        pass
    try:
        #Series keep their summary on the Series Info page
        seriesPage = detailsPageElements.xpath('//a[text()="info"]')[0].get("href")
        seriesPageElements = HTML.ElementFromURL(seriesPage)
        summary = seriesPageElements.xpath('//div[@class="overview"]/following::p')[0].text_content().strip()
        tagline = "Series: " + seriesPageElements.xpath('//h1')[0].text_content().strip()
    except:
        pass
    if tagline == "Full Movie":
        tagline = "Blockbuster"
    tagline = "DP " + tagline
    title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    metadata.collections.clear()
    metadata.collections.add(tagline)
    metadata.tagline = tagline
    metadata.title = title
    metadata.summary = summary

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[@id="movie-info-format"]//li//div//a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = str(genreLink.text_content().lower())
            movieGenres.addGenre(genreName)

    # Date
    date = detailsPageElements.xpath('//ul[contains(@class,"movie-details")]//span')[0].text_content() 
    if len(date) > 0:
        date_object = datetime.strptime(date, '%m-%d-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    searchPageElements = HTML.ElementFromURL("https://www.digitalplayground.com/search/videos/" + urllib.quote(title))
    actors = searchPageElements.xpath('//div[@class="title-text"][0]//a')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = str(actorLink.text_content().strip())
            role.name = actorName
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
            actorPhotoURL = "https:" + actorPage.xpath('//div[@class="preview-image"]//img')[0].get("src")
            role.photo = actorPhotoURL


    # Posters
    art = detailsPageElements.xpath('//div[@class="trailer-player "]')[0].get('data-poster-image')
    Log("posters DL: " + art)
    metadata.posters[art] = Proxy.Preview(HTTP.Request(art, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
    metadata.art[art] = Proxy.Preview(HTTP.Request(art, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)

    return metadata
