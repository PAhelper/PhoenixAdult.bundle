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
        #k = titleNoFormatting.rfind("-")
        #titleNoFormatting = titleNoFormatting[:k].strip()
        Log("Result Title: " + titleNoFormatting)
        curID = PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a[@class="track"]')[0].get('href')
        curID = curID.replace('/','_')
        Log("ID: " + curID)
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "]", score = score, lang = lang))
    return results


def update(metadata, siteID, movieGenres):
    detailsPageElements = HTML.ElementFromURL(str(metadata.id).split("|")[0].replace('_', '/'))

    metadata.studio = "Digital Playground"

    # Tagline
    try:
        #Typical tagline for Flixxx and Raw Cuts, etc.
        tagline = detailsPageElements.xpath('//a[contains(@class,"full-scene-button")]')[0].text_content().strip()
    except:
        pass

    # Summary
    try:
        #Typical summary for Flixxx and Raw Cuts, etc.
        summary = detailsPageElements.xpath('//span[text()="SYNOPSIS"]//following::span')[0].text_content().strip()
    except:
        pass

    try:
        #Series keep their summary on the Series Info page
        seriesPage = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//a[contains(text(),"info")]')[0].get("href")
        seriesPageElements = HTML.ElementFromURL(seriesPage)
        summary = seriesPageElements.xpath('//div[@class="overview"]//p')[0].text_content().strip()
        tagline = "Series: " + seriesPageElements.xpath('//h1')[0].text_content().strip()
    except:
        pass

    if tagline == "Full Movie":
        tagline = "Blockbuster"
    tagline = "DP " + tagline

    # Title
    title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    #k = title.rfind(" - ")
    #title = title[:k].strip()

    metadata.collections.clear()
    metadata.collections.add(tagline)
    metadata.tagline = tagline
    metadata.title = title
    metadata.summary = summary

    thisPage = detailsPageElements.xpath('//a[contains(text(),"trailer")]')[0].get('href')
    Log("thisPage: " + thisPage)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[@id="movie-info-format" and last()]/li/div/a')
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

    try:
        # This should work for most things
        actors = detailsPageElements.xpath('//span[@class="subtitle" and text()="STARRING"]//following::span[1]//a')
        Log("Actors by STARRING: " + str(len(actors)))
        if len(actors) == 0:
            raise
    except:
        try:
            # Series needs to define the Episode Number and pull only actors from that episode
            actors = detailsPageElements.xpath('//a[@href="'+thisPage+'" and last()]//following-sibling::div[@class="model-names-wrapper"]/span[@class="model-names"]/a')
            Log("Actors by Episode: " + str(len(actors)))
            if len(actors) == 0:
                raise

        except:
            try:
                # Fallback plan is to find the actors on the Search Page results
                searchPageElements = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteID) + urllib.quote(title))
                actors = searchPageElements.xpath('//h4[contains(text(),"'+title+'"]/following-sibling::a')
                Log("Actors by search page: " + str(len(actors)))
                if len(actors) == 0:
                    raise
            except:
                Log("Didn't find any actors in any method")

    Log("Actor count: " + str(len(actors)))

    if len(actors) > 0:
        for actorLink in actors:
            actorPageURL = actorLink.get("href")
            if "/model/" in actorPageURL: # dirty hack to filter out the extra actor I was getting that was named for some other scene; actual problem is probably just my xpath search for actors above
                role = metadata.roles.new()
                actorName = str(actorLink.text_content().strip())
                role.name = actorName
                actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
                actorPhotoURL = "https:" + actorPage.xpath('//div[@class="preview-image"]//img')[0].get("src")
                role.photo = actorPhotoURL


    # Posters
    art = detailsPageElements.xpath('//div[@class="trailer-player "]')[0].get('data-poster-image')
    Log("posters DL: " + art)
    metadata.posters[art] = Proxy.Preview(HTTP.Request(art, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
    metadata.art[art] = Proxy.Preview(HTTP.Request(art, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)

    return metadata
