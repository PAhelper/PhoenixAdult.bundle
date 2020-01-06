import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchJAVID = None
    splitSearchTitle = searchTitle.split(' ')
    if(unicode(splitSearchTitle[1], 'utf-8').isnumeric()):
        searchJAVID = '%s-%s' % (splitSearchTitle[0], splitSearchTitle[1])

    if searchJAVID:
        encodedTitle = searchJAVID

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//li[contains(@class, "item-list")]'):
        titleNoFormatting = searchResult.xpath('.//dt')[0].text_content().strip()
        JAVID = searchResult.xpath('.//img/@alt')[0]
        sceneURL = searchResult.xpath('.//a/@href')[0].rsplit('/', 1)[0]
        curID = sceneURL.replace('/', '$').replace('?', '!')

        if searchJAVID:
            score = 100 - Util.LevenshteinDistance(searchJAVID.lower(), JAVID.lower())
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%s' % (curID, str(siteNum)), name='[%s] %s' % (JAVID, titleNoFormatting), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split('|')[0].replace('$', '/').replace('?', '!')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//cite[@itemprop="name"]')[0].text_content().strip()

    # Summary
    try:
        description = detailsPageElements.xpath('//div[@class="cmn-box-description01"]')[0].text_content()
        metadata.summary = description.replace('Product Description', '', 1).strip()
    except:
        pass

    # Studio
    metadata.studio = detailsPageElements.xpath('//dd[@itemprop="productionCompany"]')[0].text_content().strip()

    # Director
    director = metadata.directors.new()
    directorName = detailsPageElements.xpath('//dd[@itemprop="director"]')[0].text_content().strip()
    if directorName != '----':
        director.name = directorName

    # Release Date
    date = detailsPageElements.xpath('//dd[@itemprop="dateCreated"]')[0].text_content().strip().replace('.', '').replace(',', '').replace('Sept', 'Sep').replace('June', 'Jun').replace('July', 'Jul')
    date_object = datetime.strptime(date, '%b %d %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@itemprop="actors"]//span[@itemprop="name"]')
    if len(actors) > 0:
        for actor in actors:
            fullActorName = actor.text_content().strip()
            if fullActorName != '----':
                splitActorName = fullActorName.split('(')
                mainName = splitActorName[0].strip()
                actorPhotoURL = detailsPageElements.xpath('//div[@id="%s"]//img[contains(@alt, "%s")]/@src' % (mainName.replace(' ', ''), mainName))[0]
                if actorPhotoURL.rsplit('/', 1)[1] == 'nowprinting.gif':
                    actorPhotoURL = ''
                if len(splitActorName) > 1 and mainName == splitActorName[1][:-1]:
                    actorName = mainName
                else:
                    actorName = fullActorName
                movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@itemprop="genre"]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().lower().strip()
            movieGenres.addGenre(genreName)
    metadata.collections.add('Japan Adult Video')

    # Posters
    art = []
    # img = detailsPageElements.xpath('//img[@itemprop="image"]/@src')[0]
    img = detailsPageElements.xpath('//img[contains(@alt, "cover")]/@src')[0]
    art.append(img)

    for poster in detailsPageElements.xpath('//section[@id="product-gallery"]//img/@data-src'):
        art.append(poster)

    i = 1
    Log('Artwork found: ' + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=i)
                if(width > 100 and i > 1):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=i)
                i = i + 1
            except:
                pass

    if len(metadata.art) == 0 and len(metadata.posters) > 1:
        metadata.art[art[0]] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)

    return metadata
