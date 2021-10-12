import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//a[@class="scene item light_background"]'):
        titleNoFormatting = searchResult.xpath('.//h3')[0].text_content().strip()
        sceneActors = searchResult.xpath('//p[@class="sub"]')[0].text_content().strip()
        sceneURL = searchResult.xpath('./@href')[0]
        curID = PAutils.Encode(sceneURL)

        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] [%s]' % (titleNoFormatting, sceneActors, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Studio
    metadata.studio = 'WakeUpNFuck'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="block"]//h2')[0].text_content().strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//div[@class="tags"]//a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="description"]')[0].text_content().split('Publish Date :')[-1].strip()
    date_object = datetime.strptime(date, '%d %B %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()

    actors = detailsPageElements.xpath('//div[@class="starring"]//a[@class="item"]')
    for actorLink in actors:
        actorName = actorLink.xpath('.//p')[0].text_content().strip()
        actorPhotoURL = actorLink.xpath('.//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []

    for posterLink in detailsPageElements.xpath('//video[@class="player_video"]/@poster'):
        art.append(posterLink)

    if not art:
        for script in detailsPageElements.xpath('//script'):
            try:
                match = re.search('(?<=image: ")(.*)(?=")', script.text_content())
                if match:
                    art.append(match.group(0).strip())
            except:
                pass

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
