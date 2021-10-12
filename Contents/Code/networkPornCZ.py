import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.replace(' ', '+').replace('--', '+').lower()
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)

    for searchResult in searchResults.xpath('//div[@data-href]'):
        titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//h4')[0].text_content().strip(), siteNum)
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a/@href')[0]
        curID = PAutils.Encode(sceneURL)

        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [PornCZ/%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="heading-detail"]/p')[1].text_content().strip()

    # Studio
    metadata.studio = 'PornCZ'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[contains(., "Genres")]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    for actorLink in detailsPageElements.xpath('//div[contains(., "Actors")]/a'):
        actorName = actorLink.text_content()

        modelURL = PAsearchSites.getSearchBaseURL(siteNum) + actorLink.xpath('.//@href')[0]
        if 'http' not in modelURL:
            modelURL = PAsearchSites.getSearchBaseURL(siteNum) + modelURL

        req = PAutils.HTTPRequest(modelURL)
        modelsPageElements = HTML.ElementFromString(req.text)

        actorPhotoURL = modelsPageElements.xpath('//div[@class="model-heading-photo"]//@src')[0]

        if 'http' not in actorPhotoURL:
            actorPhotoURL = PAsearchSites.getSearchBaseURL(siteNum) + actorPhotoURL

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@id="photos"]//@data-src',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if 'http' not in img:
                img = PAsearchSites.getSearchBaseURL(siteNum) + img
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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
