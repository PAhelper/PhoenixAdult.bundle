import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    url = PAsearchSites.getSearchSearchURL(siteNum).replace('www', 'content')
    req = PAutils.HTTPRequest(url + searchData.encoded)
    searchResults = req.json()['data']
    for searchResult in searchResults['videos']:
        title = searchResult['title']
        curID = PAutils.Encode(searchResult['slug'])

        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), title.lower())

        if len(title) > 29:
            title = title[:32] + '...'

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (title, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneId = PAutils.Decode(metadata_id[0])
    basePath = PAsearchSites.getSearchBaseURL(siteNum).replace('www', 'content')
    sceneURL = basePath + '/api/content/v1/videos/' + sceneId
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = req.json()['data']['item']

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    try:
        raw = detailsPageElements['description']
        summary = raw.replace('<a href="/', '').replace('">', '').replace('</a>', '')
        metadata.summary = summary
    except:
        pass

    # Studio
    metadata.studio = 'VR Bangers'

    # Tagline and Collection
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements['publishedAt']
    date_object = datetime.fromtimestamp(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements['tags']:
        genreName = genreLink['label']
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements['models']:
        actorName = actorLink['title']
        actorPhotoURL = basePath + actorLink['featuredImage']['permalink']
        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    imgUrl = basePath + detailsPageElements['sliderImage']['permalink']
    art.append(imgUrl)

    imgUrl = basePath + detailsPageElements['poster']['permalink']
    art.append(imgUrl)

    for imgObj in detailsPageElements['galleryImages']:
        imgUrl = basePath + imgObj['permalink']
        art.append(imgUrl)

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
