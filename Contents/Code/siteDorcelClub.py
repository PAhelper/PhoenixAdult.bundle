import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    # Scenes by name
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="scene"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="title"]/a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//div[@class="title"]/a/@href')[0])
        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().replace('Published', '').strip()).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    # Movies by name
    for searchResult in searchResults.xpath('//div[@class="movie"]'):
        titleNoFormatting = searchResult.xpath('./a/p')[0].text_content().strip()
        movieLink = searchResult.xpath('./a/@href')[0]
        curID = PAutils.Encode(movieLink)
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s Full Movie [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

        # Also append all the scenes from matching movies
        req = PAutils.HTTPRequest(movieLink)
        moviePageElements = HTML.ElementFromString(req.text)
        for movieScene in moviePageElements.xpath('//div[@class="scene"]'):
            titleNoFormatting = movieScene.xpath('.//div[@class="title"]/a')[0].text_content().strip()
            curID = curID = PAutils.Encode(movieScene.xpath('.//div[@class="title"]/a/@href')[0])
            releaseDate = parse(movieScene.xpath('.//span[@class="date"]')[0].text_content().replace('Published', '').strip()).strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="content_text"]')[0].text_content().strip()
    except:
        pass

    # Studio
    metadata.studio = 'Marc Dorcel'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('French porn')

    movieName = detailsPageElements.xpath('//div[@class="movie"]/a')
    if movieName:
        metadata.collections.add(movieName[0].text_content().strip())
    movieGenres.addGenre('Blockbuster Movie')

    # Actors
    movieActors.clearActors()
    if 'porn-movie' not in sceneURL:
        actors = detailsPageElements.xpath('//div[@class="scene"][1]//div[@class="actors"]//a')
    else:
        actors = detailsPageElements.xpath('//div[@class="actors"]//a')

    if actors:
        if 'porn-movie' not in sceneURL:
            if len(actors) == 3:
                movieGenres.addGenre('Threesome')
            if len(actors) == 4:
                movieGenres.addGenre('Foursome')
            if len(actors) > 4:
                movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="date"]')[0].text_content().replace('Published', '').strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Director
    director = metadata.directors.new()
    try:  # This is for getting from scene page to movie page and grabbing director, if available
        moviePage = detailsPageElements.xpath('//div[@class="movie"]/a')[0].get('href').strip()
        req = PAutils.HTTPRequest(moviePage)
        moviePageElements = HTML.ElementFromString(req.text)
        movieDirector = moviePageElements.xpath('//div[@class="infos"]/p[2]')[0].text_content().replace('Movie Director:', '').strip()
        director.name = movieDirector
    except:
        pass

    try:  # This is for getting the director if you're matching a whole movie
        director.name = detailsPageElements.xpath('//div[@class="infos"]/p[2]')[0].text_content().replace('Movie Director:', '').strip()
    except:
        pass

    # Video backgrounds
    art = []
    xpaths = [
        '//ul[@class="vid_rotator_img"]//img/@data-lazy',
        '//div[contains(@class, "pictures_container")]//img[@class="item"]/@src'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            trash = '_' + img.split('_', 3)[-1].rsplit('.', 1)[0]
            img = img.replace(trash, '', 1)

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
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
