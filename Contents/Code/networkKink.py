import re

import PAsearchSites
import PAutils

# kink.com shows an "Enter Kink" age gate (UK / Online Safety Act) before any page.
# Pressing the button sets age_gate_accepted=1; sending that cookie skips the gate.
# viewing-preferences was already sent by the shoot-ID lookup; it's now sent everywhere.
KINK_COOKIES = {'age_gate_accepted': '1', 'viewing-preferences': 'straight%2Cgay'}

# Matches the card/legend date format, e.g. "Apr 30, 2020"
DATE_RE = re.compile(r'^[A-Z][a-z]{2} \d{1,2}, \d{4}$')


def getJSONLD(detailsPageElements):
    # The page's schema.org VideoObject block. UK visitors get asterisked titles in the HTML,
    # but this block still carries the clean title, description and upload date.
    for block in detailsPageElements.xpath('//script[@type="application/ld+json"]/text()'):
        try:
            data = json.loads(block)
        except:
            continue
        if isinstance(data, dict) and data.get('@type') == 'VideoObject':
            return data
    return {}


def isCensored(text):
    return '*' in text


def search(results, lang, siteNum, searchData):
    shootID = None

    parts = searchData.title.split()
    if unicode(parts[0], 'UTF-8').isdigit():
        shootID = parts[0]
        searchData.title = searchData.title.replace(shootID, '', 1).strip()

    if shootID:
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/shoot/' + shootID
        req = PAutils.HTTPRequest(sceneURL, cookies=KINK_COOKIES)
        detailsPageElements = HTML.ElementFromString(req.text)
        jsonLD = getJSONLD(detailsPageElements)

        # Prefer the schema.org VideoObject. Without it, fall back to the HTML, but only on a
        # real scene page (it has the shoot-detail legend). Retired shoot IDs (e.g. 15393,
        # re-released as 104942) redirect to a generic "Channels" listing, which has neither
        # and must not be offered as a match.
        legend = detailsPageElements.xpath('//div[contains(@class, "shoot-detail-legend")]')
        heading = detailsPageElements.xpath('//h1')
        if jsonLD.get('name'):
            titleNoFormatting = PAutils.parseTitle(jsonLD['name'].strip(), siteNum)
        elif legend and heading:
            titleNoFormatting = PAutils.parseTitle(heading[0].text_content().strip(), siteNum)
        else:
            Log('Shoot %s: no scene data on %s (retired or redirected); not offering it' % (shootID, sceneURL))
            return results

        legendDate = [d.text_content().strip() for d in detailsPageElements.xpath('//div[contains(@class, "shoot-detail-legend")]//span[contains(@class, "text-muted")]') if DATE_RE.match(d.text_content().strip())]
        if jsonLD.get('uploadDate'):
            releaseDate = parse(jsonLD['uploadDate']).strftime('%Y-%m-%d')
        elif legendDate:
            releaseDate = parse(legendDate[0]).strftime('%Y-%m-%d')
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        curID = PAutils.Encode(sceneURL)

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s [%s] %s' % (shootID, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=100, lang=lang))
    else:
        # kink.com's search is fuzzy and lists matches newest first, 24 per page, so an older
        # scene can sit several pages down. With a date to aim for, keep paging until we hit
        # that date or go past it. If the text search finds nothing at all, browse the channel's
        # full listing (empty query) by date instead.
        baseURL = PAsearchSites.getSearchSearchURL(siteNum)
        attempts = [baseURL + searchData.encoded]
        # The listing fallback (empty query) only makes sense within one channel; for the
        # network-wide "Kink" site it would offer every scene released that day.
        if searchData.date and 'channelIds=' in baseURL:
            attempts.append(baseURL)

        for searchURL in attempts:
            if searchKinkPages(results, lang, siteNum, searchData, searchURL):
                break

    return results


KINK_PAGE_SIZE = 24


def getKinkPage(searchURL, page):
    # One page of results: (list of cards, total result count or None)
    req = PAutils.HTTPRequest('%s&page=%d' % (searchURL, page), cookies=KINK_COOKIES)
    pageElements = HTML.ElementFromString(req.text)
    # Each result is <div class="card shoot-thumbnail">. concat() pads the class list with spaces,
    # so " shoot-thumbnail " doesn't also match "shoot-thumbnail-footer".
    cards = pageElements.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " shoot-thumbnail ")]')
    # The result count is the span right after the results heading: <h1>...</h1> <span>893</span>
    # (the site menu uses the same CSS classes, so match on position, not class)
    total = None
    for totalText in pageElements.xpath('//h1/following-sibling::span[contains(@class, "text-primary")]/text()'):
        totalText = totalText.strip().replace(',', '')    # large counts are formatted "7,488"
        if totalText.isdigit():
            total = int(totalText)
            break
    return cards, total


