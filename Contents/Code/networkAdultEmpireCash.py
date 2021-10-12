import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "item-grid")]/div[@class="grid-item"]'):
        if siteNum == 815 or siteNum == 1337:
            # Modification for JAYs POV and SpankMonster
            titleNoFormatting = searchResult.xpath('.//a[@class="animated-screen"]/@title')[0]
            curID = PAutils.Encode(searchResult.xpath('.//a[@class="animated-screen"]/@href')[0])
        else:
            titleNoFormatting = searchResult.xpath('.//a[@class="grid-item-title"]')[0].text_content()
            curID = PAutils.Encode(searchResult.xpath('.//a[@class="grid-item-title"]/@href')[0])
        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        displayTitle = titleNoFormatting
        if siteNum != 815 or siteNum != 1337:
            date = searchResult.xpath(('.//div[contains(@class, "justify-content-between")]/p[@class="m-0"]/span/text()'))
            if date:
                releaseDate = date[0].strip()
                displayTitle = '%s [%s]' % (titleNoFormatting, releaseDate)

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name=displayTitle, score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="description"]/text()')[0].strip()

    # Tagline and Collection(s)
    metadata.collections.add(detailsPageElements.xpath('//div[@class="studio"]//span/text()')[1].strip())
    if 'filthykings' in sceneURL:
        metadata.collections.add(PAsearchSites.getSearchSiteName(siteNum))

    # Studio
    metadata.studio = 'AdultEmpireCash'

    # Summary
    summary = detailsPageElements.xpath('//div[@class="synopsis"]/p/text()')
    if summary:
        metadata.summary = summary[0].strip()

    # Director
    directorElement = detailsPageElements.xpath('//div[@class="director"]/text()')
    if directorElement:
        director = metadata.directors.new()
        directorName = directorElement[0].strip()
        director.name = directorName

    # Release Date
    date = detailsPageElements.xpath('//div[@class="release-date"]/text()')[0].strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="video-performer"]//img'):
        actorName = actorLink.get('title')
        actorPhotoURL = actorLink.get('data-bgsrc')

        movieActors.addActor(actorName, actorPhotoURL)

    if 'filthykings' and '796896' in sceneURL:
        movieActors.addActor('Alice Visby', '')

    # Genres
    movieGenres.clearGenres()
    for genreName in detailsPageElements.xpath('//div[@class="tags"]//a/text()'):
        movieGenres.addGenre(genreName)

    # Posters
    art = []

    for poster in detailsPageElements.xpath('//div[@id="dv_frames"]//img/@src'):
        img = poster.replace('320', '1280')
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
                if width > 10:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
