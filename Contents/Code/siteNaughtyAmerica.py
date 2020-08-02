import PAsearchSites
import PAgenres
import PAutils


def getAlgolia(url, indexName, params):
    params = json.dumps({'requests': [{'indexName': indexName, 'params': params + '&hitsPerPage=100'}]})
    headers = {
        'Content-Type': 'application/json'
    }
    data = PAutils.HTTPRequest(url, headers=headers, params=params).json()

    return data['results'][0]['hits']


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    sceneID = searchTitle.split(' ', 1)[0]
    if unicode(sceneID, 'UTF-8').isdigit():
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


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneID = metadata_id[0]

    url = PAsearchSites.getSearchSearchURL(siteID) + '?x-algolia-application-id=I6P9Q9R18E&x-algolia-api-key=08396b1791d619478a55687b4deb48b4'
    detailsPageElements = getAlgolia(url, 'nacms_scenes_production', 'filters=id=' + sceneID)[0]

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = detailsPageElements['synopsis']

    # Studio
    metadata.studio = 'Naughty America'

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)
    metadata.collections.add(detailsPageElements['site'])

    # Release Date
    date_object = datetime.fromtimestamp(detailsPageElements['published_at'])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements['fantasies']:
        genreName = genreLink

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements['performers']:
        actorName = actorLink
        actorPhotoURL = ''

        actorsPageURL = 'https://www.naughtyamerica.com/pornstar/' + actorName.lower().replace(' ', '-').replace("'", '')
        req = PAutils.HTTPRequest(actorsPageURL)
        actorsPageElements = HTML.ElementFromString(req.text)
        img = actorsPageElements.xpath('//img[@class="performer-pic"]/@src')
        if img:
            actorPhotoURL = 'https:' + img[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    req = PAutils.HTTPRequest('https://www.naughtyamerica.com/scene/0' + sceneID)
    scenePageElements = HTML.ElementFromString(req.text)
    for photo in scenePageElements.xpath('//div[contains(@class, "contain-scene-images") and contains(@class, "desktop-only")]/a/@href'):
        img = 'https:' + re.sub(r'images\d+', 'images1', photo, 1, flags=re.IGNORECASE)
        art.append(img)

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
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
