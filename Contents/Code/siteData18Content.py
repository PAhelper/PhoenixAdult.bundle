import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []
    siteResults = []
    temp = []
    count = 0

    sceneID = None
    parts = searchData.title.split()
    if unicode(parts[0], 'UTF-8').isdigit():
        sceneID = parts[0]

        if int(sceneID) > 100:
            searchData.title = searchData.title.replace(sceneID, '', 1).strip()
            sceneURL = '%s/content/%s' % (PAsearchSites.getSearchBaseURL(siteNum), sceneID)
            searchResults.append(sceneURL)

    searchData.encoded = searchData.title.replace(' ', '+')
    searchURL = '%s%s' % (PAsearchSites.getSearchSearchURL(siteNum), searchData.encoded)
    req = PAutils.HTTPRequest(searchURL, headers={'Referer': 'http://www.data18.com'})
    searchPageElements = HTML.ElementFromString(req.text)

    for searchResult in searchPageElements.xpath('//p[@class="genmed"]//parent::div'):
        sceneURL = searchResult.xpath('.//*[contains(@href, "content")]/@href')[0]

        if sceneURL not in searchResults:
            urlID = re.sub(r'.*/', '', sceneURL)

            try:
                siteName = searchResult.xpath('.//*[contains(., "Network")]')[0].text_content().replace('Network:', '').strip()
            except:
                try:
                    siteName = searchResult.xpath('.//*[contains(., "Studio")]')[0].text_content().replace('Studio:', '').strip()
                except:
                    siteName = ''

            try:
                subSite = searchResult.xpath('.//p[@class][contains(., "Site:")]')[0].text_content().replace('Site:', '').strip()
            except:
                subSite = ''

            if siteName:
                siteDisplay = '%s/%s' % (siteName, subSite) if subSite else siteName
            else:
                siteDisplay = subSite

            titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//*[contains(@href, "content")]')[1].text_content(), siteNum)
            curID = PAutils.Encode(sceneURL)
            siteResults.append(sceneURL)

            try:
                date = searchResult.xpath('.//p[@class="genmed"]')[0].text_content().strip()
                date = re.sub(r'^#(.*?)\s', '', date)
            except:
                date = ''

            if date and not date == 'unknown':
                date = date.replace('Sept', 'Sep')
                releaseDate = parse(date).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''
            displayDate = releaseDate if date else ''

            if sceneID == urlID:
                score = 100
            elif searchData.date and displayDate:
                score = 80 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 80 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            if score == 80:
                count += 1
                temp.append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, siteDisplay, displayDate), score=score, lang=lang))
            else:
                results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, siteDisplay, displayDate), score=score, lang=lang))

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if ('/content/' in sceneURL and '.html' not in sceneURL and sceneURL not in searchResults and sceneURL not in siteResults):
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)
        urlID = re.sub(r'.*/', '', sceneURL)

        try:
            siteName = detailsPageElements.xpath('//i[contains(., "Network")]//preceding-sibling::a[1]')[0].text_content().strip()
        except:
            try:
                siteName = detailsPageElements.xpath('//i[contains(., "Studio")]//preceding-sibling::a[1]')[0].text_content().strip()
            except:
                siteName = ''

        try:
            subSite = detailsPageElements.xpath('//i[contains(., "Site")]//preceding-sibling::a[1]')[0].text_content().strip()
        except:
            subSite = ''

        if siteName:
            siteDisplay = '%s/%s' % (siteName, subSite) if subSite else siteName
        else:
            siteDisplay = subSite

        titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content(), siteNum)
        curID = PAutils.Encode(sceneURL)

        try:
            date = detailsPageElements.xpath('//span[@class][./*[contains(.., "date")]]')[0].text_content().split(':', 2)[-1].strip()
        except:
            date = ''

        if date and not date == 'unknown':
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        displayDate = releaseDate if date else ''

        if sceneID == urlID:
            score = 100
        elif searchData.date and displayDate:
            score = 80 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 80 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        if score == 80:
            count += 1
            temp.append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, siteDisplay, displayDate), score=score, lang=lang))
        else:
            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, siteDisplay, displayDate), score=score, lang=lang))

    for result in temp:
        if count > 1 and result.score == 80:
            results.Append(MetadataSearchResult(id=result.id, name=result.name, score=79, lang=lang))
        else:
            results.Append(MetadataSearchResult(id=result.id, name=result.name, score=result.score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content(), siteNum)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="gen12"]/p[contains(., "Story")]')[0].text_content().split('\n', 2)[-1]
    except:
        pass

    # Studio
    try:
        metadata.studio = detailsPageElements.xpath('//i[contains(., "Network")]//preceding-sibling::a[1]')[0].text_content().strip()
    except:
        try:
            metadata.studio = detailsPageElements.xpath('//i[contains(., "Studio")]//preceding-sibling::a[1]')[0].text_content().strip()
        except:
            pass

    # Tagline and Collection(s)
    metadata.collections.clear()
    try:
        tagline = detailsPageElements.xpath('//i[contains(., "Site")]//preceding-sibling::a[1]')[0].text_content().strip()
        if len(metadata_id) > 3:
            Log('Using original series information')
            tagline = detailsPageElements.xpath('//p[contains(., "Serie")]//a[@title]')[0].text_content().strip()
            metadata.title = ("%s [Scene %s]" % (metadata_id[3], metadata_id[4]))
        if not metadata.studio:
            metadata.studio = tagline
        else:
            metadata.tagline = tagline
        metadata.collections.add(tagline)
    except:
        metadata.collections.add(metadata.studio)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    else:
        date_object = parse(detailsPageElements.xpath('//span[contains(., "Release")]')[0].text_content().split(':', 1)[1].strip())
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[./b[contains(., "Categories")]]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//p[contains(., "Starring")]//following-sibling::a[1]')
    if actors:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//img[contains(@src, "th8")]/@src',
    ]

    try:
        req = PAutils.HTTPRequest(detailsPageElements.xpath('//@href[contains(., "viewer")]')[0])
        photoPageElements = HTML.ElementFromString(req.text)
        for xpath in xpaths:
            for img in photoPageElements.xpath(xpath):
                art.append(img.replace('/th8', ''))
    except:
        pass

    try:
        img = detailsPageElements.xpath('//div[@id="moviewrap"]//@src')[0]
        art.append(img)
    except:
        pass

    images = []
    posterExists = False
    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.data18.com'})
                images.append(image)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if height > width:
                    # Item is a poster
                    posterExists = True
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    if not posterExists:
        for idx, image in enumerate(images, 1):
            try:
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[art[idx - 1]] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
