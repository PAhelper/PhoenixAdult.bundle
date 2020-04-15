import PAsearchSites
import PAgenres
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchResultsURLs = []
    googleResults = PAutils.getFromGoogleSearch(siteNum, searchTitle)

    for sceneURL in googleResults:
        if sceneURL not in searchResultsURLs:
            if '/trailers/' in sceneURL:
                searchResultsURLs.append(sceneURL)

    for url in searchResultsURLs:
        detailsPageElements = HTML.ElementFromURL(url)
        curID = url.replace('/', '_').replace('?', '!')
        titleNoFormatting = detailsPageElements.xpath('//div[contains(@class, "trailer_title")]')[0].text_content().strip()
        date = detailsPageElements.xpath('//div[@class="video-info"]//span/@data-dateadded')[0]
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [FPN/%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[contains(@class, "update")]'):
        curID = searchResult.xpath('.//a[@class="title"]/@href')[0].replace('/', '_').replace('?', '!')
        titleNoFormatting = searchResult.xpath('.//a[@class="title"]')[0].text_content().strip()
        date = searchResult.xpath('.//div[@class="info-column video-data"]/span[last()]')[0].text_content().strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [FPN/%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    url = metadata_id[0].replace('_', '/').replace('!', '?')

    detailsPageElements = HTML.ElementFromURL(url)

    # Studio
    metadata.studio = 'Full Porn Network'

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "trailer_title")]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="video-info"]//div[@class="text"]//p/text()')[1].strip()

    # Release Date
    date = detailsPageElements.xpath('//div[@class="video-info"]//span/@data-dateadded')[0]
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Tagline and Collection(s)
    metadata.collections.clear()
    for seriesName in [metadata.studio, PAsearchSites.getSearchSiteName(siteID)]:
        metadata.collections.add(seriesName)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="video-info"]//li/a')
    for genreLink in genres:
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="video-info"]//span[@class="update_models"]//a/@href')
    for actorLink in actors:
        actorPage = HTML.ElementFromURL(actorLink)
        actorName = actorPage.xpath('//h1[@class="model-name"]')[0].text_content().strip()
        actorPhotoURL = actorPage.xpath('//div[@class="model-image"]//img/@src0_1x')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [
        detailsPageElements.xpath('//div[@id="preview"]//img/@src0_2x')[0]
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
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
