import PAsearchSites
import PAgenres
import PAactors


def search(results, encodedTitle, title, searchTitle, siteNum, lang, searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="grid-item scene-list-item"]'):
        curID = String.Encode(searchResult.xpath('.//a/@href')[0])
        titleNoFormatting = searchResult.xpath('.//a/@href')[0].split('/')[2].replace('-streaming-vr-oculus-porn-videos.html', '')
        titleFormatted = searchResult.xpath('.//section//a//p[@class="scene-update-stats grid-item-title"]//span')[0].text_content().strip()
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id=curID + "|" + str(siteNum), name='%s [%s]' % (titleFormatted, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    Log('******UPDATE CALLED*******')

    path = String.Decode(str(metadata.id).split("|")[0])
    url = PAsearchSites.getSearchBaseURL(siteID) + path
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="text-center text-lg-left py-lg-3 px-3"]//h1')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@id="synopsis-full"]//p')[0].text_content().strip()

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//meta[@name="Keywords"]')[0].get('content').split(',')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre)

    # Actors
    actors = detailsPageElements.xpath('//div[@id="bodyShotModal"]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.xpath('.//img/@title')[0]
            try:
                actorPhotoURL = actorLink.xpath('.//img/@src')[0]
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName, actorPhotoURL)

    # Video Poster
    try:
        posterURL = detailsPageElements.xpath('//meta[@property="og:image"]')[0].get('content')
        art.append(posterURL)
    except:
        pass

    # Photos
    photos = detailsPageElements.xpath('//div[@class="screenshots-block breakout-stroke mb-5"]//source')
    if len(photos) > 0:
        for photo in photos:
            photoLink = photo.xpath('./@srcset')[0]
            art.append(photoLink)

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(
                        HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(
                        HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
                j = j + 1
            except:
                pass

    return metadata
