import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.replace(' ', '-')
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + '/')
    actressSearchResults = HTML.ElementFromString(req.text)

    actressPageUrl = actressSearchResults.xpath('//div[@class="item-inside"]//a/@href')[0]
    req = PAutils.HTTPRequest(actressPageUrl)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class,"listing-videos")]//div[@class="item"]'):
        titleNoFormatting = searchResult.xpath('.//span[@class="title"]')[0].text_content()
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().replace('th', '').replace('st', '').strip()).strftime('%Y-%m-%d')

        subSiteRaw = searchResult.xpath('.//div[@class="meta"]//span[@class="date-and-site"]//span')[0].text_content()
        if subSiteRaw == 'kha':
            subSite = 'KarupsHA'
        elif subSiteRaw == 'kow':
            subSite = 'KarupsOW'
        elif subSiteRaw == 'kpc':
            subSite = 'KarupsPC'

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(titleNoFormatting.lower(), searchTitle.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = metadata.id.split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1//span[@class="title"]')[0].text_content().strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="content-information-description"]//p')[0].text_content().strip()
    except:
        pass

    # Studio
    metadata.studio = 'Karups'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//h1//span[@class="sup-title"]//span')[0].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="date"]/span[@class="content"]')[0].text_content().replace(tagline, '').replace('Video added on', '').strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    if tagline == 'KarupsHA':
        genres = ['Amateur']
    if tagline == 'KarupsPC':
        genres = []
    if tagline == 'KarupsOW':
        genres = ['MILF']

    for genre in genres:
        movieGenres.addGenre(genre)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//span[@class="models"]//a'):
        actorName = actorLink.text_content().strip()

        actorPageURL = actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPageElements = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPageElements.xpath('//div[@class="model-thumb"]//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="video-player"]//video/@poster',
        '//img[@class="poster"]/@src',
        '//div[@class="video-thumbs"]//img/@src'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
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
