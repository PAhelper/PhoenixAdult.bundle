import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = None
    parts = searchData.title.split()
    searchResults = []

    if unicode(parts[0], 'UTF-8').isdigit():
        sceneID = parts[0]
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
        directURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneID + '.html'

        searchResults.append(directURL)

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if ('/update/' in sceneURL) and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if req.text:
            detailsPageElements = HTML.ElementFromString(req.text)

            curID = PAutils.Encode(sceneURL)
            titleDate = detailsPageElements.xpath('//title')[0].text_content().split('Released')
            titleNoFormatting = titleDate[0].strip()

            date = titleDate[-1].replace('!', '').strip()
            releaseDate = parse(date).strftime('%Y-%m-%d')

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneID = 0

    regex = re.search(r'-([0-9]{1,})\.', sceneURL)
    if regex:
        sceneID = int(regex.group(1))

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    titleDate = detailsPageElements.xpath('//title')[0].text_content().split('Released')
    metadata.title = titleDate[0].strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@id="Bio"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'First Time Videos'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = titleDate[-1].replace('!', '').strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = []
    if tagline == 'FTVGirls':
        genres = ['Teen', 'Solo', 'Public']
    elif tagline == 'FTVMilfs':
        genres = ['MILF', 'Solo', 'Public']

    for genreName in genres:
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = []

    for idx, actorLink in enumerate(detailsPageElements.xpath('//div[@id="ModelDescription"]//h1')):
        actorName = actorLink.text_content().replace('\'s Statistics', '').strip()
        actors.append(actorName)

        regex = re.search(r'\s(%s [A-Z]\w{1,})\s' % actorName, metadata.summary)
        if regex:
            actorName = regex.group(1)

        actorPhotoURL = detailsPageElements.xpath('//div[@id="Thumbs"]/img/@src')[idx]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//img[@id="Magazine"]/@src',
        '//div[@class="gallery"]//div[@class="row"]//@href',
        '//div[@class="thumbs_horizontal"]//@href',
        '//a[img[@class="t"]]/@href',
    ]

    scenes = photoLookup(sceneID)
    googleResults = PAutils.getFromGoogleSearch(' '.join(actors).strip(), siteNum)
    for photoURL in googleResults:
        for scene in scenes:
            if ('galleries' in photoURL or 'preview' in photoURL) and (scene in photoURL or scene == 'none'):
                req = PAutils.HTTPRequest(photoURL)
                photoPageElements = HTML.ElementFromString(req.text)
                for xpath in xpaths:
                    for img in photoPageElements.xpath(xpath):
                        art.append(img)

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            art.append(img)

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


def photoLookup(sceneID):
    if sceneID == 226:
        scenes = ['cool-colors', 'shes-on-fire', 'heating-up']
    elif sceneID == 209:
        scenes = ['amazing-figure']
    elif sceneID == 210:
        scenes = ['supersexy-vixen', 'satin-sensuality', 'outdoor-finale']
    elif sceneID == 130:
        scenes = ['elegantly-sexual']
    elif sceneID == 1569:
        scenes = ['model-like-no-other', 'teen-penetration']
    elif sceneID == 1524:
        scenes = ['petite-gaping', 'penetration-limits']
    elif sceneID == 1573 or sceneID == 283:
        scenes = []
    else:
        scenes = ['none']

    return scenes
