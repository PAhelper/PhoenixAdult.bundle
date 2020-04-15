import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="scene"]'):
        titleNoFormatting = searchResult.xpath('.//h4[@itemprop="name"]//a')[0].text_content()
        curID = searchResult.xpath('.//a/@href')[0].replace('/','_').replace('?','!')
        releaseDate  = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''

        subSite = searchResult.xpath('.//small[@class="shadow"]//a')[0].text_content().strip()
        if subSite.lower().replace(".com","").replace(" ","") == PAsearchSites.getSearchSiteName(siteNum).lower().replace(" ",""):
            siteScore = 10
        else:
            siteScore = 0

        score = siteScore + 90 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s]' % (titleNoFormatting, subSite), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    metadata_id = str(metadata.id).split('|')
    url = metadata_id[0].replace('_','/').replace('!','?')
    sceneDate = metadata_id[2]
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@itemprop="name"]')[0].text_content().strip()

    # Studio/Tagline/Collection
    metadata.studio = 'Finishes The Job'
    metadata.tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Summary
    metadata.summary = detailsPageElements.xpath('//section[@class="scene-content"]//p[@itemprop="description"]')[0].text_content().strip()

    # Date
    date_object = parse(sceneDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//section[@class="scene-content"]//h4//a')
    for actorLink in actors:
        actorName = actorLink.text_content()
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//section[@class="scene-content"]//p[1]//a')
    for genre in genres:
        movieGenres.addGenre(genre.text_content())

    # Poster
    art = []
    for posterCur in detailsPageElements.xpath('//div[contains(@class,"first-set")]//img'):
        sceneName = posterCur.get('alt')
        if sceneName.lower() == metadata.title.lower():
            art.append(posterCur.get('src'))
    art.append(detailsPageElements.xpath('//video/@poster'))

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
