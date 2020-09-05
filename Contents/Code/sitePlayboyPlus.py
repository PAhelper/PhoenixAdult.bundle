import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    data = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + '?gallery=1&terms=' + encodedTitle).json()
    searchResults = HTML.ElementFromString(data['results'][0]['html'])
    for searchResult in searchResults.xpath('//li[@class="item"]'):
        titleNoFormatting = searchResult.xpath('.//h3[@class="title"]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//p[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        img = PAutils.Encode(searchResults.xpath('.//img[contains(@class, "image")]/@data-src')[0].split('?', 1)[0])
        curID = PAutils.Encode(PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a/@href')[0])

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, img), name='%s [Playboy Plus] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    scenePoster = PAutils.Decode(metadata_id[2])
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="description-truncated"]')[0].text_content().strip().replace('...', '', 1)

    # Studio
    metadata.studio = 'Playboy Plus'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//p[contains(@class, "date")]')[0].text_content().strip()
    date_object = datetime.strptime(date, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Glamour')

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//p[@class="contributorName"]//a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, '')

    # Photos
    art = [
        scenePoster,
        detailsPageElements.xpath('//img[contains(@class, "image")]/@data-src')[0].split('?', 1)[0]
    ]
    for img in detailsPageElements.xpath('//section[@class="gallery"]//img[contains(@class, "image")]/@data-src'):
        art.append(img.split('?', 1)[0])

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
                if (width > 1 or height > width) and width < height:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
