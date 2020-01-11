import PAsearchSites
import PAgenres
import PAactors
import json


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    data = urllib.urlopen(PAsearchSites.getSearchSearchURL(siteNum) + '?gallery=1&terms=' + encodedTitle).read()
    data = json.loads(data)

    searchResults = HTML.ElementFromString(data['results'][0]['html'])

    for searchResult in searchResults.xpath('//li[@class="item"]'):
        titleNoFormatting = searchResult.xpath('.//h3[@class="title"]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//p[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        img = searchResults.xpath('.//img[contains(@class, "image")]/@data-src')[0].split('?', 1)[0].replace('/', '_').replace('?', '!')
        url = PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a/@href')[0]
        curID = url.replace('/', '_').replace('?', '!')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, img), name='%s [Playboy Plus] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    id = str(metadata.id).split('|')
    url = id[0].replace('_', '/').replace('!', '?')
    searchImg = id[2].replace('_', '/').replace('!', '?')

    detailsPageElements = HTML.ElementFromURL(url)

    # Studio
    metadata.studio = 'Playboy Plus'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="description-truncated"]')[0].text_content().strip().replace('...', '', 1)

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre("Glamour")

    # Release Date
    date = detailsPageElements.xpath('//p[contains(@class, "date")]')[0].text_content().strip()
    date_object = datetime.strptime(date, '%B %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actorName = detailsPageElements.xpath('//p[@class="contributorName"]')[0].text_content().strip()
    movieActors.addActor(actorName, '')

    # Director
    director = metadata.directors.new()
    directorName = detailsPageElements.xpath('//p[@class="contributorName"]')[1].text_content().strip()
    director.name = directorName

    # Photos
    art = [searchImg]
    img = detailsPageElements.xpath('//img[contains(@class, "image")]/@data-src')[0]
    art.append(img.split('?', 1)[0])
    for img in detailsPageElements.xpath('//section[@class="gallery"]//img[contains(@class, "image")]/@data-src'):
        art.append(img.split('?', 1)[0])

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
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
