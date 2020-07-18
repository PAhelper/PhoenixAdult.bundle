import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    sceneID = searchTitle.split(' ', 1)[0]
    try:
        sceneTitle = encodedTitle.split(' ', 1)[1]
    except:
        sceneTitle = ''

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + sceneID)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="video-details"]'):
        titleNoFormatting = searchResult.xpath('//h2[@class="h2 m-0"]')[0].text_content()
        curID = searchTitle.lower().replace(' ', '-')
        subSite = searchResult.xpath('//a[@class="username "]')[0].text_content().strip()
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        if sceneTitle:
            score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
        else:
            score = 90

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [ManyVids/%s]' % (titleNoFormatting, subSite), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = metadata.id.split('|')
    sceneURL = PAsearchSites.getSearchBaseURL(siteID) + '/video/' + metadata_id[0]
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h2[@class="h2 m-0"]')[0].text_content().strip()

    # Summary
    try:
        paragraphs = detailsPageElements.xpath('//div[@class="desc-text"]')
        pNum = 0
        summary = ""
        for paragraph in paragraphs:
            if pNum >= 0 and pNum < (len(paragraphs)):
                summary = summary + '\n\n' + paragraph.text_content()
            pNum += 1
    except:
        pass
    if summary == '':
        try:
            summary = detailsPageElements.xpath('//div[@class="desc-text"]')[0].text_content().strip()
        except:
            pass
    metadata.summary = summary.strip()

    # Studio
    metadata.studio = 'ManyVids'

    # Collections / Tagline
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//a[contains(@class,"username ")]')[0].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="tags"]/a')
    for genreLink in genres:
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actorName = detailsPageElements.xpath('//a[contains(@class,"username ")]')[0].text_content()
    actorPhotoURL = ''

    try:
        actorPhotoURL = detailsPageElements.xpath('//div[@class="pr-2"]/a/img')[0].get('src')
    except:
        pass

    movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@id="rmpPlayer"]/@data-video-screenshot'
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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
