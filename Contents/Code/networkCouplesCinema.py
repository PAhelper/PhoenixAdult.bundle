import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = searchData.title.split(' ', 1)[0]
    if unicode(sceneID, 'UTF-8').isdigit():
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    if sceneID:
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/post/details/' + sceneID
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        curID = PAutils.Encode(sceneURL)
        titleNoFormatting = detailsPageElements.xpath('//div[contains(@class, "mediaHeader")]//span[contains(@class, "title")]')[0].text_content().strip()
        studio = detailsPageElements.xpath('//span[contains(@class, "type")]')[0].text_content().split('|')[0].strip()
        score = 100

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, studio), score=score, lang=lang))
    else:
        searchData.encoded = searchData.title.replace(' ', '+')
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[contains(@class, "post")]'):
            titleNoFormatting = searchResult.xpath('.//span[contains(@class, "title")]')[0].text_content().strip()
            sceneURL = searchResult.xpath('.//a[contains(@class, "media")]/@href')[0]

            studio = searchResult.xpath('.//span[contains(@class, "source")]')[0].text_content().strip()
            sceneCover = PAutils.Encode(searchResult.xpath('.//a[contains(@class, "media")]//img[contains(@class, "image")]/@src')[0])
            releaseDate = searchData.dateFormat() if searchData.date else ''

            curID = PAutils.Encode(sceneURL)

            score = 90 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())
            if PAsearchSites.getSearchSiteName(siteNum).lower() == studio.lower():
                score += 10

            results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, releaseDate, sceneCover), name='%s [%s]' % (titleNoFormatting, studio), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    searchDate = metadata_id[2] if len(metadata_id) > 2 else ''
    sceneCover = PAutils.Decode(metadata_id[3]) if len(metadata_id) > 3 else ''

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "mediaHeader")]//span[contains(@class, "title")]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[contains(@class, "description")]')[0].text_content().strip()

    # Studio
    metadata.studio = detailsPageElements.xpath('//span[contains(@class, "type")]')[0].text_content().split('|')[0].strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.collections.add('CouplesCinema')
    metadata.collections.add(metadata.studio)

    # Release Date
    if searchDate:
        date_object = parse(searchDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    else:
        Log('Failed to parse searchDate: %s , using release year' % searchDate)
        year = detailsPageElements.xpath('//span[contains(@class, "type")]')[0].text_content().split('|')[1].strip()
        metadata.year = int(year)

    # Genres
    movieGenres.clearGenres()

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[contains(@class, "cast")]/a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//video/@poster',
    ]

    if sceneCover:
        art.append(sceneCover)

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if not img.startswith('http'):
                img = PAsearchSites.getSearchBaseURL(siteNum) + img

            art.append(img)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = HTTPRequest(posterUrl)
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
