import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    # Scenes by name
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="scenes list"]/div[@class="items"]/div[@class="scene thumbnail "]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="textual"]/a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//a[@class="title"]/@href')[0])

        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    # Movies by name
    for searchResult in searchResults.xpath('//div[@class="movies list"]/div[@class="items"]/a[@class="movie thumbnail"]'):
        titleNoFormatting = searchResult.xpath('./h2')[0].text_content().strip()
        movieLink = searchResult.xpath('./@href')[0]
        curID = PAutils.Encode(movieLink)
        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s - Full Movie [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

        # Also append all the scenes from matching movies
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + movieLink)
        moviePageElements = HTML.ElementFromString(req.text)
        for movieScene in moviePageElements.xpath('//div[@class="scenes"]/div[@class="list"]/div[@class="scene thumbnail "]'):
            titleNoFormatting = movieScene.xpath('.//div[@class="textual"]/a')[0].text_content().strip()
            curID = curID = PAutils.Encode(movieScene.xpath('.//a[@class="title"]/@href')[0])

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('///span[@class="full"]')[0].text_content().strip()
    except:
        pass

    # Studio
    metadata.studio = 'Marc Dorcel'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('French porn')

    movieName = detailsPageElements.xpath('//span[@class="movie"]/a')
    if movieName:
        metadata.collections.add(movieName[0].text_content().strip())
    movieGenres.addGenre('Blockbuster Movie')

    # Actors
    movieActors.clearActors()
    if 'porn-movie' not in sceneURL:
        actors = detailsPageElements.xpath('//div[@class="actress"]/a')
    else:
        actors = detailsPageElements.xpath('//div[@class="actor thumbnail "]/a/div[@class="name"]')

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
    if 'porn-movie' not in sceneURL:
        date = detailsPageElements.xpath('//span[@class="publish_date"]')[0].text_content().strip()
    else:
        date = detailsPageElements.xpath('//span[@class="out_date"]')[0].text_content().replace('Year :', '').strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Director
    director = metadata.directors.new()
    try:
        movieDirector = detailsPageElements.xpath('//span[@class="director"]')[0].text_content().replace(
            'Director :', '').strip()
        director.name = movieDirector
    except:
        pass

    # Poster
    art = []

    xpaths = [
        '//div[contains(@class, "photos")]//source/@data-srcset'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if ',' in img:
                img = img.split(',')[-1].split()[0]

            trash = '_' + img.split('_', 3)[-1].rsplit('.', 1)[0]
            img = img.replace(trash, '', 1)

            art.append(img)

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
