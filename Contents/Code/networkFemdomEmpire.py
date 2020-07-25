import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    # Advanced Search
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "item-info")]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Femdom Empire] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    # Difficult Scenes
    if searchTitle == 'Extreme Strap on Training':
        curID = PAutils.Encode('https://femdomempire.com/tour/trailers/EXTREMEStrap-OnTraining.html')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='EXTREME Strap-On Training [Femdom Empire] 2012-04-11', score=101, lang=lang))
    if searchTitle == 'Tease  Stroke':
        curID = PAutils.Encode('https://femdomempire.com/tour/trailers/TeaseStroke.html')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Tease & Stroke [Femdom Empire] 2012-12-05', score=101, lang=lang))
    if searchTitle == 'Cock Locked':
        curID = PAutils.Encode('https://femdomempire.com/tour/trailers/CockLocked.html')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Cock Locked [Femdom Empire] 2012-04-20', score=101, lang=lang))
    if searchTitle == "Oral Servitude":
        curID = PAutils.Encode('https://femdomempire.com/tour/trailers/OralServitude.html')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Oral Servitude [Femdom Empire] 2012-04-08', score=101, lang=lang))

    if results:
        return results

    # Standard Search
    else:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + '/tour/search.php?query=' + encodedTitle)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[contains(@class, "item-info")]'):
            titleNoFormatting = searchResult.xpath('.//a')[0].text_content().strip()
            scenePage = searchResult.xpath('.//a/@href')[0]
            curID = PAutils.Encode(scenePage)
            releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Femdom Empire] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "videoDetails")]//h3')[0].text_content().strip()

    # Summary
    description = detailsPageElements.xpath('//div[contains(@class, "videoDetails")]//p')
    if description:
        metadata.summary = description[0].text_content().strip()

    # Studio
    metadata.studio = 'Femdom Empire'

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="videoInfo clear"]//p')[0].text_content().replace('Date Added:', '').strip()
    if date:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genreLink in detailsPageElements.xpath('//div[contains(@class, "featuring")][2]//ul//li'):
        genreName = genreLink.text_content().strip().lower().replace('categories:', '').replace('tags:', '')

        movieGenres.addGenre(genreName)

    movieGenres.addGenre('Femdom')

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[contains(@class, "featuring")][1]/ul/li'):
        actorName = actorLink.text_content().strip().replace('Featuring:', '')
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    if metadata.title == 'Owned by Alexis':
        actorName = 'Alexis Monroe'
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//a[@class="fake_trailer"]//img/@src0_1x'
    ]
    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            img = PAsearchSites.getSearchBaseURL(siteID) + img

            art.append(img)

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
