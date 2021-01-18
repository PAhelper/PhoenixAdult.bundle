import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = searchData.title.split(' ', 1)[0]
    if unicode(sceneID, 'UTF-8').isdigit():
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    if sceneID:
        url = PAsearchSites.getSearchBaseURL(siteNum) + '/watch/' + sceneID
        req = PAutils.HTTPRequest(url)
        detailsPageElements = HTML.ElementFromString(req.text)

        curID = PAutils.Encode(url)
        titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name=titleNoFormatting, score=100, lang=lang))
    else:
        searchData.encoded = searchData.title.replace(' ', '+')
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//div[@class="thumbnail  thumbnail-premium thumbnail-old"]'):
            titleNoFormatting = searchResult.xpath('.//div[@class="thumbnail-title gradient"]/a/@title')[0]
            url = searchResult.xpath('.//div[@class="thumbnail-title gradient"]/a/@href')[0]

            date = searchResult.xpath('./@release')
            releaseDate = parse(date[0]).strftime('%Y-%m-%d') if date else ''

            curID = PAutils.Encode(url)

            if searchData.date and releaseDate:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if 'http' not in sceneURL:
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="watchpage-title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="scene-description__details"]//div[@class="scene-description__row"]//dd')[2].text_content().strip()

    # Studio
    metadata.studio = 'DDFProd'

    # Tagline / Collection
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date_object = parse(detailsPageElements.xpath('//span[@title="Release date"]/a')[0].text_content().strip())

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="scene-description__details"]//div[@class="scene-description__row"][2]//dd/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    if date_object:
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actor in detailsPageElements.xpath('//div[@class="scene-description__details"]//div[@class="scene-description__row"][1]//dd/a'):
        actorName = actor.text_content().strip()
        actorPhotoURL = ''
        # actorPhotoURL = 'http:' + actor.get('data-src')

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    artStyle = detailsPageElements.xpath('//div[@id="player"]/@style')[0]
    artUrl = re.search(r'\((.*?)\)', artStyle).group(1)
    art.append(artUrl)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            try:
                image = PAutils.HTTPRequest(posterUrl)

                # Add to posters
                metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)

                # Add to art items
                metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
