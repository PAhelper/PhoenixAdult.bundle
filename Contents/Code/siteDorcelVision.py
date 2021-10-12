import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//a[contains(@class, "movies")]'):
        titleNoFormatting = searchResult.xpath('.//img/@alt')[0].strip()
        curID = PAutils.Encode(searchResult.get('href'))

        releaseDate = searchData.dateFormat() if searchData.date else ''

        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    releaseDate = None
    if len(metadata_id) > 2:
        releaseDate = metadata_id[2]

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    try:
        paragraph = detailsPageElements.xpath('//meta[@name="twitter:description"]/@content')[0].strip()
    except:
        try:
            paragraph = detailsPageElements.xpath('//div[@id="summaryList"]')[0].text_content().strip()
        except:
            paragraph = ''
    metadata.summary = paragraph.replace('</br>', '\n').replace('<br>', '\n').strip()

    # Tagline
    metadata.collections.clear()

    tagline = 'Dorcel Vision'
    studioNode = detailsPageElements.xpath('//div[@class="entries"]//strong[contains(., "Studio")]/following-sibling::a')
    if studioNode:
        metadata.collections.add(tagline)
        tagline = studioNode[0].text_content().strip()

    metadata.tagline = tagline
    metadata.studio = tagline
    metadata.collections.add(tagline)

    # Release Date
    if releaseDate:
        date_object = parse(releaseDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    else:
        yearNode = detailsPageElements.xpath('//div[@class="entries"]//strong[contains(., "Production year")]/following-sibling::text()')
        if yearNode:
            year = int(yearNode[0].strip())
            metadata.year = year

    # Genres
    movieGenres.clearGenres()

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[contains(@class, "casting")]//div[contains(@class, "slider-xl")]//div[@class="col-xs-2"]'):
        actorName = actorLink.xpath('.//a/strong')[0].text_content().strip()
        actorPhotoURL = actorLink.xpath('.//img/@data-src')[0]

        if not actorPhotoURL.startswith('http:'):
            actorPhotoURL = PAsearchSites.getSearchBaseURL(siteNum) + actorPhotoURL

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    art = []
    xpaths = [
        '//div[contains(@class, "covers")]/a[contains(@class, "cover")]/@href',
        '//div[contains(@class, "screenshots")]//div[contains(@class, "slider-xl")]/div[@class="slides"]/div[@class="col-xs-2"]/a/@href',
    ]

    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            poster = poster.strip().replace('blur9/', '/')

            if not poster.startswith('http'):
                poster = PAsearchSites.getSearchBaseURL(siteNum) + poster

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
