import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="itemm"]'):
        titleNoFormatting = searchResult.xpath('.//a/@title')[0]
        releaseDate = parse(searchResult.xpath('.//span[@class="nm-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])

        subSite = searchResult.xpath('.//img[@class="domain-label"]/@src')[0]
        if 'allinternal' in subSite:
            subSite = 'AllInternal'
        elif 'asstraffic' in subSite:
            subSite = 'AssTraffic'
        elif 'givemepink' in subSite:
            subSite = 'GiveMePink'
        elif 'primecups' in subSite:
            subSite = 'PrimeCups'
        elif 'fistflush' in subSite:
            subSite = 'FistFlush'
        elif 'cumforcover' in subSite:
            subSite = 'CumForCover'
        elif 'tamedteens' in subSite:
            subSite = 'TamedTeens'
        elif 'spermswap' in subSite:
            subSite = 'SpermSwap'
        elif 'milfthing' in subSite:
            subSite = 'MilfThing'
        elif 'interview' in subSite:
            subSite = 'Interview'
        else:
            subSite = PAsearchSites.getSearchSiteName(siteNum)

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Perfect Gonzo/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h2')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="col-sm-8 col-md-8 no-padding-side"]/p')[0].text_content().strip()

    # Studio
    metadata.studio = 'Perfect Gonzo'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="col-sm-6 col-md-6 no-padding-left no-padding-right text-right"]/span')[0].text_content().replace('Added', '').strip()
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="col-sm-8 col-md-8 no-padding-side tag-container"]//a'):
        genreName = genreLink.text_content().strip().lower()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="col-sm-3 col-md-3 col-md-offset-1 no-padding-side"]/p/a'):
        actorName = actorLink.text_content().strip()

        actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPage.xpath('//div[@class="col-md-8 bigmodelpic"]/img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [
        detailsPageElements.xpath('//video/@poster')[0]
    ]
    xpaths = [
        '//ul[@class="bxslider_screenshots"]//img',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            img = poster.get('src')
            if not img:
                img = poster.get('data-original')

            if img:
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
