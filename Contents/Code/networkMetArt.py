import PAsearchSites
import PAgenres
import json

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    url = PAsearchSites.getSearchSearchURL(siteNum) + '/search-results?query[contentType]=movies&searchPhrase=' + encodedTitle
    data = urllib.urlopen(url).read()
    searchResults = json.loads(data)

    for searchResult in searchResults['items']:
        subSite = PAsearchSites.getSearchSiteName(siteNum)
        titleNoFormatting = searchResult['item']['name']

        url = searchResult['item']['path'].rsplit('/', 2)
        url = '%s/movie?name=%s&date=%s' % (PAsearchSites.getSearchSearchURL(siteNum), url[2], url[1])
        curID = url.replace('/','+').replace('?','!')

        releaseDate = parse(searchResult['item']['publishedAt']).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [MetArt/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results

def update (metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('+','/').replace('!','?')
    data = urllib.urlopen(url).read()
    detailsPageElements = json.loads(data)

    # Studio
    metadata.studio = 'MetArt'

    # Title
    metadata.title = detailsPageElements['name']

    # Summary
    metadata.summary = detailsPageElements['description']

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genre in detailsPageElements['tags']:
        genreName = genre.title()
        movieGenres.addGenre(genreName)
    movieGenres.addGenre("Glamorous")

    # Release Date
    date = detailsPageElements['publishedAt']
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

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
    for idx, posterUrl in enumerate(art):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
