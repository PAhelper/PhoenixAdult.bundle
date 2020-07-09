import PAsearchSites
import PAgenres
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    directURL = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.replace(' ', '-').lower()

    searchResults = [directURL]
    googleResults = PAutils.getFromGoogleSearch(searchTitle, siteNum)
    for sceneURL in googleResults:
        if ('/scene/' in sceneURL and sceneURL not in searchResults):
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        detailsPageElements = None
        try:
            detailsPageElements = HTML.ElementFromURL(sceneURL)
        except:
            pass

        if detailsPageElements:
            curID = PAutils.Encode(sceneURL)
            titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()
            date = detailsPageElements.xpath('//span[@class="date-display-single"] | //span[@class="u-inline-block u-mr--nine"] | //div[@class="video-meta-date"] | //div[@class="date"]')[0].text_content().strip()
            releaseDate = parse(date).strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split("|")
    sceneURL = PAutils.Decode(metadata_id[0])
    detailsPageElements = HTML.ElementFromURL(sceneURL)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "u-mb--six ")]')[0].text_content().strip()

    # Date
    date = detailsPageElements.xpath('//span[@class="date-display-single"] | //span[@class="u-inline-block u-mr--nine"] | //div[@class="video-meta-date"] | //div[@class="date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Studio/Tagline/Collection
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//a[contains(@href, "/list/category/")]'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//a[contains(@href, "/pornstars/model/")]'):
        actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get('href')
        actorPage = HTML.ElementFromURL(actorPageURL)

        actorName = actorLink.text_content()
        actorPhotoURL = actorPage.xpath('//div[contains(@class, "u-ratio--model-poster")]//img/@data-src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters/Background
    art = []
    xpaths = [
        '//div[contains(@class, "splash-screen")]/@style',
        '//a[contains(@class, "u-ratio--lightbox")]/@href',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            if poster.startswith('background-image'):
                poster.split('url(')[1].split(')')[0]

            art.append(poster)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if(width > 100 and idx > 1):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
