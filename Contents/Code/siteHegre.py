import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = encodedTitle + '&year=' + parse(searchDate).strftime('%Y') if searchDate else encodedTitle
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "item")]'):
        sceneURL = searchResult.xpath('.//a/@href')[0]
        if '/films/' in sceneURL or '/massage/' in sceneURL:
            curID = PAutils.Encode(sceneURL)
            titleNoFormatting = searchResult.xpath('.//img/@alt')[0].strip()
            releaseDate = parse(searchResult.xpath('.//div[@class="details"]/span[last()]')[0].text_content().strip()).strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    try:
        metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    except:
        try:
            metadata.title = detailsPageElements.xpath('//meta[@property="og:title"]')[0].text_content().strip()
        except:
            try:
                metadata.title = detailsPageElements.xpath('//meta[@name="twitter:title"]')[0].text_content().strip()
            except:
                pass

    # Summary
    summary = detailsPageElements.xpath('//div[@class="record-description-content record-box-content"]')[0].text_content().strip()
    metadata.summary = summary[:summary.find('Runtime')].strip()

    # Studio
    metadata.studio = 'Hegre'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//a[@class="tag"]'):
        genreName = genreLink.text_content().strip().lower()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[@class="record-model"]')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.get('title').strip()
            actorPhotoURL = actorLink.xpath('.//img/@src')[0].replace('240x', '480x')

            movieActors.addActor(actorName, actorPhotoURL)

    # Director
    director = metadata.directors.new()
    director.name = 'Petter Hegre'
    director.photo = 'https://img.discogs.com/TafxhnwJE2nhLodoB6UktY6m0xM=/fit-in/180x264/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-2236724-1305622884.jpeg.jpg'

    # Posters
    art = [
        detailsPageElements.xpath('//meta[@name="twitter:image"]/@content')[0].replace('board-image', 'poster-image').replace('1600x', '640x'),
        detailsPageElements.xpath('//meta[@name="twitter:image"]/@content')[0].replace('1600x', '1920x')
    ]

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
