import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[contains(@class, "card-simple")]'):
        titleNoFormatting = searchResult.xpath('.//a[@class="color-title"]/text()')[0]
        curID = searchResult.xpath('.//a/@href')[0].replace('/', '+').replace('?', '!')
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name=titleNoFormatting, score=score, lang=lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = metadata_id[0].replace('+', '/').replace('!', '?')
    sceneDate = metadata_id[2]
    url = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    detailsPageElements = HTML.ElementFromURL(url)

    # Studio
    metadata.studio = 'Joymii'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="font-cond"]')[0].text_content().strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = 'Step Secrets'
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = ['European', 'Taboo', 'Glamcore']
    for genre in genres:
        movieGenres.addGenre(genre)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="descripton"]')[0].text_content().strip()

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//p[@class="mb-2"]//a')
    for actorLink in actors:
        actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get('href')
        actorPage = HTML.ElementFromURL(actorPageURL)
        actorName = actorPage.xpath('//h1[contains(@class, "font-cond")]')[0].text_content().strip()
        actorPhotoURL = actorPage.xpath('//div[contains(@class, "model-about")]//img/@src')[0].split('?')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    ### Posters and artwork ###
    art = []
    xpaths = [
        '//video/@poster',
        '//div[@id="photoCarousel"]//img/@src'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