def getCardDate(card):
    # The footer holds "Channel | Mon DD, YYYY | rating%"; return the date as YYYY-MM-DD, or None
    for text in card.xpath('.//div[contains(@class, "shoot-thumbnail-footer")]//text()'):
        if DATE_RE.match(text.strip()):
            return parse(text.strip()).strftime('%Y-%m-%d')
    return None


def titleFits(searchTitle, cardTitle):
    # Is the card's title consistent with the title we searched for? At least half of the
    # searched words must appear in the card title. Censored card words ("P****") count as a
    # match for any searched word with the same first letter. With no title to check
    # (date-only search), anything fits.
    wanted = re.findall(r"[a-z0-9']+", searchTitle.lower())
    if not wanted:
        return True
    cardWords = [re.sub(r"[^a-z0-9'*]", '', w) for w in cardTitle.lower().split()]
    hits = 0
    for word in wanted:
        for cardWord in cardWords:
            if cardWord == word or (cardWord and '*' in cardWord and cardWord[0] == word[0]):
                hits += 1
                break
    return hits * 2 >= len(wanted)


def addKinkCards(results, lang, siteNum, searchData, cards, onlyExactDate):
    # Turn cards into search results. Returns True if one has exactly the date we're after.
    exactDate = False
    for card in cards:
        link = card.xpath('.//a[contains(@href, "/shoot/")]/@href')
        if not link:
            continue
        curID = PAutils.Encode(link[0])
        shootID = link[0].rstrip('/').split('/')[-1]

        # Card titles may be censored for UK visitors; they're only used for display and fallback scoring
        titleNoFormatting = card.xpath('.//a[contains(@href, "/shoot/")]/@title')
        titleNoFormatting = titleNoFormatting[0].strip() if titleNoFormatting else shootID

        cardDate = getCardDate(card)
        releaseDate = cardDate or (searchData.dateFormat() if searchData.date else '')
        displayDate = cardDate or ''

        if searchData.date and cardDate:
            if onlyExactDate and cardDate != searchData.date:
                continue
            # The date alone isn't proof: several scenes can share a release date, especially
            # in a network-wide search. A title that doesn't fit costs 10 points and doesn't
            # count as found.
            fits = titleFits(searchData.title, titleNoFormatting)
            score = 100 - Util.LevenshteinDistance(searchData.date, cardDate) - (0 if fits else 10)
            exactDate = exactDate or (cardDate == searchData.date and fits)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='[%s] %s [%s] %s' % (shootID, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))
    return exactDate


def searchKinkPages(results, lang, siteNum, searchData, searchURL):
    # Results are listed newest first, 24 per page. Page 1 is always added. With a target date
    # that isn't on page 1, binary-search the remaining pages by date: each look at a middle
    # page tells us whether the date is newer (go back) or older (go forward). An 893-scene
    # channel needs about 6 page loads instead of up to 38.
    # Returns True when it's done: a card with the exact date was found, or (with no date)
    # page 1 produced results.
    cards, total = getKinkPage(searchURL, 1)
    if not cards:
        return False
    if addKinkCards(results, lang, siteNum, searchData, cards, False):
        return True
    if not searchData.date:
        return True

    target = searchData.date
    oldest = getCardDate(cards[-1])
    if not total or not oldest or target >= oldest:
        return False                  # it would have been on page 1 (or we can't tell where to look)

    lo, hi = 2, (total + KINK_PAGE_SIZE - 1) // KINK_PAGE_SIZE
    for attempt in range(12):         # safety limit; log2 of any real channel size is far below this
        if lo > hi:
            break
        mid = (lo + hi) // 2
        cards, pageTotal = getKinkPage(searchURL, mid)
        if not cards:
            hi = mid - 1
            continue
        newest, oldest = getCardDate(cards[0]), getCardDate(cards[-1])
        if newest and target > newest:
            hi = mid - 1              # target is newer than this page: look earlier pages
        elif oldest and target < oldest:
            lo = mid + 1              # target is older than this page: look later pages
        else:
            # The target date falls inside this page. A scene on a page boundary could sit on
            # the neighbouring page, so check that too when the date matches the edge.
            found = addKinkCards(results, lang, siteNum, searchData, cards, True)
            if not found and target == newest and mid > 1:
                found = addKinkCards(results, lang, siteNum, searchData, getKinkPage(searchURL, mid - 1)[0], True)
            if not found and target == oldest:
                found = addKinkCards(results, lang, siteNum, searchData, getKinkPage(searchURL, mid + 1)[0], True)
            return found
    return False


