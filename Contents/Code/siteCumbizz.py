import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.replace(' ', '-')
    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    titleNoFormatting = detailsPageElements.xpath('//h1[@class="har_h1_title"]')[0].text_content().strip()
    curID = PAutils.Encode(sceneURL)

    score = 90

    results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, titleNoFormatting), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.Decode(metadata_id[2])

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="container text-center"]//h2')[0].text_content().strip()

    # Studio
    metadata.studio = 'Cumbizz'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//span[@class="label label-primary"]/a'):
        genreName = genreLink.text_content().strip().lower()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="breadcrumbs"]/a'):
        actorName = str(actorLink.text_content().strip())
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//section[@class="har_section har_image_bck har_wht_txt har_fixed"]/@data-image',
        '//img[@class="vidgal unos"]/@src',
        '//img[@class="vidgal dos"]/@src',
        '//img[@class="vidgal tres"]/@src',
        '//img[@class="vidgal quatros"]/@src',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            art.append(img)

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
