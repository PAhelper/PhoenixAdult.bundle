import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    sceneID = searchTitle.split(' ', 1)[0]
    try:
        sceneTitle = searchTitle.split(' ', 1)[1]
    except:
        sceneTitle = ''

    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneID + '/1'
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)
    titleNoFormatting = detailsPageElements.xpath('//title')[0].text_content().split('|')[1].strip()
    curID = PAutils.Encode(sceneURL)
    releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

    if sceneTitle:
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
    else:
        score = 90

    results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, releaseDate, sceneID), name='%s [Fitting-Room]' % titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    sceneDate = metadata_id[2]
    sceneID = metadata_id[3]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    title = detailsPageElements.xpath('//title')[0].text_content().strip()
    if '|' in title:
        title = title.split('|')[1].strip()
    metadata.title = title

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//p[@class="description"]')[0].text_content().strip()
    except:
        pass

    # Studio
    metadata.studio = 'Fitting-Room'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Get Collection from Related Videos
    collection = None
    collectionNode = detailsPageElements.xpath('//div[@id="list_videos_related_videos_items"]/div[1]/div[2]/a')
    if collectionNode:
        collection = collectionNode[0].text_content().strip()
    else:
        if metadata.title == 'Huge Tits':
            collection = 'Busty'
        elif metadata.title == 'Pool Table':
            collection = 'Fetishouse'
        elif metadata.title == 'Spanish Milf':
            collection = 'Milf'
        elif metadata.title == 'Cotton Panty':
            collection = 'Pantyhose'

    if collection:
        metadata.collections.add(collection)

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actor = detailsPageElements.xpath('//a[@class="model"]/div[1]/img')[0]
    actorName = actor.get('alt').strip()
    actorPhotoURL = actor.get('src').strip()

    movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//meta[@property="article:tag"]/@content'):
        genreName = genreLink.replace(actorName, '').strip().lower()

        movieGenres.addGenre(genreName)
    movieGenres.addGenre('Fitting Room')

    # Posters
    art = [
        'https://www.fitting-room.com/contents/videos_screenshots/0/%s/preview.jpg' % sceneID
    ]

    for photoNum in range(2, 6):
        photo = 'https://www.fitting-room.com/contents/videos_screenshots/0/%s/3840x1400/%d.jpg' % (sceneID, photoNum)

        art.append(photo)

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
