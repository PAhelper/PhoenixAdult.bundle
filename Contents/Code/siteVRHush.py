import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.replace(' ', '_')
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    detailsPageElements = HTML.ElementFromString(req.text)

    titleNoFormatting = detailsPageElements.xpath('//h1[@class="latest-scene-title"]')[0].text_content().strip()
    curID = PAutils.Encode(detailsPageElements.xpath('//link[@rel="canonical"]/@href')[0])
    releaseDate = parse(detailsPageElements.xpath('//div[contains(@class, "latest-scene-meta")]//div[contains(@class, "text-left")]')[0].text_content().strip()).strftime('%Y-%m-%d')

    if searchDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 95

    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [VRHush] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    art = []

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="latest-scene-title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[contains(@class, "full-description")]')[0].text_content().strip()

    # Studio
    metadata.studio = 'VRHush'

    # Tagline and Collection
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class, "latest-scene-meta")]//div[contains(@class, "text-left")]')[0].text_content().strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[contains(@class,"label")]')
    for genreLink in genres:
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actor in detailsPageElements.xpath('//h5[@class="latest-scene-subtitle"]//a[contains(@href, "/models/")]'):
        actorName = actor.text_content().strip()

        actorPageURL = actor.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = 'https:' + actorPage.xpath('//img[@id="model-thumbnail"]/@src')[0]

        art.append(actorPhotoURL)
        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    xpaths = [
        '//dl8-video/@poster',
        '//div[contains(@class,"owl-carousel")]//img/@src'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if not img.startswith('http'):
                img = 'https:' + img

            art.append(img)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.google.com'})
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
