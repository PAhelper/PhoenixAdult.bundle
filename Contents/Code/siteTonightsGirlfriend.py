import PAsearchSites
import PAgenres


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchString = searchTitle.lower().split('and ')[0].strip().replace(' ', '-')
    for page in range(1, 5):
        url = '%s%s/?p=%d' % (PAsearchSites.getSearchSearchURL(searchSiteID), searchString, page)
        searchResults = HTML.ElementFromURL(url).xpath('//div[@class="panel-body"]')
        for searchResult in searchResults:
            actorList = []
            firstActor = searchResult.xpath('.//span[@class="scene-actors"]//a')[0].text_content()

            actors = searchResult.xpath('.//span[@class="scene-actors"]//a')
            for actorLink in actors:
                actorName = actorLink.text_content()
                actorList.append(actorName)
            titleNoFormatting = ', '.join(actorList)

            curID = searchResult.xpath('.//a')[0].get('href').split('?')[0].replace('_', '+').replace('/', '_').replace('?', '!')

            releaseDate = parse(searchResult.xpath('.//span[@class="scene-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), firstActor.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Tonight\'s Girlfriend] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))
        if len(searchResults) < 9:
            break
    return results


def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_', '/').replace('!', '?').replace('+', '_')
    detailsPageElements = HTML.ElementFromURL(url)

    # Date
    dateRaw = detailsPageElements.xpath('//span[@class="scenepage-date"]')[0].text_content()
    date = dateRaw.replace('Added:', '').strip()
    date_object = datetime.strptime(date, '%m-%d-%y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actorList = []
    actors = detailsPageElements.xpath('//div[@class="scenepage-info"]//a')
    # sceneInfo contains actresses, who are links and have actress pages, actors (plain text), and date
    sceneInfo = detailsPageElements.xpath('//div[@class="scenepage-info"]//p')[0].text_content()
    for actorLink in actors:
        actorName = actorLink.text_content()
        actorList.append(actorName)
        # remove actress from sceneInfo
        sceneInfo = sceneInfo.replace(actorName + ',', '').strip()
        actorPageURL = actorLink.get('href').split('?')[0]

        actorPageElements = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPageElements.xpath('//div[contains(@class,"modelpage-info")]//img/@src')[0].split('?')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # rest of actors (male actors without pages on the site)
    sceneInfo = sceneInfo.replace(dateRaw, '')
    maleActors = sceneInfo.split(',')
    for maleActor in maleActors:
        actorName = maleActor.strip()
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    # Title
    # scenes on this page have no title, making title = actress names
    metadata.title = ', '.join(actorList).replace(', ',' and ', -1)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="scenepage-description"]')[0].text_content().strip()
    except:
        pass

    # Tagline, Studio, Collections
    # note: I think only tonight's girlfriend classic (old scenes) is part of NA so keeping this separate
    metadata.collections.clear()
    studio = 'Tonight\'s Girlfriend'
    metadata.studio = studio
    metadata.tagline = studio
    metadata.collections.add(studio)

    # Genres
    movieGenres.clearGenres()
    genres = ['Girlfriend Experience', 'Pornstar', 'Hotel', 'Pornstar Experience']
    if (len(actors) + len(maleActors)) == 3:
        genres.append('Threesome')
        if len(actors) == 2:
            genres.append('BGG')
        else:
            genres.append('BBG')
    for genre in genres:
        movieGenres.addGenre(genre)

    # Posters/Background
    art = [
        detailsPageElements.xpath('//img[@class="playcard"]/@src')[0]
    ]

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
