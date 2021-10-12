import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.title.replace(' ', '-') + '.html'
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)

    for searchResult in searchResults.xpath('//div[@class="card"]'):
        titleNoFormatting = searchResult.xpath('.//h1[@class="card-title"]')[0].text_content().strip()
        curID = PAutils.Encode(url)
        date = searchResult.xpath('.//i[contains(@class, "fa-clock")]/following-sibling::text()')[0].text_content().split('•')[1].strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="card-title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="card-text mb-2"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Strapon Cum'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="card"]//i[contains(@class, "fa-clock")]/following-sibling::text()')[0].text_content().split('•')[1].strip()
    if date:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Strap-On')
    movieGenres.addGenre('Lesbian')
    for genreLink in detailsPageElements.xpath('//div[contains(@class, "tag-cloud")]//a'):
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="card"]//span[contains(text(), "Featuring:")]/following-sibling::a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorPage[0].text_content().strip()
            actorPhotoURL = ''

            actorPageURL = actorLink.get('href')
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)

            actorPhotoNode = actorPage.xpath('//img[starts-with(@id, "set-target")]/@data-src0_1x')
            if actorPhotoNode:
                actorPhotoURL = actorPhotoNode[0]

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    sceneID = detailsPageElements.xpath('//div[@class="trailer"]//img/@alt')
    if sceneID:
        sceneID = [0]
        for idx in range(0, 4):
            photo = PAsearchSites.getSearchBaseURL(siteNum) + '/content/%s/%d.jpg' % (sceneID, idx)

            art.append(photo)

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
