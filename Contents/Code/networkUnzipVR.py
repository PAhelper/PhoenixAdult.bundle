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


def update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, art):
    metadata_id = str(metadata.id).split('|')
    sceneId = PAutils.Decode(metadata_id[0])
    basePath = PAsearchSites.getSearchBaseURL(siteNum).replace('www', 'content')
    sceneURL = '%s/api/content/v1/videos/%s' % (basePath, sceneId)
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = req.json()['data']['item']

    # Title
    metadata.title = detailsPageElements['title']

    # Summary
    metadata.summary = PAutils.strip_tags(detailsPageElements['description'])

    # Studio
    metadata.studio = 'Unzip VR'

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    movieCollections.addCollection(tagline)

    # Release Date
    date = detailsPageElements['publishedAt']
    date_object = datetime.fromtimestamp(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    for genreLink in detailsPageElements['categories']:
        genreName = genreLink['name']
        movieGenres.addGenre(genreName)

    # Actor(s)
    for actorLink in detailsPageElements['models']:
        actorName = actorLink['title']
        actorPhotoURL = ''

        if 'featuredImage' in actorLink and 'permalink' in actorLink['featuredImage']:
            actorPhotoURL = basePath + actorLink['featuredImage']['permalink']
        else:
            try:
                modelURL = '%s/api/content/v1/models/%s' % (basePath, actorLink['slug'])
                req = PAutils.HTTPRequest(modelURL)
                modelPageElements = req.json()['data']['item']
                actorPhotoURL = basePath + modelPageElements['featuredImage']['permalink']
            except:
                pass

        movieActors.addActor(actorName, actorPhotoURL, gender='female')

    # Posters
    maybeSlider = detailsPageElements['sliderImage']
    if maybeSlider:
        imgUrl = basePath + maybeSlider['permalink']
        art.append(imgUrl)

    maybePoster = detailsPageElements['poster']
    if maybePoster:
        imgUrl = basePath + maybePoster['permalink']
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
