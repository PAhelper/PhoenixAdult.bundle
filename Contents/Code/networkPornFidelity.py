import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle, cookies={'nats': 'MC4wLjMuNTguMC4wLjAuMC4w'})
    searchResults = HTML.ElementFromString(req.json()['html'])
    for searchResult in searchResults.xpath('//div[contains(@class, "d-flex")]'):
        titleNoFormatting = searchResult.xpath('.//a[@class="text-km"] | .//a[@class="text-pf"] | .//a[@class="text-tf"]')[0].text_content().strip()

        sceneURL = searchResult.xpath('.//a[@class="text-km"] | .//a[@class="text-pf"] | .//a[@class="text-tf"]')[0].get('href')[8:-19]
        curID = PAutils.Encode(sceneURL)

        releaseDate = searchResult.xpath('.//div[contains(@class, "text-left")]')[0].text_content().strip()[10:]
        if ', 20' not in releaseDate:
            releaseDate = releaseDate + ', ' + str(datetime.now().year)
        releaseDate = parse(releaseDate).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = 'https://' + PAutils.Decode(metadata_id[0])
    req = PAutils.HTTPRequest(sceneURL, cookies={'nats': 'MC4wLjMuNTguMC4wLjAuMC4w'})
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h4')[0].text_content()[36:].strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[contains(@class,"card-text")]')[0].text_content().strip()

    # Studio
    metadata.studio = 'PornFidelity'

    # Tagline and Collection(s)
    metadata.collections.clear()
    if 'Teenfidelity' in metadata.title:
        tagline = 'TeenFidelity'
    elif 'Kelly Madison' in metadata.title:
        tagline = 'Kelly Madison'
    else:
        tagline = 'PornFidelity'
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    for metadataPart in detailsPageElements.xpath('//div[contains(@class,"episode-summary")]//h4'):
        if 'Published' in metadataPart.text_content():
            releaseDate = metadataPart.text_content()[39:49]

            date_object = datetime.strptime(releaseDate, '%Y-%m-%d')
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Hardcore')
    movieGenres.addGenre('Heterosexual')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class, "episode-summary")]//a[contains(@href, "/models/")]')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content()

            actorPageURL = actorLink.get('href')
            req = PAutils.HTTPRequest(actorPageURL, cookies={'nats': 'MC4wLjMuNTguMC4wLjAuMC4w'})
            actorPage = HTML.ElementFromString(req.text)
            actorPhotoURL = actorPage.xpath('//img[@class="img-fluid"]/@src')[0]

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters/Background
    art = [
        'https://tour-cdn.kellymadisonmedia.com/content/episode/poster_image/%s/poster.jpg' % sceneURL.rsplit('/')[-1]
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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
