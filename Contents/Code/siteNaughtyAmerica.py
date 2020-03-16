import PAsearchSites
import PAgenres


def getAlgolia(url, indexName, params):
    params = json.dumps({'requests':[{'indexName':indexName,'params':params}]})
    req = urllib.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    data = urllib.urlopen(req, params).read()

    return json.loads(data)['results'][0]['hits']


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    sceneID = searchTitle.split(' ', 1)[0]
    if unicode(sceneID, 'utf8').isdigit():
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    url = PAsearchSites.getSearchSearchURL(siteNum) + '?x-algolia-application-id=I6P9Q9R18E&x-algolia-api-key=08396b1791d619478a55687b4deb48b4'
    if sceneID and not searchTitle:
        searchResults = getAlgolia(url, 'nacms_scenes_production', 'filters=id=' + sceneID)
    else:
        searchResults = getAlgolia(url, 'nacms_scenes_production', 'query=' + searchTitle)

    for searchResult in searchResults:
        titleNoFormatting = searchResult['title']
        curID = searchResult['id']
        releaseDate = datetime.fromtimestamp(searchResult['published_at']).strftime('%Y-%m-%d')
        siteName = searchResult['site']

        if sceneID:
            score = 100 - Util.LevenshteinDistance(sceneID, curID)
        elif searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%d|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, siteName, releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneID = metadata_id[0]

    url = PAsearchSites.getSearchSearchURL(siteID) + '?x-algolia-application-id=I6P9Q9R18E&x-algolia-api-key=08396b1791d619478a55687b4deb48b4'
    detailsPageElements = getAlgolia(url, 'nacms_scenes_production', 'filters=id=' + sceneID)[0]

    # Studio
    metadata.studio = 'Naughty America'

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = detailsPageElements['synopsis']

    # Release Date
    date_object = datetime.fromtimestamp(detailsPageElements['published_at'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)
    metadata.collections.add(detailsPageElements['site'])

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements['fantasies']:
        if genreLink and 'name' in genreLink:
            genreName = genreLink['name']

            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements['performers']:
        if actorLink and 'name' in actorLink:
            actorName = actorLink['name']
            actorPhotoURL = ''

            actorsPageElements = HTML.ElementFromURL('https://www.naughtyamerica.com/pornstar/' + actorLink['slug'])
            img = actorsPageElements.xpath('//img[@class="performer-pic"]/@src')
            if img:
                actorPhotoURL = 'https:' + img[0]

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    scenePageElements = HTML.ElementFromURL('https://www.naughtyamerica.com/scene/0' + sceneID)
    for photo in scenePageElements.xpath('//div[contains(@class, "contain-scene-images") and contains(@class, "desktop-only")]/a/@href'):
        img = 'https:' + re.sub(r'images\d+', 'images1', photo, 1, flags=re.IGNORECASE)
        art.append(img)

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
