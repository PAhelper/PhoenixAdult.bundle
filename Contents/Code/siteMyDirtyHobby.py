import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    if siteNum == 1237:
        headers = {"Accept-Language": "en-EN,en;q=0.5"}
        url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded

        req = PAutils.HTTPRequest(url, headers=headers)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@id="search-results"]//li[contains(@class, "video-panel-item")]'):
            sceneURL = searchResult.xpath('.//a/@href')[0]
            titleNoFormatting = searchResult.xpath('.//h4')[0].text_content().strip()

            curID = PAutils.Encode(sceneURL)

            date = searchResult.xpath('//i[contains(@class, "fa-calendar")]/parent::dd')[0].text_content().strip()
            releaseDate = parse(date).strftime('%Y-%m-%d')

            if searchData.date and releaseDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [MyDirtyHobby] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    else:
        headers = {"Accept-Language": "de-DE,de;q=0.5"}
        searchResults = []

        googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum, lang='de')
        for sceneURL in googleResults:
            sceneURL = sceneURL.replace('www.mydirtyhobby.de', 'de.mydirtyhobby.com')
            if '/videos/' in sceneURL:
                searchResults.append(sceneURL)
        for sceneURL in searchResults:
            req = PAutils.HTTPRequest(sceneURL, headers=headers)
            detailsPageElements = HTML.ElementFromString(req.text)

            titleNoFormatting = detailsPageElements.xpath('//div[@class="page-header clearfix"]/h1')[0].text_content()

            curID = PAutils.Encode(sceneURL)

            releaseDate = parse(detailsPageElements.xpath('//div[contains(@class, "info-wrapper")]//i[contains(@class, "calendar")]')[0].text_content().strip()).strftime('%d.%m.%y')

            if searchData.date and releaseDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [MyDirtyHobby] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    if siteNum == 1237:
        headers = {"Accept-Language": "en-EN,en;q=0.5"}
    else:
	    headers = {"Accept-Language": "de-DE,de;q=0.5"}
    req = PAutils.HTTPRequest(sceneURL, headers=headers)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    summary = detailsPageElements.xpath('//div[contains(@class, "video-description")]/p/text()')[0].strip()
    metadata.summary = summary

    # Studio
    metadata.studio = 'MyDirtyHobby'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//div[@class="info-wrapper"]//a')[0].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.collections.add('MyDirtyHobby')

    # Release Date
    date = detailsPageElements.xpath('//i[contains(@class, "fa-calendar")]/parent::dd')[0].text_content().strip()
    if date:
        if siteNum == 1237:
            date_object = datetime.strptime(date, '%m/%d/%y')
        else:
            date_object = datetime.strptime(date, '%d.%m.%y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//dd/a[@title and contains(@href, "/videos/")]'):
        genreName = genreLink.text_content().strip().lower()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[contains(@class, "profile-head-wrapper")]'):
        actorName = actorLink.xpath('.//span[contains(@class, "profile")]')[0].text_content().strip()
        actorPhotoURL = actorLink.xpath('.//div[@id="profile-avatar"]//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="video-preview-image"]//img/@src',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
