import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.replace('www.', '')
        if ('trailers' in sceneURL) and 'as3' not in sceneURL and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()
        subSite = detailsPageElements.xpath('//div[@class="about"]//h3')[0].text_content().replace('About', '').strip()
        curID = PAutils.Encode(sceneURL)

        date = ''
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        displayDate = releaseDate if date else ''

        if searchData.date and displayDate:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [PervCity/%s]' % (titleNoFormatting, subSite), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="infoBox clear"]/p')[0].text_content().strip()

    # Studio
    metadata.studio = 'PervCity'

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = detailsPageElements.xpath('//div[@class="about"]//h3')[0].text_content().replace('About', '').strip()
    metadata.collections.add(metadata.tagline)

    # Genres
    movieGenres.clearGenres()

    # Actors
    date = ''
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h3/span/a')
    for actorLink in actors:
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        modelURL = actorLink.xpath('.//@href')[0].replace(PAsearchSites.getSearchBaseURL(siteNum).replace('www.', ''), PAsearchSites.getSearchBaseURL(1165).replace('www.', ''))
        req = PAutils.HTTPRequest(modelURL)
        actorsPageElements = HTML.ElementFromString(req.text)
        actorPhotoURL = actorsPageElements.xpath('//div[@class="starPic"]/img/@src')[0]

        if not date:
            for scene in actorsPageElements.xpath('//div[@class="videoBlock"]'):
                if scene.xpath('.//h3')[0].text_content().replace('...', '').strip().lower() in metadata.title.lower():
                    date = actorsPageElements.xpath('.//div[@class="date"]')[0].text_content()

            if date:
                date_object = parse(date)
                metadata.originally_available_at = date_object
                metadata.year = metadata.originally_available_at.year

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="snap"]//@src0_3x',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if 'http' not in img:
                img = PAsearchSites.getSearchBaseURL(siteNum) + img

            art.append(img)

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
