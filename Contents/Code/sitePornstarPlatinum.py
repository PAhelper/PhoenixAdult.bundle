import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="item no-nth "]'):
        titleNoFormatting = searchResult.xpath('./div[@class="item-content"]/h3/a')[0].text_content()
        sceneURL = searchResult.xpath('./div[@class="item-content"]/h3/a/@href')[0]
        curID = PAutils.Encode(sceneURL)
        posterURL = PAutils.Encode(searchResult.xpath('./div[@class="item-header"]/a/img/@rel')[0])
        actorname = ''
        # Release Date
        date = ''
        try:
            date = searchResult.xpath('./div[@class="item-content"]/div[@style="overflow:hidden"]/span[@class="left content-date"]')[0].text_content().strip()
            actorname = searchResult.xpath('./div[@class="item-content"]/div[@style="overflow:hidden"]/span[@class="marker left"]')[0].text_content().strip()
        except:
            pass
        releaseDate = parse(date).strftime('%Y-%m-%d') if date else ''

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id='%s|%d|%s|%s|%s|%s' % (curID, siteNum, titleNoFormatting, releaseDate, posterURL, actorname), name='%s %s [%s]' % (titleNoFormatting, releaseDate, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    posterURL = PAutils.Decode(metadata_id[4])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Studio
    metadata.studio = 'Pornstar Platinum'

    # Title
    metadata.title = PAutils.Decode(metadata_id[2]).strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="panel-content"]/p')[0].text_content().strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="tagcloud"]/a'):
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)

    # Release Date
    date_object = parse(PAutils.Decode(metadata_id[3]))
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actorName = PAutils.Decode(metadata_id[5])
    actorPhotoURL = ''

    movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    if posterURL:
        art.append(posterURL)

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
