import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchPageContent = HTTP.Request("https://www.pornfidelity.com") #The search page seems to redirect to PornFidelity.com if you didn't just come from there, so I open this first to trick it...
    searchPageContent = HTTP.Request(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchPageContent = str(searchPageContent).split('":"')
    searchPageResult = searchPageContent[len(searchPageContent)-1][:-2]
    searchPageResult = searchPageResult.replace('\\n',"").replace('\\',"")
    #Log(searchPageResult)
    searchResults = HTML.ElementFromString(searchPageResult)
    for searchResult in searchResults.xpath('//div[contains(@class,"d-flex")]'):
        titleNoFormatting = searchResult.xpath('.//a[@class="text-km"] | .//a[@class="text-pf"] | .//a[@class="text-tf"]')[0].text_content().strip()
        Log(titleNoFormatting)
        curID = searchResult.xpath('.//a[@class="text-km"] | .//a[@class="text-pf"] | .//a[@class="text-tf"]')[0].get('href')
        curID = curID.replace('/','_').replace('?','!')
        curID = curID[8:-19]
        Log("ID: " + curID)
        releaseDate = searchResult.xpath('.//div[contains(@class,"text-left")]')[0].text_content().strip()[10:]
        if ", 20" not in releaseDate:
            releaseDate = releaseDate + ", " + str(datetime.now().year)
        releaseDate = parse(releaseDate).strftime('%Y-%m-%d')
        Log(str(curID))

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')

    url = "https://" + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "PornFidelity"
    metadata.summary = detailsPageElements.xpath('//p[contains(@class,"card-text")]')[0].text_content().strip()
    metadata.title = detailsPageElements.xpath('//h4')[0].text_content()[36:].strip()
    if "Teenfidelity" in metadata.title:
        tagline = "TeenFidelity"
    elif "Kelly Madison" in metadata.title:
        tagline = "Kelly Madison"
    else:
        tagline = "PornFidelity"
    Log(metadata.title)
    metadataParts = detailsPageElements.xpath('//div[contains(@class,"episode-summary")]//h4')
    for metadataPart in metadataParts:
        if "Published" in metadataPart.text_content():
            releaseDate = metadataPart.text_content()[39:49]
            Log(releaseDate)
            date_object = datetime.strptime(releaseDate, '%Y-%m-%d')
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year 

    metadata.tagline = tagline
    metadata.collections.clear()
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre("Hardcore")
    movieGenres.addGenre("Heterosexual")

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class,"episode-summary")]//a[contains(@href,"/models/")]')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="img-fluid"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    valid_names = list()
    pageSource = str(HTTP.Request(url))
    posterStartPos = pageSource.index('poster: "')
    posterEndPos = pageSource.index('"',posterStartPos+10)
    background = pageSource[posterStartPos+9:posterEndPos]
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    try:
        metadata.art[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    except:
        pass
    try:
        metadata.posters[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    except:
        pass


    
    return metadata
