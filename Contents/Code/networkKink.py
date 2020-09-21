import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    shootID = None
    for splited in searchTitle.split(' '):
        if unicode(splited, 'UTF-8').isdigit():
            shootID = splited
            break

    if shootID:
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/shoot/' + shootID
        req = PAutils.HTTPRequest(sceneURL, headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
        detailsPageElements = HTML.ElementFromString(req.text)

        titleNoFormatting = detailsPageElements.xpath('//h1[@class="shoot-title"]')[0].text_content().strip()[:-1]
        releaseDate = parse(detailsPageElements.xpath('//span[@class="shoot-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        curID = PAutils.Encode(sceneURL)

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s [%s] %s' % (shootID, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=100, lang=lang))
    else:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@class="shoot-card scene"]'):
            titleNoFormatting = searchResult.xpath('.//img/@alt')[0].strip()
            curID = PAutils.Encode(searchResult.xpath('.//a[@class="shoot-link"]/@href')[0])
            releaseDate = parse(searchResult.xpath('.//div[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            shootID = searchResult.xpath('.//span[contains(@class, "favorite-button")]/@data-id')[0]

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s [%s] %s' % (shootID, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="shoot-title"]')[0].text_content().strip()[:-1]

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="description"]')[1].text_content().strip().replace('\n', ' ').replace('Description:', '')

    # Tagline and Collection(s)
    metadata.collections.clear()
    channel = detailsPageElements.xpath('//div[contains(@class, "shoot-logo")]')[0].text_content().strip()
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
        tagline = PAsearchSites.getSearchSiteName(siteID)
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
    date = detailsPageElements.xpath('//span[@class="shoot-date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//p[@class="tag-list category-tag-list"]//a')
    for genreLink in genres:
        genreName = genreLink.text_content().replace(',', '').strip().title()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//p[@class="starring"]//a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get('href')
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            actorPhotoURL = actorPage.xpath('//div[contains(@class, "biography-container")]//img/@src')[0]

            movieActors.addActor(actorName, actorPhotoURL)

    # Director
    director = metadata.directors.new()
    try:
        directors = detailsPageElements.xpath('//p[@class="director"]/a')
        for dirname in directors:
            director.name = dirname.text_content().strip()
    except:
        pass

    # Posters
    art = []
    xpaths = [
        '//video/@poster',
        '//div[@class="player"]//img/@src',
        '//div[@id="gallerySlider"]//img/@data-image-file'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

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
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
