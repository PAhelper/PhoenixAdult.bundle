import PAsearchSites
import PAgenres
import PAactors
import re
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    firstpage = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + "/page1.html"
    req = PAutils.HTTPRequest(firstpage)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//nav[@aria-label="pagination-top"]//div[@class="dropdown-menu"]/a[@class="dropdown-item"]'):
        pageURL = searchResult.xpath('./@href')[0]
        req = PAutils.HTTPRequest(pageURL)
        pageResults = HTML.ElementFromString(req.text)
        for pageResult in pageResults.xpath('//li[@class="col-sm-6 col-lg-4"]'):
            imgURL = pageResult.xpath('.//div[@class="vidthumb"]/a[@class="diagrad"]/img/@src')[0]
            curID = PAutils.Encode(imgURL)
            titleNoFormatting = pageResult.xpath('.//div[@class="vidtitle"]/p[1]')[0].text_content().strip()
            # Release Date
            date = ''
            try:
                date = pageResult.xpath('.//div[@class="vidtitle"]/p[2]')[0].text_content().strip()
            except:
                pass
            releaseDate = parse(date).strftime('%Y-%m-%d') if date else ''
            description = pageResult.xpath('.//div[@class="collapse"]/p')[0].text_content().split(':')[1].strip()
            description = PAutils.Encode(description)

            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            results.Append(MetadataSearchResult(id='%s|%d|%s|%s|%s' % (curID, siteNum, releaseDate, titleNoFormatting, description), name='%s %s [%s]' % (titleNoFormatting, releaseDate, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    imgURL = PAutils.Decode(metadata_id[0])
    if not imgURL.startswith('http'):
        imgURL = PAsearchSites.getSearchBaseURL(siteID) + imgURL

    # Studio
    metadata.studio = 'Sicflics'

    # Title
    metadata.title = PAutils.Decode(metadata_id[3])

    # Summary
    description = PAutils.Decode(metadata_id[4])
    if description:
        metadata.summary = description.replace('\n', '').strip()
    Log(metadata.summary)

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres TODO: get genres from homepage
    movieGenres.clearGenres()
    movieGenres.addGenre("Extreme")

    # Release Date
    date_object = parse(PAutils.Decode(metadata_id[2]))
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    description = description.encode('ascii', 'replace')
    actorName = re.split("['?]", description)[1].strip()
    actorPhotoURL = ''
    if actorName:
        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    if imgURL:
        art.append(imgURL)

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
