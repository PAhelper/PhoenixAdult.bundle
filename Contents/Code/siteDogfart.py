import PAsearchSites
import PAgenres
def tagAleadyExists(tag,metadata):
    for t in metadata.genres:
        if t.lower() == tag.lower():
            return True
    return False

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

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchsiteID):
    encodedTitle = encodedTitle.replace('%20a%20','%20')
    i=0
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    Log("resultat" + str(searchResults) )
    for searchResult in searchResults.xpath('//a[@class="thumbnail clearfix"]'):
        Log(str(searchResult.get('href')))
        titleNoFormatting = searchResult.xpath('//div/h3[@class="scene-title"]')[i].text_content()
        Log(titleNoFormatting)
        curID = searchResult.get('href').replace("/"," ")
        Log(curID)
        lowerResultTitle = str(titleNoFormatting).lower()
        subSite = searchResult.xpath('//div/p[@class="help-block"]')[i].text_content()
        Log("subsite: "+ subSite)
        
        site = " [Dogfart"
        if len(subSite) > 0 and subSite != "Dogfart":
            site = site + "/" + subSite
        site = site + "] "
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(329), name = titleNoFormatting + " [Dogfart]" , score = score, lang = lang))
        i = i + 1
    return results

def update(metadata,siteID,movieGenres):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Dogfart'
    temp = str(metadata.id).split("|")[0].replace('_','/')
    Log(temp)
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    Log(url)
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//div[@class="description shorten"]').text_content().strip()
    #paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = paragraph.strip()
    tagline = detailsPageElements.xpath('//h3[@class="site-name"]').text_content()
    metadata.collections.clear()
    tagline = tagline.strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//div[@class="description-title"]').text_content()
    metadata.studio = detailsPageElements.xpath('//h3[@class="site-name"]').text_content()

    # Genres
    movieGenres.clearGenres()
    genres = "cumshot"

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)


    # Release Date
    date = " "
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    actors = detailsPageElements.xpath('//div[@class="details-container clearfix"]:div:h1')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()
            actorName = str(actorLink.text_content().strip())
            actorName = actorName.replace("\xc2\xa0", " ")
            role.name = actorName
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
            actorPhotoURL = "http:" + actorPage.xpath('//img[@class="profile-picture"]')[0].get("src")
            role.photo = actorPhotoURL

    #Posters
    try:
        background = "https" + sdetailsPageElements.xpath('//div[@data-poster]').get('data-poster')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    return metadata
