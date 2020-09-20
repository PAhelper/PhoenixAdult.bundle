import PAsearchSites
import PAgenres
import PAactors
import PAutils

joinstr = 'https://join.hollyrandall.com/'


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "item-video")]'):
        titleNoFormatting = searchResult.xpath('./div[@class="item-thumb"]/a/@title')[0]
        sceneURL = searchResult.xpath('./div[@class="item-thumb"]/a/@href')[0]
        curID = PAutils.Encode(sceneURL)

        if joinstr not in sceneURL:
            # Release Date
            date = searchResult.xpath('./div[@class="timeDate"]')[0].text_content().split('|')[1].strip()
            releaseDate = parse(date).strftime('%Y-%m-%d') if date else ''

            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, titleNoFormatting, releaseDate), name='%s %s [%s]' % (titleNoFormatting, releaseDate, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Studio
    metadata.studio = 'Holly Randall Productions'

    # Title
    metadata.title = PAutils.Decode(metadata_id[2]).strip()

    # Summary not available

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//ul[@class="tags"]/li/a'):
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)

    # Release Date
    date_object = parse(PAutils.Decode(metadata_id[3]))
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="info"]/p')[0].text_content().split('\n')[3].replace('Featuring:', '').split(',')
    for actorLink in actors:
        actorName = actorLink.strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//img[contains(@class, "update_thumb")]/@src0_3x',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(PAsearchSites.getSearchBaseURL(siteID) + poster)

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
