import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, title, encodedTitle, searchTitle, siteNum, lang, searchDate):
    try:
        fixedTitle = title.lower().replace(" ", "-")
        postFix = fixedTitle.find("-files-")
        if postFix != -1:
            fixedTitle = fixedTitle[0:postFix]

        url = PAsearchSites.getSearchBaseURL(siteNum) + "/videos/" + fixedTitle
        req = PAutils.HTTPRequest(url)
        if req:
            searchResults = HTML.ElementFromString(req.text)
            
            releaseDate = parse(searchResults.xpath('.//div[@class="info"]')[0].text_content()[-30:].strip()).strftime('%Y-%m-%d')
            # No 404 error -> perfect match
            score = 100
            curID = PAutils.Encode(url)
            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s, %s]' % (fixedTitle, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))
    except Exception as e:
        Log(e)
        pass
    
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="video-item"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="video-title"]//a')[0].text_content()
        sceneUrl = searchResult.xpath('.//a[contains(@class, "play")]/@href')[0]
        curID = PAutils.Encode(sceneUrl)
        releaseDate = parse(searchResult.xpath('.//div[@class="info"]')[0].text_content()[-30:].strip()).strftime('%Y-%m-%d')

        actorList = []
        for actor in searchResult.xpath('.//div[@class="info"]//a'):
            actorList.append(actor.text_content())
        actors = ', '.join(actorList)

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s in %s [%s, %s]' % (actors, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    
    if len(metadata_id) > 2:
        sceneDate = metadata_id[2]
    else:
        sceneDate = None
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "right-info")]//h1')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Tagline and Collection
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(metadata.studio)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    else:
        # Date
        date = parse(detailsPageElements.xpath('.//div[@class="info"]')[0].text_content()[-30:].strip()).strftime('%Y-%m-%d')
        #date = str(metadata.id).split('|')[2]
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Summary
    description = detailsPageElements.xpath('//div[@class="description"]//span[contains(@class, "full")]')
    if description:
        metadata.summary = description[0].text_content().strip()
    else:
        metadata.summary = detailsPageElements.xpath('//div[@class="description"]')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="tag-list"]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actor in detailsPageElements.xpath('//div[contains(@class, "right-info")]//div[@class="info"]//a'):
        actorName = actor.text_content().strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    style = detailsPageElements.xpath('//div[@id="player"]/@style')[0]
    img = style[style.find('\'') + 1:style.rfind('\'')].split('?', 1)[0]
    art.append(img)

    posters = detailsPageElements.xpath('//div[@class="gallery-item"]//a/@href')
    for poster in posters:
        img = poster.split('?', 1)[0]
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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
