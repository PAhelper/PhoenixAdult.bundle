import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    directURL = PAsearchSites.getSearchSearchURL(siteNum) + searchData.title.lower().replace(' ', '-').replace('\'', '-')
    searchResults = [directURL]

    if unicode(directURL[-1], 'UTF-8').isdigit() and directURL[-2] == '-':
        directURL = '%s-%s' % (directURL[:-1], directURL[-1])
    searchResults.append(directURL)

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if ('/video/' in sceneURL and sceneURL not in searchResults):
            searchResults.append(sceneURL)

    searchResults = list(dict.fromkeys([sceneURL.replace('www.', '', 1) for sceneURL in searchResults]))

    for sceneURL in searchResults:
        if sceneURL == directURL.replace('www.', '', 1):
            for original, new in plurals.items():
                sceneURL = sceneURL.replace(original, new)

        req = PAutils.HTTPRequest(sceneURL)
        if 'signup.' not in req.url:
            detailsPageElements = HTML.ElementFromString(req.text)
            titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()
            curID = PAutils.Encode(sceneURL)

            releaseDate = searchData.dateFormat() if searchData.date else ''

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL

    sceneDate = None
    if len(metadata_id) > 2:
        sceneDate = metadata_id[2]

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[contains(@id, "description")]')[0].text_content().strip()
    except:
        pass

    # Studio
    metadata.studio = 'Porn Pros'

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteNum)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@id="t2019-sinfo"]//a[contains(@href, "/girls/")]')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

            if not sceneDate:
                actorURL = actorLink.get('href')
                if not actorURL.startswith('http'):
                    actorURL = PAsearchSites.getSearchBaseURL(siteNum) + actorURL

                req = PAutils.HTTPRequest(actorURL)
                actorPageElements = HTML.ElementFromString(req.text)

                sceneDate = None
                for sceneLink in actorPageElements.xpath('//div[@class="row"]//div[contains(@class, "box-shadow")]'):
                    sceneTitle = sceneLink.xpath('.//h5[@class="card-title"]')[0].text_content().strip()
                    date = sceneLink.xpath('.//@data-date')
                    if metadata.title == sceneTitle and date:
                        sceneDate = date[0].strip()

    # Manually Add Actors
    # Add Actor Based on Title
    if 'Poke Her In The Front' == metadata.title:
        actorPhotoURL = ''

        actorName = 'Sara Luvv'
        movieActors.addActor(actorName, actorPhotoURL)

        actorName = 'Dillion Harper'
        movieActors.addActor(actorName, actorPhotoURL)

    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = []
    for key, value in genresDB.items():
        if key.lower() == siteName.lower():
            genres = value
            break

    for genreName in genres:
        movieGenres.addGenre(genreName)

    # Posters
    art = []
    xpaths = [
        '//video/@poster',
        '(//img[contains(@src, "handtouched")])[position() < 5]/@src'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            if not poster.startswith('http'):
                poster = 'http:' + poster

            art.append(poster)

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


genresDB = {
    'Anal4K': ['Anal', 'Ass', 'Creampie'],
    'BBCPie': ['Interracial', 'BBC', 'Creampie'],
    'Cum4K': ['Creampie'],
    'DeepThroatLove': ['Blowjob', 'Deep Throat'],
    'GirlCum': ['Orgasms', 'Girl Orgasm', 'Multiple Orgasms'],
    'Holed': ['Anal', 'Ass'],
    'Lubed': ['Lube', 'Raw', 'Wet'],
    'MassageCreep': ['Massage', 'Oil'],
    'PassionHD': ['Hardcore'],
    'POVD': ['Gonzo', 'POV'],
    'PureMature': ['MILF', 'Mature'],
}

plurals = {
    'brothers': 'brother-s',
    'bros': 'bro-s',
    'sisters': 'sister-s',
    'siss': 'sis-s',
    'friends': 'friend-s',
    'mothers': 'mother-s',
    'moms': 'mom-s',
    'fathers': 'father-s',
    'dads': 'dad-s',
    'sons': 'son-s',
    'daughters': 'daughter-s',
}
