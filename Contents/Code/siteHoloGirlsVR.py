import PAsearchSites
import PAgenres
import PAactors


def search(results, encodedTitle, title, searchTitle, siteNum, lang, searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="memVid"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="memVidTitle"]//a/@title')[0]
        curID = String.Encode(searchResult.xpath('.//div[@class="memVidTitle"]//a/@href')[0])
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id=curID + "|" + str(siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

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
    metadata.title = detailsPageElements.xpath('//div[@class="col-xs-12 video-title"]//h3')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="col-sm-6 col-md-6 vidpage-info"]/text()')[4].strip()

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="videopage-tags"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Actors
    actors = detailsPageElements.xpath('//div[@class="col-xs-6 col-sm-4 col-md-3"]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.xpath('.//div[@class="vidpage-mobilePad"]//a//strong/text()')[0])
            try:
                actorPhotoURL = actorLink.xpath('.//img[@class="img-responsive imgHover"]')[0].get("src")
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName, actorPhotoURL)

    # Video Poster
    try:
        posterURL = detailsPageElements.xpath('//div[@class="col-xs-12 col-sm-6 col-md-6 vidCover"]//img')[0].get('src')
        art.append(posterURL)
    except:
        pass

    # Photos
    photos = detailsPageElements.xpath('//div[@class="vid-flex-container"]//span')
    if len(photos) > 0:
        for photo in photos:
            photoLink = photo.xpath('.//img')[0].get('src').replace('_thumb', '')
            art.append(photoLink)

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                if width > 1 or height > width:
                    metadata.posters[posterUrl] = Proxy.Preview(
                        HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
                if width > 100 and width > height:
                    metadata.art[posterUrl] = Proxy.Preview(
                        HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
                j = j + 1
            except:
                pass

    return metadata
