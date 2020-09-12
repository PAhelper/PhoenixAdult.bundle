import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    modelID = searchTitle.split(' ', 1)[0].lower()
    try:
        sceneTitle = searchTitle.split(' ', 1)[1]
    except:
        sceneTitle = ''

    req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum), 'HEAD', allow_redirects=False)
    cookies = {
        'start_session_galleria': req.cookies['start_session_galleria']
    }

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + modelID, cookies=cookies)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="movie-wrap-index img-polaroid left"]'):
        titleNoFormatting = searchResult.xpath('.//h1[@class="video-title-model"]')[0].text_content().strip()
        titleNoFormattingID = PAutils.Encode(titleNoFormatting)

        description = searchResult.xpath('.//div[@class="col-lg-7"]')[0].text_content().split('Description:')[1].strip()
        descriptionID = PAutils.Encode(description)

        poster = searchResult.xpath('.//img[@class="img-responsive"]/@src')[0]
        posterID = PAutils.Encode(poster)

        actor = searchResult.xpath('//h1[@class="page-title col-lg-12"]')[0].text_content().strip()
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        curID = PAutils.Encode(searchResult.xpath('.//a[@class="thumbnail left"]/@href')[0])

        score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s|%s|%s|%s|%s' % (curID, siteNum, titleNoFormattingID, descriptionID, releaseDate, actor, posterID), name='%s [ATKGirlfriends]' % titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    sceneTitle = PAutils.Decode(metadata_id[2])
    sceneDescription = PAutils.Decode(metadata_id[3])
    sceneDate = metadata_id[4]
    sceneActor = metadata_id[5]
    scenePoster = PAutils.Decode(metadata_id[6])

    # Title
    metadata.title = sceneTitle

    # Summary
    metadata.summary = sceneDescription

    # Studio
    metadata.studio = 'ATK'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date_object = parse(sceneDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()

    actorName = sceneActor
    actorPhotoURL = ''

    movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Girlfriend Experience')
    # If scenePage is valid, try to load it to scrape genres
    try:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        genreText = detailsPageElements.xpath('//div[@class="movie-wrap img-polaroid"]')[0].text_content().split('Tags :')[1].strip()
        for genreLink in genreText.split(','):
            genreName = genreLink.strip()

            movieGenres.addGenre(genreName)
    except:
        pass

    # Posters
    art = []
    scenePoster = scenePoster.replace('sm_', '').split('1.jpg')[0]
    for photoNum in range(1, 8):
        photo = scenePoster + str(photoNum) + '.jpg'

        art.append(photo)

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
