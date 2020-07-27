import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="update_details"]'):
        curID = PAutils.Encode(searchResult.xpath('./a[last()]/@href')[0])
        titleNoFormatting = searchResult.xpath('./a[last()]')[0].text_content().strip()
        releaseDate = searchResult.xpath('.//div[@class="cell update_date"]')[0].text_content().strip()
        if not releaseDate:
            try:
                releaseDate = str(searchResult.xpath('.//div[@class="cell update_date"]/comment()')[0]).strip()
                releaseDate = releaseDate[releaseDate.find('OFF') + 4:releaseDate.find('D', releaseDate.find('OFF') + 4)].strip()
            except:
                pass

        if releaseDate:
            releaseDate = parse(releaseDate).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//span[@class="title_bar_hilite"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[@class="update_description"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Jules Jordan'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    try:
        dvdName = detailsPageElements.xpath('//span[@class="update_dvds"]')[0].text_content().replace('Movie:', '').strip()
        metadata.collections.add(dvdName)
    except:
        pass

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//span[@class="update_tags"]/a'):
        genreName = genreLink.text_content().strip().lower()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    if PAsearchSites.getSearchSiteName(siteID) == "GirlGirl":
        actors = detailsPageElements.xpath('//div[@class="item"]/span/div/a')
    else:
        actors = detailsPageElements.xpath('//div[@class="backgroundcolor_info"]/span[@class="update_models"]/a')

    if actors:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ''

            actorPageURL = actorLink.get('href')
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            try:
                actorPhotoURL = actorPage.xpath('//img[@class="model_bio_thumb stdimage thumbs target"]/@src0_3x')[0]
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                pass

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    try:
        bigScript = detailsPageElements.xpath('//script[contains(text(), "df_movie")]')[0].text_content()
        alpha = bigScript.find('useimage = "') + 12
        omega = bigScript.find('";', alpha)
        background = bigScript[alpha:omega]
        if 'http' not in background:
            background = PAsearchSites.getSearchBaseURL(siteID) + background
        art.append(background)
    except:
        pass

    # Slideshow of images from the Search page
    try:
        bigScript = detailsPageElements.xpath('//script[contains(text(), "df_movie")]')[0].text_content()
        alpha = bigScript.find('setid:"') + 7
        omega = bigScript.find('",', alpha)
        setID = bigScript[alpha:omega]

        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteID) + urllib.quote(metadata.title))
        searchPageElements = HTML.ElementFromString(req.text)
        posterUrl = searchPageElements.xpath('//img[@id="set-target-%s"]/@src' % setID)[0]
        if 'http' not in posterUrl:
            posterUrl = PAsearchSites.getSearchBaseURL(siteID) + posterUrl

        art.append(posterUrl)
        for i in range(0, 7):
            try:
                posterUrl = searchPageElements.xpath('//img[@id="set-target-%s"]/@src%d_1x' % (setID, i))[0]
                if 'http' not in posterUrl:
                    posterUrl = PAsearchSites.getSearchBaseURL(siteID) + posterUrl

                art.append(posterUrl)
            except:
                pass
    except:
        pass

    # Photos page
    try:
        photoPageURL = detailsPageElements.xpath('//div[@class="cell content_tab"]/a[text()="Photos"]')[0].get('href')
        req = PAutils.HTTPRequest(photoPageURL)
        photoPageElements = HTML.ElementFromString(req.text)
        bigScript = photoPageElements.xpath('//script[contains(text(),"var ptx")]')[0].text_content()
        ptx1600starts = bigScript.find('1600')
        ptx1600ends = bigScript.find('togglestatus', ptx1600starts)
        ptx1600 = bigScript[ptx1600starts:ptx1600ends]
        photos = []
        imageCount = ptx1600.count('ptx["1600"][')
        for i in range(1, imageCount + 1):
            alpha = ptx1600.find('{src: "', omega) + 7
            omega = ptx1600.find('"', alpha)
            posterUrl = ptx1600[alpha:omega]
            if 'http' not in posterUrl:
                posterUrl = PAsearchSites.getSearchBaseURL(siteID) + posterUrl
            photos.append(posterUrl)
        for x in range(10):
            art.append(photos[random.randint(1, imageCount)])
    except:
        pass

    # Vidcaps page
    try:
        capsPageURL = detailsPageElements.xpath('//div[@class="cell content_tab"]/a[text()="Caps"]')[0].get('href')
        req = PAutils.HTTPRequest(capsPageURL)
        capsPageElements = HTML.ElementFromString(req.text)
        bigScript = capsPageElements.xpath('//script[contains(text(),"var ptx")]')[0].text_content()
        ptxjpgstarts = bigScript.find('ptx["jpg"] = {};')
        ptxjpgends = bigScript.find('togglestatus', ptxjpgstarts)
        ptxjpg = bigScript[ptxjpgstarts:ptxjpgends]
        vidcaps = []
        imageCount = ptxjpg.count('ptx["jpg"][')
        for i in range(1, imageCount + 1):
            alpha = ptxjpg.find('{src: "', omega) + 7
            omega = ptxjpg.find('"', alpha)
            posterUrl = ptxjpg[alpha:omega]
            if 'http' not in posterUrl:
                posterUrl = PAsearchSites.getSearchBaseURL(siteID) + posterUrl
            vidcaps.append(posterUrl)
        for x in range(10):
            art.append(vidcaps[random.randint(1, imageCount)])
    except:
        pass

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
