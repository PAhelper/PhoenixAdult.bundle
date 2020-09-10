import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    searchResults = []
    googleResults = PAutils.getFromGoogleSearch(searchTitle, siteNum)
    for sceneURL in googleResults:
        if ('/tour1/' in sceneURL and sceneURL.endswith('.html') and sceneURL not in searchResults):
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        curID = PAutils.Encode(sceneURL)
        titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()
        releaseDate = searchDate if searchDate else ''

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    if len(metadata_id) > 2:
        sceneDate = metadata_id[2]

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    m = re.search("'playlistfile': '(.+playlist\.xml)'", req.text)
    if m:
        playListUrl = m.group(1)

        xmlPlaylistElements = XML.ElementFromURL(playListUrl)
        poster = xmlPlaylistElements.xpath('//channel/item/*[name()="media:group"]/*[name()="media:thumbnail"]/@url')
        if poster:
            posterURL = poster[0]
    else:
        Log('Playlist file NOT found.')
        m = re.search("'image': '(.+bookend\.jpg)'", req.text)
        if m:
            posterURL = m.group(1)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@id="video-page-desc"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Dirty Hard Drive'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Actors
    movieActors.clearActors()
    actorLink = detailsPageElements.xpath('//div[@id="video-specs"]//span')
    if actorLink:
        actorName = actorLink[-1].text_content().strip()
        actorPhotoURL = ''

        if not actorName:
            actorPageURL = actorLink.get('href')
            actorName = actorPageURL.rsplit('/', 2)[-1].replace('.html', '', 1).replace('pornstar_', '', 1).replace('_', ' ').strip().title()
            if actorPageURL.startswith('http'):
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID)

            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            actorPhoto = actorPage.xpath('//div[@id="global-model-img"]//img/@src')
            if actorPhoto:
                actorPhotoURL = actorPhoto[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Posters/Background
    art = []
    xpaths = []

    if posterURL:
        art.append(posterURL)

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
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
