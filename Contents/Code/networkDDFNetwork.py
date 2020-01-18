import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    sceneID = None
    for search in searchTitle.split(' '):
        if unicode(search, 'UTF-8').isdigit():
            sceneID = search
            break

    if sceneID:
        url = PAsearchSites.getSearchBaseURL(siteNum) + '/videos/get/' + sceneID
        detailsPageElements = HTML.ElementFromURL(url)

        searchTitle = detailsPageElements.xpath('//h1')[0].text_content().strip()

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.replace(' ', '+'))
    for searchResult in searchResults.xpath('//div[@id="content"]//div[contains(@class, "card-body")]'):
        titleNoFormatting = searchResult.xpath('.//a/@title')[0]

        releaseDate = searchResult.xpath('.//small[@class="text-muted"]/@datetime')
        if releaseDate:
            releaseDate = parse(releaseDate[0]).strftime('%Y-%m-%d')
        else:
            releaseDate = ''

        sceneCover = searchResult.xpath('.//..//img/@data-src')[0].replace('/','_').replace('?','!')
        url = searchResult.xpath('.//..//img/@data-src')[0]
        if not url.startswith('http'):
            url = PAsearchSites.getSearchBaseURL(siteNum) + url
        curID = searchResult.xpath('.//a/@href')[0].replace('/','_').replace('?','!')
        if searchDate and releaseDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, sceneCover), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split('|')[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Studio
    metadata.studio = "DDFProd"

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@id="descriptionBoxMobile"]')[0].text_content().strip()

    # Tagline / Collection
    tagline = PAsearchSites.getSearchSiteName(siteID)

    metadata.tagline = tagline
    metadata.collections.clear()
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[contains(@class, "tags")]//li')

    for genreLink in genres:
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)

    # Release Date
    date_object = None
    for item in detailsPageElements.xpath('//div[@id="video-specs"]//div//p'):
        try:
            item = item.text_content().strip()
            if item:
                date_object = parse(item)
                break
        except:
            pass
    if date_object:
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class, "pornstar-card")]//img')
    for actor in actors:
        actorName = actor.xpath('.//../@title')[0]
        actorPhotoURL = 'http:' + actor.get('data-src')

        movieActors.addActor(actorName, actorPhotoURL)

    #Posters
    art = [
        str(metadata.id).split('|')[2].replace('_','/').replace('!','?')
    ]
    xpaths = [
        '//meta[@itemprop="thumbnailUrl"]/@content',
        '//div[@id="innerVideoBlock"]//img/@src',
        '//div[@id="photoSliderGuest"]//a/@href'
    ]
    for xpath in xpaths:
        try:
            for img in detailsPageElements.xpath(xpath):
                art.append(img)
        except:
            pass

    j = 1
    Log('Artwork found: %d' % len(art))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if (width > 1 or height > width) and width < height:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
                j = j + 1
            except:
                pass

    return metadata
