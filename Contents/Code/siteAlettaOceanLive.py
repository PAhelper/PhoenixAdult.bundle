import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []
    for page in range(1, 100):
        url = PAsearchSites.getSearchSearchURL(siteNum) % page
        req = PAutils.HTTPRequest(url)
        if req.ok:
            searchPageElements = HTML.ElementFromString(req.text)

            if searchPageElements.xpath('//div[contains(@class, "movie-set-list-item")]'):
                searchResult = searchPageElements.xpath('//div[contains(@class, "movie-set-list-item")][contains(., "%s")]' % searchData.title)
                if searchResult:
                    searchResults.append(searchResult[0])
                    break
            else:
                break
        else:
            break

    for searchResult in searchResults:
        sceneURL = searchResult.xpath('.//a/@href')[0]
        curID = PAutils.Encode(sceneURL)
        titleNoFormatting = searchResult.xpath('.//div[contains(@class, "movie-set-list-item__title")]')[0].text_content().strip()

        date = searchResult.xpath('.//div[contains(@class, "movie-set-list-item__date")]')[0].text_content().strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneID = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]

    req = PAutils.HTTPRequest(sceneID)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()

    # Actors
    movieActors.clearActors()
    movieActors.addActor('Aletta Ocean', '')

    # Posters
    art = []

    script = detailsPageElements.xpath('//script[contains(., "/trailers/")]')
    if script:
        regex = re.search(r'src=\"https://.*\.com/trailers/(\d+)\.', script[0].text_content().strip())
        if regex:
            sceneID = regex.group(1)
            for idx in range(0, 1):
                art.append('https://alettaoceanlive.com/tour/content/%s/%d.jpg' % (sceneID, idx))

    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
