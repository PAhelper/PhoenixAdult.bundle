import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    sceneID = searchTitle.split(' ', 1)[0]
    try:
        sceneTitle = searchTitle.split(' ', 1)[1]
    except:
        sceneTitle = ''

    url = PAsearchSites.getSearchSearchURL(siteNum) + sceneID + '/1'
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="wxt7nk-0 JqBNK"]//div[1]/h2'):
        titleNoFormatting = searchResult.xpath('//div[1]/h2')[0].text_content().replace('Trailer', '').strip()
        curID = PAutils.Encode(url)

        if sceneTitle:
            score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())
        else:
            score = 90

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [TrueAmatuers]' % titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    metadata.title = detailsPageElements.xpath('//h2[@class="wxt7nk-4 fSsARZ"]')[0].text_content().replace('SML-', '').replace('Trailer', '').strip()

    # Studio
    metadata.studio = 'TrueAmateurs'

    # Tagline and Collection(s)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.tagline)

    # Genres
    for genreLink in detailsPageElements.xpath('//div[@class="tjb798-2 flgKJM"]/span[1]/a'):
        genreName = genreLink.text_content().replace(',', '').strip().lower()

        movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="tjb798-3 gFvmpb"]/span[last()]')
    if date:
        date = date[0].text_content().strip().replace('Release Date:', '')
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    try:
        actors = detailsPageElements.xpath('//a[@class="wxt7nk-6 czvZQW"]')
        if actors:
            if len(actors) == 3:
                movieGenres.addGenre('Threesome')
            if len(actors) == 4:
                movieGenres.addGenre('Foursome')
            if len(actors) > 4:
                movieGenres.addGenre('Orgy')

            for actorLink in actors:
                actorPageURL = actorLink.get('href')
                req = PAutils.HTTPRequest(actorPageURL)
                actorPage = HTML.ElementFromString(req.text)
                actorPhotoURL = 'http:' + actorPage.xpath('//div[@class="profilePic_in"]//img/@src')[0]

                movieActors.addActor(actorName, actorPhotoURL)
    except:
        pass

    # Posters
    art = []
    xpaths = [
        '//div[@class="tg5e7m-2 evtSOm"]/img/@src'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

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
