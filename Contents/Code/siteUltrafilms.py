import PAsearchSites
import PAextras
import PAutils


def search(results, lang, siteNum, searchData):
    url = PAsearchSites.getSearchSearchURL(siteNum) + '%22' + searchData.encoded + '%22'
    maxscore = 0

    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//main//article[contains(@class,"thumb-block")]'):
        titleNoFormatting = searchResult.xpath('.//a/@title')[0].strip()
        image = PAutils.Encode(searchResult.xpath('.//img/@src')[0])
        curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])

        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, image), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

        if maxscore < score:
            maxscore = score

    if maxscore < 100:
        url = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded
        req = PAutils.HTTPRequest(url)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//main//article[contains(@class,"thumb-block")]'):
            titleNoFormatting = searchResult.xpath('.//a/@title')[0].strip()
            image = PAutils.Encode(searchResult.xpath('.//img/@src')[0])
            curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, image), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    try:
        metadata.title = detailsPageElements.xpath('//h1[@class="entry-title"]')[-1].text_content().strip()
    except:
        pass

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Collections / Tagline
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    for genreLink in detailsPageElements.xpath('//div[@class="tags-list"]/a//i[@class="fa fa-folder-open"]/..'):
        genreName = genreLink.text_content().replace('Movies', '').strip().lower()

        movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@id="video-date"]')[0].text_content().strip()
    if date:
        date = date.replace('Date:', '').strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()

    actors = detailsPageElements.xpath('//div[@id="video-actors"]//a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    image = PAutils.Decode(metadata_id[2])
    if image:
        art.append(image)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
