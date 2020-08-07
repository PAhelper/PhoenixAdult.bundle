import PAsearchSites
import PAgenres
import PAactors
import PAutils
from dateutil.relativedelta import relativedelta


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    url = PAsearchSites.getSearchSearchURL(siteNum) + "%22" + encodedTitle + "%22"
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)

    for searchResult in searchResults.xpath('//div[@class="listado-escenas listado-busqueda"]//div[@class="medida"]/a'):
        titleNoFormatting = searchResult.xpath('.//h2')[0].text_content().strip()
        curID = PAutils.Encode(PAsearchSites.getSearchBaseURL(siteNum) + searchResult.get('href'))

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [CumLouder]' % titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@id="content-more-less"]/p')[0].text_content().strip()

    # Studio
    metadata.studio = 'CumLouder'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//ul[@class="tags"]/li/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Release Date - no actual date aviable, guessing (better than nothing)
    date = detailsPageElements.xpath('//div[@class="added"]')[0].text_content().strip()
    timeframe = date.split(' ')[2]
    timenumber = int(date.split(' ')[1])
    today = datetime.now()

    if timeframe:
        if timeframe == 'minutes':
            date_object = today
        elif timeframe == 'hour' or timeframe == 'hours':
            date_object = today - relativedelta(hours=timenumber)
        elif timeframe == 'day' or timeframe == 'days':
            date_object = today - relativedelta(days=timenumber)
        elif timeframe == 'week' or timeframe == 'weeks':
            date_object = today - relativedelta(weeks=timenumber)
        elif timeframe == 'month' or timeframe == 'months':
            date_object = today - relativedelta(months=timenumber)
        elif timeframe == 'year' or timeframe == 'years':
            date_object = today - relativedelta(years=timenumber)

        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[@class="pornstar-link"]')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@class="box-video box-video-html5"]/video/@lazy'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
