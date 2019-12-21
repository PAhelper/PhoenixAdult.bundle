import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="col col-33 t-col-50 m-col-100"]'):
        titleNoFormatting = searchResult.xpath('.//div[@data-item="c-11 r-11 / bottom"]/a')[0].get('title')
        subSite = searchResult.xpath('.//div[@data-item="c-21 r-11 / bottom right"]/a')[0].get('title')
        curID = searchResult.xpath('.//div[@data-item="c-11 r-11 / bottom"]/a')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//div[@data-item="c-21 r-21 / middle right"]/p')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [LetsDoeIt/" + subSite + "] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = "Porndoe Premium"

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="no-space transform-none"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//meta[@name="description"]')[0].get('content')

    # Tagline and Collection(s)
    tagline = detailsPageElements.xpath('//div[@class="actors"]/h4/a')[0].text_content()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//a[@class="inline-links"]')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="h5 h5-published nowrap color-rgba255-06"]')[0].text_content().strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%d %B %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//span[@class="group inline"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorName = actorPage.xpath('//div[@data-item="c-13 r-11 m-c-15 / middle"]/h1')[0].text_content().strip()
            try:
                actorPhotoURL = actorPage.xpath('//div[@class="avatar"]/picture[2]/img')[0].get("data-src")
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName, actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//picture[@class="poster"]//img')[0].get('src')
        art.append(twitterBG)
    except:
        pass

    # Photos
    photos = detailsPageElements.xpath('//div[@id="gallery-thumbs"]//img')
    if len(photos) > 0:
        for photoLink in photos:
            photo = photoLink.get('src')
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
