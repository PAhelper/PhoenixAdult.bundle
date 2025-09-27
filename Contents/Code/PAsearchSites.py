import PAsiteList
import PAutils


def getSearchSiteName(siteNum):
    siteName = None
    if PAsiteList.searchSites[siteNum]:
        siteName = PAsiteList.searchSites[siteNum][0]

    return siteName


def getSearchBaseURL(siteNum):
    url = None
    if PAsiteList.searchSites[siteNum]:
        url = PAsiteList.searchSites[siteNum][1]

    return url


def getSearchSearchURL(siteNum):
    url = None
    if PAsiteList.searchSites[siteNum]:
        url = PAsiteList.searchSites[siteNum][2]
        if not url.startswith('http'):
            url = getSearchBaseURL(siteNum) + url

    return url


def getSiteNumByFilter(searchFilter):
    searchResults = []
    searchFilter = re.sub(r'[^a-z0-9]', '', searchFilter.lower())
    for siteNum in PAsiteList.searchSites:
        siteName = getSearchSiteName(siteNum)
        if siteName:
            siteName = re.sub(r'[^a-z0-9]', '', siteName.lower())

            if searchFilter.startswith(siteName):
                searchResults.append((siteNum, siteName))

    if searchResults:
        from operator import itemgetter

        return max(searchResults, key=itemgetter(1))[0]

    return None


def getSearchSettings(mediaTitle, filename):
    plexScannerBlacklist = map(str.strip, map(str.lower, Prefs['blacklist_list'].split(',')))

    if filename and Prefs['blacklist_enable']:
        cleanFilename = re.sub(r'\W', ' ', filename.rsplit('/', 1)[-1].lower()).strip().split()
        splitMediaTitle = mediaTitle.split()

        for word in plexScannerBlacklist:
            if word in cleanFilename:
                Log('Restoring %s to SearchTitle' % word)

                for idx in [i for i, x in enumerate(cleanFilename) if x == word]:
                    replaceWord = splitMediaTitle[map(str.lower, splitMediaTitle).index(cleanFilename[idx - 1])]
                    splitMediaTitle[map(str.lower, splitMediaTitle).index(cleanFilename[idx - 1])] = '%s %s' % (replaceWord, word)

                mediaTitle = ' '.join(splitMediaTitle)

    Log('mediaTitle w/ possible abbreviation: %s' % mediaTitle)

    for abbreviation, full in PAsiteList.abbreviations:
        r = re.compile(abbreviation, flags=re.IGNORECASE)
        if r.match(mediaTitle) and not mediaTitle.lower().startswith(full.lower()):
            mediaTitle = r.sub(full, mediaTitle, 1)
            break

    Log('mediaTitle w/ possible abbrieviation fixed: %s' % mediaTitle)

    result = {
        'siteNum': None,
        'siteName': None,
        'searchTitle': None,
        'searchDate': None,
    }

    # Remove Site from Title
    siteNum = getSiteNumByFilter(mediaTitle)
    if siteNum is not None:
        Log('^^^^^^^ siteNum: %d' % siteNum)
        Log('^^^^^^^ Shortening Title')

        title = mediaTitle.lower()
        site = getSearchSiteName(siteNum).lower()

        # \u0410-\u042F == А-Я, \u0430-\u044F == а-я
        title = re.sub(ur'[^A-Za-z0-9#&, \u0410-\u042F\u0430-\u044F]', ' ', title.decode('UTF-8')).encode('UTF-8')
        site = re.sub(r'\W', '', site)

        matched = False
        while(' ' in title):
            if title.lower().startswith(site):
                matched = True
                break
            else:
                title = title.replace(' ', '', 1)

        if matched:
            searchTitle = re.sub(site, '', title, 1, flags=re.IGNORECASE)
            searchTitle = ' '.join(searchTitle.split())

            searchTitle = re.sub(r'\sS\b', '\'s', searchTitle, flags=re.IGNORECASE)
            searchTitle = PAutils.parseTitle(searchTitle, siteNum)

            Log('Search Title (before date processing): %s' % searchTitle)

            # Search Type
            searchDate = None
            regex = [
                (r'\b\d{4} \d{2} \d{2}\b', '%Y %m %d'),
                (r'\b\d{2} \d{2} \d{2}\b', '%y %m %d')
            ]
            date_obj = None
            for r, dateFormat in regex:
                date = re.search(r, searchTitle)
                if date:
                    try:
                        date_obj = datetime.strptime(date.group(), dateFormat)
                    except:
                        pass

                    if date_obj:
                        searchDate = date_obj.strftime('%Y-%m-%d')
                        searchTitle = ' '.join(re.sub(r, '', searchTitle, 1).split())
                        break

            searchTitle = searchTitle[0].upper() + searchTitle[1:]

            result['siteNum'] = siteNum
            result['siteName'] = site
            result['searchTitle'] = searchTitle
            result['searchDate'] = searchDate

    return result


def posterAlreadyExists(posterUrl, metadata):
    posterUrl = PAutils.getClearURL(posterUrl)
    for url in metadata.posters.keys():
        if url.lower() == posterUrl.lower():
            Log('Found %s in posters collection' % posterUrl)
            return True

    for url in metadata.art.keys():
        if url.lower() == posterUrl.lower():
            Log('Found %s in art collection' % posterUrl)
            return True

    return False


def posterOnlyAlreadyExists(posterUrl, metadata):
    posterUrl = PAutils.getClearURL(posterUrl)
    for url in metadata.posters.keys():
        if url.lower() == posterUrl.lower():
            Log('Found %s in posters collection' % posterUrl)
            return True

    return False
