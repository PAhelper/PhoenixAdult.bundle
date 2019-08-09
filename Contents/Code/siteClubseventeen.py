import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.replace('%20','_'))
    for searchResult in searchResults.xpath('//div[@class="col-xs-6 mt-10"] | //div[@class="col-xs-6 col-md-4 mt-10"]'):
        titleNoFormatting = searchResult.xpath('.//h3[@class="video-description"]/span[@class="featuring"]')[0].text_content().strip()
        curID = "https:+_++_+www.clubseventeen.com+_+" + searchResult.xpath('.//h3[@class="video-description"]/a')[0].get('href').replace('/','+_+').replace('?','!')
        Log("curID: " + curID)
        releaseDate = parse(searchResult.xpath('.//h3[@class="video-description"]')[0].text_content().strip().splitlines()[0]).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = releaseDate + " " + titleNoFormatting + " [clubseventeen] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('+_+','/').replace('!','?')
    Log("url: "+url)
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Clubseventeen'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="top"]/h3/span')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="bottom"]/p[@class="mt-0 hidden-lg"]')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="top"]/div[@class="item-tag mt-5"]/a/span')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)
    movieGenres.addGenre("Genre")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="top"]/p[@class="mt-10 letter-space-1"]')[0].text_content().split("|")[0].strip().split(' ')[2]
    Log("Date: "+ date)
    if len(date) > 0:
        date_object = datetime.strptime(date, '%d-%m-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="middle"]/p[@class="mt-10"]/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = 'https://www.clubseventeen.com/' + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="profile-image-container"]/a/img')[0].get("src")
            if 'http' not in actorPhotoURL:
            	actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    #twitterBG = detailsPageElements.xpath('//div[@class="ratio-16-9 video-item static-item progressive-load loaded"]')[0].get('data-image')
    #Log('twitterBG: ' + str(twitterBG))
    try:
        twitterBG = detailsPageElements.xpath('//div[@class="video-wrapper static-video-wrapper"]/div[@class="ratio-16-9 video-item static-item progressive-load loaded"]')[0].get_attribute('data-image')
        Log('twitterBG: ' + twitterBG)
        art.append(twitterBG)
    except:
        pass

    # Photos
    photos = detailsPageElements.xpath('//img[contains(@class, "update_thumbs")]')
    if len(photos) > 0:
        for photoLink in photos:
            photo = PAsearchSites.getSearchBaseURL(siteID) + photoLink.get('poster')
            art.append(photo)

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