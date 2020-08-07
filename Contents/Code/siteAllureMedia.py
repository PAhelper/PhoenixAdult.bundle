import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)

    # Amateur Allure
    if siteNum == 564:
        for searchResult in searchResults.xpath('//div[@class="update_details"]'):
            titleNoFormatting = searchResult.xpath('.//div[@class="update_title"]/a')[0].text_content().strip()
            releaseDate = parse(searchResult.xpath('.//div[@class="update_date"]')[0].text_content().replace('Added:', '').strip()).strftime('%Y-%m-%d')
            curID = PAutils.Encode(searchResult.xpath('.//a[1]/@href')[0])

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            if len(titleNoFormatting) > 29:
                titleNoFormatting = titleNoFormatting[:32] + '...'

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    # Swallow Salon
    if siteNum == 565:
        for searchResult in searchResults.xpath('//div[@class="update_details"]'):
            titleNoFormatting = searchResult.xpath('./a[2]')[0].text_content().strip()
            releaseDate = parse(searchResult.xpath('.//div[@class="cell update_date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            curID = PAutils.Encode(searchResult.xpath('./a[2]/@href')[0])

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            if len(titleNoFormatting) > 29:
                titleNoFormatting = titleNoFormatting[:32] + '...'

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[@class="update_description"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Allure Media'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class,"update_date")]')[0].text_content().strip()
    if not date:
        try:
            date = str(detailsPageElements.xpath('.//div[@class="cell update_date"]/comment()')[0]).strip()
            date = date[date.find('OFF') + 4:date.find('D', date.find('OFF') + 4)].strip()
        except:
            pass

    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//span[@class="update_tags"]//a'):
        genreName = genreLink.text_content().strip('\n').lower()

        movieGenres.addGenre(genreName)
    movieGenres.addGenre('Amateur')

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="backgroundcolor_info"]//span[@class="update_models"]/a'):
        actorName = str(actorLink.text_content().strip())

        actorPageURL = actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        img = actorPage.xpath('//div[@class="cell_top cell_thumb"]/img/@src')
        if img:
            actorPhotoURL = img[0]
            if not actorPhotoURL.startswith('http'):
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL

        movieActors.addActor(actorName, actorPhotoURL)

    # Manually Add Actors
    for actorName in ['Faith', 'Nikki Rhodes', 'Talia Tyler', 'Hadley', 'Evangeline', 'Zoe Voss', 'Raquel Diamond', 'Shay Golden', 'Emily Grey',
                      'Allyssa Hall', 'Alexa Grace', 'Remy LaCroix', 'Nadine Sage', 'Chloe Starr', 'Melissa Moore', 'Taylor Renae', 'Veronica Rodriguez',
                      'Naomi Woods', 'Amanda Aimes', 'Alice Green', 'Kimber Woods', 'Alina Li', 'Holly Michaels', 'Layla London', 'Dakota Brookes', 'Adriana Chechik',
                      'Belle Noire', 'Lilly Banks', 'Linda Lay', 'Miley May', 'Belle Knox', 'Ava Taylor', 'Stella May', 'Claire Heart', 'Kennedy Leigh', 'Lucy Tyler',
                      'Cadence Lux', 'Goldie Glock', 'Jayma Reid', 'Samantha Sin', 'Emma Hix', 'Lexi Mansfield', 'Emma Wilson', 'Kenzie Reeves', 'Devon Green', 'Jane Wilde',
                      'Lena Anderson', 'Lilly Banks', 'Linda Lay', 'Belle Knox', 'Miley May'
                      ]:
        if actorName in metadata.title or actorName in metadata.summary:
            movieActors.addActor(actorName, '')

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
    photoPageURL = None
    photoPageURL = detailsPageElements.xpath('//div[@class="cell content_tab"]/a[text()="Photos"]/@href')[0]
    req = PAutils.HTTPRequest(photoPageURL)
    photoPageElements = HTML.ElementFromString(req.text)
    bigScript = photoPageElements.xpath('//script[contains(text(), "var ptx")]')[0].text_content()
    try:
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
            if i == 5:
                actorPhotoURL = posterUrl
            photos.append(posterUrl)
        for x in range(10):
            art.append(photos[random.randint(1, imageCount)])
    except:
        pass

    # Vidcaps page
    try:
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
            if i == 5:
                actorPhotoURL = posterUrl
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
                referer = photoPageURL if photoPageURL else sceneURL
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': referer})
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
