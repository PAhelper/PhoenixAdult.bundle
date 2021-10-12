import PAsearchSites
import PAutils

supported_lang = ['en', 'de', 'fr', 'es', 'it']


def search(results, lang, siteNum, searchData):
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded

    headers = {}
    if lang in supported_lang:
        url = url.replace('://en.', '://%s.' % lang, 1)
        headers['Accept-Language'] = lang

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

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL

    headers = {}
    if lang in supported_lang:
        sceneURL = sceneURL.replace('://en.', '://%s.' % lang, 1)
        headers['Accept-Language'] = lang

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
        date_object = parse(date)
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
