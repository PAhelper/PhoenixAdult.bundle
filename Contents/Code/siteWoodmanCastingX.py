import PAsearchSites
import PAutils

cookies = {}


def getSiteData(url, cookies=cookies):
    req = PAutils.HTTPRequest(url, cookies=cookies)
    detailsPageElements = HTML.ElementFromString(req.text)

    item = detailsPageElements.xpath('//div[@id and not(@id="error")]/@id')
    if len(item) == 1:
        cookies[item[0]] = '1'

        detailsPageElements = getSiteData(url)

    return detailsPageElements


def search(results, lang, siteNum, searchData):
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded
    searchResults = getSiteData(url)
    for searchResult in searchResults.xpath('//div[contains(@class, "items")]/a[contains(@class, "scene")]'):
        sceneURL = searchResult.xpath('./@href')[0]
        if not sceneURL.startswith('http'):
            titleNoFormatting = searchResult.xpath('./img/@alt')[0]
            curID = PAutils.Encode(sceneURL)

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    detailsPageElements = getSiteData(sceneURL)

    # Studio
    metadata.studio = 'Woodman Casting X'

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    description = detailsPageElements.xpath('//p[@class="description"]')
    if description:
        description = description[0].text_content().strip()
        description = ' '.join(description.split())

        metadata.summary = description

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//span[contains(., "Published")]/following-sibling::text()')
    if date:
        date = date[0].replace(':', '').strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="tags"]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()

    actors = detailsPageElements.xpath('//div[contains(@class, "block_girls_videos")]/a[@class="girl_item"]')
    if actors:
        for actorLink in actors:
            actorName = actorLink.xpath('.//span[@class="name"]')[0].text_content().strip()
            actorPhotoURL = actorLink.xpath('.//img/@src')[0]

            movieActors.addActor(actorName, actorPhotoURL)
    else:
        actorName = detailsPageElements.xpath('//div[@id="breadcrumb"]/span[@class="crumb"]')[0].text_content().split('-')[0].strip()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    for posterLink in detailsPageElements.xpath('//video[@class="player_video"]/@poster'):
        art.append(posterLink)

    script = detailsPageElements.xpath('//script[contains(., "var player")]')
    if script:
        regex = re.search(r'image: \"(.*?)\"', script[0].text_content().strip())
        if regex:
            art.append(regex.group(1))

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
