import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//li[@class="featured-video morestdimage grid_4 mb"]'):
        detailsPage = searchResult.xpath('./a/@href')[0]
        titleNoFormatting = searchResult.xpath('./div[@class="details"]//h5')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('./div[@class="details"]/p/strong')[0].text_content().strip()).strftime('%Y-%m-%d')
        curID = PAutils.Encode(detailsPage)

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [GloryHoleSecrets] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h2[@class="H_underline"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="desc"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Aziani'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//p[@class="mb0"]')
    if date:
        date = date[0].text_content().strip()
        date_object = datetime.strptime(date[12:], '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    elif sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//h5[@class="video_categories"]//a'):
        genreName = genreLink.text_content().strip().lower()
        if 'cumshots' not in genreName:
            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="video_details mb mt0"]/h5[1]/a'):
        actorName = actorLink.text_content().strip()

        sceneImg = detailsPageElements.xpath('//meta[@property="og:image"]/@content')[0]
        actorFullName = sceneImg.split('/')[4]
        actorFirstName = actorName.split(' ')[0]
        if actorFirstName.lower() == actorFullName[:len(actorFirstName)].lower() and len(actorFullName) > len(actorName):
            actorLastName = actorFullName[len(actorFirstName):].capitalize()
            actorName = actorFirstName + " " + actorLastName

        actorPageURL = PAsearchSites.getSearchSearchURL(siteID) + '/tour/' + actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPage.xpath('//img[@class="thumbs"]/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="grid_10 alpha"]/a/img/@src',
        '//div[@class="grid_4"]//img/@src'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            art.append(PAsearchSites.getSearchBaseURL(siteID) + img)

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
