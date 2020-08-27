import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    sceneID = searchTitle.split(' ', 1)[0]
    if unicode(sceneID, 'UTF-8').isdigit():
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    if sceneID and not searchTitle:
        sceneURL = '%s/Scenes/Videos/%s' % (PAsearchSites.getSearchBaseURL(siteNum), sceneID)
        req = PAutils.HTTPRequest(sceneURL)
        searchResults = HTML.ElementFromString(req.text)

        titleNoFormatting = searchResults.xpath('//div[@class="col-xs-12 video-title"]//h3')[0].text_content().strip()
        curID = PAutils.Encode(sceneURL)
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        score = 100

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))
    else:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@class="memVid"]'):
            titleNoFormatting = searchResult.xpath('.//div[@class="memVidTitle"]//a/@title')[0]
            curID = PAutils.Encode(searchResult.xpath('.//div[@class="memVidTitle"]//a/@href')[0])
            releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="col-xs-12 video-title"]//h3')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="col-sm-6 col-md-6 vidpage-info"]/text()')[4].strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="videopage-tags"]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="col-xs-6 col-sm-4 col-md-3"]'):
        actorName = actorLink.xpath('.//div[@class="vidpage-mobilePad"]//a//strong/text()')[0].strip()
        actorPhotoURL = ''

        try:
            actorPhotoURL = actorLink.xpath('.//img[@class="img-responsive imgHover"]/@src')[0]
        except:
            pass

        movieActors.addActor(actorName, actorPhotoURL)

    # Photos
    art = []
    try:
        posterURL = detailsPageElements.xpath('//div[@class="col-xs-12 col-sm-6 col-md-6 vidCover"]//img/@src')[0]
        art.append(posterURL)
    except:
        pass

    for photo in detailsPageElements.xpath('//div[@class="vid-flex-container"]//span'):
        photoLink = photo.xpath('.//img/@src')[0].replace('_thumb', '')
        art.append(photoLink)

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
