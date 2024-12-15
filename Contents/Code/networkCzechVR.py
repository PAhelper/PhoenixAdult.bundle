import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = None
    parts = searchData.title.split()
    if unicode(parts[0], 'utf8').isdigit():
        sceneID = parts[0]
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
    searchData.encoded = searchData.title.replace(' ', '-')
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[contains(@class, "postTag")]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="nazev"]//h2//a')[0].text_content()
        curSceneID = searchResult.xpath('.//div[@class="nazev"]//h2//a')[0].text_content().split(" -")[0]
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
        releaseDate = parse(searchResult.xpath('.//div[@class="datum"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        actors = searchResult.xpath('.//div[@class="nazev"]//div[@class="featuring"]//a')

        actorList = []
        for actor in actors:
            actorName = actor.text_content().strip()

            actorList.append(actorName)
        actorsPrint = ', '.join(actorList)
        if sceneID:
            score = 100 - Util.LevenshteinDistance(sceneID, curSceneID)
        elif searchData.date:
            score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s in %s [%s] %s' % (actorsPrint, titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors, art):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//head/title')[0].text_content().replace('Czech VR Network', '').replace(' - Czech VR Fetish Porn Videos', '').replace('Czech VR Fetish', '').replace('Czech VR Casting', '').replace('Czech VR', '').strip()

    # Summary
    maybeSummary = detailsPageElements.xpath('//div[@class="text"]')
    if maybeSummary:
        metadata.summary = maybeSummary[0].text_content().strip()
    else:
        metadata.summary = detailsPageElements.xpath('//div[@class="textDetail"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'CzechVR'

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class, "nazev")]//div[@class="datum"]')[0].text_content().strip()
    if date:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    for genreLink in detailsPageElements.xpath('//div[@class="tag new"]//a'):
        genreName = genreLink.text_content().lower().strip()
        movieGenres.addGenre(genreName)
    for genreLink in detailsPageElements.xpath('//div[@class="tag"]//a'):
        genreName = genreLink.text_content().lower().strip()
        movieGenres.addGenre(genreName)

    # Actor(s)
    for actorLink in detailsPageElements.xpath('//div[@class="modelky"]//a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    for actorLink in detailsPageElements.xpath('(//div[contains(@class, "nazev")])[1]//div[@class="featuring"]//a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    xpaths = [
        '//div[@class="foto"]//dl8-video/@poster',
        '//div[@class="galerka"]//a/@href'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            poster = poster[1:]
            if not poster.startswith('http'):
                poster = PAsearchSites.getSearchBaseURL(siteNum) + poster

            art.append(poster)

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
