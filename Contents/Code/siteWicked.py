import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.replace(' ', '-')
    if '/' not in encodedTitle:
        encodedTitle.replace('-', '/', 1)

    if 'scene' not in encodedTitle.lower():
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@class="sceneContainer"]'):
            titleNoFormatting = searchResult.xpath('.//h3')[0].text_content().strip().title().replace('Xxx', 'XXX')
            curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
            releaseDate = parse(searchResult.xpath('.//p[@class="sceneDate"]')[0].text_content().strip()).strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Wicked/Scene] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

        dvdTitle = searchResults.xpath('//h3[@class="dvdTitle"]')[0].text_content().strip().title().replace('Xxx', 'XXX')
        curID = PAutils.Encode(searchResults.xpath('//link[@rel="canonical"]/@href')[0])
        releaseDate = parse(searchResults.xpath('//li[@class="updatedOn"]')[0].text_content().replace('Updated', '').strip()).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), dvdTitle.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Wicked/Full Movie] %s' % (dvdTitle, releaseDate), score=score, lang=lang))

    else:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + '/en/video/' + encodedTitle)
        searchResults = HTML.ElementFromString(req.text)
        titleNoFormatting = searchResults.xpath('//h1//span')[0].text_content().strip().title().replace('Xxx', 'XXX')
        curID = PAutils.Encode(searchResults.xpath('//link[@rel="canonical"]/@href')[0])
        releaseDate = parse(searchResults.xpath('//li[@class="updatedDate"]')[0].text_content().replace('Updated', '').replace('|', '').strip()).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Wicked/Scene] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.starstswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    metadata.title = detailsPageElements.xpath('//h1//span')[0].text_content().strip().title().replace('Xxx', 'XXX')

    # Studio
    metadata.studio = 'Wicked Pictures'

    # Release Date
    date = detailsPageElements.xpath('//li[@class="updatedOn"] | //li[@class="updatedDate"]')[0].text_content().replace('Updated', '').replace('|', '').strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Scene update
    if '/video/' in url:

        # Genres
        for genreLink in detailsPageElements.xpath('//div[contains(@class, "sceneColCategories")]/a'):
            genreName = genreLink.text_content().strip()

            movieGenres.addGenre(genreName)

        # Actors
        for actorLink in detailsPageElements.xpath('//div[contains(@class, "sceneColActors")]//a'):
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            try:
                actorPageURL = urlBase + actorLink.get('href')
                req = PAutils.HTTPRequest(actorPageURL)
                actorPage = HTML.ElementFromString(req.text)
                actorPhotoURL = actorPage.xpath('//img[@class="actorPicture"]/@src')[0]
            except:
                pass

            movieActors.addActor(actorName, actorPhotoURL)

        script_text = detailsPageElements.xpath('//script')[7].text_content()

        # Background
        alpha = script_text.find('picPreview":"')
        omega = script_text.find('"', alpha + 13)
        previewBG = script_text[alpha + 13:omega].replace('\/', '/')
        art.append(previewBG)

        # Get dvd page for some info
        dvdPageURL = urlBase + detailsPageElements.xpath('//div[@class="content"]//a[contains(@class,"dvdLink")]/@href')[0]
        req = PAutils.HTTPRequest(dvdPageURL)
        dvdPageElements = HTML.ElementFromString(req.text)

        # Tagline and Collection(s)
        tagline = dvdPageElements.xpath('//h3[@class="dvdTitle"]')[0].text_content().strip().title().replace('Xxx', 'XXX')
        metadata.tagline = tagline
        metadata.collections.add(tagline)

        # Summary
        try:
            metadata.summary = dvdPageElements.xpath('//p[@class="descriptionText"]')[0].text_content().strip()
        except:
            pass

        # Director
        director = metadata.directors.new()
        try:
            directors = dvdPageElements.xpath('//ul[@class="directedBy"]')
            for dirname in directors:
                director.name = dirname.text_content().strip()
        except:
            pass

        # DVD cover
        dvdCover = dvdPageElements.xpath('//img[@class="dvdCover"]/@src')[0]
        art.append(dvdCover)

        # Extra photos for the completist
        photoPageURL = urlBase + detailsPageElements.xpath('//div[contains(@class, "picturesItem")]//a')[0].get('href').split('?')[0]
        req = PAutils.HTTPRequest(photoPageURL)
        photoPageElements = HTML.ElementFromString(req.text)

        #  good 2:3 poster picture
        poster = photoPageElements.xpath('//div[@class="previewImage"]//img/@src')[0]
        art.append(poster)

        #  more Pictures
        extraPix = photoPageElements.xpath('//li[@class="preview"]//a[@class="imgLink pgUnlocked"]/@href')
        for pictureURL in extraPix:
            art.append(pictureURL)

    #  Full DVD update
    else:
        # Genres
        for genreLink in detailsPageElements.xpath('//p[@class="dvdCol"]/a'):
            genreName = genreLink.text_content().strip()

            movieGenres.addGenre(genreName)

        # Actors
        for actorLink in detailsPageElements.xpath('//div[@class="actorCarousel"]//a'):
            actorName = actorLink.xpath('.//span')[0].text_content().strip()
            actorPhotoURL = ''

            try:
                actorPhotoURL = actorLink.xpath('.//img/@src')[0].get("src")
            except:
                pass

            movieActors.addActor(actorName, actorPhotoURL)

        # Tagline/collections
        tagline = 'Wicked Pictures'
        metadata.tagline = tagline
        metadata.collections.add(tagline)

        # Summary
        try:
            metadata.summary = detailsPageElements.xpath('//p[@class="descriptionText"]')[0].text_content().strip()
        except:
            pass

        # Director
        director = metadata.directors.new()
        try:
            directors = detailsPageElements.xpath('//ul[@class="directedBy"]')
            for dirname in directors:
                director.name = dirname.text_content().strip()
        except:
            pass

        # Backgrounds
        scenePreviews = detailsPageElements.xpath('//div[@class="sceneContainer"]//img[contains(@id,"clip")]/@data-original')
        for scenePreview in scenePreviews:
            previewIMG = scenePreview.split('?')[0]

            art.append(previewIMG)

        # DVD cover
        dvdCover = detailsPageElements.xpath('//img[@class="dvdCover"]/@src')[0]
        art.append(dvdCover)

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
