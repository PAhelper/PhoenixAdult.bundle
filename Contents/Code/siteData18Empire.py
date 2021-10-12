import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []
    siteResults = []
    temp = []
    directID = False
    count = 0

    sceneID = None
    parts = searchData.title.split()
    if unicode(parts[0], 'UTF-8').isdigit():
        sceneID = parts[0]

        if int(sceneID) > 100:
            searchData.title = searchData.title.replace(sceneID, '', 1).strip()
            movieURL = '%s/%s' % (PAsearchSites.getSearchBaseURL(siteNum), sceneID)
            searchResults.append(movieURL)
            directID = True

    searchData.encoded = searchData.title.replace(' ', '+')
    searchURL = '%s%s' % (PAsearchSites.getSearchSearchURL(siteNum), searchData.encoded)
    req = PAutils.HTTPRequest(searchURL, headers={'Referer': 'http://www.data18.empirestores.co'})
    searchPageElements = HTML.ElementFromString(req.text)
    if not directID:
        for searchResult in searchPageElements.xpath('//a[@class="boxcover"]'):
            movieURL = '%s%s' % (PAsearchSites.getSearchBaseURL(siteNum), searchResult.xpath('./@href')[0])
            urlID = searchResult.xpath('./@href')[0].split('/')[1]
            if movieURL not in searchResults:
                titleNoFormatting = PAutils.parseTitle(searchResult.xpath('./span/span/text()')[0].strip(), siteNum)
                curID = PAutils.Encode(movieURL)
                siteResults.append(movieURL)

                if sceneID == urlID:
                    score = 100
                elif searchData.date and displayDate:
                    score = 80 - Util.LevenshteinDistance(searchData.date, releaseDate)
                else:
                    score = 80 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                if score > 70:
                    sceneURL = PAutils.Decode(curID)
                    req = PAutils.HTTPRequest(sceneURL)
                    detailsPageElements = HTML.ElementFromString(req.text)

                    # Find date on movie specific page
                    date = detailsPageElements.xpath('//div[@class="release-date" and ./span[contains(., "Released:")]]/text()')[0].strip()
                    if date and not date == 'unknown':
                        try:
                            releaseDate = datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')
                        except:
                            releaseDate = ''
                    else:
                        releaseDate = searchData.dateFormat() if searchData.date else ''
                    displayDate = releaseDate if date else ''

                    # Studio
                    try:
                        studio = detailsPageElements.xpath('//div[@class="studio"]/a/text()')[0].strip()
                    except:
                        studio = ''
                    if sceneID == urlID:
                        score = 100
                    elif searchData.date and displayDate:
                        score = 80 - Util.LevenshteinDistance(searchData.date, releaseDate)
                    else:
                        score = 80 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                    if score == 80:
                        count += 1
                        temp.append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, studio, displayDate), score=score, lang=lang))
                    else:
                        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, studio, displayDate), score=score, lang=lang))

                    # Split Scenes
                    scenes = detailsPageElements.xpath('//div[@class="item-grid item-grid-scene"]/div/a/@href')
                    sceneCount = len(scenes)
                    for sceneNum in range(0, sceneCount):
                        section = 'Scene %d' % (sceneNum + 1)
                        if score == 80:
                            count += 1
                            temp.append(MetadataSearchResult(id='%s|%d|%s|%d' % (curID, siteNum, releaseDate, sceneNum), name='%s [%s][%s] %s' % (titleNoFormatting, section, studio, displayDate), score=score, lang=lang))
                        else:
                            results.Append(MetadataSearchResult(id='%s|%d|%s|%d' % (curID, siteNum, releaseDate, sceneNum), name='%s [%s][%s] %s' % (titleNoFormatting, section, studio, displayDate), score=score, lang=lang))
                else:
                    if score == 80:
                        count += 1
                        temp.append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s %s' % (titleNoFormatting, displayDate), score=score, lang=lang))
                    else:
                        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s %s' % (titleNoFormatting, displayDate), score=score, lang=lang))

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for movieURL in googleResults:
        if ('/movies/' in movieURL and '.html' not in movieURL and movieURL not in searchResults and movieURL not in siteResults):
            searchResults.append(movieURL)

    for movieURL in searchResults:
        req = PAutils.HTTPRequest(movieURL)
        detailsPageElements = HTML.ElementFromString(req.text)
        urlID = re.sub(r'.*/', '', movieURL)
        titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//h1[@class="description"]/text()')[0].strip(), siteNum)
        curID = PAutils.Encode(movieURL)

        date = detailsPageElements.xpath('//div[@class="release-date" and ./span[contains(., "Released:")]]/text()')[0].strip()
        if date and not date == 'unknown':
            try:
                releaseDate = datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')
            except:
                releaseDate = ''
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        displayDate = releaseDate if date else ''

        if sceneID == urlID:
            score = 100
        elif searchData.date and displayDate:
            score = 80 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 80 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        # Studio
        try:
            studio = detailsPageElements.xpath('//div[@class="studio"]/a/text()')[0].strip()
        except:
            studio = ''

        if score == 80:
            count += 1
            temp.append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, studio, displayDate), score=score, lang=lang))
        else:
            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, studio, displayDate), score=score, lang=lang))

        # Split Scenes
        scenes = detailsPageElements.xpath('//div[@class="item-grid item-grid-scene"]/div/a/@href')
        sceneCount = len(scenes)
        for sceneNum in range(1, sceneCount + 1):
            section = 'Scene %d' % (sceneNum)
            if score == 80:
                count += 1
                temp.append(MetadataSearchResult(id='%s|%d|%s|%d' % (curID, siteNum, releaseDate, sceneNum), name='%s [%s][%s] %s' % (titleNoFormatting, section, studio, displayDate), score=score, lang=lang))
            else:
                results.Append(MetadataSearchResult(id='%s|%d|%s|%d' % (curID, siteNum, releaseDate, sceneNum), name='%s [%s][%s] %s' % (titleNoFormatting, section, studio, displayDate), score=score, lang=lang))

    for result in temp:
        if count > 1 and result.score == 80:
            results.Append(MetadataSearchResult(id=result.id, name=result.name, score=79, lang=lang))
        else:
            results.Append(MetadataSearchResult(id=result.id, name=result.name, score=result.score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    splitScene = False
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    if len(metadata_id) > 3:
        Log('Split Scene: %d' % int(metadata_id[3]))
        splitScene = True

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1[@class="description"]/text()')[0], siteNum).strip()
    if splitScene:
        metadata.title = '%s [Scene %s]' % (metadata.title, metadata_id[3])

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="synopsis"]')[0].text_content().strip()

    # Studio
    try:
        studio = detailsPageElements.xpath('//div[@class="studio"]/a/text()')[0].strip()
    except:
        studio = ''

    if studio:
        metadata.studio = studio

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = ''
    try:
        tagline = detailsPageElements.xpath('//p[contains(text(), "A scene from")]/a/text()')[0].strip()
        metadata.collections.add(tagline)
    except:
        try:
            tagline = detailsPageElements.xpath('//a[@data-label="Series List"]/h2/text()')[0].strip().replace('Series:', '').replace('(%s)' % studio, '').strip()
            metadata.collections.add(tagline)
        except:
            metadata.collections.add(metadata.studio)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="categories"]/a'):
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()

    actors = []
    if splitScene:
        actorNames = detailsPageElements.xpath('//div[@class="item-grid item-grid-scene"]/div[@class="grid-item"][%d]/div/div[@class="scene-cast-list"]/a/text()' % int(metadata_id[3]))
        for name in actorNames:
            actors.append(detailsPageElements.xpath('//div[@class="video-performer"]/a[./img[@title="%s"]]/span/span' % (name))[0])
    else:
        actors = detailsPageElements.xpath('//div[@class="video-performer"]/a/span/span')

    for actorLink in actors:
        actorName = actorLink.text_content().strip()
        actorPhotoURL = detailsPageElements.xpath('//div[@class="video-performer"]/a/img[@title="%s"]/@data-bgsrc' % (actorName))[0].strip()
        if actorName:
            movieActors.addActor(actorName, actorPhotoURL)

    # Director
    metadata.directors.clear()
    director = metadata.directors.new()
    try:
        directorName = detailsPageElements.xpath('//div[@class="director"]/a/text()')[0].text_content().split(':')[2].strip()
        if not directorName == 'Unknown':
            director.name = directorName
    except:
        pass

    # Posters
    art = []
    cover = '//div[@id="video-container-details"]/div/section/a/picture/source[1]/@data-srcset'
    scene = '//div[@class="item-grid item-grid-scene"]/div/a/img/@src'
    gallery = '//div[@id="video-container-details"]/div/section/div[2]/div[2]/a[@data-label="Gallery"]/@href'
    gallery_image = '//div[@class="item-grid item-grid-gallery"]/div[@class="grid-item"]/a/img/@data-src'
    try:
        art.append(detailsPageElements.xpath(cover)[0])
        gallery = detailsPageElements.xpath(gallery)
        if gallery:
            req = PAutils.HTTPRequest('%s%s' % (PAsearchSites.getSearchBaseURL(siteNum), gallery[0]))
            galleryPageElement = HTML.ElementFromString(req.text)
            art = art + galleryPageElement.xpath(gallery_image)
        if splitScene:
            art.append(detailsPageElements.xpath(scene)[int(metadata_id[3])])
    except:
        pass

    images = []
    posterExists = False
    Log('Artwork found: %d' % len(art))
    numPosters = 20
    numArt = 5
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                if random.randint(0, 1) == 0 and idx != 0:
                    continue
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.data18.empirestores.co'})
                images.append(image)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if height > width:
                    # Item is a poster
                    if numPosters != 0:
                        numPosters = numPosters - 1
                    else:
                        continue
                    posterExists = True
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > height:
                    # Item is an art item
                    if numArt != 0:
                        numArt = numArt - 1
                    else:
                        continue
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
