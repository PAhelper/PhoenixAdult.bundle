import PAsearchSites
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchString = searchTitle.replace(" ","-").replace(",","").replace("'","").replace("?","").lower().strip()

    modelsPageSortByLetter = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle[:1] #here we get first letter of searchTitle
    actorResults = HTML.ElementFromURL(modelsPageSortByLetter)
    actorPage = actorResults.xpath('//a[contains(@href, "%s")]/@href' % searchString)[0] # looking for our model
    searchResults = HTML.ElementFromURL(actorPage) # scene search is carried out through the model page

    for searchResult in searchResults.xpath('//div[@class="content-box"]'):
        titleNoFormatting = searchResult.xpath('.//h2//span')[0].text_content().strip()
        sceneUrl = searchResult.xpath('.//a/@href')[0]
        curID = sceneUrl.replace('/', '_').replace('?', '!')

        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split("|")
    pageURL = metadata_id[0].replace('_', '/').replace('!', '?')
    sceneDate = metadata_id[2]

    detailsPageElements = HTML.ElementFromURL(pageURL)

    # Summary
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.studio = siteName
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="description"]//p')[0].text_content().strip()
        metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    except:
        pass

    # Director
    metadata.directors.clear()
    director = metadata.directors.new()
    director.name = 'Charles Dera'

    # Collections / Tagline
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Genres
    try:
        genres = detailsPageElements.xpath('//dd[2]')
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre('All Sex')
    except:
        pass

    # Release Date
    date_object = parse(sceneDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()

    actors = detailsPageElements.xpath('//dd[1]')
    for actorLink in actors:
        actorName = actorLink.xpath('.//a[1]')[0].text_content().strip()
        actorPhotoURL = actorLink.xpath('.//a[2]//img')[0].get('src')
        movieActors.addActor(actorName,actorPhotoURL)
        try:
            actorName = actorLink.xpath('.//a[3]')[0].text_content().strip()
            actorPhotoURL = actorLink.xpath('.//a[4]//img')[0].get('src')
            movieActors.addActor(actorName, actorPhotoURL)
        except:
            pass

    # Posters/Background
    art = []
    posters = HTML.ElementFromURL(detailsPageElements.xpath('//dd[1]//a/@href')[0])

    for poster in posters.xpath('//a[contains(@href,"' + pageURL + '")]//img/@src'):
        art.append(poster)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
