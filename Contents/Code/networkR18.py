import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    searchJAVID = None
    splitSearchTitle = searchTitle.split(' ')
    if(unicode(splitSearchTitle[1], 'UTF-8').isdigit()):
        searchJAVID = '%s%%2B%s' % (splitSearchTitle[0], splitSearchTitle[1])

    if searchJAVID:
        encodedTitle = searchJAVID

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//li[contains(@class, "item-list")]'):
        titleNoFormatting = searchResult.xpath('.//dt')[0].text_content().strip()
        JAVID = searchResult.xpath('.//img/@alt')[0]
        sceneURL = searchResult.xpath('.//a/@href')[0].rsplit('/', 1)[0]
        curID = PAutils.Encode(sceneURL)

        if searchJAVID:
            score = 100 - Util.LevenshteinDistance(searchJAVID.lower(), JAVID.lower())
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s' % (JAVID, titleNoFormatting), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//cite[@itemprop="name"]')[0].text_content().strip()

    # Summary
    try:
        description = detailsPageElements.xpath('//div[@class="cmn-box-description01"]')[0].text_content()
        metadata.summary = description.replace('Product Description', '', 1).strip()
    except:
        pass

    # Studio
    metadata.studio = detailsPageElements.xpath('//dd[@itemprop="productionCompany"]')[0].text_content().strip()

    # Director
    director = metadata.directors.new()
    directorName = detailsPageElements.xpath('//dd[@itemprop="director"]')[0].text_content().strip()
    if directorName != '----':
        director.name = directorName

    # Release Date
    date = detailsPageElements.xpath('//dd[@itemprop="dateCreated"]')[0].text_content().strip().replace('.', '').replace(',', '').replace('Sept', 'Sep').replace('June', 'Jun').replace('July', 'Jul')
    date_object = datetime.strptime(date, '%b %d %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actor in detailsPageElements.xpath('//div[@itemprop="actors"]//span[@itemprop="name"]'):
        fullActorName = actor.text_content().strip()
        if fullActorName != '----':
            splitActorName = fullActorName.split('(')
            mainName = splitActorName[0].strip()

            actorPhotoURL = detailsPageElements.xpath('//div[@id="%s"]//img[contains(@alt, "%s")]/@src' % (mainName.replace(' ', ''), mainName))[0]
            if actorPhotoURL.rsplit('/', 1)[1] == 'nowprinting.gif':
                actorPhotoURL = ''

            if len(splitActorName) > 1 and mainName == splitActorName[1][:-1]:
                actorName = mainName
            else:
                actorName = fullActorName

            movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//a[@itemprop="genre"]'):
        genreName = genreLink.text_content().lower().strip()

        movieGenres.addGenre(genreName)
    metadata.collections.add('Japan Adult Video')

    # Posters
    art = []
    xpaths = [
        '//img[@itemprop="image"]/@src',
        '//img[contains(@alt, "cover")]/@src',
        '//section[@id="product-gallery"]//img/@data-src'
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
