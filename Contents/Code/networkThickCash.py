import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    try:
        modelID = '-'.join(searchData.title.split(' ', 2)[:2])
        try:
            sceneTitle = searchData.title.split(' ', 2)[2]
        except:
            sceneTitle = ''
    except:
        modelID = searchData.title.split(' ', 1)[0]
        try:
            sceneTitle = searchData.title.split(' ', 1)[1]
        except:
            sceneTitle = ''

    url = PAsearchSites.getSearchSearchURL(siteNum) + modelID + '.html'
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)

    for searchResult in searchResults.xpath('//div[@class="updateBlock clear"]'):
        titleNoFormatting = searchResult.xpath('.//h3')[0].text_content().strip()
        description = searchResult.xpath('.//p')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//h4/text()')[0].split(':')[-1].strip()).strftime('%Y-%m-%d')

        poster = searchResult.xpath('.//@src')[0]
        subSite = PAsearchSites.getSearchSiteName(siteNum)

        # Fake Unique CurID
        curID = PAutils.Encode(titleNoFormatting)
        descriptionID = PAutils.Encode(description)
        posterID = PAutils.Encode(poster)

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        elif sceneTitle:
            score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
        else:
            score = 60

        results.Append(MetadataSearchResult(id='%s|%d|%s|%s|%s' % (curID, siteNum, descriptionID, releaseDate, posterID), name='%s [Thick Cash/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneTitle = PAutils.Decode(metadata_id[0])
    sceneDescription = PAutils.Decode(metadata_id[2])
    sceneDate = metadata_id[3]
    scenePoster = PAutils.Decode(metadata_id[4])

    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    metadata.title = sceneTitle

    # Summary
    metadata.summary = sceneDescription

    # Studio
    metadata.studio = 'Thick Cash'

    # Tagline and Collection(s)
    subSite = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = subSite
    metadata.collections.add(subSite)

    # Genres
    if subSite.lower() == 'Family Lust'.lower():
        for genreName in ['Family Roleplay']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'Over 40 Handjobs'.lower():
        for genreName in ['MILF', 'Handjob']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'Ebony Tugs'.lower():
        for genreName in ['Ebony', 'Handjob']:
            movieGenres.addGenre(genreName)
    elif subSite.lower() == 'Teen Tugs'.lower():
        for genreName in ['Teen', 'Handjob']:
            movieGenres.addGenre(genreName)

    # Release Date
    date_object = parse(sceneDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Posters
    art = [
        scenePoster
    ]

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
