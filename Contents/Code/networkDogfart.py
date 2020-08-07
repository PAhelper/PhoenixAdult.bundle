import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.replace(' a ', ' ')

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//a[contains(@class, "thumbnail")]'):
        titleNoFormatting = searchResult.xpath('.//h3[@class="scene-title"]')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.get('href').split('?')[0])
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
        fullSubSite = searchResult.xpath('.//div/p[@class="help-block"]')[0].text_content().strip()

        if 'BehindTheScenes' in fullSubSite and 'BTS' not in titleNoFormatting:
            titleNoFormatting = titleNoFormatting + ' BTS'
        subSite = fullSubSite.split('.com')[0]

        if subSite == PAsearchSites.getSearchSiteName(siteNum):
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        else:
            score = 60 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [Dogfart/%s]' % (titleNoFormatting, subSite), score=score, lang=lang))

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
    metadata.title = detailsPageElements.xpath('//div[@class="icon-container"]/a/@title')[0]

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "description")]')[0].text_content().strip().replace('...read more', '').replace('\n', ' ')

    # Studio
    metadata.studio = 'Dogfart Network'

    # Collections / Tagline
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//h3[@class="site-name"]')[0].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.add(PAsearchSites.getSearchSiteName(siteID))

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="categories"]/p/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//h4[@class="more-scenes"]/a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="icon-container"]//img/@src'
    ]
    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            art.append(img)

    for pageURL in detailsPageElements.xpath('//div[contains(@class, "preview-image-container")]//a/@href'):
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteID) + pageURL)
        posterPage = HTML.ElementFromString(req.text)

        posterUrl = posterPage.xpath('//div[contains(@class, "remove-bs-padding")]/img/@src')[0]
        art.append(posterUrl)

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
                if width > height and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
