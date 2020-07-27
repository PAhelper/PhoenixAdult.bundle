import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    try:
        modelID = '-'.join(searchTitle.split(' ', 2)[:2])
        try:
            sceneTitle = searchTitle.split(' ', 2)[2]
        except:
            sceneTitle = ''
    except:
        modelID = searchTitle.split(' ', 1)[0]
        try:
            sceneTitle = searchTitle.split(' ', 1)[1]
        except:
            sceneTitle = ''

    url = PAsearchSites.getSearchSearchURL(siteNum) + modelID + '.html'
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)

    for searchResult in searchResults.xpath('//div[@class="update_block"]'):
        titleNoFormatting = searchResult.xpath('.//span[@class="update_title"]')[0].text_content().strip()
        description = searchResult.xpath('.//span[@class="latest_update_description"]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//span[@class="update_date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        actorList = []
        actors = searchResult.xpath('.//span[@class="tour_update_models"]/a')
        for actorLink in actors:
            actorName = actorLink.text_content().strip()

            actorList.append(actorName)
        actors = ', '.join(actorList)

        poster = searchResult.xpath('.//div[@class="update_image"]/a/img/@src')[0]
        subSite = PAsearchSites.getSearchSiteName(siteNum)

        # Fake Unique CurID
        curID = PAutils.Encode(titleNoFormatting)
        descriptionID = PAutils.Encode(description)
        posterID = PAutils.Encode(poster)

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        elif sceneTitle:
            score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
        else:
            score = 60

        results.Append(MetadataSearchResult(id='%s|%d|%s|%s|%s|%s' % (curID, siteNum, descriptionID, releaseDate, actors, posterID), name='%s [PureCFNM/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneTitle = PAutils.Decode(metadata_id[0])
    sceneDescription = PAutils.Decode(metadata_id[2])
    sceneDate = metadata_id[3]
    sceneActors = metadata_id[4]
    scenePoster = PAutils.Decode(metadata_id[5])

    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    metadata.title = sceneTitle

    # Summary
    metadata.summary = sceneDescription

    # Studio
    metadata.studio = 'PureCFNM'

    # Tagline and Collection(s)
    subSite = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = subSite
    metadata.collections.add(subSite)

    # Genres
    if subSite.lower() == 'AmateurCFNM'.lower():
        for genreName in ['CFNM']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'CFNMGames'.lower():
        for genreName in ['CFNM', 'Femdom']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'GirlsAbuseGuys'.lower():
        for genreName in ['CFNM', 'Femdom', 'Male Humiliation']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'HeyLittleDick'.lower():
        for genreName in ['CFNM', 'Femdom', 'Small Penis Humiliation']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'LadyVoyeurs'.lower():
        for genreName in ['CFNM', 'Voyeur']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'PureCFNM'.lower():
        for genreName in ['CFNM']:
            movieGenres.addGenre(genreName)

    # Release Date
    date_object = parse(sceneDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    actors = sceneActors.split(',')
    if actors:
        if len(actors) == 2:
            movieGenres.addGenre('Threesome')
        elif len(actors) == 3:
            movieGenres.addGenre('Foursome')
        elif len(actors) > 3:
            movieGenres.addGenre('Group')

        for actorLink in actors:
            actorName = actorLink.strip()
            actorPhotoURL = ' '

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [
        scenePoster
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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
