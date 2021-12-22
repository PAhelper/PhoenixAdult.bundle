import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.replace(' ', '-')

    searchResults = []
    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if ('/updates/' in sceneURL and '/tour_hwxxx/' in sceneURL) and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)

            titleNoFormatting = detailsPageElements.xpath('//div[@class="trailerInfo"]/h2')[0].text_content().strip()
            date = detailsPageElements.xpath('//div[@class="trailerInfo"]/div[@class="released2 trailerStarr"]')[0].text_content().strip().split(',')[0]
            releaseDate = parse(date).strftime('%Y-%m-%d')
            curID = PAutils.Encode(sceneURL)

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'HotwifeXXX'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="trailerInfo"]/h2')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="dvdDescription"]/p')[0].text_content().replace('description: ', '').strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # No genres for scenes

    # Release Date
    date = detailsPageElements.xpath('//div[@class="trailerInfo"]/div[@class="released2 trailerStarr"]')[0].text_content().strip().split(',')[0]
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="trailerMInfo"]//span[@class="tour_update_models"]/a')
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
        req = PAutils.HTTPRequest(actorPageURL)
        if req.ok:
            actorPage = HTML.ElementFromString(req.text)
            actorPhotoNode = actorPage.xpath('//div[@class="modelBioPic"]/img/@src0_3x')
            if actorPhotoNode:
                actorPhotoURL = actorPhotoNode[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//span[@id="trailer_thumb"]//img/@src',
    ]

    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            poster = poster.strip()
            
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
