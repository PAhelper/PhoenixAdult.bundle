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
            sceneURL = '%s/scenes/%s' % (PAsearchSites.getSearchBaseURL(siteNum), sceneID)
            searchResults.append(sceneURL)

    searchData.encoded = searchData.title.replace('\'', '').replace(',', '').replace('& ', '')
    searchURL = '%s%s&key2=%s&next=1&page=0' % (PAsearchSites.getSearchSearchURL(siteNum), searchData.encoded, searchData.encoded)
    req = PAutils.HTTPRequest(searchURL, headers={'Referer': 'https://www.data18.com'})
    searchPageElements = HTML.ElementFromString(req.text)

    searchPages = re.search(r'(?<=pages:\s).*(?=])', req.text)
    if searchPages:
        numSearchPages = int(searchPages.group(0))
    else:
        numSearchPages = 1

    for idx in range(0, numSearchPages):
        for searchResult in searchPageElements.xpath('//a'):
            sceneURL = searchResult.xpath('./@href')[0]

            if ('/scenes/' in sceneURL and sceneURL not in searchResults):
                urlID = re.sub(r'.*/', '', sceneURL)

                try:
                    siteDisplay = PAutils.parseTitle(searchResult.xpath('.//i')[0].text_content().strip(), siteNum)
                except:
                    siteDisplay = ''

                titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//p[@class="gen12 bold"]')[0].text_content(), siteNum)
                curID = PAutils.Encode(sceneURL)

                if '...' in titleNoFormatting:
                    searchResults.append(sceneURL)
                else:
                    siteResults.append(sceneURL)

                    try:
                        date = searchResult.xpath('.//span[@class="gen11"]/text()')[0].strip()
                    except:
                        date = ''

                    if date and not date == 'unknown':
                        releaseDate = datetime.strptime(date, "%B %d, %Y").strftime('%Y-%m-%d')
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

        if numSearchPages > 1 and not idx + 1 == numSearchPages:
            searchURL = '%s%s&key2=%s&next=1&page=%d' % (PAsearchSites.getSearchSearchURL(siteNum), searchData.encoded, searchData.encoded, idx + 1)
            req = PAutils.HTTPRequest(searchURL, headers={'Referer': 'https://www.data18.com'})
            searchPageElements = HTML.ElementFromString(req.text)

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.replace('/content/', '/scenes/').replace('http:', 'https:')
        if ('/scenes/' in sceneURL and '.html' not in sceneURL and sceneURL not in searchResults and sceneURL not in siteResults):
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)
        urlID = re.sub(r'.*/', '', sceneURL)

        try:
            siteName = detailsPageElements.xpath('//b[contains(., "Network")]//following-sibling::b')[0].text_content().strip()
        except:
            try:
                siteName = detailsPageElements.xpath('//b[contains(., "Studio")]//following-sibling::a')[0].text_content().strip()
            except:
                siteName = ''

        try:
            subSite = detailsPageElements.xpath('//p[contains(., "Site:")]//following-sibling::a[@class="bold"]')[0].text_content().strip()
        except:
            subSite = ''

        if siteName:
            siteDisplay = '%s/%s' % (siteName, subSite) if subSite else siteName
        else:
            siteDisplay = subSite

        titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content(), siteNum)
        curID = PAutils.Encode(sceneURL)

        try:
            date = detailsPageElements.xpath('//@datetime')[0].strip()
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


def update(metadata, lang, siteNum, movieGenres, movieActors, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content(), siteNum)

    # Summary
    try:
        summary = detailsPageElements.xpath('//div[@class="gen12"]/div[contains(., "Story")]')[0].text_content().split('Story -')[-1].strip()
    except:
        try:
            summary = detailsPageElements.xpath('//div[@class="gen12"]/div[contains(., "Description")]')[0].text_content().rsplit('---')[-1].strip()
        except:
            summary = ''

    metadata.summary = summary

    # Studio
    try:
        metadata.studio = detailsPageElements.xpath('//b[contains(., "Network")]//following-sibling::b')[0].text_content().strip()
    except:
        try:
            metadata.studio = detailsPageElements.xpath('//b[contains(., "Studio")]//following-sibling::a')[0].text_content().strip()
        except:
            pass

    # Tagline and Collection(s)
    metadata.collections.clear()
    try:
        tagline = detailsPageElements.xpath('//p[contains(., "Site:")]//following-sibling::a[@class="bold"]')[0].text_content().strip()
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
        date_object = detailsPageElements.xpath('//span[contains(., "Release date")]')[0].text_content().strip().replace("Release date: ","").replace(", more updates...","")
        Log(date_object)
             
        # Month
        month = 0
        if "January" in date_object:
            month = 1
            date_object = date_object.replace('January ','')
        elif "February" in date_object:
            month = 2 
            date_object = date_object.replace('February ','')
        elif "March" in date_object:
            month = 3 
            date_object = date_object.replace('March ','')
        elif "April" in date_object:
            month = 4
            date_object = date_object.replace('April ','')
        elif "May" in date_object:
            month = 5
            date_object = date_object.replace('May ','')
        elif "June" in date_object:
            month = 6
            date_object = date_object.replace('June ','')
        elif "July" in date_object:
            month = 7
            date_object = date_object.replace('July ','')
        elif "August" in date_object:
            month = 8
            date_object = date_object.replace('August ','')
        elif "September" in date_object:
            month = 9
            date_object = date_object.replace('September ','')
        elif "October" in date_object:
            month = 10
            date_object = date_object.replace('October ','')     
        elif "November" in date_object:
            month = 11
            date_object = date_object.replace('November ','')
        elif "December" in date_object:
            month = 12
            date_object = date_object.replace('December ','')        
                
        #Day
        day = int(date_object[:2])
        Log('Day:' + date_object[:2])
                
        #Year
        date_object = date_object.replace(date_object[:4],'')
        year = int(date_object[:4])
           
        try:
            date_object = parse(year+'-'+month+'-'+day)
        except:
            date_object = datetime(year, month, day)
                
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[./b[contains(., "Categories")]]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath("//div[contains(@style,'margin-left: -15px;')]//a[contains(@href, '/name/')]//img")
    
    for actorLink in actors:
        actorName = actorLink.xpath('./@alt')[0].strip()
        actorPhotoURL = actorLink.xpath('./@data-src')[0].strip()

        if actorName:
            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    xpaths = [
        '//img[@id="photoimg"]/@src',
        '//img[contains(@src, "th8")]/@src',
        '//img[contains(@data-original, "th8")]/@data-original',
    ]

    try:
        if siteNum == 1073 or siteNum == 1370:
            cover = '//a[@class="pvideof"]/@href'
            img = detailsPageElements.xpath(cover)[0]
            art.append(img)
    except:
        pass

    try:
        galleries = detailsPageElements.xpath('//div[@id="galleriesoff"]//div')
        sceneID = re.sub(r'.*/', '', sceneURL)

        for gallery in galleries:
            galleryID = gallery.xpath('./@id')[0].replace('gallery', '')
            photoViewerURL = ("%s/sys/media_photos.php?s=1&scene=%s&pic=%s" % (PAsearchSites.getSearchBaseURL(siteNum), sceneID[1:], galleryID))
            req = PAutils.HTTPRequest(photoViewerURL)
            photoPageElements = HTML.ElementFromString(req.text)

            for xpath in xpaths:
                for img in photoPageElements.xpath(xpath):
                    art.append(img.replace('/th8', '').replace('-th8', ''))
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
