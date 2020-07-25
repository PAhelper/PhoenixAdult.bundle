import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="scene"]'):
        titleNoFormatting = searchResult.xpath('.//h4[@itemprop="name"]//a')[0].text_content()
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        subSite = searchResult.xpath('.//small[@class="shadow"]//a')[0].text_content().strip()
        if subSite.lower().replace('.com', '').replace(' ', '') == PAsearchSites.getSearchSiteName(siteNum).lower().replace(' ', ''):
            siteScore = 10
        else:
            siteScore = 0

        score = siteScore + 90 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, subSite), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@itemprop="name"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//section[@class="scene-content"]//p[@itemprop="description"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Finishes The Job'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//section[@class="scene-content"]//h4//a')
    for actorLink in actors:
        actorName = actorLink.text_content()
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//section[@class="scene-content"]//p[1]//a')
    for genre in genres:
        movieGenres.addGenre(genre.text_content())

    # Poster
    art = []
    xpaths = [
        '//video/@poster'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            art.append(img)

    for posterCur in detailsPageElements.xpath('//div[contains(@class, "first-set")]//img'):
        sceneName = posterCur.get('alt')
        if sceneName.lower() == metadata.title.lower():
            art.append(posterCur.get('src'))

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
