import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = searchData.title.split(' ', 1)[0]
    if unicode(sceneID, 'UTF-8').isdigit():
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    searchResults = []
    if sceneID:
        directURL = PAsearchSites.getSearchSearchURL(siteNum) + 'show_video.php?galid=' + sceneID
        searchResults.append(directURL)

    googleResults = PAutils.getFromGoogleSearch(searchData.title, siteNum)
    for sceneURL in googleResults:
        if ('show_video' in sceneURL and 'index' not in sceneURL) and sceneURL not in searchResults:
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        req = PAutils.HTTPRequest(sceneURL, headers={'Referer': 'https://www.puba.com/pornstarnetwork/index.php'}, cookies={'PHPSESSID': 'rvo9ieo5bhoh81knnmu88c3lf3'})
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)
            titleNoFormatting = detailsPageElements.xpath('//div[@id="body-player-container"]//div//div[@class="tour-video-title"]')[0].text_content().strip()
            if 'http' not in sceneURL:
                sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + 'show_video.php?galid=' + sceneID
            curID = PAutils.Encode(sceneURL)

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s' % (PAsearchSites.getSearchSiteName(siteNum), titleNoFormatting), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    req = PAutils.HTTPRequest(sceneURL, headers={'Referer': 'https://www.puba.com/pornstarnetwork/index.php'}, cookies={'PHPSESSID': 'rvo9ieo5bhoh81knnmu88c3lf3'})
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@id="body-player-container"]//div//div[@class="tour-video-title"]')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//center//div//a[contains(@class, "btn-outline-secondary")]')
    for genre in genres:
        genreName = genre.text_content().strip()
        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//center//div//a[contains(@class, "btn-secondary")]')
    for actor in actors:
        actorName = actor.text_content().strip()
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    # Posters/Background
    art = []
    art.append(PAsearchSites.getSearchBaseURL(siteNum) + detailsPageElements.xpath('//div[@id="body-player-container"]/div/a/img/@style')[0].split('url(')[1].split(')')[0])
    Log(art)

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
