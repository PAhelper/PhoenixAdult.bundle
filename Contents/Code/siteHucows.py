import PAsearchSites
import PAgenres
import PAactors
import PAutils

# Known Issues
#   Just a straight copy of JavBus, needs complete rebuild for new site
#   
#   xpath for search results: //article
#   xpath for date match: //article/div/div[@itemprop="datePublished"]
#   
#   
#   
#   
#   



def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    date_object = datetime.strptime(searchDate, '%Y-%m-%d')
    # sceneDate = date_object.strftime("%#d %b %Y")
    mediaDate = str(date_object.year) + '/' + str(date_object.month)

    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + mediaDate
    req = PAutils.HTTPRequest(sceneURL)
    searchResults = HTML.ElementFromString(req.text)

    for searchResult in searchResults.xpath('//article'):
        titleNoFormatting = searchResult.xpath('./header/a/h1')[0].text_content().strip()

        sceneDate = searchResult.xpath('./div/div[@itemprop="datePublished"]')[0].text_content().strip()
        sceneDate = datetime.strptime(sceneDate, '%d %b %Y')
        dateText = sceneDate.strftime('%Y-%m-%d')

        sceneURL = str(searchResult.xpath('./header/a/@href')[0]).strip()
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


    # Studio
    metadata.studio = 'HuCows.com'
 

    # Title
    Title = detailsPageElements.xpath('//head/title')[0].text_content().strip().replace(' - HuCows.com', '')
    metadata.title = Title


    # Release Date
    date = detailsPageElements.xpath('//article/div/div[@itemprop="datePublished"]')[0].text_content().strip().replace('Release Date: ', '')
    date_object = datetime.strptime(date, '%d %b %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year


    # Actors
    # -- No Actor Data Available On Site Metadata --

    # Summary
    try:
        description = detailsPageElements.xpath('//article/div[@class="entry-content"]/p')[0].text_content()
        metadata.summary = description.strip()
    except:
        pass

    # Genres

        # Default Genres
    genres = ['Hucows', 'Breasts', 'Nipples', 'Nipple Torture', 'Breast Torture', 'Fetish', 'BDSM']
    for genre in genres:
        movieGenres.addGenre(genre)

        # Dynamic Genres
    for genreLink in detailsPageElements.xpath('//div/span/a[@rel="category tag"]'):
        genreName = genreLink.text_content().lower().strip()
        movieGenres.addGenre(genreName)
    


    # Posters
    art = []
    xpaths = [
        '//div/article/div/a[@class="lightboxhover"]/img/@src',
        '//div/center/a/img[@class="lightboxhover"]/@src',
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            art.append(poster)

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
