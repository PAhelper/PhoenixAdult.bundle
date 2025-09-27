# coding=utf-8
import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//a[@class="video-card__item"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="video-card__title"]')[0].text_content()
        sceneUrl = searchResult.get('href')
        curID = PAutils.Encode(sceneUrl)
        actors = searchResult.xpath('.//div[@class="video-card__actors"]')[0].text_content()

        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s in %s [%s]' % (actors, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "right-info")]//h1')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    movieCollections.addCollection(metadata.studio)

    # Release Date
    sceneDate = detailsPageElements.xpath('//div[contains(@class, "info mt-5")]')[0].text_content().split('•')[1].strip()
    date_object = parse(sceneDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Summary
    description = detailsPageElements.xpath('//div[@class="description"]//span[contains(@class, "full")]')
    if description:
        metadata.summary = description[0].text_content().strip()
    else:
        metadata.summary = detailsPageElements.xpath('//details[@class="description"]')[0].text_content().strip()

    # Genres
    for genreLink in detailsPageElements.xpath('//div[contains(@class, "tag-list")]'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actor(s)
    for actorLink in detailsPageElements.xpath('//div[contains(@class, "right-info")]//div[contains(@class, "info")]//a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    img = detailsPageElements.xpath('//meta[@property="og:image"]/@content')[0]
    art.append(img)

    posters = detailsPageElements.xpath('//div[@class="gallery-item"]//a/@href')
    for poster in posters:
        img = poster.split('?', 1)[0]
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
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
