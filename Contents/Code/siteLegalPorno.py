import PAsearchSites
import PAgenres


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    if 'Search for' in searchResults.xpath('//title/text()')[0]:
        for searchResult in searchResults.xpath('//div[@class="thumbnails"]/div'):
            curID = searchResult.xpath('.//a/@href')[0].replace('/', '+').replace('?', '!')
            titleNoFormatting = searchResult.xpath('.//div[contains(@class, "thumbnail-title")]//a/@title')[0]
            releaseDate = parse(searchResult.xpath('./@release')[0]).strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name = '%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))
    else:
        curID = urllib.unquote(searchResults.xpath('//div[@class="user--guest"]//a/@href')[0]).split('=', 1)[1].replace('/', '+').replace('?', '!')
        titleNoFormatting = searchResults.xpath('//h1[@class="watchpage-title"]')[0].text_content().strip()
        releaseDate = parse(searchResults.xpath('//span[@class="scene-description__detail"]//a/text()')[0]).strftime('%Y-%m-%d')

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name = '%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=100, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    url = metadata_id[0].replace('+', '/').replace('?', '!')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="watchpage-title"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'LegalPorno'

    # Release Date
    releaseDate = detailsPageElements.xpath('//span[@class="scene-description__detail"]//a/text()')[0]
    date_object = parse(releaseDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//a[@class="watchpage-studioname"]/text()')[0].strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//dd/a[contains(@href, "/niche/")]')

    for genreLink in genres:
        genreName = genreLink.text_content().title()
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//dd/a[contains(@href, "model") and not(contains(@href, "forum"))]')
    for actorLink in actors:
        actorName = actorLink.text_content()
        actorPageURL = actorLink.get('href')
        actorPage = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPage.xpath('//div[@class="model--avatar"]//img/@src')[0]
        movieActors.addActor(actorName, actorPhotoURL)

    # Director
    director = metadata.directors.new()
    if tagline == 'Giorgio Grandi' or tagline == 'Giorgio\'s Lab':
        director.name = 'Giorgio Grandi'
    try:
        directors = detailsPageElements.xpath('//p[@class="director"]/a')
        for dirname in directors:
            director.name = dirname.text_content().strip()
    except:
        pass

    # Posters/Background
    art = [
        detailsPageElements.xpath('//div[@id="player"]/@style')[0].split('url(')[1].split(')')[0]
    ]

    for img in detailsPageElements.xpath('//div[contains(@class, "thumbs2 gallery")]//img/@src'):
        art.append(img)

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
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass
    
    return metadata
