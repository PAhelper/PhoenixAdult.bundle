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

        if len(searchResults.xpath('//h1[@class="section__title mb-20"]')) == 0:
            # if there is only one result returned by the search function it automatically redirects to the video page
            titleNoFormatting = searchResults.xpath('//h1[@class="watch__title h2 mb-15"]')[0].text_content().strip()

            url = searchResults.xpath('//a[@class="btn btn-black __pagination_button __pagination_button--more"]/@href')[0]
            curID = PAutils.Encode(url)

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))
            return results

        for searchResult in searchResults.xpath('//div[@class="col d-flex"]//div[@class="card-scene__text"]'):
            titleNoFormatting = searchResult.xpath('./a')[0].text_content().strip()

            url = searchResult.xpath('./a/@href')[0]
            curID = PAutils.Encode(url)

            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if 'http' not in sceneURL:
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="watch__title h2 mb-15"]/text()')[0].strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="text-mob-more p-md"]')[0].text_content().strip()
    except:
        Log('Failed to extract summary')

    # Studio
    metadata.studio = 'DDFProd'

    # Tagline / Collection
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date_object = parse(detailsPageElements.xpath('//i[@class="bi bi-calendar3 me-5"]')[0].text_content().strip())

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="genres-list p-md text-primary"]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    if date_object:
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//h1[@class="watch__title h2 mb-15"]//a'):
        actorName = actorLink.text_content().strip()
        actorPhotoURL = ''
        # actorPhotoURL = 'http:' + actorLink.get('data-src')

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = [
        detailsPageElements.xpath('//video/@data-poster')[0],
    ]

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
