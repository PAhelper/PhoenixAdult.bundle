import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.replace(' ', '+')
    for searchPageNum in range(1, 3):
        url = PAsearchSites.getSearchSearchURL(siteNum) + '%s&page=%d' % (searchData.encoded, searchPageNum)
        req = PAutils.HTTPRequest(url)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[contains(@class, "video-thumb") or contains(@class, "item-video")]'):
            titleNoFormatting = searchResult.xpath('(.//p[@class="text-thumb"] | .//div[@class="item-title"])/a')[0].text_content().strip()
            curID = PAutils.Encode(searchResult.xpath('(.//p[@class="text-thumb"] | .//div[@class="item-title"])/a/@href')[0])
            subSite = searchResult.xpath('.//p[@class="text-thumb"]/a[@class="badge"] | .//div[@class="item-sitename"]/a')[0].text_content().strip()

            date = searchResult.xpath('.//span[@class="date"] | .//div[@class="item-date"]')[0].text_content().split('|')[-1].strip()
            releaseDate = parse(date).strftime('%Y-%m-%d')

            actorNames = []
            for actorLink in searchResult.xpath('(.//span[@class="category"] | .//div[@class="item-models"])//a'):
                actorName = actorLink.text_content().strip()

                actorNames.append(actorName)
            actorNames = ', '.join(actorNames)

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s in %s [CherryPimps/%s] %s' % (actorNames, titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//*[@class="trailer-block_title"] | //h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="info-block"]//p[@class="text"] | //div[@class="update-info-block"]//p')[0].text_content().strip()

    # Studio
    metadata.studio = 'Cherry Pimps'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="info-block_data"]//p[@class="text"] | //div[@class="update-info-row"]')[0].text_content().split('|')[0].replace('Added', '').replace(':', '').strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="info-block"]//a | //ul[@class="tags"]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="info-block_data"]//a | //div[contains(@class, "model-list-item")]//a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            if not actorName:
                actorName = actorLink.xpath('//span')[0].text_content().strip()
            actorPhotoURL = ''

            actorPhoto = actorLink.xpath('//img/@src0_1x')
            if actorPhoto:
                actorPhotoURL = actorPhoto[0]
            else:
                actorPageURL = actorLink.get('href')
                if not actorPageURL.startswith('http'):
                    actorPageURL = PAsearchSites.getSearchBaseURL(siteNum) + '/' + actorPageURL

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
        '//img[contains(@class, "update_thumb")]/@src',
        '//img[contains(@class, "update_thumb")]/@src0_1x',
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
