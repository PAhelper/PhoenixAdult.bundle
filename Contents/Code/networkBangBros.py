import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    for searchPageNum in range(1, 3):
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded + "/" + str(searchPageNum))
        searchResults = HTML.ElementFromString(req.text)

        for searchResult in searchResults.xpath('//div[@class="thumbsHolder elipsTxt"]/div[1]/div[@class="echThumb"]'):
            if searchResult.xpath('.//a[contains(@href, "/video")]'):
                titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//a[contains(@href, "/video")]/@title')[0], siteNum).replace('’', '\'')
                curID = PAutils.Encode(searchResult.xpath('.//a[contains(@href, "/video")]//@href')[0])
                subSite = searchResult.xpath('.//span[@class="faTxt"]')[0].text_content().strip()
                releaseDate = parse(searchResult.xpath('.//span[@class="faTxt"]')[1].text_content().strip()).strftime('%Y-%m-%d')

                if searchData.date:
                    score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [BangBros/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content(), siteNum).replace('’', '\'')

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="vdoDesc"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Bang Bros'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//a[contains(@href, "/websites")]')[1].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.add(metadata.tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[contains(@class, "vdoTags")]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="vdoCast"]//a[contains(@href, "/model")]'):
        actorName = actorLink.text_content().strip()

        actorPageURL = actorLink.get('href')
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = 'http:' + actorPage.xpath('//div[@class="profilePic_in"]//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//img[contains(@id, "player-overlay-image")]/@src',
        '//div[@class="WdgtPic modal-overlay"]//img/@src'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            if not poster.startswith('http'):
                poster = 'http:' + poster
            if 'big' not in poster:
                (poster, filename) = poster.rsplit('/', 1)
                poster = poster + '/big' + filename

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
