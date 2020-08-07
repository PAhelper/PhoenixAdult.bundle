import PAsearchSites
import PAgenres
import PAactors
import PAutils



# Known Issues
#   [Resolved/BugFix] Only returns one result
#       - Due to saving full URL in curID, it had a unique ID per search result, changed to just saving JAVID.
# 
#   [Resolved/Working As Designed] Only returns result with JAVID, extra text causes search fail
#       - This appears to be a limit of the search on the site, even throwing the titles in there kills it.
# 
#   Tagline section is generally borked and needs rework (labels and series)
#   
#   
#   


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    searchJAVID = None
    splitSearchTitle = searchTitle.split(' ')
    if(unicode(splitSearchTitle[1], 'UTF-8').isdigit()):
         searchJAVID = '%s%%2B%s' % (splitSearchTitle[0], splitSearchTitle[1])

    Log("searchJAVID: " + searchJAVID)

    if searchJAVID:
        encodedTitle = searchJAVID
    Log("Encoded Title: " + encodedTitle)

    searchTypes = ['Censored', 'Uncensored']


    for type in searchTypes:
        if type == 'Uncensored': sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + 'uncensored/search/' + encodedTitle
        elif type == 'Censored': sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + 'search/' + encodedTitle
        req = PAutils.HTTPRequest(sceneURL)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//a[@class="movie-box"]'):
            titleNoFormatting = searchResult.xpath('.//span[1]')[0].text_content().strip().replace('\t', '').replace('\r\n', '')
            JAVID = searchResult.xpath('.//date[1]')[0].text_content().strip()

            sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.replace('%20', '-').replace('%2B', '-')
            curID = PAutils.Encode(JAVID)

            if searchJAVID:
                score = 100 - Util.LevenshteinDistance(searchJAVID.lower(), JAVID.lower())
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s][%s] %s' % (type, JAVID, titleNoFormatting), score=score, lang=lang))

            Log('Title: ' + '[' + type + ']' + '[' + JAVID + '] ' + titleNoFormatting.title())

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchSearchURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)
    JAVID = sceneURL.rsplit('/', 1)[1]

    # Studio
    javStudio = detailsPageElements.xpath('//p/a[contains(@href, "/studio/")]')[0].text_content().strip()
    metadata.studio = javStudio
 
    # Title
    javTitle = detailsPageElements.xpath('//head/title')[0].text_content().strip().replace(' - JavBus', '')
    if JAVID.replace('-', '').replace('_', '').replace(' ', '').isdigit(): javTitle = javStudio + ' '  + javTitle
    metadata.title = javTitle

    # Tagline
    taglineJav = ['N', 'N', 0]

    try:
        labelJav = detailsPageElements.xpath('//p/a[contains(@href, "/label/")]')[0].text_content().strip()
        Log('labelJav: ' +  labelJav)
        taglineJav[0] = labelJav
        taglineJav[2] = taglineJav[2] + 1
    except:
        pass

    try:
        seriesJav = detailsPageElements.xpath('//p/a[contains(@href, "/series/")]')[0].text_content().strip()
        Log('seriesJav: ' +  seriesJav)
        taglineJav[1] = seriesJav
        taglineJav[2] = taglineJav[2] + 2
    except:
        pass

    if taglineJav[2] == 0:
        tagline = ''
    elif taglineJav[2] == 1: 
        tagline = taglineJav[0]
    elif taglineJav[2] == 2: 
        tagline = taglineJav[1]
    elif taglineJav[2] == 3: 
        tagline = 'Both Match'
    Log('Tagline: ' + tagline)

    metadata.tagline = tagline

    # Release Date
    date = detailsPageElements.xpath('//div[@class="col-md-3 info"]/p[2]')[0].text_content().strip().replace('Release Date: ', '')
    date_object = datetime.strptime(date, '%Y-%m-%d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    for actorLink in detailsPageElements.xpath('//a[@class="avatar-box"]'):
        fullActorName = actorLink.text_content().strip()

        actorPhotoURL = detailsPageElements.xpath('//a[@class="avatar-box"]/div[@class="photo-frame"]/img[contains(@title, "%s")]/@src' % (fullActorName))[0]
        if actorPhotoURL.rsplit('/', 1)[1] == 'nowprinting.gif':
            actorPhotoURL = ''


        movieActors.addActor(fullActorName, actorPhotoURL)

    # Genres
    for genreLink in detailsPageElements.xpath('//span[@class="genre"]/a[contains(@href, "/genre/")]'):
        genreName = genreLink.text_content().lower().strip()
        movieGenres.addGenre(genreName)

    # Posters
    art = []
    xpaths = [
        '//a[contains(@href, "/cover/")]/@href',
        '//a[@class="sample-box"]/div/img/@src',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

    # try:
    coverImage = detailsPageElements.xpath('//a[contains(@href, "/cover/")]/@href')
    coverImageCode = coverImage[0].rsplit('/', 1)[1].split('.')[0].split('_')[0]
    imageHost = coverImage[0].rsplit('/', 2)[0]
    coverImage = imageHost + '/thumb/'  + coverImageCode + '.jpg'
    if coverImage.count('/images.') == 1:
        coverImage = coverImage.replace("thumb", "thumbs")

    art.append(coverImage)
    # except:
    #     pass

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
