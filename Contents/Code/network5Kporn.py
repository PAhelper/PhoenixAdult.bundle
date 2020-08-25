import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    sceneID = re.sub('\D.*', '', searchTitle)
    cookies = {'nats': 'MC4wLjMuNTguMC4wLjAuMC4w'}

    if sceneID:
        sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + sceneID
        req = PAutils.HTTPRequest(sceneURL, cookies=cookies)
        searchResult = HTML.ElementFromString(req.text)

        titleNoFormatting = re.sub(r'(\s\|).*', '', searchResult.xpath('//title')[0].text_content())
        curID = PAutils.Encode(sceneURL)
        date = re.sub(r'\D(?=\D)', '',searchResult.xpath('//h5[contains(.,"Published")]')[0].text_content().strip())
        score = 100

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), date), score=score, lang=lang))
    else:
        encodedTitle =  searchTitle.replace(' ', '-')
        searchURL = PAsearchSites.getSearchBaseURL(siteNum) + '/models/' + encodedTitle

        req = PAutils.HTTPRequest(searchURL, cookies=cookies)
        searchResults = HTML.ElementFromString(req.text)

        for searchResult in searchResults.xpath('//div[contains(@class,"epwrap")]'):
            sceneURL = searchResult.xpath('.//h3//@href')[0]
            req = PAutils.HTTPRequest(sceneURL, cookies=cookies)
            sceneResult = HTML.ElementFromString(req.text)

            titleNoFormatting = re.sub(r'(\s\|).*', '', sceneResult.xpath('//title')[0].text_content())
            curID = PAutils.Encode(sceneURL)
            date = re.sub(r'\D(?=\D)', '', sceneResult.xpath('//h5[contains(.,"Published")]')[0].text_content().strip())

            if date:
                releaseDate = parse(date).strftime('%Y-%m-%d')
            else:
                releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
            releaseDate = parse(date).strftime('%Y-%m-%d')
            displayDate = releaseDate if date else ''

            if searchDate and displayDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))


    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    try:
        sceneDate = metadata_id[2]
    except:
        pass

    cookies = {'nats': 'MC4wLjMuNTguMC4wLjAuMC4w'}
    req = PAutils.HTTPRequest(sceneURL, cookies=cookies)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = re.sub(r'(\s\|).*', '', detailsPageElements.xpath('//title')[0].text_content())

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class=""]')[0].text_content()

    # Studio
    metadata.studio = '5Kporn'

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.add(metadata.tagline)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h5[contains(.,"Starring")]')

    if actors:
        for actorLink in actors:
            actorName = re.sub(r'\D.*(?:\:)', '', actorLink.text_content().strip())

            modelURL = actorLink.xpath('.//@href')[0]
            Log(modelURL)
            req = PAutils.HTTPRequest(modelURL, cookies=cookies)
            actorsPageElements = HTML.ElementFromString(req.text)

            img = actorsPageElements.xpath('//div[contains(@class,"model-bio")]//img/@src')[1]
            if img:
                actorPhotoURL = img

            movieActors.addActor(actorName, actorPhotoURL)

    # Date
    date = re.sub(r'\D(?=\D)', '', detailsPageElements.xpath('//h5[contains(.,"Published")]')[0].text_content().strip())

    if date:
        date = parse(date).strftime('%d-%m-%Y')
        date_object = datetime.strptime(date, '%d-%m-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()

    # Posters
    art = []
    xpaths = [
        '//div[contains(@class,"gal")]//img/@src',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            art.append(img)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': sceneURL}, cookies=cookies)
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
