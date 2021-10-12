import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = re.sub(r'\D', '', searchData.title)
    actorName = re.sub(r'\s\d.*', '', searchData.title).replace(' ', '-')
    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + actorName + '/' + sceneID

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)
    titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()

    curID = PAutils.Encode(sceneURL)

    score = 100

    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    summary_xpaths = [
        '//div[@class="p-desc"]',
        '//div[contains(@class, "desc")]'
    ]

    for xpath in summary_xpaths:
        for summary in detailsPageElements.xpath(xpath):
            metadata.summary = summary.text_content().replace('Read More »', '').strip()
            break

    # Studio
    metadata.studio = 'Score Group'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(metadata.tagline)

    # Release Date
    date = detailsPageElements.xpath('//div/span[@class="value"]')
    if date:
        date = date[1].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div/span[@class="value"]/a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)
    
    if siteNum == 1344:
        movieActors.addActor('Christy Marks', '')

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="mb-3"]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Posters/Background
    art = []

    match = re.search(r'posterImage: \'(.*)\'', req.text)
    if match:
        art.append(match.group(1))

    xpaths = [
        '//div[contains(@class, "thumb")]/img/@src',
        '//div[contains(@class, "p-image")]/a/img/@src',
        '//div[contains(@class, "dl-opts")]/a/img/@src',
        '//div[contains(@class, "p-photos")]/div/div/a/@href',
        '//div[contains(@class, "gallery")]/div/div/a/@href'
    ]

    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            if not poster.startswith('http'):
                poster = 'http:' + poster

            if 'shared-bits' not in poster:
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
