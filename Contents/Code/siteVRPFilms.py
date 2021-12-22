import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    site_name = PAsearchSites.getSearchSiteName(siteNum).lower() + '-'
    scene_slug = searchData.filename.lower().replace(' ', '-').replace('_', ' ').replace(site_name, '')
    directURL = PAsearchSites.getSearchSearchURL(siteNum) + scene_slug.lower()
    req = PAutils.HTTPRequest(directURL)

    if req and req.ok:
        detailsPageElements = HTML.ElementFromString(req.text)
        curID = PAutils.Encode(directURL)
        titleNoFormatting = detailsPageElements.xpath('//section[@class="login-banner parallax"]/h1')[0].text_content().strip()
        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//section[@class="login-banner parallax"]/h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="col-md-8 text-justify"]')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Actors
    movieActors.clearActors()
    for actor in detailsPageElements.xpath('//a[@class="starring_contain"]'):
        actorName = actor.xpath('//div[@class="col-xs-12 video-star-title"]/h3')[0].text_content().strip()
        actorPhotoURL = actor.xpath('//div[@class="starring_image"]/@style')[0].split('url(')[1].split(')')[0].replace("'", "")
        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="single__download tags"]')[0].text_content().strip().split(', '):
        movieGenres.addGenre(genreLink)

    art = []
    # Posters/Background
    background = detailsPageElements.xpath('//section[@class="login-banner parallax"]/@style')[0].split('url(')[1].split(')')[0].replace("'", "")
    art.append(background)

    for poster in detailsPageElements.xpath('//div[@class="col-md-12 gallery-body"]/div/div/div/a/@href'):
        art.append(poster)

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
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
