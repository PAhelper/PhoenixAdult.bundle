import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.replace(' ', '-').replace('--', '-').replace('\'', '').lower()
    if '/' not in searchData.encoded and re.match(r'\d+.*', searchData.encoded):
        searchData.encoded = searchData.encoded.replace('-', '/', 1)

    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    curID = PAutils.Encode(sceneURL)
    titleNoFormatting = detailsPageElements.xpath('//h1[@class="title"] | //h2[@class="title"]')[0].text_content().strip()

    date = detailsPageElements.xpath('//span[contains(@class, "date")] | //span[contains(@class, "hide")]')
    if date:
        releaseDate = parse(date[0].text_content().strip()).strftime('%Y-%m-%d')
    else:
        releaseDate = searchData.dateFormat() if searchData.date else ''
    displayDate = releaseDate if date else ''

    if searchData.date and displayDate:
        score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
    else:
        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

    results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="title"] | //h2[@class="title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "desc")]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Stepped Up Media'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    if tagline == 'Swallowed':
        movieGenres.addGenre('Blowjob')
        movieGenres.addGenre('Cum Swallow')
    elif tagline in ['TrueAnal', 'AllAnal', 'AnalOnly']:
        movieGenres.addGenre('Anal')
        movieGenres.addGenre('Gaping')
    elif tagline == 'Nympho':
        movieGenres.addGenre('Nympho')
    movieGenres.addGenre('Hardcore')
    movieGenres.addGenre('Heterosexual')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('(//h4[@class="models"])[1]//a')
    for actorLink in actors:
        actorName = actorLink.text_content().strip()

        actorPageURL = actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPage.xpath('//div[contains(@class, "model")]//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)
    movieActors.addActor('Mike Adriano', 'https://imgs1cdn.adultempire.com/actors/470003.jpg')

    # Posters
    art = []
    xpaths = [
        '//div[@id="trailer-player"]/@data-screencap',
        '//video[contains(@id, "ypp-player")]/@poster',
        '//a[@href="%s"]//img/@src' % sceneURL,
        '//div[@class="view-thumbs"]//img/@src',
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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
