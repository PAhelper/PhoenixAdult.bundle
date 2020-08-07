import PAsearchSites
import PAgenres
import PAactors
import PAextras
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//article//a'):
        siteName = PAsearchSites.getSearchSiteName(siteNum) + '.xxx'
        titleNoFormatting = searchResult.xpath('./@title')[0]
        curID = PAutils.Encode(searchResult.xpath('./@href')[0])

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, siteName), score=score, lang=lang))

    url = PAsearchSites.getSearchSearchURL(siteNum).replace('.xxx', '.tv', 1)
    req = PAutils.HTTPRequest(url + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "entry")]//h3//a'):
        siteName = PAsearchSites.getSearchSiteName(siteNum) + '.tv'
        titleNoFormatting = searchResult.xpath('./text()')[0].strip()
        curID = PAutils.Encode(searchResult.xpath('./@href')[0])

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, siteName), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    if '.xxx' in sceneURL:
        # Title
        metadata.title = detailsPageElements.xpath('//h1[@class="entry-title"]/text()')[0].strip()

        # Summary
        metadata.summary = detailsPageElements.xpath('//div[@class="video-description"]')[0].text_content().strip()

        # Genres & Actors
        movieGenres.clearGenres()
        movieActors.clearActors()
        tags = detailsPageElements.xpath('//div[@class="tags"]//a')
        for tagLink in tags:
            tagName = tagLink.xpath('./@title')[0]
            tagURL = tagLink.xpath('./@href')[0]
            if '/teen/' not in tagURL:
                movieGenres.addGenre(tagName)
            else:
                movieActors.addActor(tagName, '')
    else:
        # Title
        metadata.title = detailsPageElements.xpath('//h1[@class="title"]/text()')[0].strip()

        # Summary
        metadata.summary = detailsPageElements.xpath('//div[contains(@class, "entry")]//p')[2].text_content().strip()

        # Genres & Actors
        movieGenres.clearGenres()
        movieActors.clearActors()
        tags = detailsPageElements.xpath('//div[@class="post-meta"]//a')
        for tagLink in tags:
            tagName = tagLink.xpath('./text()')[0].strip()
            tagURL = tagLink.xpath('./@href')[0]
            if '/models/' not in tagURL:
                movieGenres.addGenre(tagName)
            else:
                movieActors.addActor(tagName, '')

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Posters
    art = []
    xpaths = [
        '//video/@poster',
        '//dl[@class="gallery-item"]//img/@src'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
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
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
