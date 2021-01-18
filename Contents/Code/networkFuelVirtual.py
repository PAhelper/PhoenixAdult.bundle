import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@align="left"]'):
        titleNoFormatting = searchResult.xpath('.//td[@valign="top"][2]/a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//td[@valign="top"][2]/a/@href')[0])

        date = searchResult.xpath('.//span[@class="date"]')[0].text_content().replace('Added', '').strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [FuelVirtual/%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = '%s/membersarea/%s' % (PAsearchSites.getSearchBaseURL(siteNum), PAutils.Decode(metadata_id[0]))
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().split('-')[0].strip()

    # Studio
    metadata.studio = 'FuelVirtual'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//td[@class="plaintext"]/a[@class="model_category_link"]'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)
    movieGenres.addGenre('18-Year-Old')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@id="description"]//td[@align="left"]/a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//a[@class="jqModal"]/img/@src'
    ]
    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            img = PAsearchSites.getSearchBaseURL(siteNum) + img

            art.append(img)

    photoPageUrl = sceneURL.replace('vids', 'highres')
    req = PAutils.HTTPRequest(photoPageUrl)
    photoPage = HTML.ElementFromString(req.text)
    for img in photoPage.xpath('//a[@class="jqModal"]/img/@src'):
        img = PAsearchSites.getSearchBaseURL(siteNum) + img

        art.append(img)

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
