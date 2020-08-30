import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    if searchDate:
        url = PAsearchSites.getSearchSearchURL(siteNum) + 'date/' + searchDate + '/' + searchDate
        req = PAutils.HTTPRequest(url)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[contains(@class, "content-grid-item")]'):
            titleNoFormatting = searchResult.xpath('//span[@class= "title"]/a')[0].text_content().strip()
            curID = searchResult.xpath('//span[@class="title"]/a/@href')[0].split('/')[3]
            releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    sceneID = searchTitle.split(' ')[0]
    if unicode(sceneID, 'utf-8').isdigit():
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/video/watch/' + sceneID
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        detailsPageElements = detailsPageElements.xpath('//div[contains(@class, "content-pane-title")]')[0]
        titleNoFormatting = detailsPageElements.xpath('//h2')[0].text_content()
        curID = sceneID
        releaseDate = parse(detailsPageElements.xpath('//span[@class= "date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        score = 100

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAsearchSites.getSearchBaseURL(siteID) + '/video/watch/' + metadata_id[0]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "content-pane-title")]//h2')[0].text_content().strip()

    # Summary
    description = detailsPageElements.xpath('//div[@class="col-12 content-pane-column"]/div')
    if not description:
        description = ''
        for paragraph in detailsPageElements.xpath('//div[@class="col-12 content-pane-column"]//p'):
            description += '\n\n' + paragraph.text_content()
    else:
        description = description[0].text_content()

    metadata.summary = description.strip()

    # Studio
    metadata.studio = 'Nubiles'

    # Collections / Tagline
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class, "content-pane")]//span[@class="date"]')[0].text_content().strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="categories"]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[contains(@class, "content-pane-performer")]/a'):
        actorName = actorLink.text_content().strip()

        actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = 'http:' + actorPage.xpath('//div[contains(@class, "model-profile")]//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    if 'Logan Long' in metadata.summary:
        movieActors.addActor('Logan Long', '')
    elif 'Patrick Delphia' in metadata.summary:
        movieActors.addActor('Patrick Delphia', '')
    elif 'Seth Gamble' in metadata.summary:
        movieActors.addActor('Seth Gamble', '')
    elif 'Alex D.' in metadata.summary:
        movieActors.addActor('Alex D.', '')
    elif 'Lucas Frost' in metadata.summary:
        movieActors.addActor('Lucas Frost', '')
    elif 'Van Wylde' in metadata.summary:
        movieActors.addActor('Van Wylde', '')
    elif 'Tyler Nixon' in metadata.summary:
        movieActors.addActor('Tyler Nixon', '')
    elif 'Logan Pierce' in metadata.summary:
        movieActors.addActor('Logan Pierce', '')
    elif 'Johnny Castle' in metadata.summary:
        movieActors.addActor('Johnny Castle', '')
    elif 'Damon Dice' in metadata.summary:
        movieActors.addActor('Damon Dice', '')
    elif 'Scott Carousel' in metadata.summary:
        movieActors.addActor('Scott Carousel', '')
    elif 'Dylan Snow' in metadata.summary:
        movieActors.addActor('Dylan Snow', '')
    elif 'Michael Vegas' in metadata.summary:
        movieActors.addActor('Michael Vegas', '')
    elif 'Xander Corvus' in metadata.summary:
        movieActors.addActor('Xander Corvus', '')
    elif 'Chad White' in metadata.summary:
        movieActors.addActor('Chad White', '')

    # Posters
    art = []
    xpaths = [
        '//video/@poster'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            if not poster.startswith('http'):
                poster = 'http:' + poster

            art.append(poster)

    galleryURL = 'https://nubiles-porn.com/photo/gallery/' + metadata_id[0]
    req = PAutils.HTTPRequest(galleryURL)
    photoPageElements = HTML.ElementFromString(req.text)
    for poster in photoPageElements.xpath('//div[@class="img-wrapper"]//source[1]/@src'):
        if not poster.startswith('http'):
            poster = 'http:' + poster

        art.append(poster)

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
