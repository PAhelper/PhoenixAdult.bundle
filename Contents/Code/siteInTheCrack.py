import PAsearchSites
import PAutils
import string


def search(results, lang, siteNum, searchData):
    sceneID = ''
    all = string.maketrans('', '')
    nodigs = all.translate(all, string.digits)

    try:
        sceneTitle = searchData.title.split(' ', 2)[0]
        sceneID = sceneTitle.translate(all, nodigs)
        if sceneID != '':
            searchData.title = searchData.title.split(' ', 2)[1]

        searchData.title = searchData.title.lower()
    except:
        pass

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.title[0])
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//ul[@class="collectionGridLayout"]/li'):
        discoveredname = searchResult.xpath('.//span')[0].text_content().strip().lower()

        if searchData.title in discoveredname:
            modellink = searchResult.xpath('.//a/@href')[0]
            req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + modellink)
            searchResults = HTML.ElementFromString(req.text)

            for searchResult in searchResults.xpath('//ul[@class="Models"]/li'):
                titleNoFormatting = searchResult.xpath('.//figure/p[1]')[0].text_content().replace('Collection: ', '').strip()
                titleNoFormattingID = PAutils.Encode(titleNoFormatting)

                # Release Date
                date = searchResult.xpath('.//figure/p[2]')[0].text_content().replace('Release Date:', '').strip()
                releaseDate = parse(date).strftime('%Y-%m-%d') if date else ''

                curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])

                score = 100 - Util.LevenshteinDistance(sceneID, titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, titleNoFormattingID, releaseDate), name='%s %s [%s]' % (titleNoFormatting, releaseDate, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h2//span')[0].text_content().strip()

    # Summary
    for searchResult in detailsPageElements.xpath('//p[@id="CollectionDescription"]'):
        metadata.summary = searchResult.text_content().strip()

    # Studio
    metadata.studio = 'InTheCrack'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Solo')

    # Release Date
    date = PAutils.Decode(metadata_id[3])
    if date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actorstr = detailsPageElements.xpath('//title')[0].text_content().split('#')[1]
    actorstr = (''.join(i for i in list(actorstr) if not i.isdigit())).strip()
    actorstr = actorstr.replace(',', '&')
    actorlist = actorstr.split('&')

    for actor in actorlist:
        actorName = actor.strip()
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    scenepic = PAsearchSites.getSearchBaseURL(siteNum).strip() + detailsPageElements.xpath('//style')[0].text_content().split('\'')[1].strip()

    art.append(scenepic)

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
            except Exception as e:
                Log('Error during image download: \n%s', e)
                pass

    return metadata