def getKinkPersonPhoto(personURL):
    # Performer and director pages sit behind the same age gate as scenes, so send the cookies.
    # The photo moved from .biography-container to .kink-slider-images. Visitors who get
    # "safe-images" see a blurred placeholder of a different person, so skip those rather
    # than attach the wrong face. The query string is a signature, so keep the full URL.
    req = PAutils.HTTPRequest(personURL, cookies=KINK_COOKIES)
    personPage = HTML.ElementFromString(req.text)
    for xpath in ('//div[contains(@class, "biography-container")]//img/@src',
                  '//div[contains(@class, "kink-slider-images")]//img/@src',
                  '//div[contains(@class, "kink-slider-images")]//img/@data-src'):
        for src in personPage.xpath(xpath):
            if '/safe-images/' not in src:
                return src
    return ''


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    sceneDate = None
    if len(metadata_id) > 2:
        sceneDate = metadata_id[2]

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL

    req = PAutils.HTTPRequest(sceneURL, cookies=KINK_COOKIES)
    detailsPageElements = HTML.ElementFromString(req.text)
    jsonLD = getJSONLD(detailsPageElements)

    # Add \n to <br> entries to fix summary
    for br in detailsPageElements.xpath('*//br'):
        br.tail = '\n' + br.tail if br.tail else '\n'

    # Title
    if jsonLD.get('name'):
        metadata.title = PAutils.parseTitle(jsonLD['name'].strip(), siteNum)
    else:
        metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content().strip(), siteNum)

    # Summary
    if jsonLD.get('description'):
        # The description is Markdown: turn [text](url) into text and drop **bold** markers
        summary = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', jsonLD['description']).replace('**', '')
        metadata.summary = summary.replace('\n', ' ').strip()
    else:
        metadata.summary = detailsPageElements.xpath('//div[contains(@class, "description")]/span[contains(@class, "fw-200")]')[0].text_content().replace('\n', ' ').strip()

    # Tagline and Collection(s)
    channel = detailsPageElements.xpath('//div[contains(@class, "shoot-detail-legend")]//a[contains(@href, "/channel/")]/@href')[0].split('/channel/')[-1].replace('-', '').lower()
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
    elif 'fetishnetworkmale' in channel:
        tagline = 'Fetish Network Male'
    elif 'fetishnetwork' in channel:
        tagline = 'Fetish Network'
    else:
        tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    movieCollections.addCollection(tagline)

    # Studio
    if tagline == 'Chantas Bitches' or tagline == 'Fucked and Bound' or tagline == 'Captive Male':
        metadata.studio = 'Twisted Factory'
    elif tagline == 'Sexual Disgrace' or tagline == 'Strapon Squad' or tagline == 'Fetish Network Male' or tagline == 'Fetish Network':
        metadata.studio = 'Fetish Network'
    else:
        metadata.studio = 'Kink'

    # Release Date
    date = [d.text_content().strip() for d in detailsPageElements.xpath('//div[contains(@class, "shoot-detail-legend")]//span[contains(@class, "text-muted")]') if DATE_RE.match(d.text_content().strip())]
    if jsonLD.get('uploadDate'):
        date_object = parse(jsonLD['uploadDate'][:10])
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    elif date:
        date_object = parse(date[0])
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    elif sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    genres = detailsPageElements.xpath('//p[normalize-space()="Categories"]/ancestor::div[contains(@class, "container")][1]//a[contains(@href, "/tag/")]')
    for genreLink in genres:
        genreName = genreLink.text_content().replace(',', '').strip()
        if isCensored(genreName):
            # /tag/double-anal-bdsm -> "Double Anal"
            slug = genreLink.get('href').rstrip('/').split('/tag/')[-1]
            slug = re.sub(r'-bdsm$', '', slug)
            genreName = slug.replace('-', ' ').title()

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
                actorPhotoURL = getKinkPersonPhoto(PAsearchSites.getSearchBaseURL(siteNum) + actorLink.get('href'))
            except:
                pass

            movieActors.addActor(actorName, actorPhotoURL)

    # Director(s)
    directors = detailsPageElements.xpath('//span[contains(@class, "director-name")]/a')
    for directorLink in directors:
        directorName = directorLink.text_content().strip()
        directorPhotoURL = ''
        try:
            directorPhotoURL = getKinkPersonPhoto(PAsearchSites.getSearchBaseURL(siteNum) + directorLink.get('href'))
        except:
            pass

        movieActors.addDirector(directorName, directorPhotoURL)

    # Posters
    xpaths = [
        '//video/@poster',
        '//div[@class="player"]/div/@poster',
        '//div[@id="galleryWrapper"]//img/@data-image-file',
        # Current page design: gallery images are img.gallery-img; data-image-file is the full-size, unsigned URL
        '//img[contains(@class, "gallery-img")]/@data-image-file'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            if '/safe-images/' in poster:
                continue
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
