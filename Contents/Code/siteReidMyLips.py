import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.lower().replace(' ', '-')
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    detailsPageElements = HTML.ElementFromString(req.text)

    titleNoFormatting = detailsPageElements.xpath('//title')[0].text_content().split('|')[-1].strip()
    curID = PAutils.Encode(url)
    releaseDate = parse(detailsPageElements.xpath('/html/body/div/div[4]/div[4]/div/main/div[2]/div[2]/div/div/div[2]/div/div/div[4]/p/span')[0].text_content().strip()).strftime('%Y-%m-%d')

    score = 100

    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [ReidMyLips] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    movieGenres.clearGenres()

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().split('|')[-1].strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//meta[@name="description"]')[0].get('content').strip()

    # Studio
    metadata.studio = 'ReidMyLips'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('/html/body/div/div[4]/div[4]/div/main/div[2]/div[2]/div/div/div[2]/div/div/div[4]/p/span')[0].text_content().strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actorName = 'Riley Reid'
    actorPhotoURL = ''

    movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    photos = detailsPageElements.xpath('//div[@id="pro-gallery-margin-container"]//a[@class="block-fullscreen gallery-item-social-download  pull-right  gallery-item-social-button"]//@href')
    for photoLink in photos:
        photo = photoLink.split('?')[0]

        art.append(photo)

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
