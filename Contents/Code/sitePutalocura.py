import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchResults = []

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum, lang='enes')
    for sceneURL in googleResults:
        sceneURL = sceneURL.replace('index.php/', '')
        sceneURL = sceneURL.replace('es/', '')
        if '/tags/' not in sceneURL and '/actr' not in sceneURL and '?pag' not in sceneURL and '/xvideos' not in sceneURL and '/tag/' not in sceneURL and sceneURL not in searchResults:
            searchResults.append(sceneURL)
            if '/en/' in sceneURL:
                searchResults.append(sceneURL.replace('en/', ''))

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        try:
            if '/en/' in sceneURL:
                language = 'English'
                titleNoFormatting = PAutils.parseTitle(detailsPageElements.xpath('//title')[0].text_content().split('|')[0].split('-')[0].strip(), siteNum)
            else:
                language = 'Español'
                titleNoFormatting = detailsPageElements.xpath('//title')[0].text_content().split('|')[0].split('-')[0].strip()

            curID = PAutils.Encode(sceneURL)

            date = detailsPageElements.xpath('//div[@class="released-views"]/span')[0].text_content().strip()
            if date:
                releaseDate = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
            else:
                releaseDate = searchData.dateFormat() if searchData.date else ''
            displayDate = releaseDate if date else ''

            if searchData.date and displayDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s {%s} [%s] %s' % (titleNoFormatting, language, PAsearchSites.getSearchSiteName(siteNum), displayDate), score=score, lang=lang))
        except:
            pass

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    if '/en/' in sceneURL:
        metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//title')[0].text_content().split('|')[0].split('-')[0].strip(), siteNum)
    else:
        metadata.title = detailsPageElements.xpath('//title')[0].text_content().split('|')[0].split('-')[0].strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="description clearfix"]')[0].text_content().split(':')[-1].strip().replace('\n', ' ')

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.studio = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="categories"]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    if '/en/' in sceneURL:
        if '&' in metadata.title:
            actors = metadata.title.split('&')
        else:
            actors = detailsPageElements.xpath('//span[@class="site-name"]')[0].text_content().split(' and ')
    else:
        if '&' in metadata.title:
            actors = metadata.title.split('&')
        else:
            actors = detailsPageElements.xpath('//span[@class="site-name"]')[0].text_content().split(' y ')

    for actorLink in actors:
        actorName = actorLink.strip()

        modelURL = '%s/actrices/%s' % (PAsearchSites.getSearchBaseURL(siteNum), metadata.title[0].lower())
        req = PAutils.HTTPRequest(modelURL)
        modelPageElements = HTML.ElementFromString(req.text)
        for model in modelPageElements.xpath('//div[@class="c-boxlist__box--image"]//parent::a'):
            if model.text_content().strip().lower() == metadata.title.lower():
                actorName = metadata.title
                break

        if 'africa' in actorName.lower():
            actorName = 'Africat'
        elif metadata.title == 'MAMADA ARGENTINA':
            actorName = 'Alejandra Argentina'
        elif actorName == 'Alika':
            actorName = 'Alyka'

        modelURL = '%s/actrices/%s' % (PAsearchSites.getSearchBaseURL(siteNum), actorName[0].lower())
        req = PAutils.HTTPRequest(modelURL)
        modelPageElements = HTML.ElementFromString(req.text)

        actorPhotoURL = ''
        for model in modelPageElements.xpath('//div[@class="c-boxlist__box--image"]//parent::a'):
            if model.text_content().strip().lower() == actorName.lower():
                actorPhotoURL = model.xpath('.//img/@src')[0].strip()
                break

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    img = detailsPageElements.xpath('//div[@class="top-area-content"]/script')[0].text_content().strip()
    posterImage = re.search(r'(?<=posterImage:\s").*(?=")', img)
    if posterImage:
        img = posterImage.group(0)
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
                if height > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
