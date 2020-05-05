import PAsearchSites
import PAgenres
import PAactors
import PAUtils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    directURL = '%s%s.html' % (PAsearchSites.getSearchSearchURL(siteNum), searchTitle.lower().replace(' ', '-'))
    searchResults = [directURL]

    googleResults = PAUtils.getFromGoogleSearch(searchTitle, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.lower()
        if ('/trailers/' in sceneURL) and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        data = PAUtils.HTTPRequest(sceneURL)
        if data:
            searchResult = HTML.ElementFromString(data)

            titleNoFormatting = searchResult.xpath('//h2[@class="title"]/text()')[0]
            curID = String.Encode(sceneURL)
            releaseDate = parse(searchDate) if searchDate else ''

            score = 100 - Util.LevenshteinDistance(searchTitle, titleNoFormatting)

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [Girls Rimming]' % titleNoFormatting, score=score, lang=lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneURL = String.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    detailsPageElements = HTML.ElementFromURL(sceneURL)

    # Studio
    metadata.studio = 'Girls Rimming'

    # Title
    metadata.title = detailsPageElements.xpath('//h2[@class="title"]/text()')[0]

    # Summary
    metadata.summary = detailsPageElements.xpath('//meta[@name="description"]/@content')[0]

    #Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    actors = []

    genres = detailsPageElements.xpath('//meta[@name="keywords"]/@content')[0].split(',')
    for genreLink in genres:
        genreName = genreLink.strip()
        if ' Id ' in genreName:
            actors.append(genreName)
        else:
            movieGenres.addGenre(genreName.title())

    movieGenres.addGenre('Rim Job')

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorLink in actors:
        actorLink = actorLink.split(' Id ')
        actorName = actorLink[0].strip()
        actorPhotoURL = ''

        actorPageURL = '%s/tour/models/%s.html' % (PAsearchSites.getSearchBaseURL(siteID), actorName.lower().replace(' ', '-'))
        data = PAUtils.HTTPRequest(actorPageURL)
        if data:
            actorPage = HTML.ElementFromString(data)
            actorPhotoURL = actorPage.xpath('//div[contains(@class, "model_picture")]//img/@src0_3x')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    #Posters
    art = [
        detailsPageElements.xpath('//div[@id="fakeplayer"]//img/@src0_3x')[0]
    ]

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
