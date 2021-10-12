import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.split('?')[0]
        if ('com/video' in sceneURL or 'com/player' in sceneURL) and 'mobile' not in sceneURL and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        try:
            titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//span[@class="vdetitle"] | //h1')[0].text_content().strip(), siteNum)
            curID = PAutils.Encode(sceneURL)

            try:
                date = detailsPageElements.xpath('//span[@class="vdedate"]')[0].strip()
            except:
                date = ''

            if date:
                releaseDate = parse(date).strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''
            displayDate = releaseDate if date else ''

            subSite = detailsPageElements.xpath('//script[@type="text/javascript"][contains(., "siteName")]')[0].text_content().split('siteName = \'')[-1].split('\'')[0].strip()

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, displayDate), name='%s [BangBros/%s] %s' % (titleNoFormatting, subSite, displayDate), score=score, lang=lang))
        except:
            pass

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//span[@class="vdetitle"] | //h1')[0].text_content().strip(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[@class="vdtx"] | //p[@class="videoDetail"]')[0].text_content().strip().replace('\n', '')

    # Studio
    metadata.studio = 'BangBros'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//script[@type="text/javascript"][contains(., "siteName")]')[0].text_content().split('siteName = \'')[-1].split('\'')[0].strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//meta[@http-equiv="keywords"]/@content')[0].split(',')
    for genreLink in genres:
        if tagline.replace(' ', '').lower() not in genreLink.replace(' ', '').lower():
            genreName = genreLink.strip()

            movieGenres.addGenre(genreName)

    # Posters
    art = []
    xpaths = [
        '//div[@class="hideWhilePlaying"]/img/@src',
    ]

    if tagline == 'Mia Khalifa':
        movieActors.addActor('Mia Khalifa', '')
        shootId = detailsPageElements.xpath('//script[@type="text/javascript"][contains(., "siteName")]')[0].text_content().split('com/')[-1].split('/')[0].strip()

        art.append('http://images.miakhalifa.com/shoots/%s/members/626x420.jpg' % shootId)

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            img = re.sub(r'////', 'http://', img)
            if 'http' not in img:
                img = 'http:' + img

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
