import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@style="position:relative; background:black;"]'):
        titleNoFormatting = searchResult.xpath('.//a/@title')[0]

        SubSite = searchResult.xpath('.//img/@src')[0]
        if 'wetandpissy' in SubSite:
            SubSite = 'Wet and Pissy'
        if 'weliketosuck' in SubSite:
            SubSite = 'We Like To Suck'
        if 'wetandpuffy' in SubSite:
            SubSite = 'Wet and Puffy'
        if 'simplyanal' in SubSite:
            SubSite = 'Simply Anal'
        if 'eurobabefacials' in SubSite:
            SubSite = 'Euro Babe Facials'

        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [Puffy Network/%s]' % (titleNoFormatting, SubSite), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    sceneDate = metadata_id[2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div/section[1]/div[2]/h2/span')[0].text_content().strip()

    # Summary
    all_summary = detailsPageElements.xpath('//div/section[3]/div[2]')[0].text_content().strip()
    tags_summary = detailsPageElements.xpath('//div/section[3]/div[2]/p')[0].text_content().strip()
    summary = all_summary.replace(tags_summary, '')
    summary = summary.split('Show more...')[0].strip()
    metadata.summary = summary

    # Studio
    metadata.studio = 'Puffy Network'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div/section[2]/dl/dt[2]')[0].text_content().replace('Released on:', '')
    if not date and sceneDate:
        date = sceneDate

    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div/section[3]/div[2]/p/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div/section[2]/dl/dd[1]/a')
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

            actorPageURL = actorLink.get('href')
            if 'http' not in actorPageURL:
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorPageURL
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            actorPhotoNode = actorPage.xpath('//div/section[1]/div/div[1]/img/@src')
            if actorPhotoNode:
                actorPhotoURL = actorPhotoNode[0]
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    twitterBG = None
    cover = sceneURL.split('-video-')[1]
    if 'Wet and Pissy' in tagline:
        twitterBG = 'https://media.wetandpissy.com/videos/video-' + cover + 'cover/hd.jpg'
    elif 'We Like To Suck' in tagline:
        twitterBG = 'https://media.weliketosuck.com/videos/video-' + cover + 'cover/hd.jpg'
    elif 'Wet and Puffy' in tagline:
        twitterBG = 'https://media.wetandpuffy.com/videos/video-' + cover + 'cover/hd.jpg'
    elif 'Simply Anal' in tagline:
        twitterBG = 'https://media.simplyanal.com/videos/video-' + cover + 'cover/hd.jpg'
    elif 'Euro Babe Facials' in tagline:
        twitterBG = 'https://media.eurobabefacials.com/videos/video-' + cover + 'cover/hd.jpg'

    if twitterBG:
        art.append(twitterBG)

    xpaths = [
        '//div[contains(@id, "pics")]//@src'
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
