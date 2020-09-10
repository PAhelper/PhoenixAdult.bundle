import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    actressID = searchTitle.split(' ', 1)[0]
    try:
        sceneTitle = searchTitle.split(' ', 1)[1]
    except:
        sceneTitle = ''

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + actressID)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//ul[@class="Models"]/li'):
        titleNoFormatting = searchResult.xpath('.//figure/p[1]')[0].text_content().strip()
        titleNoFormattingID = PAutils.Encode(titleNoFormatting)

        actor = searchResult.xpath('//li[@class="modelCurrent"]')[0].text_content().strip()

        # Release Date
        date = searchResult.xpath('.//figure/p[2]')[0].text_content().replace('Release Date:', '').strip()
        releaseDate = parse(date).strftime('%Y-%m-%d') if date else ''

        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])

        score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s|%s|%s' % (curID, siteNum, titleNoFormattingID, releaseDate, actor), name='%s [InTheCrack]' % titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h2//span')[0].text_content().strip()

    # Studio
    metadata.studio = 'InTheCrack'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Solo')

    # Release Date
    date = PAutils.Decode(metadata_id[3])
    if date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actor = PAutils.Decode(metadata_id[4])
    if actor:
        actorName = actor
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    scenepic = PAsearchSites.getSearchBaseURL(siteID).strip() + detailsPageElements.xpath('//style')[0].split('\'')[1].strip()

    if scenepic:
        art.append(scenepic)

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
