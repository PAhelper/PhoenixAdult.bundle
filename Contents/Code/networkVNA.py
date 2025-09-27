import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = searchData.title.split(' ', 1)[0]
    if unicode(sceneID, 'UTF-8').isdigit():
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    searchResults = []
    if sceneID:
        directURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneID
        searchResults.append(directURL)

    googleResults = PAutils.getFromSearchEngine(searchData.title, siteNum)
    for sceneURL in googleResults:
        if ('videos/' in sceneURL and '/page/' not in sceneURL) and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)
            titleNoFormatting = detailsPageElements.xpath('//h1[@class="customhcolor"]')[0].text_content()
            if 'http' not in sceneURL:
                sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneID
            curID = PAutils.Encode(sceneURL)

            releaseDate = ''
            date = detailsPageElements.xpath('//*[@class="date"]')[0].text_content().strip()
            if date:
                releaseDate = parse(date).strftime('%Y-%m-%d')

            if searchData.date and releaseDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s %s' % (PAsearchSites.getSearchSiteName(siteNum), titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneID = sceneURL.split('/')[-2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1[@class="customhcolor"]')[0].text_content().strip(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//*[@class="customhcolor2"]')[0].text_content().strip()

    if siteNum == 1287:
        metadata.summary = metadata.summary.split('Don\'t forget to join me')[0]

    # Studio
    metadata.studio = 'VNA Network'

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    movieCollections.addCollection(tagline)

    # Release Date
    date = detailsPageElements.xpath('//*[@class="date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    genres = detailsPageElements.xpath('//h4[@class="customhcolor"]')[0].text_content().strip()
    for genreLink in genres.split(','):
        genreName = genreLink.strip()

        movieGenres.addGenre(genreName)

    # Actor(s)
    actors = detailsPageElements.xpath('//h3[@class="customhcolor"]')[0].text_content().strip()

    # Fixing previous values to compensate for broken html tags
    if siteNum == 1288:
        metadata.summary = metadata.summary.replace(actors, '').strip()
        actors = actors.replace(genres, '')

    for actorLink in actors.replace('&nbsp', '').split(','):
        actorName = actorLink.strip()
        actorPhotoURL = ''

        if actorName.endswith(' XXX'):
            actorName = actorName[:-4]

        movieActors.addActor(actorName, actorPhotoURL)

    if siteNum == 1314:
        movieActors.addActor('Siri', '')

    # Manually Add Actors
    # Add Actor Based on Title
    for actor in PAutils.getDictValuesFromKey(actorsDB, sceneID):
        movieActors.addActor(actor[0], '', gender=actor[1])

    # Posters/Background
    xpaths = [
        '//center//img/@src',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if 'http' not in img:
                img = PAsearchSites.getSearchBaseURL(siteNum) + '/' + img

            art.append(img)

    # add thumbnails not found on scene page
    if art and 'thumb_1' in art[0]:
        art.extend([
            art[0].replace('thumb_1', 'thumb_2'),
            art[0].replace('thumb_1', 'thumb_3'),
        ])

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata


actorsDB = {
    '36260': [('Sarah Arabic', 'female')],
}
