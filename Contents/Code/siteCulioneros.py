import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    sceneID = None
    splited = searchTitle.split(' ')
    if unicode(splited[0], 'UTF-8').isdigit():
        sceneID = splited[0]
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()

    if sceneID:
        sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneID + '.htm'
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)
        searchResult = detailsPageElements.xpath('//title')[0].text_content().split('|')

        titleNoFormatting = searchResult[0].strip()
        subSite = searchResult[1].strip()
        curID = PAutils.Encode(sceneURL)
        date = detailsPageElements.xpath('//div[@class="playerText-new fright"]//p')[0].text_content().split('on')
        releaseDate = parse(date[-1].strip()).strftime('%Y-%m-%d')

        score = 100

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [Culioneros/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)
    info = detailsPageElements.xpath('//title')[0].text_content().split('|')

    # Title
    metadata.title = info[0].strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//meta[@http-equiv="description"]/@content')[0]
    except:
        pass

    # Studio
    metadata.studio = 'Culioneros'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = info[1].strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genre List
    genres = detailsPageElements.xpath('//meta[@http-equiv="keywords"]/@content')[0].replace(', pornditos', '').replace(', porn', '').replace(tagline, '').replace('prono', 'porno')

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//p[contains(string(),"Cast")]/a'):
        actorName = actorLink.text_content()

        actorPhotoURL = ''
        modelBaseURL = PAsearchSites.getSearchBaseURL(siteID) + '/t1/most-liked-girls/'
        genres = genres.replace(actorName, '')
        
        for x in range(1, 6):
            modelPageURL = "%s%s" % (modelBaseURL, x)
            req = PAutils.HTTPRequest(modelPageURL)
            modelPageElements = HTML.ElementFromString(req.text)

            try:
                actorPhotoURL = modelPageElements.xpath('//a[@href="' + actorLink.xpath('.//@href')[0] + '"]' + '//img[@alt="' + actorName + '"]/@src')[0]
                break
            except:
                pass

        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    for genre in genres.split(','):
        genreName = genre.strip()

        movieGenres.addGenre(genreName)

    modelURL = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//p[contains(string(),"Cast")]/a/@href')[0]
    req = PAutils.HTTPRequest(modelURL)
    modelPageElements = HTML.ElementFromString(req.text)

    # Posters
    art = []
    xpaths = [
        '//div[@id="thumb-container"]//*[contains(@alt,"' + metadata.title + '")]/@src',
    ]

    for xpath in xpaths:
        for img in modelPageElements.xpath(xpath):
            art.append(img)

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