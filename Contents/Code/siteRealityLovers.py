import PAsearchSites
import PAutils

def search(results, encodedTitle, title, searchTitle, siteNum, lang, searchDate):
    url = PAsearchSites.getSearchSearchURL(siteNum)
    post_values = {
        "sortBy": "MOST_RELEVANT",
        "searchQuery": searchTitle,
        "videoView": "MEDIUM"
    }
    params = json.dumps(post_values)
    req = urllib.Request(url, data=params, headers={'content-type': 'application/json;charset=UTF-8'})
    data = urllib.urlopen(req).read()
    searchResults = json.loads(data)

    for searchResult in searchResults['contents']:
        releaseDate = parse(searchResult['released']).strftime('%Y-%m-%d')
        curID = PAutils.Encode(searchResult['videoUri'])
        posterID = PAutils.Encode(searchResult['mainImageSrcset'].split(',')[1][:-3].replace("https", "http"))
        siteName = PAsearchSites.getSearchSiteName(siteNum)
        titleNoFormatting = '%s [%s] %s' % (searchResult['title'], siteName, releaseDate)
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, posterID), name=titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    Log('******UPDATE CALLED*******')

    id = str(metadata.id).split('|')
    videoUri = PAutils.Decode(id[0])
    posterUri = PAutils.Decode(id[2])
    url = PAsearchSites.getSearchBaseURL(siteID) + videoUri
    detailsPageElements = HTML.ElementFromURL(url)

    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="video-detail-name"]')[0].text_content().strip()

    # Summary
    rawSummary = detailsPageElements.xpath('//p[@itemprop="description"]')[0].text_content().replace('…', '').replace('Read more', '')
    metadata.summary = ' '.join(rawSummary.split())

    # Tagline and Collection(s)
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Genres
    genres = detailsPageElements.xpath('//span[@itemprop="keywords"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="videoClip__Details-infoValue"]')[0].text_content().strip()
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//span[@itemprop="actors"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoLinks = actorPage.xpath('//img[@class="girlDetails-posterImage"]')[0].get("srcset")
                actorPhotoURLs = str(actorPhotoLinks).split(',')
                actorPhotoURL = actorPhotoURLs[1][:-3].replace("https", "http")
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName, actorPhotoURL)

    # Photos
    art = []
    photos = detailsPageElements.xpath('//img[contains(@class, "videoClip__Details--galleryItem")]')
    if len(photos) > 0:
        for photo in photos:
            photoURLs = photo.get('data-big').split(',')
            photoURL = photoURLs[len(photoURLs) - 1][:-6].replace("https", "http")
            art.append(photoURL)
    for idx, imageUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(imageUrl, metadata):
            try:
                metadata.art[imageUrl] = Proxy.Preview(
                    HTTP.Request(imageUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    # Poster
    try:
        metadata.posters[posterUri] = Proxy.Preview(
            HTTP.Request(posterUri, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
    except:
        pass

    return metadata
