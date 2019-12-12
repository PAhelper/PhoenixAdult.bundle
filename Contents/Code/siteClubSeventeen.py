import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchString = encodedTitle.replace('%20',"_")
    Log("searchString: " + searchString)
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchString
    searchResult = HTML.ElementFromURL(url)

    titleNoFormatting = searchResult.xpath('//h3[@class="dvd-title mb-0 mt-0"]/span')[0].text_content().strip()
    curID = url.replace('/','+').replace('?','!')
    releaseDate = searchResult.xpath('//p[@class="mt-10 letter-space-1"]')[0].text_content().split("DATE ADDED:")[1].split("|", 1)[0].strip()
    releaseDate = parse(releaseDate).strftime('%Y-%m-%d')
    if searchDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 90
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [ClubSeventeen] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('+','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'ClubSeventeen'

    # Title
    metadata.title = detailsPageElements.xpath('//h3[@class="dvd-title mb-0 mt-0"]/span')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="mt-0 hidden-lg"]')[0].text_content().strip()

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    # Series
    try:
        series = detailsPageElements.xpath('//p[@class="mt-10 letter-space-1"]/a')[0].text_content().strip()
        metadata.collections.add(series)
    except:
        pass

    # Genres
    genres = detailsPageElements.xpath('//div[@class="item-tag mt-5"]/a/span')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//p[@class="mt-10 letter-space-1"]')[0].text_content().split("DATE ADDED:")[1].split("|", 1)[0].strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%d-%m-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="middle"]/p/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + "/" + actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//img[@class="model-profile-image"]')[0].get("src")
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//div[@class="ratio-16-9 video-item static-item progressive-load"]')[0].get('data-image')
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