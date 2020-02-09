import PAsearchSites
import PAgenres
import PAactors
import re


def getAPIKey(url):
    req = urllib.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    data = urllib.urlopen(req).read()

    return re.search(r'\"apiKey\":\"(.*?)\"', data).group(1)


def getAlgolia(url, params, referer):
    params = json.dumps({'params':params})
    req = urllib.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Referer', referer)
    data = urllib.urlopen(req, params).read()

    return json.loads(data)


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    sceneID = searchTitle.split(' ', 1)[0]
    if unicode(sceneID, 'utf8').isdigit():
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    apiKEY = getAPIKey(PAsearchSites.getSearchBaseURL(siteNum))
    for sceneType in ['scenes', 'movies']:
        url = PAsearchSites.getSearchSearchURL(siteNum).replace('*', 'girlfriendsfilms_' + sceneType, 1) + '?x-algolia-application-id=TSMKFA364Q&x-algolia-api-key=' + apiKEY
        data = getAlgolia(url, 'query=' + searchTitle, PAsearchSites.getSearchBaseURL(siteNum))

        searchResults = data['hits']
        for searchResult in searchResults:
            if sceneType == 'scenes':
                releaseDate = parse(searchResult['release_date'])

                actors = []
                for actorLink in searchResult['female_actors']:
                    actors.append(actorLink['name'])
                sceneData = ', '.join(actors)
                curID = searchResult['clip_id']
                titleNoFormatting = '%s %s' % (searchResult['title'], sceneData)
            else:
                date = 'last_modified' if searchResult['last_modified'] else 'date_created'
                releaseDate = parse(searchResult[date])
                curID = searchResult['movie_id']
                titleNoFormatting = searchResult['title']

            description = searchResult['description']
            if description.startswith('Previously released on'):
                date = description.replace('Previously released on', '', 1).replace('th', '', 1).strip()
                releaseDate = parse(date)

            if searchDate:
                date = parse(searchDate)
                if date.year < releaseDate.year:
                    releaseDate = date

            releaseDate = releaseDate.strftime('%Y-%m-%d')

            if sceneID:
                score = 100 - Util.LevenshteinDistance(sceneID, curID)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%d|%d|%s|%s' % (curID, siteNum, sceneType, releaseDate), name='[%s] %s %s' % (sceneType.capitalize(), titleNoFormatting, releaseDate), score=score, lang=lang))

    searchResults = HTML.ElementFromURL('https://www.girlfriendsfilms.net/Search?media=2&q=' + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="grid-item"]'):
        titleNoFormatting = searchResult.xpath('.//span[@class="overlay-inner"]//text()')[0]
        sceneURL = 'https://www.girlfriendsfilms.net' + searchResult.xpath('.//a/@href')[0]
        curID = sceneURL.replace('/', '_').replace('?', '!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[DVD] %s' % (titleNoFormatting), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneType = metadata_id[2] if len(metadata_id) > 2 else None

    if sceneType:
        sceneID = int(metadata_id[0])
        sceneIDName = 'clip_id' if sceneType == 'scenes' else 'movie_id'
        sceneDate = metadata_id[3]
        apiKEY = getAPIKey(PAsearchSites.getSearchBaseURL(siteID))
        urlParams = '?x-algolia-application-id=TSMKFA364Q&x-algolia-api-key=' + apiKEY

        url = PAsearchSites.getSearchSearchURL(siteID).replace('*', 'girlfriendsfilms_' + sceneType, 1) + urlParams
        data = getAlgolia(url, 'filters=%s=%d' % (sceneIDName, sceneID), PAsearchSites.getSearchBaseURL(siteID))
        detailsPageElements = data['hits'][0]

        url = PAsearchSites.getSearchSearchURL(siteID).replace('*', 'girlfriendsfilms_scenes', 1) + urlParams
        data = getAlgolia(url, 'query=%s' % detailsPageElements['url_title'], PAsearchSites.getSearchBaseURL(siteID))['hits']
        data = sorted(data, key=lambda i: i['clip_id'])
        scenesPagesElements = enumerate(data, 1)

        # Studio
        metadata.studio = detailsPageElements['studio_name']

        # Title
        if sceneType == 'scenes':
            for idx, scene in scenesPagesElements:
                if scene['clip_id'] == sceneID:
                    metadata.title = '%s, Scene %d' % (detailsPageElements['title'], idx)
        if not metadata.title:
            metadata.title = detailsPageElements['title']

        # Summary
        description = detailsPageElements['description']
        if not description.startswith('Previously released on'):
            metadata.summary = description

        # Release Date
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

        # Tagline and Collection(s)
        metadata.collections.clear()
        for collectionName in ['network_name', 'serie_name', 'movie_title']:
            if collectionName in detailsPageElements:
                metadata.collections.add(detailsPageElements[collectionName])

        # Genres
        movieGenres.clearGenres()
        genres = detailsPageElements['categories']
        for genreLink in genres:
            genreName = genreLink['name']
            movieGenres.addGenre(genreName)

        # Actors
        movieActors.clearActors()
        actors = detailsPageElements['actors']
        for actorLink in actors:
            actorName = actorLink['name']

            url = PAsearchSites.getSearchSearchURL(siteID).replace('*', 'girlfriendsfilms_actors', 1) + urlParams
            data = getAlgolia(url, 'filters=actor_id=' + actorLink['actor_id'], PAsearchSites.getSearchBaseURL(siteID))
            actorData = data['hits'][0]
            if actorData['pictures']:
                max_quality = sorted(actorData['pictures'].keys())[-1]
                actorPhotoURL = 'https://images-fame.gammacdn.com/actors' + actorData['pictures'][max_quality]
            else:
                actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

        # Posters
        art = [
            'https://images-fame.gammacdn.com/movies/{0}/{0}_{1}_front_400x625.jpg'.format(detailsPageElements['movie_id'], detailsPageElements['url_title'].lower().replace('-', '_'))
        ]

        if 'pictures' in detailsPageElements:
            max_quality = sorted(detailsPageElements['pictures'].keys())[-3]
            art.append('https://images-fame.gammacdn.com/movies/' + detailsPageElements['pictures'][max_quality])
        else:
            for idx, scene in scenesPagesElements:
                max_quality = sorted(scene['pictures'].keys())[-3]
                art.append('https://images-fame.gammacdn.com/movies/' + scene['pictures'][max_quality])
    else:
        sceneURL = metadata_id[0].replace('_', '/').replace('!', '?')
        data = urllib.urlopen(sceneURL).read()
        detailsPageElements = HTML.ElementFromString(data)

        # Studio
        metadata.studio = detailsPageElements.xpath('//div[@class="studio"]//a/text()')[0]

        # Title
        metadata.title = detailsPageElements.xpath('//h1[@class="description"]/text()')[0]

        # Summary
        metadata.summary = detailsPageElements.xpath('//div[@class="synopsis"]')[0].text_content().strip()

        # Release Date
        date = detailsPageElements.xpath('//div[@class="release-date"]/text()')[0].strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

        # Tagline and Collection(s)
        metadata.collections.clear()
        metadata.collections.add(metadata.studio)

        # Genres
        movieGenres.clearGenres()
        genres = detailsPageElements.xpath('//div[@class="categories"]//a')
        for genreLink in genres:
            genreName = genreLink.xpath('./text()')[0]
            movieGenres.addGenre(genreName)

        # Actors
        movieActors.clearActors()
        actors = detailsPageElements.xpath('//div[@class="video-performer"]//img')
        for actorLink in actors:
            actorName = actorLink.xpath('./@title')[0]
            actorPhotoURL = actorLink.xpath('./@data-bgsrc')[0]
            if 'image-not-available-performer-female' in actorPhotoURL:
                actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

        # Posters
        art = [
            detailsPageElements.xpath('//picture//img/@src')[-1]
        ]

        images = re.findall(r'img = \"(.*?)\";', data)
        for image in images:
            if image not in art:
                art.append(image)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
