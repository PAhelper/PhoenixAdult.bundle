import PAsearchSites
import PAgenres
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    encodedTitle = encodedTitle.replace('%20', '+')
    url = PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle
    data = PAutils.HTTPRequest(url, cookies={
        'sst': 'ulang-en'
    })
    searchResults = HTML.ElementFromString(data)
    for searchResult in searchResults.xpath('//ul[@class="cards-list"]//li'):
        titleNoFormatting = searchResult.xpath('.//div[@class="card__footer"]//div[@class="card__h"]/text()')[0]
        curID = searchResult.xpath('.//a/@href')[0].replace('/', '_').replace('?', '!')
        releaseDate = parse(searchResult.xpath('.//div[@class="card__date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneURL = metadata_id[0].replace('_', '/').replace('!', '?')
    art = []

    url = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="detail__title"]')[0].text_content()

    # Studio/Tagline/Collection
    metadata.collections.clear()
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "detail__txt")]')[0].text_content().strip()

    # Date
    date = detailsPageElements.xpath('//span[@class="detail__date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[contains(@class, "tag-list")]//a')
    for genre in genres:
        movieGenres.addGenre(genre.text_content().strip())

    # Posters and artwork
    try:
        art.insert(0, detailsPageElements.xpath('//meta[@property="og:image"]/@content')[0].replace('cover', 'hero').replace('medium.jpg', 'large.jpg'))
    except:
        pass

    # Actors / possible posters
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="detail__models"]//a')
    for actorLink in actors:
        actorName = actorLink.text_content().strip()
        actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get('href')
        actorPage = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPage.xpath('//div[@class="person__avatar"]//source/@srcset')[1].replace('.webp', '.jpg')
        art.append(actorPhotoURL)
        movieActors.addActor(actorName, actorPhotoURL)

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
                if width > 1 and height >= width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
