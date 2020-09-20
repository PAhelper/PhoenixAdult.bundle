import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.replace(' ', '-') + '.html'
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="card"]'):
        titleNoFormatting = searchResult.xpath('.//div[2]/div/div[1]/h1')[0].text_content().strip()
        curID = PAutils.Encode(url)
        releaseDate = parse(searchResult.xpath('.//div[2]/div/div[1]/p[2]/small')[0].text_content().replace('Posted on', '').strip()).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Straplezz] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="card"]/div[2]/div/div[1]/h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="card"]/div[2]/div/div[1]/p[3]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Straplezz'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="card"]/div[2]/div/div[1]/p[2]/small')[0].text_content().replace('Posted on', '').strip()
    if date:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//li[@class="list-inline-item tag"]/a'):
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)
    movieGenres.addGenre('Strap-On')
    movieGenres.addGenre('Lesbian')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="card model m-0"]/a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorPageURL = actorLink.get('href')
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)

            actorName = actorPage.xpath('//div[@class="row mb-3"]/div[2]/h1')[0].text_content().strip()
            actorPhotoURL = actorPage.xpath('//div[@class="row mb-3"]/div[1]/img/@src0_1x')[0]

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    try:
        sceneID = detailsPageElements.xpath('//div[@class="col-md-12 col-lg-3 d-none d-md-block"]/div/div[1]/a/img/@alt')[0]
        for idx in range(0, 4):
            photo = '%s/content/%s/%d.jpg' % (PAsearchSites.getSearchBaseURL(siteID), sceneID, idx)

            art.append(photo)
    except:
        pass

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
