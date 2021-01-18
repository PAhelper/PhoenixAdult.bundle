import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = None
    parts = searchData.title.split()
    if unicode(parts[0], 'UTF-8').isdigit():
        sceneID = parts[0]

    url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded + '.html'
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "video-item") and @data-get-thumbs-url]'):
        titleNoFormatting = searchResult.xpath('.//p[@class="title-video"]')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('./a/@href')[0])
        date = searchResult.xpath('.//div[@class="infos-video"]/p')[0].text_content().replace('Added on', '').strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    # SceneId search
    if sceneID:
        url = PAsearchSites.getSearchBaseURL(siteNum) + '/en/videos/show/' + sceneID
        req = PAutils.HTTPRequest(url)
        detailsPageElements = HTML.ElementFromString(req.text)

        titleNoFormatting = detailsPageElements.xpath('//div[@class="video-player"]/h1')[0].text_content().strip()
        curID = PAutils.Encode(url)

        score = 100

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="video-player"]/h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="video-description"]/p')[0].text_content().strip()

    # Studio
    metadata.studio = 'Jacquie Et Michel TV'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genre in detailsPageElements.xpath('//span[@class="categories"]//strong'):
        genreName = genre.text_content().replace(',', '').strip()
        if genreName == 'Sodomy':
            genreName = 'Anal'

        movieGenres.addGenre(genreName)

    movieGenres.addGenre('French porn')

    # Release Date
    date = detailsPageElements.xpath('//span[@class="publication"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Poster
    art = []

    xpaths = [
        '//img[@id="video-player-poster"]/@data-src'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if ',' in img:
                img = img.split(',')[-1].split()[0]

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
