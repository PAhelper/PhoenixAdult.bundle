import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="videodetails"]'):
        titleNoFormatting = searchResult.xpath('./div[contains(@class, "videocontent")]/@data-title')[0]
        sceneURL = searchResult.xpath('./div[contains(@class, "videocontent")]/h2/a/@href')[0]
        curID = PAutils.Encode(sceneURL)

        # Release Date
        date = ''
        try:
            date = searchResult.xpath('./div[contains(@class, "videocontent")]/h2/span')[0].text_content().strip()
        except:
            pass
        releaseDate = parse(date).strftime('%Y-%m-%d') if date else ''

        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, titleNoFormatting, releaseDate), name='%s %s [%s]' % (titleNoFormatting, releaseDate, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Studio
    metadata.studio = 'Angela White'

    # Title
    metadata.title = PAutils.Decode(metadata_id[2]).strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="desc"]/p')[0].text_content().strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//meta[@name="keywords"]/@content')[0].replace('.', '').split(',')
    for genreLink in genres:
        genreName = genreLink.strip()
        movieGenres.addGenre(genreName)

    # Release Date
    date_object = parse(PAutils.Decode(metadata_id[3]))
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actorstr = metadata.title.replace('BTS', '')
    actorstr = (''.join(i for i in list(actorstr) if not i.isdigit())).strip()
    actors = actorstr.split(' X ')
    for actorLink in actors:
        actorName = actorLink.strip().lower()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//img[contains(@class, "tour-area-thumb")]/@data-src',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(PAsearchSites.getSearchBaseURL(siteNum) + poster)

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
