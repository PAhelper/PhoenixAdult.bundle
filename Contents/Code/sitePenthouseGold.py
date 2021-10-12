import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="scene"]'):
        url = searchResult.xpath('.//a[@data-track="TITLE_LINK"]/@href')[0]
        if '/scenes/' in url:
            curID = PAutils.Encode(url)
            titleNoFormatting = searchResult.xpath('.//a[@data-track="TITLE_LINK"]')[0].text_content()
            releaseDate = parse(searchResult.xpath('./span[@class="scene-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    # search for exact scene name
    urlTitle = searchData.encoded.replace('%20', '-')
    urls = [PAsearchSites.getSearchBaseURL(siteNum) + '/scenes/video---' + urlTitle + '_vids.html',
            PAsearchSites.getSearchBaseURL(siteNum) + '/scenes/movie---' + urlTitle + '_vids.html']

    for url in urls:
        try:
            sceneReq = PAutils.HTTPRequest(url)
            scenePage = HTML.ElementFromString(sceneReq.text)

            curID = PAutils.Encode(url)
            titleNoFormatting = scenePage.xpath('//div[@class="content-desc content-new-scene"]//h1')[0].text_content().strip()
            releaseDate = parse(scenePage.xpath('//meta[@itemprop="uploadDate"]')[0].get('content'))
            score = 100

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))
        except:
            pass

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
    metadata.title = detailsPageElements.xpath('//div[@class="content-desc content-new-scene"]//h1')[0].text_content().replace('Video -', '').replace('Movie -', '').strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="content-desc content-new-scene"]//p')[0].text_content().strip()
    except:
        pass

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//ul[contains(@class, "scene-tags")]/li'):
        genreName = genreLink.xpath('.//a')[0].text_content().lower()

        movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//meta[@itemprop="uploadDate"]')[0].get('content')
    if date:
        date_object = datetime.strptime(date, '%m/%d/%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    elif sceneDate:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorPage in detailsPageElements.xpath('//ul[@id="featured_pornstars"]//div[@class="model"]'):
        actorName = actorPage.xpath('.//h3')[0].text_content().strip()
        actorPhotoURL = actorPage.xpath('.//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [detailsPageElements.xpath('//div[@id="trailer_player_finished"]//img/@src')[0]]

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
