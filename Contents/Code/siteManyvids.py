import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    sceneID = encodedTitle.split('%20', 1)[0]
    Log("SceneID: " + sceneID)
    try:
        sceneTitle = encodedTitle.split('%20', 1)[1].replace('%20', ' ')
    except:
        sceneTitle = ''
    Log("Scene Title: " + sceneTitle)
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + sceneID)
    for searchResult in searchResults.xpath('//div[@class="video-details"]'):
        titleNoFormatting = searchResult.xpath('//h2[@class="h2 m-0"]')[0].text_content()
        curID = searchTitle.lower().replace(" ","-").replace("'","-")
        subSite = searchResult.xpath('//a[@class="username "]')[0].text_content().strip()
        if sceneTitle:
            score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
        else:
            score = 90
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [ManyVids/" + subSite + "] ", score = score, lang = lang))
    return results



def update(metadata,siteID,movieGenres,movieActors):
    detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + '/video/' + str(metadata.id).split("|")[0])
    art = []

    # Title
    metadata.title = detailsPageElements.xpath('//h2[@class="h2 m-0"]')[0].text_content().strip()

    # Studio
    metadata.studio = "ManyVids"

    # Summary
    try:
        paragraphs = detailsPageElements.xpath('//div[@class="desc-text"]')
        pNum = 0
        summary = ""
        for paragraph in paragraphs:
            if pNum >= 0 and pNum < (len(paragraphs)):
                summary = summary + '\n\n' + paragraph.text_content()
            pNum += 1
    except:
        pass
    if summary == '':
        try:
            summary = detailsPageElements.xpath('//div[@class="desc-text"]')[0].text_content().strip()
        except:
            pass
    metadata.summary = summary.strip()

    # Collections / Tagline
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//a[contains(@class,"username ")]')[0].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Date

    # Actors
    movieActors.clearActors()
    actorName = detailsPageElements.xpath('//a[contains(@class,"username ")]')[0].text_content()
    try:
        actorPhotoURL = detailsPageElements.xpath('//div[@class="pr-2"]/a/img')[0].get('src')
    except:
        actorPhotoURL = ''
    movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="tags"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//div[@id="rmpPlayer"]')[0].get('data-video-screenshot').strip()
        Log("Background:" + twitterBG)
        art.append(twitterBG)
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