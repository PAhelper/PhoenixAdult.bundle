import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "main-content")]//div[@class="-g-vc-grid"]'):
        titleNoFormatting = searchResult.xpath('./div[@class="-g-vc-item-title"]//a/@title')[0]
        subSite = searchResult.xpath('./div[@class="-g-vc-item-channel"]//a/@title')[0]
        curID = PAutils.Encode(searchResult.xpath('./div[@class="-g-vc-item-title"]//a/@href')[0])
        date = searchResult.xpath('./div[@class="-g-vc-item-date"]')[0].text_content().strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [LetsDoeIt/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Studio
    metadata.studio = 'Porndoe Premium'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="no-space transform-none"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//meta[@name="description"]/@content')[0].replace('&#039;', '\'')

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//div[@class="actors"]/h2/a')[0].text_content().strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//a[@class="inline-links"]'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="h5 h5-published nowrap color-rgba255-06"]')[0].text_content().strip()
    if date:
        date = date.split('•')[-1].strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//span[@class="group inline"]/a'):
        actorName = ''
        actorPhotoURL = ''

        actorPageURL = actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorName = actorPage.xpath('//div[@class="-aph-heading"]//h1')[0].text_content().strip()
        try:
            actorPhotoURL = actorPage.xpath('//div[@class="-api-poster-item"]//img/@data-src')[0]
            if 'http' not in actorPhotoURL:
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteNum) + actorPhotoURL
        except:
            pass

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//picture[@class="poster"]//img/@src',
        '//div[@id="gallery-thumbs"]/div/a/svg/@data-bg'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
