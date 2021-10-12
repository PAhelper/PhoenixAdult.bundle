import PAsearchSites
import PAutils


def getJSONfromPage(url):
    req = PAutils.HTTPRequest(url)
    detailsPageElements = HTML.ElementFromString(req.text)

    if req.ok:
        data = None
        node = detailsPageElements.xpath('//script[contains(., "window.__DATA__")]')
        if node:
            data = node[0].text_content().split('=', 1)[1].strip()

        if data:
            return json.loads(data)['data']

    return None


def search(results, lang, siteNum, searchData):
    sceneID = None
    parts = searchData.title.split()
    if unicode(parts[0], 'UTF-8').isdigit():
        sceneID = int(parts[0])

        if sceneID > 100:
            searchData.title = searchData.title.replace(str(sceneID), '', 1).strip()

    searchData.encoded = searchData.title.replace(' ', '%20')
    searchResults = getJSONfromPage(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)['videos']

    if 'items' in searchResults:
        for searchResult in searchResults['items']:
            titleNoFormatting = searchResult['title']
            resultID = searchResult['id']

            sceneURLTitle = re.sub(r'(?:\W)+$', '', titleNoFormatting.lower())
            sceneURLTitle = re.sub(r'^(?:\W)+', '', titleNoFormatting.lower())
            sceneURLTitle = re.sub(r'\W+', '-', sceneURLTitle)
            sceneURL = '%s/scenes/%s/%s' % (PAsearchSites.getSearchBaseURL(siteNum), resultID, sceneURLTitle)
            curID = PAutils.Encode(sceneURL)

            date = searchResult['release_date']
            if date:
                releaseDate = parse(date).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''
            displayDate = releaseDate if date else ''

            if resultID == sceneID:
                score = 100
            elif searchData.date and displayDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [TWM/%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    basePageElements = getJSONfromPage(sceneURL)
    detailsPageElements = basePageElements['video']

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = PAutils.cleanHTML(detailsPageElements['description'])

    # Studio
    metadata.studio = 'Top Web Models'

    # Tagline and Collection(s)
    metadata.collections.clear()
    if 'sites' in detailsPageElements:
        tagline = re.sub(r"(\w)([A-Z])", r"\1 \2", json.loads(json.dumps(detailsPageElements['sites'][0]))['name'])
    else:
        tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Date
    date = detailsPageElements['release_date']
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements['tags']:
        genreName = genreLink['name']

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements['models']:
        actorName = actorLink['name']
        actorPhotoURL = actorLink['thumb']

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [
        detailsPageElements['thumb'],
        basePageElements['file_poster'],
    ]

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
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
