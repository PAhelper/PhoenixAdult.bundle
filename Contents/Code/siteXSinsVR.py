import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.title
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)


    for searchResult in searchResults.xpath('//div[@class="tn-video tn-video--horizontal"]'):
        titleNoFormatting = searchResult.xpath('.//div/a[@class="tn-video-name"]')[0].text_content().strip()
        sceneURL = searchResult.xpath('.//a[@class="tn-video-media"]')[0].get('href')
        if not sceneURL.startswith('http'):
            sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
        curID = PAutils.Encode(sceneURL)
        releaseDate = ''
        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())
        actorsList = []
        for actor in searchResult.xpath('.//div/div[@class="tn-video-models"]/a'):
            Log('actor.href: ' + actor.text_content().strip())
            actorsList.append(actor.text_content().strip())
        actors = ', '.join(actorsList)
        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] with %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), actors), score=score, lang=lang))

    return results



def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().strip().split('•')[0]

    # Summary
    summary = ''
    for paragraph in detailsPageElements.xpath('//li/div[@class="small"]/p'):
        summary = summary + paragraph.text_content()
    metadata.summary = summary

    # Studio
    metadata.studio = 'SinsVR'

    # Tagline and Collection
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//span//time')[0].text_content().strip()
    if date:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for tag in detailsPageElements.xpath('//div[@class="tags-item"]'):
        genreName = tag.text_content().strip()
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div/strong[text()="Starring"]//following-sibling::span/a[@class="tiny-link"]'):
        actorName = actorLink.text_content().strip()
        actorPageURL = PAsearchSites.getSearchBaseURL(siteNum) + actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPage.xpath('//div[@class="model-header__photo"]/img')[0].get('src')[0]
        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    for poster in detailsPageElements.xpath('//div[contains(@class, "tn-photo__container")]/div/a/div/img/@src'):
        if poster.startswith('http'):
            img = poster.replace('sceneGallerySmall', 'sceneGallery')
            art.append(img)

    poster = detailsPageElements.xpath('//dl8-video')[0]
    img = poster.get('poster')
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
