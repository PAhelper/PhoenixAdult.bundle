import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    searchResultElements = searchResults.xpath('//div[@align="left"]')
    Log(str(len(searchResultElements)) + ' results.')
    for searchResult in searchResultElements:
        link = searchResult.xpath('.//a[@class="update_title"]')[1]
        titleNoFormatting = link.text_content().strip()
        titleNoFormattingID = PAutils.Encode(titleNoFormatting)

        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()[6:]).strftime('%Y-%m-%d')

        curID = PAutils.Encode(link.xpath('./@href')[0])

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Desperate Amateurs] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + '/fintour/' + sceneURL
    
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="title_bar"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="gallery_description"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'Desperate Amateurs'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date_object = parse(detailsPageElements.xpath('.//td[@class="date"]')[0].text_content().strip()[6:])
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actorLinks = detailsPageElements.xpath('//a[starts-with(@href, "sets")]')
    Log(str(len(actorLinks)) + ' actors.')
    for actorLink in actorLinks:
        actorName = actorLink.text_content().strip()

        actorPageURL = actorLink.xpath('./@href')[0].strip()
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteID) + '/fintour/' + actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPage.xpath('//img[@class="thumbs"]/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    for GenreLink in detailsPageElements.xpath('//a[starts-with(@href, "category")]'):
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)

    # Posters
    posterUrl = detailsPageElements.xpath('//meta[@name="twitter:image"]/@content')[0]
    image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.google.com'})
    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=0)

    return metadata
