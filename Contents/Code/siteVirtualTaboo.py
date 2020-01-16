import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    try:
        searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(searchSiteID) + encodedTitle)
        for searchResult in searchResults.xpath('//div[@class="video-item"]'):
            titleNoFormatting = searchResult.xpath('.//div[@class="video-title"]//a')[0].text_content()
            sceneUrl = searchResult.xpath('.//a[contains(@class, "play")]/@href')[0]
            curID = sceneUrl.replace('/', '$').replace('?', '!')
            releaseDate = parse(searchResult.xpath('.//div[@class="info"]')[0].text_content()[-30:].strip()).strftime('%Y-%m-%d')

            actorList = []
            for actor in searchResult.xpath('.//div[@class="info"]//a'):
                actorList.append(actor.text_content())
            actors = ', '.join(actorList)

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s in %s [%s, %s]' % (actors, titleNoFormatting, PAsearchSites.getSearchSiteName(searchSiteID), releaseDate), score=score, lang=lang))
    except Exception as e:
        Log(e)
        pass

    return results


def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split('|')[0].replace('$', '/').replace('?', '!')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//div[contains(@class, "right-info")]//h1')[0].text_content().strip()

    # Studio/Tagline/Collection
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Date
    date = str(metadata.id).split('|')[2]
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Summary
    description = detailsPageElements.xpath('//div[@class="description"]//span[contains(@class, "full")]')

    if description:
        metadata.summary = description[0].text_content().strip()
    else:
        metadata.summary = detailsPageElements.xpath('//div[@class="description"]')[0].text_content().strip()

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class, "right-info")]//div[@class="info"]//a')
    if actors:
        for actor in actors:
            actorName = actor.text_content().strip()
            movieActors.addActor(actorName, '')

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="tag-list"]//a')
    if genres:
        for genre in genres:
            genreName = genre.text_content().strip()
            movieGenres.addGenre(genreName)

    # Posters
    art = []

    style = detailsPageElements.xpath('//div[@id="player"]/@style')[0]
    img = style[style.find("'") + 1:style.rfind("'")].split('?', 1)[0]
    art.append(img)

    posters = detailsPageElements.xpath('//div[@class="gallery-item"]//a/@href')
    for poster in posters:
        img = poster.split('?', 1)[0]
        art.append(img)

    i = 1
    Log('Artwork found: %d' % len(art))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
    }
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                req = urllib.Request(posterUrl, headers=headers)
                img_file = urllib.urlopen(req)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers=headers).content, sort_order=i)
                if(width > 100 and i > 1):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers=headers).content, sort_order=i)
                i = i + 1
            except:
                pass

    return metadata
