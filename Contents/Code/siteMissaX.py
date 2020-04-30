import PAsearchSites
import PAgenres


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="updateItem"] | //div[@class="photo-thumb video-thumb"]'):
        titleNoFormatting = searchResult.xpath('.//h4//a | .//p[@class="thumb-title"]')[0].text_content().strip()
        curID = searchResult.xpath('.//a')[0].get('href').replace('/', '_').replace('?', '!')
        releaseDate = parse(searchResult.xpath('.//span[@class="update_thumb_date"] | .//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        actors = searchResult.xpath('.//span[@class="tour_update_models"]//a | .//p[@class="model-name"]//a')
        firstActor = actors[0].text_content().strip()
        numActors = len(actors) - 1

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s + %d in %s [%s] %s' % (firstActor, numActors, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score = score, lang = lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    metadata_id = str(metadata.id).split('|')
    url = metadata_id[0].replace('_', '/').replace('!', '?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//span[@class="update_title"] | //p[@class="raiting-section__title"]')[0].text_content().strip()

    # Studio/Tagline/Collection
    metadata.collections.clear()
    metadata.studio = 'AllHerLuv/MissaX'
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//span[@class="latest_update_description"] | //p[contains(@class,"text")]')[0].text_content().replace("Includes:","").replace("Synopsis:","").strip()
    except:
        Log('No summary found')

    # Date
    try:
        date = detailsPageElements.xpath('//span[@class="update_date"]')[0].text_content().strip()
    except:
        date = detailsPageElements.xpath('//p[@class="dvd-scenes__data"]')[0].text_content().split('|')[1].replace('Added:', '').strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="update_block"]//span[@class="tour_update_models"]//a | //p[@class="dvd-scenes__data"][1]//a')
    for actorLink in actors:
        actorName = actorLink.text_content().strip()
        actorPageURL = actorLink.get('href')
        actorPageElements = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPageElements.xpath('//img[contains(@class, "model_bio_thumb")]/@src0_1x')[0]
        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//span[@class="tour_update_tags"]//a | //p[@class="dvd-scenes__data"][2]//a')
    for genreLink in genres:
        genre = genreLink.text_content()
        movieGenres.addGenre(genre)

    # Posters/Background
    art = [
        detailsPageElements.xpath('//img[contains(@class, "update_thumb")]/@src0_1x')[0]
    ]

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
