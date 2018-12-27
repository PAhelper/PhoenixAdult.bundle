import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//article[@class="card card--release"]'):
        titleNoFormatting = searchResult.xpath('.//p[@class="card-info__title"]//a[1]')[0].get('title')
        curID = searchResult.xpath('.//p[@class="card-info__title"]//a[1]')[0].get('href').replace('/','_')
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        subSite = searchResult.xpath('.//div[@class="card-info__meta"]//a[1]')[0].text_content.strip().replace(' ','')
        releaseDate = parse(searchResult.xpath('.//span[@class="card-info__meta-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [RealityKings/"+subSite+"] "+releaseDate, score = score, lang = lang))    

    return results



def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('_','/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "Reality Kings"
    paragraph = detailsPageElements.xpath('//div[@id="trailer-desc-txt"]//p')[0].text_content()
    paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = paragraph.strip()
    metadata.title = detailsPageElements.xpath('//h1[@class="section_title"]')[0].text_content()
    metadata.tagline = detailsPageElements.xpath('//div[@id="trailer-desc-txt"]//div[@class="category"]//a')[0].text_content()
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)
    dateElements = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteID) + urllib.quote(metadata.title))
    date = dateElements.xpath('//span[@class="card-info__meta-date"]')[0].text_content()
    Log("Date:" + date)
    date_object = datetime.strptime(date, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year    
        
    
    # Genres
    movieGenres.clearGenres()
    # No Source for Genres, add manual
    t = metadata.tagline
    if t == "40 Inch Plus" or t == "Extreme Asses" or t == "Round and Brown":
        movieGenres.addGenre("Big Butt")
    if t == "First Time Auditions":
        movieGenres.addGenre("Audition")
    if t == "Dangerous Dongs" or t == "Teens Love Huge Cocks":
        movieGenres.addGenre("Big Dick")
    if t == "Big Naturals" or t == "Big Tits Boss":
        movieGenres.addGenre("Big Tits")
    if t == "Bikini Crashers":
        movieGenres.addGenre("Bikini")
    if t == "Street Blowjobs":
        movieGenres.addGenre("Blowjob")
    if t == "Captain Stabbin":
        movieGenres.addGenre("Boat")
    if t == "In The VIP":
        movieGenres.addGenre("Club")
    if t == "Round and Brown":
        movieGenres.addGenre("Ebony")
    if t == "Euro Sex Parties" or t == "Mikes Apartment":
        movieGenres.addGenre("Euro")
    if t == "Euro Sex Parties":
        movieGenres.addGenre("Group")
    if t == "Hot Bush":
        movieGenres.addGenre("Hairy Pussy")
    if t == "We Live Together" or t == "Moms Lick Teens":
        movieGenres.addGenre("Lesbian")
    if t == "8th Street Latinas" or t == "Saturday Night Latinas":
        movieGenres.addGenre("Latina")
    if t == "Happy Tugs":
        movieGenres.addGenre("Massage")
        movieGenres.addGenre("Handjob")
    if t == "Milf Hunter" or t == "Milf Next Door" or t == "Moms Lick Teens" or t == "Moms Bang Teens":
        movieGenres.addGenre("MILF")
    if t == "Real Orgasms":
        movieGenres.addGenre("Masturbation")
        movieGenres.addGenre("Solo")
    if t == "Wives in Pantyhouse":
        movieGenres.addGenre("Pantyhouse")
    if t == "Team Squirt":
        movieGenres.addGenre("Squirt")
    if t == "Pure 18" or t == "Teens Love Huge Cocks" or t == "Moms Bang Teens":
        movieGenres.addGenre("Teen")
    if t == "Tranny Surprise":
        movieGenres.addGenre("Tranny")
        movieGenres.addGenre("Shemale")
    movieGenres.addGenre("Hardcore")
    movieGenres.addGenre("Heterosexual")


    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@id="trailer-desc-txt"]//div[contains(@class,"models-name")]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.xpath('.//a')[0].text_content()
            actorPageURL = actorLink.xpath('.//a')[0].get("href")
            actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID)+actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[contains(@class,"model-picture__thumb js-model-picture__thumb")]')[0]
            actorPhotoURL = actorPhotoURL.xpath('.//img')[0].get("data-bind").split("'")[1]
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    posters = detailsPageElements.xpath('//a[@class="card-thumb__img"]')
    background = detailsPageElements.xpath('//video')[0].get("poster")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    posterNum = 1
    for posterCur in posters:
        posterURL = posterCur.get("href")
        try:
            metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        except:
            pass
        posterNum = posterNum + 1    
    


    
    return metadata
