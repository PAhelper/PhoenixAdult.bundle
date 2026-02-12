import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    cookies = {'18-plus-modal': 'hidden'}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}
    if searchData.date:
        url = PAsearchSites.getSearchSearchURL(siteNum) + 'date/' + searchData.date + '/' + searchData.date
        req = PAutils.HTTPRequest(url, cookies=cookies, headers=headers)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[contains(@class, "content-grid-item")]'):
            title = searchResult.xpath('.//span[@class="title"]/a')[0].text_content().split('-')
            if len(title) > 1:
                titleNoFormatting = '%s - %s' % (PAutils.parseTitle(title[0].strip(), siteNum), title[1])
            else:
                titleNoFormatting = PAutils.parseTitle(title[0].strip(), siteNum)

            curID = searchResult.xpath('.//span[@class="title"]/a/@href')[0].split('/')[3]
            releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower().rsplit('-')[0])

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    sceneID = searchData.title.split()[0]
    if unicode(sceneID, 'utf-8').isdigit():
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/video/watch/' + sceneID
        req = PAutils.HTTPRequest(sceneURL, cookies=cookies, headers=headers)
        detailsPageElements = HTML.ElementFromString(req.text)

        detailsPageElements = detailsPageElements.xpath('//div[contains(@class, "content-pane-title")]')[0]
        titleNoFormatting = detailsPageElements.xpath('//h2')[0].text_content()
        curID = sceneID
        releaseDate = parse(detailsPageElements.xpath('//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        score = 100

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    cookies = {'18-plus-modal': 'hidden'}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/video/watch/' + metadata_id[0]
    req = PAutils.HTTPRequest(sceneURL, cookies=cookies, headers=headers)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    title = detailsPageElements.xpath('//div[contains(@class, "content-pane-title")]//h2')[0].text_content().split('-')
    if len(title) > 1:
        metadata.title = '%s - %s' % (PAutils.parseTitle(title[0].strip(), siteNum), title[1])
    else:
        metadata.title = PAutils.parseTitle(title[0].strip(), siteNum)

    # Summary
    description = detailsPageElements.xpath('//div[@class="col-12 content-pane-column"]/div')
    if not description:
        description = ''
        for paragraph in detailsPageElements.xpath('//div[@class="col-12 content-pane-column"]//p'):
            description += '\n\n' + paragraph.text_content()
    else:
        description = description[0].text_content().split('Show More')[0]

    metadata.summary = description.strip()

    # Studio
    metadata.studio = 'Nubiles'

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    movieCollections.addCollection(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class, "content-pane")]//span[@class="date"]')[0].text_content().strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genreLink in detailsPageElements.xpath('//div[@class="categories"]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actor(s)
    for actorLink in detailsPageElements.xpath('//div[contains(@class, "content-pane-performer")]/a'):
        actorName = actorLink.text_content().strip()

        actorPageURL = PAsearchSites.getSearchBaseURL(siteNum) + actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL, cookies=cookies, headers=headers)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPage.xpath('//div[contains(@class, "model-profile")]//img/@src')[0]
        if not actorPhotoURL.startswith('http'):
            actorPhotoURL = 'http:%s' % actorPhotoURL

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
    xpaths = [
        '//video/@poster',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            if not poster.startswith('http'):
                poster = 'http:' + poster

            art.append(poster)

    try:
        try:
            galleryURL = PAsearchSites.getSearchBaseURL(siteNum) + detailsPageElements.xpath('//div[contains(@class, "content-pane-related-links")]/a[contains(., "Pic")]/@href')[0]
        except:
            match = re.search(r'(?<=videos\/).*(?=\/sample)', detailsPageElements.xpath('//video/@poster')[0])
            if match:
                sceneID = match.group(0)
            galleryURL = '%s/galleries/%s/screenshots' % (PAsearchSites.getSearchBaseURL(siteNum), sceneID)

        req = PAutils.HTTPRequest(galleryURL, cookies=cookies, headers=headers)
        photoPageElements = HTML.ElementFromString(req.text)
        for poster in photoPageElements.xpath('//div[@class="img-wrapper"]//picture/source[1]/@srcset'):
            if not poster.startswith('http'):
                poster = 'http:' + poster

            art.append(poster)
    except:
        pass

    images = []
    posterExists = False
    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
                im = StringIO(image.content)
                images.append(image)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                    posterExists = True
                if width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    if not posterExists:
        for idx, image in enumerate(images, 1):
            try:
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[art[idx - 1]] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
