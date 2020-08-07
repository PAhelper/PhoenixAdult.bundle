import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@id="inner_content"]/div[@class="entry"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="title_holder"]/h1/a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//div[@class="title_holder"]/h1/a/@href')[0])

        day = searchResult.xpath('.//div[@class="date_holder"]/span[2]')[0].text_content().strip()
        month = searchResult.xpath('.//div[@class="date_holder"]/span[1]')[0].text_content()[:3].strip()
        year = searchResult.xpath('.//div[@class="date_holder"]/span[1]/span')[0].text_content().strip()
        date = '-'.join((month, day, year))
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [MomPOV] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    try:
        metadata.title = detailsPageElements.xpath('//a[@class="title"]')[0].text_content().strip()
    except:
        metadata.title = detailsPageElements.xpath('//meta[@property="og:title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="entry_content"]/p')[0].text_content().strip()

    # Studio
    metadata.studio = 'MomPOV'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="date_holder"]')[0].text_content().strip()
    if date:
        date_object = datetime.strptime(date, '%b %Y %d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('MILF')

    # Actors
    movieActors.clearActors()

    # Posters
    art = []
    xpaths = [
        '//div[@id="inner_content"]/div[1]/a/img/@src'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

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
                if width > 1 and height >= width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
