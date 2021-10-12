import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    directURL = '%s%s.html' % (PAsearchSites.getSearchSearchURL(siteNum), searchData.title.lower().replace(' ', '-'))
    searchResults = [directURL]

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.lower()
        if ('/trailers/' in sceneURL) and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if req and req.text != 'Page not found':
            searchResult = HTML.ElementFromString(req.text)

            titleNoFormatting = searchResult.xpath('//h2[@class="title"]/text()')[0]
            curID = PAutils.Encode(sceneURL)
            releaseDate = parse(searchData.date) if searchData.date else ''

            score = 100 - Util.LevenshteinDistance(searchData.title, titleNoFormatting)

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [Girls Rimming]' % titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h2[@class="title"]/text()')[0]

    # Summary
    metadata.summary = detailsPageElements.xpath('//meta[@name="description"]/@content')[0]

    # Studio
    metadata.studio = 'Girls Rimming'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

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

    # Actors
    movieActors.clearActors()
    for actorLink in actors:
        actorLink = actorLink.split(' Id ')
        actorName = actorLink[0].strip()
        actorPhotoURL = ''

        actorPageURL = '%s/tour/models/%s.html' % (PAsearchSites.getSearchBaseURL(siteNum), actorName.lower().replace(' ', '-'))
        data = PAutils.HTTPRequest(actorPageURL)
        if not data or data == 'Page not found':
            googleResults = PAutils.getFromGoogleSearch(actorName, siteNum)
            for actorURL in googleResults:
                actorURL = actorURL.lower()
                if ('/models/' in actorURL):
                    data = PAutils.HTTPRequest(actorURL)
                    break

        actorPage = HTML.ElementFromString(data.text)
        actorPhotoURL = actorPage.xpath('//div[contains(@class, "model_picture")]//img/@src0_3x')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [
        detailsPageElements.xpath('//div[@id="fakeplayer"]//img/@src0_3x')[0]
    ]

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
