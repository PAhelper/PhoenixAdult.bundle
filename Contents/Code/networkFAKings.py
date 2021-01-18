import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.replace(' ', '-')

    searchURL = '%s%s' % (PAsearchSites.getSearchSearchURL(siteNum), searchData.encoded)
    req = PAutils.HTTPRequest(searchURL)
    searchPageElements = HTML.ElementFromString(req.text)

    for searchResult in searchPageElements.xpath('//div[@class="zona-listado2"]'):
        sceneURL = searchResult.xpath('.//@href')[0]

        titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//h3')[0].text_content().strip(), siteNum)
        curID = PAutils.Encode(sceneURL)

        subSite = PAutils.parseTitle(searchResult.xpath('.//strong/a')[0].text_content().strip(), siteNum)

        date = searchResult.xpath('.//p[@class="txtmininfo calen sinlimite"]//text()')[0].strip()
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        displayDate = releaseDate if date else ''

        if searchData.date and displayDate:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [FAKings/%s] %s' % (titleNoFormatting[:20] + '...', subSite, displayDate), score=score, lang=lang))

    searchURL = '%s%s' % (PAsearchSites.getSearchSearchURL(siteNum).replace('/en', ''), searchData.encoded)
    req = PAutils.HTTPRequest(searchURL)
    searchPageElements = HTML.ElementFromString(req.text)

    for searchResult in searchPageElements.xpath('//div[@class="zona-listado2"]'):
        sceneURL = searchResult.xpath('.//@href')[0]

        titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//h3')[0].text_content().strip(), siteNum)
        curID = PAutils.Encode(sceneURL)

        subSite = PAutils.parseTitle(searchResult.xpath('.//strong/a')[0].text_content().strip(), siteNum)

        date = searchResult.xpath('.//p[@class="txtmininfo calen sinlimite"]//text()')[0].strip()
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = searchData.dateFormat() if searchData.date else ''
        displayDate = releaseDate if date else ''

        if searchData.date and displayDate:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [FAKings/%s] %s' % (titleNoFormatting[:20] + '...', subSite, displayDate), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1')[0].text_content().strip(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[@class="grisoscuro"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'FAKings'

    # Collections / Tagline
    metadata.collections.clear()
    tagline = PAutils.parseTitle(detailsPageElements.xpath('//strong[contains(.,"Serie")]//following-sibling::a')[0].text_content().strip(), siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//strong[contains(.,"Categori")]//following-sibling::a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Posters
    art = []
    img = ''

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//strong[contains(.,"Actr")]//following-sibling::a'):
        actorName = actorLink.text_content().strip()

        modelURL = actorLink.xpath('.//@href')[0]
        req = PAutils.HTTPRequest(modelURL)
        actorPageElements = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPageElements.xpath('//div[@class="zona-imagen"]//img[@class]/@src')[0].strip()

        if not img:
            for scene in actorPageElements.xpath('//div[@class="zona-listado2"]'):
                if sceneURL == scene.xpath('.//@href')[0]:
                    img = scene.xpath('.//img[@class]/@src')[0].strip()

                    art.append(img)
                    break

        movieActors.addActor(actorName, actorPhotoURL)

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
                if height > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
