import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[contains(@class, "episode-list")]/div[contains(@class, "episode")]'):
        titleNoFormatting = searchResult.xpath('.//h2')[0].text_content().strip()
        sceneURL = searchResult.xpath('.//a/@href')[0]
        if not sceneURL.startswith('http'):
            sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
        curID = PAutils.Encode(sceneURL)
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split("|")
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    detailsPageElements = HTML.ElementFromURL(sceneURL)
    movieActors.clearActors()

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "title")]/h2')[0].text_content().strip()
	
    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="description"]/div[@class="desc-text"]')[0].text_content().strip()

    # Studio/Tagline/Collection
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//ul[contains(@class, "tags")]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Posters/Background
    art = []
    xpaths = [
        '//meta[@property="og:image"]/@content',
        '//div[contains(@class, "thumbnails")]//img/@src',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            poster = poster.split('?')[0]

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
