import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    directURL = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.replace(' ', '-').lower() + '/'

    searchResults = [directURL]
    googleResults = PAutils.getFromGoogleSearch(searchTitle, siteNum)
    for sceneURL in googleResults:
        if ('/video/' in sceneURL and sceneURL not in searchResults):
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        detailsPageElements = None
        try:
            detailsPageElements = HTML.ElementFromURL(sceneURL)
        except:
            pass

        if detailsPageElements:
            curID = PAutils.Encode(sceneURL)
            titleNoFormatting = detailsPageElements.xpath('//div[@class="single-part-details"]//h2')[0].text_content().strip()
            date = detailsPageElements.xpath('//div[@class="video-info-left-icon"]//span[3]/text()')[0].strip()
            releaseDate = datetime.strptime(date, '%d%b,%Y').strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    detailsPageElements = HTML.ElementFromURL(sceneURL)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="single-part-details"]//h2')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[(contains(@class, "video-bottom-txt"))]')[0].text_content().strip()

    # Studio/Tagline/Collection
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[(contains(@class, "video-tag-section"))]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[(contains(@class, "video-info-left pull-left"))]/h3/span/a'):
        actorName = actorLink.text_content().strip()
        actorPageURL = actorLink.get('href')

        actorPage = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPage.xpath('//div[(contains(@class, "single-porn-pic"))]/img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)
	
    # Release Date
    date = detailsPageElements.xpath('//div[@class="video-info-left-icon"]//span[3]/text()')[0].strip()
    date_object = datetime.strptime(date, '%d%b,%Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Posters/Background
    art = []
    xpaths = [
        '//div[(contains(@class, "sub-video"))]/a/@href'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            poster = poster.split('?')[0]

            art.append(poster)

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
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
