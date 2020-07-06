import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//section[@role="main"]/article'):
        titleNoFormatting = searchResult.xpath('.//h2[@itemprop="name"]')[0].text_content().strip()
        sceneURL = searchResult.xpath('./a/@href')[0]
        if not sceneURL.startswith('http'):
            sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
        curID = PAutils.Encode(sceneURL)

        date = searchResult.xpath('.//td/h2[not(@class)]')[0].text_content().replace('PUBLISHED:', '').replace('&nbsp', ' ').strip()
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')
        else:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
        displayDate = releaseDate if date else ''

        if searchDate and displayDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split("|")
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    detailsPageElements = HTML.ElementFromURL(sceneURL)
    movieActors.clearActors()

    # Title
    metadata.title = detailsPageElements.xpath('//meta[@property="og:title"]/@content')[0].split('|')[0].strip()

    # Summary
    description = detailsPageElements.xpath('//meta[@property="og:description"]/@content')[0].replace('&quot;', '').strip() + '...'
    metadata.summary = description

    # Studio/Tagline/Collection
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Date
    date = detailsPageElements.xpath('//meta[@property="article:published_time"]/@content')[0].split('T')[0].strip()
    if not date and sceneDate:
        date = sceneDate

    if date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Posters/Background
    art = []
    xpaths = [
        '//img[(contains(@class, "alignnone") and contains(@class, "size-full") or contains(@class, "size-medium")) and (not(contains(@class, "wp-image-4512") or contains(@class, "wp-image-492")))]/@src',
        '//div[@class="iehand"]/a/@href',
        '//a[contains(@class, "colorbox-cats")]/@href',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            o = urlparse.urlparse(poster, 'http')
            link = urlparse.parse_qs(o.query)
            if 'src' in link:
                poster = link['src'][0]

            art.append(poster)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if(width > 100 and idx > 1):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
