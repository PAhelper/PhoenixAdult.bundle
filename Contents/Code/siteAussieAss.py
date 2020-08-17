import PAsearchSites
import PAgenres
import PAactors
import PAutils
import string
import re


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = re.sub(r'\d+', '', searchTitle.replace(' ', '').replace('--', '').lower())
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle + ".html")
    modelResults = HTML.ElementFromString(req.text)
    sceneID = re.sub('\D', '', searchTitle)

    pageResults = (int)(modelResults.xpath('//span[@class="number_item "]')[0].text_content().strip())
    Log(pageResults)

    if not pageResults:
        pageResults = 1

    for x in range(pageResults):
        if x == 1:
            modelResults.xpath('//a[contains(@class,"in_stditem")]/@href')[1]
            req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + modelResults.xpath('//a[contains(@class,"in_stditem")]/@href')[1])
            modelResults = HTML.ElementFromString(req.text)
        for searchResult in modelResults.xpath('//div[@class="infos"]'):
            resultTitleID = string.capwords(searchResult.xpath('.//span[@class="video-title"]')[0].text_content().strip())

            titleNoFormatting = re.sub(r'\d+', '', resultTitleID)

            resultID = re.sub('\D', '', resultTitleID)

            sceneURL = searchResult.xpath('.//a/@href')[0]
            curID = PAutils.Encode(sceneURL)

            date = searchResult.xpath('.//span[@class="video-date"]')[0].text_content().strip()

            if date:
                releaseDate = parse(date).strftime('%Y-%m-%d')
            else:
                releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
            releaseDate = parse(date).strftime('%Y-%m-%d')
            displayDate = releaseDate if date else ''

            if sceneID == resultID:
                score = 100
            elif searchDate and displayDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    metadata.title = re.sub(r'\d+', '', string.capwords(detailsPageElements.xpath('//h4/span')[0].text_content()))

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="row"]//a/@title')[0].strip()
    except:
        pass
    Log (metadata.summary)
    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Actors
    actors = detailsPageElements.xpath('//h5//a')
    actorPhotoURL = ''

    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 5:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = string.capwords(actorLink.text_content())

            modelURL = actorLink.xpath('./@href')[0]
            req = PAutils.HTTPRequest(modelURL)
            actorsPageElements = HTML.ElementFromString(req.text)

            img = actorsPageElements.xpath('//img[contains(@id,"set-target")]/@src')[0]
            if img:
                actorPhotoURL = img
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL

            movieActors.addActor(actorName, actorPhotoURL)

    date = sceneDate
    date = parse(date).strftime('%d-%m-%Y')

    if date:
        date_object = datetime.strptime(date, '%d-%m-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genre in detailsPageElements.xpath('//meta[@name="keywords"]/@content')[0].replace('Aussie Ass','').split(','):
        movieGenres.addGenre(genre.strip())

    # Posters
    art = []
    xpaths = [
        '//img[contains(@alt,"content")]/@src'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if 'http' not in img:
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
