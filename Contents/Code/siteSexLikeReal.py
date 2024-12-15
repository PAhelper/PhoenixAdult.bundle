import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    directURL = PAsearchSites.getSearchSearchURL(siteNum) + searchData.title.replace(' ', '-').lower()

    searchResults = [directURL]
    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if ('/scenes/' in sceneURL and sceneURL not in searchResults):
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)
            curID = PAutils.Encode(sceneURL)
            titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()
            releaseDate = parse(detailsPageElements.xpath('//time/@datetime')[0]).strftime('%Y-%m-%d')

            Log("directURL: " + str(directURL))
            Log("sceneURL: " + str(sceneURL))
            if directURL == sceneURL:
                score = 100
            elif searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    maybeSummary = detailsPageElements.xpath('//div[contains(@class, "u-lh--opt u-fs--fo u-wh")]')
    if maybeSummary and len(maybeSummary) == 1:
        metadata.summary = maybeSummary[0].text_content().strip()

    # Studio
    metadata.studio = detailsPageElements.xpath('//div[contains(@class, "u-inline-block u-align-y--m u-relative u-fw--bold")]')[0].text_content().strip()

    # Tagline and Collection(s)
    metadata.collections.add(metadata.studio)

    # Release Date
    maybeDate = detailsPageElements.xpath('//div[contains(@class, "u-flex u-flex-wrap u-align-i--center u-fs--fo u-dw u-mt--three u-flex-grow--one desktop:u-mt--four desktop:u-fs--si")]/time/@datetime')[0]
    if maybeDate:
        date_object = parse(maybeDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    else:
        date = detailsPageElements.xpath('//time[contains(@class, "u-inline-block u-align-y--m")]/@datetime')[0]
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genreName in detailsPageElements.xpath('//meta[@property="video:tag"]/@content'):
        movieGenres.addGenre(genreName)

    # Actor(s)
    actors = detailsPageElements.xpath('//meta[@property="video:actor"]/@content')
    for actorName in actors:
        actorLink = '/pornstars/' + actorName.replace(' ', '-').lower()
        actorPageURL = PAsearchSites.getSearchBaseURL(siteNum) + actorLink

        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPage.xpath('//div[@class="u-ratio u-ratio--top u-ratio--model u-radius--two u-mb--four"]/img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters/Background
    xpaths = [
        '//meta[@property="og:image"]/@content',
        '//a[contains(@class, "u-ratio--lightbox")]/@href',
    ]

    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
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
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
