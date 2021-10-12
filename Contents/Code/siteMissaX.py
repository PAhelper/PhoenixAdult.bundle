import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="updateItem"] | //div[@class="photo-thumb video-thumb"]'):
        titleNoFormatting = searchResult.xpath('.//h4//a | .//p[@class="thumb-title"]')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
        releaseDate = parse(searchResult.xpath('.//span[@class="update_thumb_date"] | .//span[@class="date"] | .//div[contains(@class, "updateDetails")]/p/span[2]')[0].text_content().strip())
        if not siteNum == 1252:
            releaseDate = releaseDate.strftime('%Y-%m-%d')

        actors = searchResult.xpath('.//span[@class="tour_update_models"]//a | .//p[@class="model-name"]//a')
        if actors:
            firstActor = actors[0].text_content().strip()
            numActors = len(actors) - 1

        displayName = '%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate)
        if firstActor:
            displayName = '%s + %d in %s' % (firstActor, numActors, displayName)

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name=displayName, score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//span[@class="update_title"] | //p[@class="raiting-section__title"]')[0].text_content().strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//span[@class="latest_update_description"] | //p[contains(@class, "text")]')[0].text_content().replace('Includes:', '').replace('Synopsis:', '').strip()
    except:
        pass

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = metadata.studio
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    try:
        date = detailsPageElements.xpath('//span[@class="update_date"] | //span[contains(@class, "availdate")]')[0].text_content().replace('Available to Members Now', '').strip()
    except:
        date = detailsPageElements.xpath('//p[@class="dvd-scenes__data"]')[0].text_content().split('|')[1].replace('Added:', '').strip()

    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="update_block"]//span[@class="tour_update_models"]//a | //p[@class="dvd-scenes__data"][1]//a')
    for actorLink in actors:
        actorName = actorLink.text_content().strip()

        if siteNum == 1264 and metadata.title.endswith(': ' + actorName):
            metadata.title = metadata.title[:-len(': ' + actorName)]

        actorPageURL = actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPageElements = HTML.ElementFromString(req.text)
        actorPhotoURL = ''
        actorPhotoElement = actorPageElements.xpath('//img[contains(@class, "model_bio_thumb")]/@src0_1x')
        if actorPhotoElement:
            actorPhotoURL = actorPhotoElement[0]
            if not actorPhotoURL.startswith('http'):
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteNum) + actorPhotoURL

        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//span[contains(@class, "update_tags")]//a | //p[@class="dvd-scenes__data"][2]//a')
    for genreLink in genres:
        genreName = genreLink.text_content()

        movieGenres.addGenre(genreName)

    # Posters/Background
    art = []
    xpaths = [
        '//img[contains(@class, "update_thumb")]/@src0_4x',
        '//img[contains(@class, "update_thumb")]/@src0_1x',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if not img.startswith('http'):
                img = PAsearchSites.getSearchBaseURL(siteNum) + '/' + img
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
                if width > 1 and height >= width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
