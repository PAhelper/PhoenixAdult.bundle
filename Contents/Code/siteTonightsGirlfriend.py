import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.lower().split('and ')[0].strip().replace(' ', '-')
    for page in range(1, 5):
        req = PAutils.HTTPRequest('%s%s/?p=%d' % (PAsearchSites.getSearchSearchURL(siteNum), searchData.encoded, page))
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@class="panel-body"]'):
            actorList = []
            firstActor = searchResult.xpath('.//span[@class="scene-actors"]//a')[0].text_content()

            actors = searchResult.xpath('.//span[@class="scene-actors"]//a')
            for actorLink in actors:
                actorName = actorLink.text_content()
                actorList.append(actorName)
            titleNoFormatting = ', '.join(actorList)

            curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0].split('?')[0])

            releaseDate = parse(searchResult.xpath('.//span[@class="available-date"]')[0].text_content().strip()).strftime('%m-%d-%y')

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), firstActor.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Tonight\'s Girlfriend] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

        if len(searchResults) < 9:
            break

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Actors
    movieActors.clearActors()
    actorList = []
    actors = detailsPageElements.xpath('//div[@class="scenepage-info"]//a')

    sceneInfo = detailsPageElements.xpath('//div[@class="scenepage-info"]//p')[0].text_content()
    for actorLink in actors:
        actorName = actorLink.text_content()
        actorList.append(actorName)

        sceneInfo = sceneInfo.replace(actorName + ',', '').strip()
        actorPageURL = actorLink.get('href').split('?')[0]

        req = PAutils.HTTPRequest(actorPageURL)
        actorPageElements = HTML.ElementFromString(req.text)
        actorPhotoURL = 'https:' + actorPageElements.xpath('//div[contains(@class, "modelpage-info")]//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Title
    metadata.title = ', '.join(actorList).replace(', ', ' and ', -1)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="scenepage-description"]')[0].text_content().strip()
    except:
        pass

    # Studio
    studio = 'Tonight\'s Girlfriend'
    metadata.studio = studio

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = studio
    metadata.collections.add(studio)

    # Release Date
    dateRaw = detailsPageElements.xpath('//span[@class="scenepage-date"]')[0].text_content()
    date = dateRaw.replace('Added:', '').strip()
    date_object = datetime.strptime(date, '%m-%d-%y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # rest of actors (male actors without pages on the site)
    sceneInfo = sceneInfo.replace(dateRaw, '')
    maleActors = sceneInfo.split(',')
    for maleActor in maleActors:
        actorName = maleActor.strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = ['Girlfriend Experience', 'Pornstar', 'Hotel', 'Pornstar Experience']
    if (len(actors) + len(maleActors)) == 3:
        genres.append('Threesome')
        if len(actors) == 2:
            genres.append('BGG')
        else:
            genres.append('BBG')

    for genreLink in genres:
        genreName = genreLink

        movieGenres.addGenre(genreName)

    # Posters/Background
    art = [
        'https:' + detailsPageElements.xpath('//img[@class="playcard"]/@src')[0]
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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
