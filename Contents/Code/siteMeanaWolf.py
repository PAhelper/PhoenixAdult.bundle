import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="videoBlock"]'):
        titleNoFormatting = searchResult.xpath('./p/a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('./p/a/@href')[0])
        img = PAutils.Encode(searchResult.xpath('.//img[@class="video_placeholder"]/@src')[0])

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, img), name='%s [Meana Wolf]' % titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = metadata.id.split('|')
    sceneURL = PAsearchSites.getSearchBaseURL(siteID) + '/video/' + metadata_id[0]
    scenePoster = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="trailerArea"]/h3')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="trailerContent"]/p')[0].text_content().strip()

    # Studio
    metadata.studio = 'Meana Wolf'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="videoContent"]/ul/li[2]')[0].text_content().replace('ADDED:', '').strip()
    if date:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieActors.clearActors()
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="videoContent"]/ul/li[position()=last()]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    for actorLink in detailsPageElements.xpath('//div[@class="videoContent"]/ul/li[3]/a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''
        try:
            actorPageURL = actorLink.get('href')
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            actorPhotoURL = actorPage.xpath('//div[@class="modelBioPic"]/img/@src0_3x')[0]
            if 'http' not in actorPhotoURL:
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
        except:
            pass

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [
        scenePoster
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
