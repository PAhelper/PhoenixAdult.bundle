import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="list-page-grid-container"]//div[@class="grid-item"]'):
        titleNoFormatting = searchResult.xpath('.//span[@class="overlay-inner"]')[0].text_content().strip()
        curID = searchResult.xpath('.//a[@class="boxcover"]')[0].get('href').replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Elegant Angel] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Elegant Angel'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="description"]')[0].text_content().strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="synopsis"]/p')[0].text_content().strip()
    except:
        pass

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="categories"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="release-date"]')[0].text_content().replace('Released:','').strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="scene-cast-list"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//div[@class="container-fluid px-0"]//img')[0].get("src")
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    # Director
    director = metadata.directors.new()
    try:
        directors = detailsPageElements.xpath('//div[@class="director"]/a')
        for dirname in directors:
            director.name = dirname.text_content().strip()
    except:
        pass

    ### Posters and artwork ###

    # DVD Cover
    try:
        twitterBG = detailsPageElements.xpath('//div[@class="carousel-item active"]/img')[0].get('data-src')
        art.append(twitterBG)
    except:
        pass

    # Scene photos page
    try:
        photoPageUrl = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//div[@class="user-actions"]/a[2]')[0].get('href')
        photoPage = HTML.ElementFromURL(photoPageUrl)
        unlockedPhotos = photoPage.xpath('//div[@class="item-grid item-grid-gallery"]//img')
        for unlockedPhoto in unlockedPhotos:
            if 'http' not in unlockedPhoto.get('data-src'):
                art.append(PAsearchSites.getSearchBaseURL(siteID) + unlockedPhoto.get('data-src'))
            else:
                art.append(unlockedPhoto.get('data-src'))
    except:
        photos = detailsPageElements.xpath('//div[@class="item-grid item-grid-scene"]//img[@class="img-full-fluid"]')
        if len(photos) > 0:
            for photoLink in photos:
                photo = photoLink.get('data-src')
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