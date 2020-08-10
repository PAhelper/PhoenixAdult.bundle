import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    if searchDate:
        encodedTitle = parse(searchDate).strftime('%Y/%m')
    else:
        encodedTitle = '?s=%s' % searchTitle.replace(' ', '+')

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//article'):
        sceneURL = searchResult.xpath('.//a/@href')[1].strip()
        curID = PAutils.Encode(sceneURL)
        titleNoFormatting = searchResult.xpath('.//h1 | .//h2')[0].text_content().strip()

        date = searchResult.xpath('.//div[@itemprop="datePublished"]')[0].text_content().strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        sceneID = 'N/A'
        imgNode = searchResult.xpath('.//img/@src')
        if imgNode:
            sceneID = imgNode[0].strip().rsplit('/', 1)[1].rsplit('.', 1)[0]

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s [%s] %s' % (sceneID, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchSearchURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    Title = detailsPageElements.xpath('//head/title')[0].text_content().strip().replace(' - HuCows.com', '')
    metadata.title = Title.title()

    # Studio
    metadata.studio = 'HuCows.com'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = 'HuCows'
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@itemprop="datePublished"]')[0].text_content().strip().replace('Release Date: ', '')
    date_object = datetime.strptime(date, '%d %b %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Summary
    try:
        description = detailsPageElements.xpath('//article/div[@class="entry-content"]/p')[0].text_content()
        metadata.summary = description.strip()
    except:
        pass

    # Genres
    movieGenres.clearGenres()

    # Default Genres
    genres = ['HuCows', 'Breasts', 'Nipples', 'Nipple Torture', 'Breast Torture', 'Fetish', 'BDSM']
    for genreName in genres:
        movieGenres.addGenre(genreName)

    # Dynamic Genres
    for genreLink in detailsPageElements.xpath('//div/span/a[@rel="category tag"]'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//a[@rel="tag"]'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div/article/div/a[@class="lightboxhover"]/img/@src',
        '//div/center/a/img[@class="lightboxhover"]/@src',
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
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
