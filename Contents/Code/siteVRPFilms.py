import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//article[contains(@class, "movie-column")]'):
        titleNoFormatting = searchResult.xpath('.//h3')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))
    
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    sceneDate = metadata_id[2]
    detailsPageElements = HTML.ElementFromURL(sceneURL)

    script_text = detailsPageElements.xpath('//script[@type="application/ld+json"]')[0].text_content()
    sceneData = json.loads(script_text)

    WebPage = None
    ImageObject = None
    for item in sceneData['@graph']:
        if item['@type'] == 'ImageObject':
            ImageObject = item
        elif item['@type'] == 'WebPage':
            WebPage = item

    # Title
    metadata.title = detailsPageElements.xpath('//h3[contains(@class, "release-title")]/span')[0].text_content().strip()

    # Summary
    description = ''
    for item in detailsPageElements.xpath('//div[contains(@class,"movie-content")]/p'):
        description += item.text_content().strip() + '\n'
    metadata.summary = description

    # Studio/Tagline/Collection
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Release Date
    if WebPage:
        date = WebPage['datePublished']
    elif sceneDate:
        date = sceneDate

    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actorName = detailsPageElements.xpath('//div[@class="detail"][2]//p/text()[2]')[0].strip()
    actorPageURL = '%s/pornstar/%s' % (PAsearchSites.getSearchBaseURL(siteID), actorName.replace(' ', '-'))
    actorPage = HTML.ElementFromURL(actorPageURL)
    actorPhotoURL = actorPage.xpath('//section[contains(@id, "pornstar-profile")]//img/@src')[0]

    movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="movies-description"]//div[3]//p/text()[2]')[0].split(','):
        genreName = genreLink

        movieGenres.addGenre(genreName)

    # Posters/Background
    art = []
    xpaths = [
        '//div[contains(@class, "movies-gallery")]//a/@href',
    ]
    if ImageObject:
        art.insert(0, ImageObject['url'])

    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if(width > 100 and idx > 1):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
