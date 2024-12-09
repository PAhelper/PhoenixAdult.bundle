import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    directURL = PAsearchSites.getSearchSearchURL(siteNum) + slugify(searchData.title)
    searchResults = [directURL]

    if unicode(directURL[-1], 'UTF-8').isdigit() and directURL[-2] == '-':
        directURL = '%s-%s' % (directURL[:-1], directURL[-1])
    searchResults.append(directURL)

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if '/video/' in sceneURL and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    pluralResults = list(searchResults)
    for sceneURL in searchResults:
        if sceneURL == directURL.replace('www.', '', 1):
            for original, new in plurals.items():
                sceneURL = sceneURL.replace(original, new)
            pluralResults.append(sceneURL)

    searchResults = list(dict.fromkeys([sceneURL.replace('www.', '', 1) for sceneURL in pluralResults]))

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if 'signup.' not in req.url:
            detailsPageElements = HTML.ElementFromString(req.text)

            titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content().strip(), siteNum)
            subSite = PAsearchSites.getSearchSiteName(siteNum)

            curID = PAutils.Encode(sceneURL)

            releaseDate = searchData.dateFormat() if searchData.date else ''

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, subSite), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    actorDate = None

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content().strip(), siteNum)

    metadata.title = title

    # Summary
    try:
        if 'pornplus' or 'tiny4k' in sceneURL:
            summary = detailsPageElements.xpath('//div[contains(@class, "space-x-4 items-start")]//span')[0].text_content().strip()
        else:
            summary = detailsPageElements.xpath('//div[contains(@id, "description")]')[0].text_content().strip()
    except:
        summary = ''

    metadata.summary = summary

    # Studio
    metadata.studio = 'PornPros'

    # Tagline and Collection(s)
    siteName = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Actor(s)
    if 'pornplus' or 'tiny4k' in sceneURL:
        actors = detailsPageElements.xpath('//div[contains(@class, "space-y-4 p-4")]//a[contains(@href, "/models/")]')
    else:
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

            if '&' in actorName:
                actorNames = actorName.split('&')
                for name in actorNames:
                    movieActors.addActor(name.strip(), actorPhotoURL)
            else:
                movieActors.addActor(actorName, actorPhotoURL)

            if not actorDate:
                actorURL = actorLink.get('href')
                if not actorURL.startswith('http'):
                    actorURL = PAsearchSites.getSearchBaseURL(siteNum) + actorURL.replace('girls?page=', '')

                req = PAutils.HTTPRequest(actorURL)
                actorPageElements = HTML.ElementFromString(req.text)

                actorDate = None
                if 'pornplus' in sceneURL:
                    sceneLinkxPath = '//div[contains(@class, "video-thumbnail flex")]'
                    sceneTitlexPath = './/a[contains(@class, "dropshadow")]'
                    sceneDatexpath = './/span[contains(@class, "font-extra-light")]/text()'
                    dateFormat = '%m/%d/%Y'
                else:
                    sceneLinkxPath = '//div[@class="row"]//div[contains(@class, "box-shadow")]'
                    sceneTitlexPath = './/h5[@class="card-title"]'
                    sceneDatexpath = './/@data-date'
                    dateFormat = '%B %d, %Y'

                for sceneLink in actorPageElements.xpath(sceneLinkxPath):
                    sceneTitle = re.sub(r'\W', '', sceneLink.xpath(sceneTitlexPath)[0].text_content().strip().replace(' ', '')).lower()
                    date = sceneLink.xpath(sceneDatexpath)
                    if re.sub(r'\W', '', metadata.title.replace(' ', '')).lower() == sceneTitle and date:
                        actorDate = date[0].strip()
                        break

    # Manually Add Actors
    # Add Actor Based on Title
    for actor in PAutils.getDictValuesFromKey(actorsDB, metadata.title):
        movieActors.addActor(actor, '')

    # Release Date
    if actorDate:
        date_object = datetime.strptime(actorDate, dateFormat)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    elif sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    genres = PAutils.getDictValuesFromKey(genresDB, siteName)
    for genreLink in genres:
        genreName = genreLink.strip()

        movieGenres.addGenre(genreName)

    # Posters
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

actorsDB = {
    'Poke Her In The Front': ['Sara Luvv', 'Dillion Harper'],
    'Best Friends With Nice Tits!': ['April O\'Neil', 'Victoria Rae Black'],
}

plurals = {
    'brothers': 'brother-s',
    'bros': 'bro-s',
    'sisters': 'sister-s',
    'siss': 'sis-s',
    'mothers': 'mother-s',
    'moms': 'mom-s',
    'fathers': 'father-s',
    'dads': 'dad-s',
    'sons': 'son-s',
    'daughters': 'daughter-s',
}
