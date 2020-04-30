import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    encodedTitle = encodedTitle.replace('%20a%20','%20')

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//a[@class="thumbnail clearfix"]'):
        titleNoFormatting = searchResult.xpath('.//div/h3[@class="scene-title"]')[0].text_content()
        curID = searchResult.get('href').replace("_","$").replace("/","_").split("?")[0]
        if searchDate:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d')
        else:
            releaseDate = ''
        fullSubSite = searchResult.xpath('.//div/p[@class="help-block"]')[0].text_content()
        Log("Full subSite: "+ fullSubSite)
        if 'BehindTheScenes' in fullSubSite and 'BTS' not in titleNoFormatting:
            titleNoFormatting = titleNoFormatting + ' BTS'
        subSite = fullSubSite.split('.com')[0]
        Log("Subsite: " + subSite)
        if subSite == PAsearchSites.getSearchSiteName(siteNum):
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        else:
            score = 60 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " [Dogfart/" + subSite + "] ", score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('_','/').replace("$","_")
    Log(temp)
    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    Log(url)
    detailsPageElements = HTML.ElementFromURL(url)

    # Studio
    metadata.studio = "Dogfart Network"

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="icon-container"]/a')[0].get("title")

    # Summary
    summary = detailsPageElements.xpath('//div[@class="description shorten"]')[0].text_content().strip().replace('...read more','').replace('\n', ' ')
    metadata.summary = summary

    # Collections / Tagline
    tagline = detailsPageElements.xpath('//h3 [@class="site-name"]')[0].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.clear()
    collection = str(PAsearchSites.getSearchSiteName(siteID))
    metadata.collections.add(collection)

    # Release Date
    try:
        date = str(metadata.id).split("|")[2]
        if len(date) > 0:
            date_object = parse(date)
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
            Log("Date from file")
    except:
        pass

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="categories"]/p/a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    metadata.roles.clear()
    actors = detailsPageElements.xpath('//h4[@class="more-scenes"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    #Posters
    try:
        background = "https:" + detailsPageElements.xpath('//div[@class="icon-container"]//img')[0].get('src')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass
    i=0
    for posterUrls in detailsPageElements.xpath('//div[@class="preview-image-container col-xs-6 col-md-2 clearfix"]//a'):
        page = PAsearchSites.getSearchBaseURL(siteID) + posterUrls.get("href")
        posterpage = HTML.ElementFromURL(page)
        posterUrl = posterpage.xpath('//div[@class="col-xs-12 remove-bs-padding"]/img')[0].get('src')
            #Download image file for analysis
        try:
            if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size

                metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i)
                if width > height and i > 1:
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i )
                i = i + 1
                if i>15:
                    break


        except:
            pass

    return metadata
