import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    title = searchTitle.lower().replace(' ','-')
    url = PAsearchSites.getSearchSearchURL(siteNum) + title + '.html'
    Log("URL: " + url)
    searchResult = HTML.ElementFromURL(url)
    titleNoFormatting = searchResult.xpath('//meta[@name="twitter:title"]')[0].get('content').strip()
    curID = url.replace('/','_').replace('?','!')
    releaseDate = parse(searchResult.xpath('//div[@class="trailer topSpace"]/div[2]/p')[0].text_content().split('\\')[1].strip()).strftime('%Y-%m-%d')
    if searchDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 90
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [GirlsOutWest] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'GirlsOutWest'

    # Title
    metadata.title = detailsPageElements.xpath('//meta[@name="twitter:title"]')[0].get('content').strip()

    # Summary

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.addGenre("Amateur")
    movieGenres.addGenre("Australian")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="trailer topSpace"]/div[2]/p')[0].text_content().split('\\')[1].strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%m/%d/%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="trailer topSpace"]/div[2]/p/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPage.xpath('//div[@class="profilePic"]/img')[0].get("src0_3x")
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//div[@class="videoplayer"]/img')[0].get('src0_3x')
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