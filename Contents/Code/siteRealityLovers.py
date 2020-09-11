import PAsearchSites
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    params = json.dumps({
        'sortBy': 'MOST_RELEVANT',
        'searchQuery': searchTitle,
        'videoView': 'MEDIUM'
    })
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum), params=params, headers={'Content-Type': 'application/json'})
    searchResults = req.json()
    for searchResult in searchResults['contents']:
        releaseDate = parse(searchResult['released']).strftime('%Y-%m-%d')
        curID = PAutils.Encode(searchResult['videoUri'])
        posterID = PAutils.Encode(searchResult['mainImageSrcset'].split(',')[1][:-3].replace('https', 'http'))
        siteName = PAsearchSites.getSearchSiteName(siteNum)
        titleNoFormatting = '%s [%s] %s' % (searchResult['title'], siteName, releaseDate)

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, posterID), name=titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + "/" + sceneURL
    posterUri = PAutils.Decode(metadata_id[2])
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="video-detail-name"]')[0].text_content().strip()

    # Summary
    rawSummary = detailsPageElements.xpath('//p[@itemprop="description"]')[0].text_content().replace('…', '').replace('Read more', '')
    metadata.summary = ' '.join(rawSummary.split())

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="videoClip__Details-infoValue"]')[0].text_content().strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genreLink in detailsPageElements.xpath('//span[@itemprop="keywords"]/a'):
        genreName = genreLink.text_content().strip().lower()
        movieGenres.addGenre(genreName)

    # Actors
    actors = detailsPageElements.xpath('//span[@itemprop="actors"]/a')
    for actorLink in detailsPageElements.xpath('//span[@itemprop="actors"]/a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        try:
            actorPageURL = actorLink.get('href')
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            actorPhotoLinks = actorPage.xpath('//img[@class="girlDetails-posterImage"]/@srcset')[0]
            actorPhotoURL = actorPhotoLinks.split(',')[1][:-3].replace('https', 'http')
        except:
            pass

        movieActors.addActor(actorName, actorPhotoURL)

    # Photos
    art = []

    for photo in detailsPageElements.xpath('//img[contains(@class, "videoClip__Details--galleryItem")]/data-big'):
        photoURLs = photo.split(',')
        photoURL = photoURLs[len(photoURLs) - 1][:-6].replace('https', 'http')

        art.append(photoURL)

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
