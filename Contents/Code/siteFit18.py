import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    actorName = searchData.title.lower()
    baseURL = PAsearchSites.getSearchSearchURL(siteNum) + actorName.replace(' ', '-') + '%3A'
    count = 0
    while True:
        count += 1
        searchURL = baseURL + 'scene%d' % count
        req = PAutils.HTTPRequest(searchURL)
        if not req.ok:
            break

        searchPageElements = HTML.ElementFromString(req.text)

        titleNoFormatting = searchPageElements.xpath('//div[contains(@class, "info")]/h1/text()')[0]
        titleNoFormatting = PAutils.parseTitle(titleNoFormatting, siteNum)

        curID = PAutils.Encode(searchURL)
        actor = searchPageElements.xpath('//div[contains(@class, "info")]/h3/span/a/text()')[0]

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=80, lang=lang))


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "info")]/h1/text()')[0]

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "info")]/p/text()')[0]

    # Studio
    metadata.studio = 'Fit18'

    # Collections / Tagline
    metadata.collections.clear()
    tagline = 'Fit18'
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Young')
    movieGenres.addGenre('Gym')

    # Actors
    movieActors.clearActors()
    actorName = detailsPageElements.xpath('//div[contains(@class, "info")]/h3/span/a/text()')[0]
    actorPhotoURL = ''

    movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[contains(@class, "gallery-image")]/img/@src',
    ]

    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

    art = [o for o in art if len(art) >= 10]

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
