import PAsearchSites
import PAgenres
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResultsURLs = []
    googleResults = PAutils.getFromGoogleSearch(searchTitle, siteNum)

    for sceneURL in googleResults:
        if sceneURL not in searchResultsURLs:
            if '/scene/' in sceneURL:
                searchResultsURLs.append(sceneURL)

    for url in searchResultsURLs:
        detailsPageElements = HTML.ElementFromURL(url)
        curID = String.Encode(url)
        titleNoFormatting = detailsPageElements.xpath('//h4')[0].text_content().strip()
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [FPN/%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.replace(' ', '_'))
    for searchResult in searchResults.xpath('//div[contains(@class, "section-updates")]'):
        curID = String.Encode(searchResult.xpath('.//a/@href')[0])
        titleNoFormatting = searchResult.xpath('.//div[contains(@class, "scene-info")]//a')[0].text_content().strip()
        poster = searchResult.xpath('.//img/@src')[0]
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, releaseDate, poster), name='%s [FPN/%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    url = String.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    poster = metadata_id[3] if len(metadata_id) > 3 else None

    detailsPageElements = HTML.ElementFromURL(url)

    # Studio
    metadata.studio = 'Full Porn Network'

    # Title
    metadata.title = detailsPageElements.xpath('//h4')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="hide-for-small-only"]')[0].text_content().strip()

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Tagline and Collection(s)
    metadata.collections.clear()
    for seriesName in [metadata.studio, PAsearchSites.getSearchSiteName(siteID)]:
        metadata.collections.add(seriesName)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="small-12"]//a[contains(@href, "/category/")]/text()')
    for genreLink in genres:
        genreName = genreLink.strip()
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="small-12"]//a[contains(@href, "/model/")]/@href')
    for actorLink in actors:
        actorPage = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteID) + actorLink)
        actorName = actorPage.xpath('//h1')[0].text_content().strip()
        actorPhotoURL = actorPage.xpath('//img[@alt="%s"]/@src' % actorName)[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [
        poster
    ]

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
