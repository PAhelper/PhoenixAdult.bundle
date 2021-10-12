import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded, cookies={'nats': 'MC4wLjMuNTguMC4wLjAuMC4w'})
    searchResults = HTML.ElementFromString(req.json()['html'])
    for searchResult in searchResults.xpath('//div[@class="card episode"]'):
        titleNoFormatting = searchResult.xpath('.//a[@class="text-km"] | .//a[@class="text-pf"] | .//a[@class="text-tf"]')[0].text_content().strip()

        sceneURL = searchResult.xpath('.//a[@class="text-km"] | .//a[@class="text-pf"] | .//a[@class="text-tf"]')[0].get('href')
        curID = PAutils.Encode(sceneURL)

        releaseDate = searchData.dateFormat() if searchData.date else ''

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL, cookies={'nats': 'MC4wLjMuNTguMC4wLjAuMC4w'})
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="level-left"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="column is-three-fifths"]')[0].text_content().replace('Episode Summary', '').strip()

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
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Hardcore')
    movieGenres.addGenre('Heterosexual')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[@class="is-underlined"]')
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
            actorPhotoURL = actorPage.xpath('//div[contains(@class, "one")]//@src')[0]

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters/Background
    art = [
        'https://tour-cdn.kellymadisonmedia.com/content/episode/poster_image/%s/poster.jpg' % sceneURL.rsplit('/')[-1],
        'https://tour-cdn.kellymadisonmedia.com/content/episode/episode_thumb_image_1/%s/1.jpg' % sceneURL.rsplit('/')[-1],
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
