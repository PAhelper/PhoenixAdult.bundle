import PAsearchSites
import PAgenres
import PAactors
import PAutils

# Known Issues
#   Just a straight copy of JavBus, needs complete rebuild for new site
#   
#   
#   
#   
#   
#   
#   

def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    searchJAVID = None
    # splitSearchTitle = searchTitle.split(' ')
    # if(unicode(splitSearchTitle[1], 'UTF-8').isdigit()):
    #      searchJAVID = '%s%%2B%s' % (splitSearchTitle[0], splitSearchTitle[1])

    # Log("searchJAVID: " + searchJAVID)

    if searchJAVID:
        encodedTitle = searchJAVID
    Log("Encoded Title: " + encodedTitle)

    # Normal (censored films) Search Results
    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + 'search/' + encodedTitle
    req = PAutils.HTTPRequest(sceneURL)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//a[@class="movie-box"]'):
        titleNoFormatting = searchResult.xpath('.//span[1]')[0].text_content().strip()
        # Log('titleNoFormatting: ' + titleNoFormatting)
        JAVID = searchResult.xpath('.//date[1]')[0].text_content().strip()
        # Log('JAVID: ' + JAVID)
        sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.replace('%20', '-').replace('%2B', '-')
        curID = PAutils.Encode(sceneURL)

        if searchJAVID:
            score = 100 - Util.LevenshteinDistance(searchJAVID.lower(), JAVID.lower())
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s' % (JAVID, titleNoFormatting.title()), score=score, lang=lang))

    # Uncensored Films Search Results
    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + 'uncensored/search/' + encodedTitle
    reqUN = PAutils.HTTPRequest(sceneURL)
    searchResultsUN = HTML.ElementFromString(reqUN.text)
    for searchResultUN in searchResultsUN.xpath('//a[@class="movie-box"]'):
        titleNoFormatting = searchResultUN.xpath('.//span[1]')[0].text_content().strip().replace('\t', '').replace('\r\n', '')
        # Log('titleNoFormatting: ' + titleNoFormatting)
        JAVID = searchResultUN.xpath('.//date[1]')[0].text_content().strip()
        # Log('JAVID: ' + JAVID)

        sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.replace('%20', '-').replace('%2B', '-')
        curID = PAutils.Encode(sceneURL)

        if searchJAVID:
            score = 100 - Util.LevenshteinDistance(searchJAVID.lower(), JAVID.lower())
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[Uncensored][%s] %s' % (JAVID, titleNoFormatting.title()), score=score, lang=lang))
        # Log('Search Result Append:' + str(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[Uncensored][%s] %s' % (JAVID, titleNoFormatting.title()), score=score, lang=lang)))
    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
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

    # # Tagline
    # taglineJav = []
    # try:
    #     labelJav = detailsPageElements.xpath('//p/a[contains(@href, "/label/")]')[0].text_content().strip()
    #     Log('labelJav: ' +  labelJav)
    #     if labelJav: taglineJav.append(labelJav)

    #     seriesJav = detailsPageElements.xpath('//p/a[contains(@href, "/series/")]')[0].text_content().strip()
    #     Log('seriesJav: ' +  seriesJav)
    #     if seriesJav: taglineJav.append(seriesJav)
    
    #     Log('taglineJav: ' + str(taglineJav[0:]))

    #     if len(taglineJav) == 0:
    #         taglineJav = []
    #     elif len(taglineJav) == 1:
    #         metadata.tagline = taglineJav[0]
    #     elif len(taglineJav) == 2:
    #         metadata.tagline = 'Label: ' + taglineJav[0] + ', Series: ' + taglineJav[1]
    # except: 
    #     pass


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
