import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []
    directURL = '%s/video/%s' % (PAsearchSites.getSearchBaseURL(siteNum), slugify(searchData.title))
    searchResults.append(directURL)

    googleResults = PAutils.getFromSearchEngine(searchData.title, siteNum)
    for sceneURL in googleResults:
        sceneURL = sceneURL.rsplit('/', 1)[0].split('/join.php')[0]
        if '/video/' in sceneURL and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)

            try:
                titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//h1[@class="customhcolor"]')[0].text_content().replace('-', ' ').strip(), siteNum)
                curID = PAutils.Encode(sceneURL)

                date = detailsPageElements.xpath('//span[@class="date"]')
                if date:
                    releaseDate = parse(date[0].text_content().strip()).strftime('%Y-%m-%d')
                else:
                    releaseDate = searchData.dateFormat() if searchData.date else ''

                displayDate = releaseDate if date else ''

                if searchData.date:
                    score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))
            except:
                pass

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//h1[@class="customhcolor"]')[0].text_content().replace('-', ' ').strip(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//h2[@class="customhcolor2"]')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    movieCollections.addCollection(metadata.studio)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actor(s)
    actors = re.split(r',|\sand\s', detailsPageElements.xpath('//h3')[0].text_content())
    for actorLink in actors:
        actorName = re.sub(r'\d', '', actorLink).strip().replace('&nbsp', '')
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    xpaths = [
        '//center/img/@src',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if 'http' not in img:
                img = '%s/%s' % (PAsearchSites.getSearchBaseURL(siteNum), img)

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
