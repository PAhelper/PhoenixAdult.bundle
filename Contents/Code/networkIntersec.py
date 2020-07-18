import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "is-multiline")]/div[contains(@class, "column")]'):
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
        titleNoFormatting = searchResult.xpath('.//div[@class="has-text-weight-bold"]/text()')[0]
        releaseDate = parse(searchResult.xpath('.//span[contains(@class, "tag")]/text()')[0]).strftime('%Y-%m-%d')
        scenePoster = PAutils.Encode(searchResult.xpath('.//img/@src')[0])

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, scenePoster), name='%s [Intersec/%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = '%s/iod/%s' % (PAsearchSites.getSearchBaseURL(siteID), PAutils.Decode(metadata_id[0]))
    scenePoster = PAutils.Decode(metadata_id[2])
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "has-text-weight-bold")]/text()')[0]

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "has-text-white-ter")][3]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Intersec Interactive'

    # Tagline and Collection(s)
    metadata.collections.clear()
    taglineText = detailsPageElements.xpath('//div[contains(@class, "has-text-white-ter")][1]//a[contains(@class, "is-dark")][last()]/text()')[0]
    if 'sexuallybroken' in taglineText:
        tagline = 'Sexually Broken'
    elif 'infernalrestraints' in taglineText:
        tagline = 'Infernal Restraints'
    elif 'realtimebondage' in taglineText:
        tagline = 'Real Time Bondage'
    elif 'hardtied' in taglineText:
        tagline = 'Hardtied'
    elif 'topgrl' in taglineText:
        tagline = 'Topgrl'
    elif 'sensualpain' in taglineText:
        tagline = 'Sensual Pain'
    elif 'paintoy' in taglineText:
        tagline = 'Pain Toy'
    elif 'renderfiend' in taglineText:
        tagline = 'Renderfiend'
    elif 'hotelhostages' in taglineText:
        tagline = 'Hotel Hostages'
    else:
        tagline = 'Intersex'
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class, "has-text-white-ter")][1]//span[contains(@class, "is-dark")][1]/text()')[0]
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('BDSM')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class, "has-text-white-ter")][1]//a[contains(@class, "is-dark")][position() < last()]/text()')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorName in actors:
            movieActors.addActor(actorName, '')

    # Posters
    art = [
        scenePoster, detailsPageElements.xpath('//video-js/@poster')[0]
    ]

    for img in detailsPageElements.xpath('//figure/img/@src'):
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
