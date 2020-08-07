import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//ul[@id="search_results"]//li[contains(@class, "col-sm-6")]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="scene"]//div//h3//a')[0].text_content()
        curID = PAutils.Encode(searchResult.xpath('.//div[@class="scene"]//div//h3//a/@href')[0])
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [Private]' % titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Summary
    metadata.summary = detailsPageElements.xpath('//meta[@itemprop="description"]/@content')[0]

    # Studio
    metadata.studio = 'Private'

    # Tagline and Collection(s)
    metadata.collections.clear()
    try:
        tagline = detailsPageElements.xpath('//span[@class="title-site"]')[0].text_content()
    except:
        tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//ul[contains(@class,"scene-tags")]//li'):
        genreName = genreLink.xpath('.//a')[0].text_content().lower()

        movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//meta[@itemprop="uploadDate"]')[0].get('content')
    if date:
        date_object = datetime.strptime(date, '%m/%d/%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    elif sceneDate:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorPage in detailsPageElements.xpath('//ul[@id="featured_pornstars"]//li[contains(@class, "featuring")]'):
        actorName = actorPage.xpath('.//div[@class="model"]//a/@title')[0]
        actorPhotoURL = actorPage.xpath('.//div[@class="model"]//a//picture//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//meta[@itemprop="thumbnailUrl"]/@content'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

    backgrounds = detailsPageElements.xpath('//meta[@itemprop="contentURL"]/@content')[0]
    j = backgrounds.rfind('upload/')
    k = backgrounds.rfind('trailers/')
    sceneID = backgrounds[j + 7:k - 1]
    backgrounds = backgrounds[:k] + 'Fullwatermarked/'
    for i in range(1, 10):
        img = backgrounds + sceneID.lower() + '_' + '{0:0=3d}'.format(i * 5) + '.jpg'

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
