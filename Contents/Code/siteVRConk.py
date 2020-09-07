import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    directURL = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.replace(' ', '-').lower()

    searchResults = [directURL]
    googleResults = PAutils.getFromGoogleSearch(searchTitle, siteNum)
    for sceneURL in googleResults:
        if ('/virtualreality/' in sceneURL and sceneURL not in searchResults):
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)

            if detailsPageElements:
                curID = PAutils.Encode(sceneURL)
                titleNoFormatting = detailsPageElements.xpath('//div[contains(@class, "video-details")]//h1[1]')[0].text_content().strip()
                date = detailsPageElements.xpath('//div[@class="stats-container"]//li[3]//span[2]')[0].text_content().strip()
                releaseDate = parse(date).strftime('%Y-%m-%d')

                if searchDate and releaseDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "video-details")]//h1[1]')[0].text_content().strip()

    # Summary
    summary = detailsPageElements.xpath('(.//*[@class="d-container"])[4]')[0].text_content().strip()
    metadata.summary = ' '.join(summary.splitlines())

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="stats-container"]//li[3]//span[2]')[0].text_content().strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('.//*[@class="models-list"]//img'):
        actorName = actorLink.get('alt')
        actorPhotoURL = actorLink.get('src')

        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    for genre in detailsPageElements.xpath('//a[@class="link12"]'):
        genreName = genre.text_content().strip()

        movieGenres.addGenre(genreName)

    # Posters
    art = []
    xpaths = [
        '//a[contains(@title, "Image")]/@href'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            poster = poster.split('?')[0]

            art.append(poster)
    art.insert(0, detailsPageElements.xpath('//div[contains(@class, "splash-screen")]/@style')[0].split('url(')[1].split(')')[0])

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
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
