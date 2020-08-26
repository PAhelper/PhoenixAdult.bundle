import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    cookies = {'nats': 'MC4wLjMuNTguMC4wLjAuMC4w'}
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle, cookies=cookies)
    searchResults = HTML.ElementFromString(req.json()['html'])
    for sceneURL in searchResults.xpath('//div[@class="ep"]'):
        titleNoFormatting = searchResults.xpath('.//h3[@class="ep-title"]')[0].text_content().strip()
        sceneURL = searchResults.xpath('.//a/@href')[0]
        curID = PAutils.Encode(sceneURL)

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    cookies = {'nats': 'MC4wLjMuNTguMC4wLjAuMC4w'}
    req = PAutils.HTTPRequest(sceneURL, cookies=cookies)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().split('|')[0]

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "video-summary")]//p[@class=""]')[0].text_content()

    # Studio
    metadata.studio = '5Kporn'

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.add(metadata.tagline)

    # Date
    date = detailsPageElements.xpath('//h5[contains(., "Published")]')
    if date:
        date = date[0].text_content().replace('Published:', '').strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h5[contains(., "Starring")]/a')
    for actorLink in actors:
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        modelURL = actorLink.xpath('.//@href')[0]
        req = PAutils.HTTPRequest(modelURL, cookies=cookies)
        actorsPageElements = HTML.ElementFromString(req.text)

        img = actorsPageElements.xpath('//img[@class="model-image"]/@src')
        if img:
            actorPhotoURL = img[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[contains(@class, "gal")]//img/@src',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            art.append(img)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': sceneURL}, cookies=cookies)
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
