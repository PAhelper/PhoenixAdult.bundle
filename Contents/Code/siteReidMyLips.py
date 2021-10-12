import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.lower().replace(' ', '-')
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded + '.html'
    req = PAutils.HTTPRequest(url)
    detailsPageElements = HTML.ElementFromString(req.text)

    titleNoFormatting = detailsPageElements.xpath('//span[@class="update_title"]')[0].text_content().strip()
    curID = PAutils.Encode(url)
    date = detailsPageElements.xpath('//span[@class="availdate"]/text()')[0].strip()
    releaseDate = parse(date).strftime('%Y-%m-%d')

    score = 100

    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [ReidMyLips] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//span[@class="update_title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[@class="latest_update_description"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'ReidMyLips'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="availdate"]/text()')[0].strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//span[@class="update_tags"]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actorName = 'Riley Reid'
    actorPhotoURL = ''

    movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="update_image"]//img/@src0_2x',
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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
