import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@id="left-area"]/article'):
        titleNoFormatting = searchResult.xpath('.//h2[@class="entry-title"]/a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//h2[@class="entry-title"]/a/@href')[0])
        releaseDate = parse(searchResult.xpath('.//span[@class="published"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [LittleCaprice] %s ' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = metadata.id.split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Studio
    metadata.studio = 'LittleCaprice'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="entry-title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="et_pb_text et_pb_module et_pb_bg_layout_light et_pb_text_align_left"]/p')[0].text_content().strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//meta[@property="article:published_time"]/@content')[0].split('T')[0]
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class,"et_pb_text_align_left")]/ul/li[contains(.,"Models")]/a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().strip()

            actorPageURL = actorLink.get('href')
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)

            actorPhotoURL = actorPage.xpath('//img[@class="model-page"]/@src')[0]
            actorPhotoURL = actorPhotoURL.replace('media.', '')
            if 'http' not in actorPhotoURL:
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    try:
        twitterBG = detailsPageElements.xpath('//meta[@property="og:image"]/@content')[0]
        art.append(twitterBG)
    except:
        pass

    photos = detailsPageElements.xpath('//span[@class="et_pb_image_wrap "]/img/@src')
    for photoLink in photos:
        art.append(PAsearchSites.getSearchBaseURL(siteID) + photoLink)

    try:
        photoPageUrl = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//div[contains(@class, "et_pb_text_align_left")]/ul/li[contains(., "Pictures:")]/a/@href')[0]
        req = PAutils.HTTPRequest(photoPageUrl)
        photoPage = HTML.ElementFromString(req.text)
        for unlockedPhoto in photoPage.xpath('//div[@class="et_pb_gallery_image landscape"]/a/@href'):
            if not unlockedPhoto.startswith('http'):
                unlockedPhoto = PAsearchSites.getSearchBaseURL(siteID) + unlockedPhoto

            art.append(unlockedPhoto)
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
