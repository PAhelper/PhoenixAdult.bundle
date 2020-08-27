import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = re.sub('\D.*', '', searchTitle)

    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
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
    try:
        sceneDate = metadata_id[2]
    except:
        pass
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
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.add(metadata.tagline)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h1')[0].text_content().strip().split(',')
    for actor in actors:
        actorName = actor.strip()
        actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + 'media/models/' + actorName.lower() + '.jpg'

        movieActors.addActor(actor, actorPhotoURL)

    # Date
    date = ""

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
    for genre in genres.split(','):
        movieGenres.addGenre(genre.strip())

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