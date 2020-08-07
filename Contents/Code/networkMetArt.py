import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + '/search-results?query[contentType]=movies&searchPhrase=' + encodedTitle)
    searchResults = req.json()
    for searchResult in searchResults['items']:
        subSite = PAsearchSites.getSearchSiteName(siteNum)
        titleNoFormatting = searchResult['item']['name']

        sceneURL = searchResult['item']['path'].rsplit('/', 2)
        sceneURL = '%s/movie?name=%s&date=%s' % (PAsearchSites.getSearchSearchURL(siteNum), sceneURL[2], sceneURL[1])
        curID = PAutils.Encode(sceneURL)

        releaseDate = parse(searchResult['item']['publishedAt']).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [MetArt/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = req.json()

    # Title
    metadata.title = detailsPageElements['name']

    # Summary
    metadata.summary = detailsPageElements['description']

    # Studio
    metadata.studio = 'MetArt'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements['publishedAt']
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genre in detailsPageElements['tags']:
        genreName = genre.title()

        movieGenres.addGenre(genreName)
    movieGenres.addGenre('Glamorous')

    # Actors
    movieActors.clearActors()
    for actor in detailsPageElements['models']:
        actorName = actor['name']
        actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actor['headshotImagePath']

        movieActors.addActor(actorName, actorPhotoURL)

    # Director
    director = metadata.directors.new()
    for dirname in detailsPageElements['photographers']:
        director.name = dirname['name']

    # Posters
    siteUUID = detailsPageElements['siteUUID']
    CDNurl = 'https://cdn.metartnetwork.com/' + siteUUID
    art = [
        CDNurl + detailsPageElements['coverImagePath'],
        CDNurl + detailsPageElements['splashImagePath']
    ]

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
                if height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
