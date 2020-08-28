import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    sceneID = None
    splited = searchTitle.split(' ')
    if unicode(splited[0], 'UTF-8').isdigit():
        sceneID = splited[0]
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()
    
    if sceneID:
        sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneID
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().replace(',', ' and')
        curID = PAutils.Encode(sceneURL)

        score = 100

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().replace(',', ' and') + 'from ' + PAsearchSites.getSearchSiteName(siteID).replace(' ', '') + '.com'

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//meta[@name="description"]/@content')[0]
    except:
        pass

    # Studio
    metadata.studio = 'Teen Core Club'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h1')[0].text_content().strip().split(',')
    for actor in actors:
        actorName = actor.strip()
        actorPhotoURL = '%s/media/models/%s.jpg' % (PAsearchSites.getSearchBaseURL(siteID), actorName.lower())

        movieActors.addActor(actorName, actorPhotoURL)

    # Date
    try:
        date = detailsPageElements.xpath('//li')[1].text_content().strip()
        date_object = datetime.strptime(date, '%Y')

        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    except:
        pass

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//meta[@name="keywords"]/@content')[0]
    for genreLink in genres.split(','):
        genreName = genreLink.strip()

        movieGenres.addGenre(genreName)

    # Posters
    art = []
    xpaths = [
        '//div[contains(@class,"video-detail")]//img/@src',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            img = 'https:' + img
            if 'www' in img:
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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
