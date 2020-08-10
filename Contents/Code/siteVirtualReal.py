import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.lower().replace(' ', '-')
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchPage = HTML.ElementFromString(req.text)

    titleNoFormatting = searchPage.xpath('//h1')[0].text_content().replace('VR Porn video', '').strip()
    curID = PAutils.Encode(searchPage.xpath('//link[@rel="canonical"]/@href')[0])

    firstActor = searchPage.xpath('//div[@class="w-portfolio-item-image modelBox"]//img/@alt')[0]

    script_text = searchPage.xpath('//script[@type="application/ld+json"]')[1].text_content()
    alpha = script_text.find('datePublished')
    omega = script_text.find('"', alpha + 6)
    script_date = script_text[alpha + 16:omega]
    releaseDate = parse(script_date).strftime('%Y-%m-%d')

    if searchDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s - %s [%s] %s' % (firstActor, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))
    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().replace('VR Porn video', '').strip()

    # Summary
    description = detailsPageElements.xpath('//div[@class="g-cols onlydesktop"]')
    if description:
        metadata.summary = description[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Tagline and Collection
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    script_text = detailsPageElements.xpath('//script[@type="application/ld+json"]')[1].text_content()
    alpha = script_text.find('datePublished')
    omega = script_text.find('"', alpha + 16)
    date = script_text[alpha + 16:omega]
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//a[@class="g-btn type_default"]//span'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="w-portfolio-item-image modelBox"]//img'):
        actorName = actorLink.get('alt')
        actorPhotoURL = actorLink.get('src')

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//dl8-video/@poster',
        '//figure[contains(@itemprop, "associatedMedia")]/a/@href'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

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
