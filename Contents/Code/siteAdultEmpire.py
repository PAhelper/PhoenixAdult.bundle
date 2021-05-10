import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []
    siteResults = []
    temp = []
    directID = False
    count = 0
    scene_matched = False

    sceneID = None
    parts = searchData.title.split()
    if unicode(parts[0], 'UTF-8').isdigit():
        sceneID = parts[0]

        if int(sceneID) > 100:
            searchData.title = searchData.title.replace(sceneID, '', 1).strip()
            movieURL = '%s/%s' % (PAsearchSites.getSearchBaseURL(siteNum), sceneID)
            searchResults.append(movieURL)
            directID = True

    scene_break = re.search(r'.*(?=Scene\s\d)', searchData.title)
    if scene_break:
        scene_break = (scene_break.group().strip(), searchData.title[-1])
        searchData.title = scene_break[0]
        Log("scenebreak: %s %s" % (scene_break[0], scene_break[1]))

    searchData.encoded = searchData.title.replace(' ', '+')
    searchURL = '%s%s' % (PAsearchSites.getSearchSearchURL(siteNum), searchData.encoded)
    req = PAutils.HTTPRequest(searchURL, headers={'Referer': 'http://www.data18.empirestores.co'})
    searchPageElements = HTML.ElementFromString(req.text)
    if not directID:
        for searchResult in searchPageElements.xpath('//div[@class="product-card"]'):
            if scene_matched:
                break
            movieURL = '%s%s' % (PAsearchSites.getSearchBaseURL(siteNum), searchResult.xpath('./div[@class="boxcover-container"]/a/@href')[0].strip())
            urlID = searchResult.xpath('./div[@class="boxcover-container"]/a/@href')[0].split("/")[1]
            if movieURL not in searchResults:
                titleNoFormatting = PAutils.parseTitle(searchResult.xpath('./div[@class="product-details"]/div/a/text()')[0].strip(), siteNum)
                curID = PAutils.Encode(movieURL)
                siteResults.append(movieURL)

                if sceneID == urlID:
                    score = 100
                else:
                    score = 80 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                if score > 70:
                    sceneURL = PAutils.Decode(curID)
                    req = PAutils.HTTPRequest(sceneURL)
                    detailsPageElements = HTML.ElementFromString(req.text)

                    # Find date on movie specific page
                    date = detailsPageElements.xpath('//ul[@class="list-unstyled m-b-2"]/li[contains(., "Released:")]/text()')[0].strip()
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
                        studio = detailsPageElements.xpath('//ul[@class="list-unstyled m-b-2"]/li[contains(., "Studio:")]/a/text()')[0].strip()
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
                    scenes = detailsPageElements.xpath('//div[@class="product-details-container"]/div[@class="container"]/div[@class="row"]')
                    sceneCount = (len(scenes) - 1) / 2
                    for sceneNum in range(0, sceneCount):
                        section = 'Scene %d' % (sceneNum + 1)
                        actorNames = ', '.join(detailsPageElements.xpath('//div[@class="container"]/div[@class="row"][./div[@class="col-sm-6 text-right text-left-xs m-b-1"]][%d]/div[2]/div/a/text()' % (sceneNum + 1)))

                        if scene_break and titleNoFormatting == scene_break[0] and sceneNum + 1 == int(scene_break[1]):
                            scene_matched = True
                            results.Append(MetadataSearchResult(id='%s|%d|%s|%d' % (curID, siteNum, releaseDate, sceneNum + 1), name='%s/#%d[%s][%s] %s' % (titleNoFormatting, sceneNum + 1, actorNames, studio, displayDate), score=100, lang=lang))
                            break
                        elif score == 80:
                            count += 1
                            temp.append(MetadataSearchResult(id='%s|%d|%s|%d' % (curID, siteNum, releaseDate, sceneNum + 1), name='%s/#%d[%s][%s] %s' % (titleNoFormatting, sceneNum + 1, actorNames, studio, displayDate), score=score, lang=lang))
                        else:
                            results.Append(MetadataSearchResult(id='%s|%d|%s|%d' % (curID, siteNum, releaseDate, sceneNum + 1), name='%s/#%d[%s][%s] %s' % (titleNoFormatting, sceneNum + 1, actorNames, studio, displayDate), score=score, lang=lang))
                else:
                    if score == 80:
                        count += 1
                        temp.append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s' % (titleNoFormatting), score=score, lang=lang))
                    else:
                        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s' % (titleNoFormatting), score=score, lang=lang))

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for movieURL in googleResults:
        if ('/movies/' in movieURL and '.html' not in movieURL and movieURL not in searchResults and movieURL not in siteResults):
            searchResults.append(movieURL)

    for movieURL in searchResults:
        req = PAutils.HTTPRequest(movieURL)
        detailsPageElements = HTML.ElementFromString(req.text)
        urlID = re.sub(r'.*/', '', movieURL)
        titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//h1/text()')[0].strip(), siteNum)
        curID = PAutils.Encode(movieURL)

        date = detailsPageElements.xpath('//ul[@class="list-unstyled m-b-2"]/li[contains(., "Released:")]/text()')[0].strip()
        if date and not date == 'unknown':
            try:
                releaseDate = datetime.strptime(date, '%b %d %Y').strftime('%Y-%m-%d')
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
            studio = detailsPageElements.xpath('//ul[@class="list-unstyled m-b-2"]/li[contains(., "Studio:")]/a/text()')[0].strip()
        except:
            studio = ''

        if score == 80:
            count += 1
            temp.append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, studio, displayDate), score=score, lang=lang))
        else:
            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, studio, displayDate), score=score, lang=lang))

        # Split Scenes
        scenes = detailsPageElements.xpath('//div[@class="product-details-container"]/div[@class="container"]/div[@class="row"]')
        sceneCount = (len(scenes) - 1) / 2
        for sceneNum in range(0, sceneCount):
            actorNames = ', '.join(detailsPageElements.xpath('//div[@class="container"]/div[@class="row"][./div[@class="col-sm-6 text-right text-left-xs m-b-1"]][%d]/div[2]/div/a/text()' % (sceneNum + 1)))
            if score == 80:
                count += 1
                temp.append(MetadataSearchResult(id='%s|%d|%s|%d' % (curID, siteNum, releaseDate, sceneNum + 1), name='%s/#%d[%s][%s] %s' % (titleNoFormatting, sceneNum + 1, actorNames, studio, displayDate), score=score, lang=lang))
            else:
                results.Append(MetadataSearchResult(id='%s|%d|%s|%d' % (curID, siteNum, releaseDate, sceneNum + 1), name='%s/#%d[%s][%s] %s' % (titleNoFormatting, sceneNum + 1, actorNames, studio, displayDate), score=score, lang=lang))

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
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1/text()')[0], siteNum).strip()
    if splitScene:
        metadata.title = '%s [Scene %s]' % (metadata.title, metadata_id[3])

    # Summary
    summary = ''
    try:
        summary = '\n'.join([line.text_content().strip() for line in detailsPageElements.xpath('//div[@class="product-details-container"]/div[@class="row breakout bg-lightgrey"]//h4/p')])
    except:
        pass
    metadata.summary = summary

    # Studio
    try:
        studio = detailsPageElements.xpath('//ul[@class="list-unstyled m-b-2"]/li[contains(., "Studio:")]/a/text()')[0].strip()
    except:
        studio = ''

    if studio:
        metadata.studio = studio

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = ''
    try:
        tagline = re.sub(r'\(.*\)', '', detailsPageElements.xpath('//div[@class="container"]/h2/a[@label="Series"]/text()')[0].strip().split('"')[1]).strip()
        metadata.tagline = tagline
        metadata.collections.add(tagline)
    except:
        if splitScene:
            metadata.collections.add(PAutils.parseTitle(detailsPageElements.xpath('//h1/text()')[0], siteNum).strip())
        else:
            metadata.collections.add(studio)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="col-sm-4 m-b-2"]/ul/li//a[@label="Category"]'):
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()

    actors = []
    if splitScene:
        actorNames = detailsPageElements.xpath('//div[@class="container"]/div[@class="row"][./div[@class="col-sm-6 text-right text-left-xs m-b-1"]][%d]/div[2]/div/a' % int(metadata_id[3]))
        for name in actorNames:
            try:
                actors.append(name)
            except:
                pass
    else:
        actors = detailsPageElements.xpath('//div[@class="col-sm-4 m-b-2"]/ul/li/a[@label="Performers - detail"]')

    for actorLink in actors:
        actorName = actorLink.text_content().strip()
        actorPhotoURL = detailsPageElements.xpath('//div[@class="itempage"]/div/div[@class="row"]/div[@class="col-sm-3 col-md-4 col-lg-3 m-b-2"]/div/a[@label="Performer"][contains(., "%s")]//img/@src' % actorName)[0].strip()
        if actorName:
            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    cover = '//div[@class="boxcover-container"]/a/img/@src'
    splitscenes = ''
    if splitScene:
        splitscenes = '//div[@class="product-details-container"]/div[@class="container"]/div[@class="row"][./div[@class="col-sm-9 col-md-10"]][%d]/div[@class="col-sm-9 col-md-10"]/div/div/a/@href' % int(metadata_id[3])
    try:
        if splitScene:
            art = art + detailsPageElements.xpath(splitscenes)
        art.append(detailsPageElements.xpath(cover)[0])
    except:
        pass

    images = []
    posterExists = False
    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.data18.empirestores.co'})
                images.append(image)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                posterExists = True
                metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
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
