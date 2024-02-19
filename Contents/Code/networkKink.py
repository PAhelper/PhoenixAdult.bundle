import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    shootID = None

    parts = searchData.title.split()
    if unicode(parts[0], 'UTF-8').isdigit():
        shootID = parts[0]
        searchData.title = searchData.title.replace(shootID, '', 1).strip()

    if shootID:
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/shoot/' + shootID
        req = PAutils.HTTPRequest(sceneURL, headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
        detailsPageElements = HTML.ElementFromString(req.text)

        titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//h1[contains(@class, "fs-0")]')[0].text_content().strip(), siteNum)
        releaseDate = parse(detailsPageElements.xpath('//div[contains(@class, "shoot-detail-legend")]//span[@class="text-muted ms-2"]')[0].text_content()).strftime('%Y-%m-%d')
        curID = PAutils.Encode(sceneURL)

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s [%s] %s' % (shootID, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=100, lang=lang))
    else:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@class="shoot-card scene"]'):
            titleNoFormatting = searchResult.xpath('.//img/@alt')[0].strip()
            curID = PAutils.Encode(searchResult.xpath('.//a[@class="shoot-link"]/@href')[0])
            shootID = searchResult.xpath('.//div[contains(@class, "favorite-button")]/@data-id')[0]

            date = searchResult.xpath('.//div[@class="date"]')
            if date:
                releaseDate = parse(date[0].text_content().strip()).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''
            displayDate = releaseDate if date else ''

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='[%s] %s [%s] %s' % (shootID, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    try:
        sceneDate = metadata_id[2]
    except IndexError:
        # for some reason this is no longer passing three items, only two.
        # this fix appears to work
        # TODO: resolve the underlying issue.
        sceneDate = None
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Add \n to <br> entries to fix summary
    for br in detailsPageElements.xpath('*//br'):
        br.tail = '\n' + br.tail if br.tail else '\n'

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1[contains(@class, "fs-0")]')[0].text_content().strip(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "description")]/span[contains(@class, "fw-200")]')[0].text_content().replace('\n', ' ').strip()

    # Tagline and Collection(s)
    channel = detailsPageElements.xpath('//div[contains(@class, "shoot-detail-legend")]//a[contains(@href, "/channel/")]/text()')[0].strip().lower()
    if 'boundgangbangs' in channel:
        tagline = 'Bound Gangbangs'
    elif 'brutalsessions' in channel:
        tagline = 'Brutal Sessions'
    elif 'devicebondage' in channel:
        tagline = 'Device Bondage'
    elif 'familiestied' in channel:
        tagline = 'Families Tied'
    elif 'hardcoregangbang' in channel:
        tagline = 'Hardcore Gangbang'
    elif 'hogtied' in channel:
        tagline = 'Hogtied'
    elif 'kinkfeatures' in channel:
        tagline = 'Kink Features'
    elif 'kinkuniversity' in channel:
        tagline = 'Kink University'
    elif 'publicdisgrace' in channel:
        tagline = 'Public Disgrace'
    elif 'sadisticrope' in channel:
        tagline = 'Sadistic Rope'
    elif 'sexandsubmission' in channel:
        tagline = 'Sex and Submission'
    elif 'thetrainingofo' in channel:
        tagline = 'The Training of O'
    elif 'theupperfloor' in channel:
        tagline = 'The Upper Floor'
    elif 'waterbondage' in channel:
        tagline = 'Water Bondage'
    elif 'everythingbutt' in channel:
        tagline = 'Everything Butt'
    elif 'footworship' in channel:
        tagline = 'Foot Worship'
    elif 'fuckingmachines' in channel:
        tagline = 'Fucking Machines'
    elif 'tspussyhunters' in channel:
        tagline = 'TS Pussy Hunters'
    elif 'tsseduction' in channel:
        tagline = 'TS Seduction'
    elif 'ultimatesurrender' in channel:
        tagline = 'Ultimate Surrender'
    elif '30minutesoftorment' in channel:
        tagline = '30 Minutes of Torment'
    elif 'boundgods' in channel:
        tagline = 'Bound Gods'
    elif 'boundinpublic' in channel:
        tagline = 'Bound in Public'
    elif 'buttmachineboys' in channel:
        tagline = 'Butt Machine Boys'
    elif 'menonedge' in channel:
        tagline = 'Men on Edge'
    elif 'nakedkombat' in channel:
        tagline = 'Naked Kombat'
    elif 'divinebitches' in channel:
        tagline = 'Divine Bitches'
    elif 'electrosluts' in channel:
        tagline = 'Electrosluts'
    elif 'meninpain' in channel:
        tagline = 'Men in Pain'
    elif 'whippedass' in channel:
        tagline = 'Whipped Ass'
    elif 'wiredpussy' in channel:
        tagline = 'Wired Pussy'
    elif 'chantasbitches' in channel:
        tagline = 'Chantas Bitches'
    elif 'fuckedandbound' in channel:
        tagline = 'Fucked and Bound'
    elif 'captivemale' in channel:
        tagline = 'Captive Male'
    elif 'submissivex' in channel:
        tagline = 'SubmissiveX'
    elif 'filthyfemdom' in channel:
        tagline = 'Filthy Femdom'
    elif 'straponsquad' in channel:
        tagline = 'Strapon Squad'
    elif 'sexualdisgrace' in channel:
        tagline = 'Sexual Disgrace'
    elif 'fetishnetwork' in channel:
        tagline = 'Fetish Network'
    elif 'fetishnetworkmale' in channel:
        tagline = 'Fetish Network Male'
    else:
        tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Studio
    if tagline == 'Chantas Bitches' or tagline == 'Fucked and Bound' or tagline == 'Captive Male':
        metadata.studio = 'Twisted Factory'
    elif tagline == 'Sexual Disgrace' or tagline == 'Strapon Squad' or tagline == 'Fetish Network Male' or tagline == 'Fetish Network':
        metadata.studio = 'Fetish Network'
    else:
        metadata.studio = 'Kink'

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class, "shoot-detail-legend")]//span[@class="text-muted ms-2"]')
    if date:
        date_object = parse(date[0].text_content().strip())
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    elif sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    genres = detailsPageElements.xpath('//a[contains(@href, "/tag/")]')
    for genreLink in genres:
        genreName = genreLink.text_content().replace(',', '').strip()

        movieGenres.addGenre(genreName)

    # Actor(s)
    actors = detailsPageElements.xpath('//span[contains(@class, "text-primary")]//a[contains(@href, "/model/")]')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().replace(',', '').strip()
            actorPhotoURL = ''
            try:
                actorPageURL = PAsearchSites.getSearchBaseURL(siteNum) + actorLink.get('href')
                req = PAutils.HTTPRequest(actorPageURL)
                actorPage = HTML.ElementFromString(req.text)
                actorPhotoURL = actorPage.xpath('//div[contains(@class, "biography-container")]//img/@src')[0]
            except:
                pass

            movieActors.addActor(actorName, actorPhotoURL)

    # Director(s)
    directors = detailsPageElements.xpath('//span[contains(@class, "director-name")]/a')
    for directorLink in directors:
        directorName = directorLink.text_content().strip()
        directorPhotoURL = ''
        try:
            directorPageURL = PAsearchSites.getSearchBaseURL(siteNum) + directorLink.get('href')
            req = PAutils.HTTPRequest(directorPageURL)
            directorPage = HTML.ElementFromString(req.text)
            directorPhotoURL = directorPage.xpath('//div[contains(@class, "biography-container")]//img/@src')[0]
        except:
            pass

        movieActors.addDirector(directorName, directorPhotoURL)

    # Posters
    xpaths = [
        '//video/@poster',
        '//div[@class="player"]/div/@poster',
        '//div[@id="galleryWrapper"]//img/@data-image-file'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster.split('?')[0])

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
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
