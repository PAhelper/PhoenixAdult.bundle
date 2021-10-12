import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    # Advanced Search
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "item-info")]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        if searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Femdom Empire] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    # Difficult Scenes
    if searchData.title in manualMatch:
        item = manualMatch[searchData.title]
        curID = PAutils.Encode(item['curID'])

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name=item['name'], score=101, lang=lang))

    if results:
        return results

    # Standard Search
    else:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + '/tour/search.php?query=' + searchData.encoded)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[contains(@class, "item-info")]'):
            titleNoFormatting = searchResult.xpath('.//a')[0].text_content().strip()
            scenePage = searchResult.xpath('.//a/@href')[0]
            curID = PAutils.Encode(scenePage)
            releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Femdom Empire] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
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
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
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
            img = PAsearchSites.getSearchBaseURL(siteNum) + img

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata


manualMatch = {
    'Extreme Strap on Training': {
        'curID': 'https://femdomempire.com/tour/trailers/EXTREMEStrap-OnTraining.html',
        'name': 'EXTREME Strap-On Training [Femdom Empire] 2012-04-11',
    },
    'Cock Locked': {
        'curID': 'https://femdomempire.com/tour/trailers/CockLocked.html',
        'name': 'Cock Locked [Femdom Empire] 2012-04-20',
    },
    'Oral Servitude': {
        'curID': 'https://femdomempire.com/tour/trailers/OralServitude.html',
        'name': 'Oral Servitude [Femdom Empire] 2012-04-08',
    },
}
