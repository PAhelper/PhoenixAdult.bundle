import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.lower().replace(' ', '-', 1).replace(' ', '_')
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)

    titleNoFormatting = searchResults.xpath('//h1')[0].text_content().strip()
    curID = encodedTitle

    date = searchResults.xpath('//span[@class="date-display-single"] | //span[@class="u-inline-block u-mr--nine"] | //div[@class="video-meta-date"] | //div[@class="date"]')[0].text_content().strip()
    releaseDate = parse(date).strftime('%Y-%m-%d')

    score = 100

    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAsearchSites.getSearchSearchURL(siteID) + metadata_id[0]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="video-group-bottom"]/p | //p[@class="u-lh--opt"] | //div[@class="video-info"]/p | //div[@class="desc"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'HighTechVR'

    # Tagline and Collection
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//title')[0].text_content().split('|')[1].strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="date-display-single"] | //span[@class="u-inline-block u-mr--nine"] | //div[@class="video-meta-date"] | //div[@class="date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[contains(@class, "video-tags")]//a | //div[@class="tags"]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="video-actress-name"]//a | //div[@class="u-mt--three u-mb--three"]//a | //div[@class="model-one-inner js-trigger-lazy-item"]//a | //div[@class="featuring commed"]//a'):
        actorName = actorLink.text_content().strip()

        actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPage.xpath('//div[contains(@class, "model-img-wrapper")]/figure/a/img | //div[contains(@class, "u-ratio--model-poster")]//img | //div[contains(@class, "model-one-inner")]//img | //div[contains(@class, "row actor-info")]//img')[0].get('src').split('?')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    for poster in detailsPageElements.xpath('//div[contains(@class,"video-gallery")]//div//figure//a | //a[@class="u-block u-ratio u-ratio--lightbox u-bgc--back-opt u-z--zero"] | //div[@class="scene-previews-container"]//a'):
        img = poster.get('href').split('?')[0]
        if img.startswith('http'):
            art.append(img)

    poster = detailsPageElements.xpath('//div[@class="splash-screen fullscreen-message is-visible"]/@style')[0]
    img = poster.split('url(')[1].split(')')[0]
    art.append(img)

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
