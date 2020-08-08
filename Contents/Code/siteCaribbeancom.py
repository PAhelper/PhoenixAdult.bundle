import PAsearchSites
import PAgenres
import PAactors
import PAutils

# Known Issues
#   - Actors section needs advanced logic, since the site's meta data for actors is garbage
#   
#   
#   
#   
#   
#   
#   

def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):

    if searchTitle[0:10].replace('-', '').replace(' ', '').replace('_', '').isdigit():
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + '/moviepages/' + searchTitle[0:10].replace(' ', '-') + '/index.html'
        Log(sceneURL)
        req = PAutils.HTTPRequest(sceneURL)
        searchResult = HTML.ElementFromString(req.text)

        titleNoFormatting = searchResult.xpath('//div/div/div/div/div/h1[@itemprop="name"]')[0].text_content().strip()
        sceneDate = searchResult.xpath('//ul/li/span[@itemprop="uploadDate"]')[0].text_content().strip()
        sceneDate = datetime.strptime(sceneDate, '%Y/%m/%d')
        dateText = sceneDate.strftime('%Y-%m-%d')

        curID = PAutils.Encode(sceneURL)

        score = 100

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] [%s] %s' % (dateText, searchTitle[0:10].replace(' ', '-'), titleNoFormatting), score=score, lang=lang))

    elif len(searchTitle.replace('The', '').replace('the', '')) > 3:
        sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.replace(' ', '+')
        req = PAutils.HTTPRequest(sceneURL)
        searchResults = HTML.ElementFromString(req.text)

        for searchResult in searchResults.xpath('//div/div/div/div/div[@class="grid-item"]'):
            titleNoFormatting = searchResult.xpath('./div/div/div/a[@itemprop="url"]')[0].text_content().strip()

            sceneDate = searchResult.xpath('./div/div/div[@class="meta-data"][1]')[0].text_content().strip()
            sceneDate = datetime.strptime(sceneDate, '%Y-%m-%d')
            dateText = sceneDate.strftime('%Y-%m-%d')

            sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + str(searchResult.xpath('./div/div/div[@class="meta-title"]/a/@href')[0]).strip().replace('/eng','')
            Log(sceneURL)
            curID = PAutils.Encode(sceneURL)

            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s' % (dateText, titleNoFormatting), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchSearchURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)
    videoID = sceneURL.rsplit('/', 2)[1]

    # Studio
    metadata.studio = 'Caribbeancom.com'
 

    # Title
    Title = detailsPageElements.xpath('//div/div/div/div/div/h1[@itemprop="name"]')[0].text_content().strip()
    Title = 'Caribbeancom %s %s' % (videoID, Title)
    metadata.title = Title

    # Release Date
    date = detailsPageElements.xpath('//ul/li/span[@itemprop="uploadDate"]')[0].text_content().strip()
    date_object = datetime.strptime(date, '%Y/%m/%d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year


    # Actors
    # actors = str(detailsPageElements.xpath('//head/meta[@name="keywords"]/@content').split(',')
    # for actor in actors:
    #     fullActorName = actor.strip()
    #     if fullActorName != '----':

    #         actorPhotoURL = detailsPageElements.xpath('//div[@id="%s"]//img[contains(@alt, "%s")]/@src' % (mainName.replace(' ', ''), mainName))[0]
    #         if actorPhotoURL.rsplit('/', 1)[1] == 'nowprinting.gif':
    #             actorPhotoURL = ''

    #         if len(splitActorName) > 1 and mainName == splitActorName[1][:-1]:
    #             actorName = mainName
    #         else:
    #             actorName = fullActorName

    #         movieActors.addActor(actorName, actorPhotoURL)

    # Summary
    try:
        description = detailsPageElements.xpath('//p[@itemprop="description"]')[0].text_content()
        metadata.summary = description.strip()
    except:
        pass

    # Genres
    for genreLink in detailsPageElements.xpath('//span[text()="Tags:"]/following-sibling::span/a[@class="spec__tag"]'):
        genreName = genreLink.text_content().lower().strip()
        movieGenres.addGenre(genreName)
    


    # Posters
    art = []
    xpaths = [
        #'substring-before(substring-after(//*/div[@class="vjs-poster"]/@style,\'background-image: url("\'),\'");\')',
        '//div[@class="gallery-ratio"]/a[@class="gallery-image-wrap fancy-gallery"]/@href',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            posterPath = PAsearchSites.getSearchBaseURL(siteID) + poster
            art.append(posterPath)

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