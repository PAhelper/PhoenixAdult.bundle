import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.lower().replace(' ', '-')
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    detailsPageElements = HTML.ElementFromString(req.text)

    script_text = detailsPageElements.xpath('//script[@type="application/ld+json"]')[-1].text_content()
    sceneData = json.loads(script_text)

    titleNoFormatting = sceneData['name'].split('|')[0].strip()
    firstActor = sceneData['actors'][0]['name']
    sceneURL = sceneData['url']
    curID = PAutils.Encode(sceneURL)

    date = sceneData['datePublished']
    releaseDate = parse(date).strftime('%Y-%m-%d')

    if searchData.date:
        score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
    else:
        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s - %s [%s] %s' % (firstActor, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    script_text = detailsPageElements.xpath('//script[@type="application/ld+json"]')[-1].text_content()
    sceneData = json.loads(script_text)

    # Title
    metadata.title = sceneData['name'].split('|')[0].strip()

    # Summary
    metadata.summary = sceneData['description']

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    metadata.collections.add(metadata.studio)

    # Release Date
    date = sceneData['datePublished']
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genreLink in sceneData['keywords'].split(','):
        genreName = genreLink.strip()

        movieGenres.addGenre(genreName)

    # Actor(s)
    for actorLink in sceneData['actors']:
        actorName = actorLink['name']
        actorPhotoURL = detailsPageElements.xpath('//div[@class="model-box"]//a//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art.append(sceneData['image'])

    xpaths = [
        '//figure[contains(@itemprop, "associatedMedia")]/a/@href',
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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
