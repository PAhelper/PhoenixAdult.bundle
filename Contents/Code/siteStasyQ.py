import PAsearchSites
import PAutils

cookies = {
    'lang': 'en',
}


def search(results, lang, siteNum, searchData):
    shootID = None
    for parts in searchData.title.split():
        if unicode(parts, 'UTF-8').isdigit():
            shootID = parts
            break

    if shootID:
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/r/Q/' + shootID
        req = PAutils.HTTPRequest(sceneURL, cookies=cookies)
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)

            titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()
            curID = PAutils.Encode(sceneURL)

            releaseDate = searchData.dateFormat() if searchData.date else ''

            score = 100

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    releaseDate = metadata_id[2]

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL

    req = PAutils.HTTPRequest(sceneURL, cookies=cookies)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "about-section__text")]/p')[0].text_content().strip()

    # Studio
    metadata.studio = 'StasyQ'

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.collections.add('StasyQ')

    # Release Date
    if releaseDate:
        date_object = parse(releaseDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//section[contains(@class, "about-section")]//div[contains(@class, "tags")]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//section[contains(@class, "content-section")]//div[contains(@class, "release-card__model")]//a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="js-release-gallery "]//a/@href',
    ]

    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
