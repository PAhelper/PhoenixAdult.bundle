import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.replace(' ', '-').lower()

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.title[:1])
    actorResults = HTML.ElementFromString(req.text)

    actorPage = actorResults.xpath('//a[contains(@href, "%s")]/@href' % searchData.encoded)[0]
    req = PAutils.HTTPRequest(actorPage)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="content-box"]'):
        titleNoFormatting = searchResult.xpath('.//h2//span')[0].text_content().strip()
        sceneURL = searchResult.xpath('.//a/@href')[0]
        curID = PAutils.Encode(sceneURL)

        releaseDate = searchData.dateFormat() if searchData.date else ''

        score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="description"]//p')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Collections / Tagline
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//dd[2]')
    for genreLink in detailsPageElements.xpath('//dd[2]'):
        genreName = genreLink.text_content().strip().lower()

        movieGenres.addGenre(genreName)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()

    actors = detailsPageElements.xpath('//dd[1]')
    for actorLink in actors:
        actorName = actorLink.xpath('.//a[1]')[0].text_content().strip()
        actorPhotoURL = actorLink.xpath('.//a[2]//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

        try:
            actorName = actorLink.xpath('.//a[3]')[0].text_content().strip()
            actorPhotoURL = actorLink.xpath('.//a[4]//img/@src')[0]
            movieActors.addActor(actorName, actorPhotoURL)
        except:
            pass

    # Director
    metadata.directors.clear()
    director = metadata.directors.new()
    director.name = 'Charles Dera'

    # Posters
    art = []
    req = PAutils.HTTPRequest(detailsPageElements.xpath('//dd[1]//a/@href')[0])
    posters = HTML.ElementFromString(req.text)
    for poster in posters.xpath('//a[contains(@href, "%s")]//img/@src' % sceneURL):
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
