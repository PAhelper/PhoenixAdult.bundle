import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.replace(' ', '-').replace('--', '-').lower()
    if '/' not in encodedTitle:
        encodedTitle = encodedTitle.replace('-', '/', 1)

    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    curID = PAutils.Encode(sceneURL)
    titleNoFormatting = detailsPageElements.xpath('//h1[@class="title"] | //h2[@class="title"]')[0].text_content().strip()

    date = detailsPageElements.xpath('//span[contains(@class,"date")] | //span[contains(@class,"hide")]')
    if date:
        releaseDate = parse(date[0].text_content().strip()).strftime('%Y-%m-%d')
    else:
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
    displayDate = releaseDate if date else ''

    if searchDate and displayDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

    results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

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
    metadata.title = detailsPageElements.xpath('//h1[@class="title"] | //h2[@class="title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class,"desc")]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Stepped Up Media'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
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
    elif tagline == "TrueAnal" or "AllAnal":
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
        actorPhotoURL = actorPage.xpath('//div[contains(@class,"model")]/img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)
    movieActors.addActor('Mike Adriano', 'https://imgs1cdn.adultempire.com/actors/470003.jpg')

    # Posters
    art = []
    xpaths = [
        '//div[@id="trailer-player"]/@data-screencap',
        '//video[@id="ypp-player"]/@poster',
        '//a[@href="%s"]//img/@src' % sceneURL,
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
