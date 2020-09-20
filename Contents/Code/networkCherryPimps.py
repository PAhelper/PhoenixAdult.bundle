import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    for searchPageNum in range(1, 3):
        url = PAsearchSites.getSearchSearchURL(siteNum) + '%s&page=%d' % (searchTitle.replace(' ', '+'), searchPageNum)
        req = PAutils.HTTPRequest(url)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[contains(@class, "video-thumb")]'):
            titleNoFormatting = searchResult.xpath('.//p[@class="text-thumb"]/a')[0].text_content().strip()
            curID = PAutils.Encode(searchResult.xpath('.//p[@class="text-thumb"]/a/@href')[0])
            subSite = searchResult.xpath('.//p[@class="text-thumb"]//a[@class="badge"]')[0].text_content().strip()

            date = searchResult.xpath('.//span[@class="date"]')[0].text_content().split('|')[1].strip()
            releaseDate = parse(date).strftime('%Y-%m-%d')

            actorNames = []
            for actorLink in searchResult.xpath('.//span[@class="category"]//a'):
                actorName = actorLink.text_content().strip()

                actorNames.append(actorName)
            actorNames = ', '.join(actorNames)

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s in %s [CherryPimps/%s] %s' % (actorNames, titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//*[@class="trailer-block_title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="info-block"]//p[@class="text"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Cherry Pimps'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="info-block_data"]//p[@class="text"]')[0].text_content().split('|')[0].replace('Added', '').strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="info-block"]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="info-block_data"]//a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            actorPageURL = actorLink.get('href')
            if not actorPageURL.startswith('http'):
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + '/' + actorPageURL

            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)

            img = actorPage.xpath('//img[contains(@class, "model_bio_thumb")]/@src')
            if not img:
                img = actorPage.xpath('//img[contains(@class, "model_bio_thumb")]@src0_1x')

            if img:
                actorPhotoURL = img[0]
                if not actorPhotoURL.startswith('http'):
                    actorPhotoURL = 'https:' + actorPhotoURL

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//img[contains(@class, "update_thumb")]/@src'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            if poster.startswith('http'):
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
