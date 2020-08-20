import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):

    sceneID = re.sub('\D.*', '', searchTitle)

    if sceneID:
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + "/webmasters/" + sceneID
        req = PAutils.HTTPRequest(sceneURL)
        searchResults = HTML.ElementFromString(req.text)
        titleNoFormatting = re.sub(r'^\d+', '', searchResults.xpath('//h1/text()')[0].title())
        curID = PAutils.Encode(sceneURL)

        score = 100

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))
    else:
        # Handle 3 Types of Links: First, Last; First Only; First-Last
        try:
            encodedTitle = re.search(r'^\S*.\S*', searchTitle).group(0).replace(' ', '').lower()

            req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + ".html")
            searchResults = HTML.ElementFromString(req.text)

            if searchResults.xpath('//html')[0].text_content() == 'Page not found':
                raise Exception
        except:
            try:
                encodedTitle = re.search(r'^\S*.\S*', searchTitle).group(0).replace(' ', '-').lower()

                req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + ".html")
                searchResults = HTML.ElementFromString(req.text)

                if searchResults.xpath('//html')[0].text_content() == 'Page not found':
                    raise Exception
            except:
                encodedTitle = re.search(r'^\S*', searchTitle).group(0).lower()

                req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + ".html")
                searchResults = HTML.ElementFromString(req.text)
        try:
            pageResults = (int)(searchResults.xpath('//span[@class="number_item "]')[0].text_content().strip())
        except:
            pageResults = 1

        for x in range(pageResults):
            if x == 1:
                searchResults.xpath('//a[contains(@class,"in_stditem")]/@href')[1]
                req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + searchResults.xpath('//a[contains(@class,"in_stditem")]/@href')[1])
                searchResults = HTML.ElementFromString(req.text)
            for searchResult in searchResults.xpath('//div[@class="infos"]'):
                resultTitleID = searchResult.xpath('.//span[@class="video-title"]')[0].text_content().strip().title()

                titleNoFormatting = re.sub(r'^\d+', '', resultTitleID)

                resultID = re.sub('\D.*', '', resultTitleID)

                sceneURL = searchResult.xpath('.//a/@href')[0]
                curID = PAutils.Encode(sceneURL)

                date = searchResult.xpath('.//span[@class="video-date"]')[0].text_content().strip()

                if date:
                    releaseDate = parse(date).strftime('%Y-%m-%d')
                else:
                    releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
                releaseDate = parse(date).strftime('%Y-%m-%d')
                displayDate = releaseDate if date else ''

                if sceneID == resultID:
                    score = 100
                elif searchDate and displayDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    try:
        sceneDate = metadata_id[2]
    except:
        pass
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    if 'webmasters' in sceneURL:
        resultTitleID = detailsPageElements.xpath('//h1/text()')[0].title()
        metadata.title = re.sub(r'^\d+', '', resultTitleID)
    else:
        resultTitleID = detailsPageElements.xpath('//h4/span')[0].text_content().title()
        metadata.title = re.sub(r'^\d+', '', resultTitleID)

    sceneID = re.sub('\D.*', '', resultTitleID)

    # Summary
    try:
        if 'webmasters' in sceneURL:
            metadata.summary = detailsPageElements.xpath('//div[@class="row gallery-description"]//div')[1].text_content().strip()
        else:
            metadata.summary = detailsPageElements.xpath('//div[@class="row"]//a/@title')[0].strip()
    except:
        pass

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Actors
    if 'webmasters' in sceneURL:
        actors = detailsPageElements.xpath('//spam[@class="key-words"]//a')
    else:
        actors = detailsPageElements.xpath('//h5//a')

    actorPhotoURL = ''

    # Remove Actor Names from Genre List
    genres = detailsPageElements.xpath('//meta[@name="keywords"]/@content')[0].replace('Aussie Ass', '')
    genres = re.sub(r'id.\d*', '', genres, flags=re.IGNORECASE)

    if actors:
        for actorLink in actors:
            actorName = actorLink.text_content().title()
            genres = genres.replace(actorName, '')

            modelURL = actorLink.xpath('./@href')[0]
            req = PAutils.HTTPRequest(modelURL)
            actorsPageElements = HTML.ElementFromString(req.text)

            img = actorsPageElements.xpath('//img[contains(@id,"set-target")]/@src')[0]
            if img:
                actorPhotoURL = img
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL

            movieActors.addActor(actorName, actorPhotoURL)

    # Date
    date = ""

    try:
        if 'webmasters' in sceneURL:

            pageResults = (int)(actorsPageElements.xpath('//span[@class="number_item "]')[0].text_content().strip())

            if not pageResults:
                pageResults = 1

            for x in range(pageResults):
                if x == 1:
                    actorsPageElements.xpath('//a[contains(@class,"in_stditem")]/@href')[1]
                    req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteID) + actorsPageElements.xpath('//a[contains(@class,"in_stditem")]/@href')[1])
                    actorsPageElements = HTML.ElementFromString(req.text)

                for sceneElements in actorsPageElements.xpath('//div[@class="box"]'):
                    if sceneID in sceneElements.xpath('.//a/text()')[1]:
                        date = actorsPageElements.xpath('.//span[@class="video-date"]')[0].text_content().strip()
                        break
        else:
            date = sceneDate
    except:
        date = sceneDate

    if date:
        date = parse(date).strftime('%d-%m-%Y')
        date_object = datetime.strptime(date, '%d-%m-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genre in genres.split(','):
        movieGenres.addGenre(genre.strip())

    # Posters
    art = []
    xpaths = [
        '//img[contains(@alt,"content")]/@src',
        '//div[@class="box"]//img/@src',
    ]

    altURL = ""

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if 'http' not in img:
                if 'join' in img:
                    break
                elif 'webmasters' in sceneURL:
                    img = sceneURL + "/" + img
                else:
                    img = PAsearchSites.getSearchBaseURL(siteID) + img
            art.append(img)
        if 'webmasters' not in sceneURL:
            altURL = PAsearchSites.getSearchBaseURL(siteID) + "/webmasters/" + sceneID
            req = PAutils.HTTPRequest(altURL)
            detailsPageElements = HTML.ElementFromString(req.text)
            sceneURL = altURL

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
