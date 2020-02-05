import PAsearchSites
import PAgenres
import PAactors
import PAextras


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//article//a'):
        siteName = PAsearchSites.getSearchSiteName(siteNum) + '.xxx'
        titleNoFormatting = searchResult.xpath('./@title')[0]
        sceneURL = searchResult.xpath('./@href')[0]
        curID = sceneURL.replace('/', '_').replace('?', '!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, siteName), score=score, lang=lang))

    url = PAsearchSites.getSearchSearchURL(siteNum).replace('.xxx', '.tv', 1)
    searchResults = HTML.ElementFromURL(url + encodedTitle)
    for searchResult in searchResults.xpath('//div[contains(@class, "entry")]//h3//a'):
        siteName = PAsearchSites.getSearchSiteName(siteNum) + '.tv'
        titleNoFormatting = searchResult.xpath('./text()')[0].strip()
        sceneURL = searchResult.xpath('./@href')[0]
        curID = sceneURL.replace('/', '_').replace('?', '!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, siteName), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    url = metadata_id[0].replace('_', '/').replace('!', '?')
    detailsPageElements = HTML.ElementFromURL(url)

    if '.xxx' in url:
        # Title
        metadata.title = detailsPageElements.xpath('//h1[@class="entry-title"]/text()')[0].strip()

        # Summary
        metadata.summary = detailsPageElements.xpath('//div[@class="video-description"]')[0].text_content().strip()

        # Genres & Actors
        movieGenres.clearGenres()
        movieActors.clearActors()
        tags = detailsPageElements.xpath('//div[@class="tags"]//a')
        for tagLink in tags:
            tagName = tagLink.xpath('./@title')[0]
            tagURL = tagLink.xpath('./@href')[0]
            if '/teen/' not in tagURL:
                movieGenres.addGenre(tagName)
            else:
                movieActors.addActor(tagName, '')
    else:
         # Title
        metadata.title = detailsPageElements.xpath('//h1[@class="title"]/text()')[0].strip()

        # Summary
        metadata.summary = detailsPageElements.xpath('//div[contains(@class, "entry")]//p')[2].text_content().strip()

        # Genres & Actors
        movieGenres.clearGenres()
        movieActors.clearActors()
        tags = detailsPageElements.xpath('//div[@class="post-meta"]//a')
        for tagLink in tags:
            tagName = tagLink.xpath('./text()')[0].strip()
            tagURL = tagLink.xpath('./@href')[0]
            if '/models/' not in tagURL:
                movieGenres.addGenre(tagName)
            else:
                movieActors.addActor(tagName, '')

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Posters
    art = []
    xpaths = [
        '//video/@poster',
        '//dl[@class="gallery-item"]//img/@src'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
                }
                req = urllib.Request(posterUrl, headers=headers)
                img_file = urllib.urlopen(req)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers=headers).content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers=headers).content, sort_order=idx)
            except:
                pass

    return metadata
