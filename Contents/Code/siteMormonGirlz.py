import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//*[contains(@class, " post ")]'):
        titleNoFormatting = searchResult.xpath('.//h1[@class="entry-title"]/a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//h1[@class="entry-title"]/a/@href')[0])

        date = searchResult.xpath('.//time[@class="entry-date"]/@datetime')[0].strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [MormonGirlz] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//meta[@property="og:title"]/@content')[0].replace(' - Mormon Girlz', '').strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//*[contains(@id, "post-")]/aside[2]/div/div[1]')[0].text_content().strip()

    # Studio
    metadata.studio = 'MormonGirlz'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//meta[@property="article:published_time"]/@content')[0].strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    xpaths = [
        '//h1[contains(text(), "more of") and not(contains(text(), "Mormon Girls"))]'
    ]
    for xpath in xpaths:
        for genreLink in detailsPageElements.xpath(xpath):
            genreName = genreLink.text.replace('more of', '').strip()

            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()

    # Posters
    art = []
    xpaths = [
        '//*[@class="ngg-gallery-thumbnail"]/a/@href'
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
                if width > 1 and height >= width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
