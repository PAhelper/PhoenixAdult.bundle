import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneID = searchData.title.split(' ', 1)[0]
    if unicode(sceneID, 'UTF-8').isdigit():
        searchData.title = searchData.title.replace(sceneID, '', 1).strip()
    else:
        sceneID = None

    if sceneID and not searchData.title:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum) + '/' + sceneID, cookies={
            'sst': 'ulang-en'
        })
        if req.ok:
            detailsPageElements = HTML.ElementFromString(req.text)
            titleNoFormatting = detailsPageElements.xpath('//h1[@class="detail__title"]')[0].text_content()
            curID = PAutils.Encode(PAsearchSites.getSearchBaseURL(siteNum) + '/' + sceneID)

            releaseDate = ''
            date = detailsPageElements.xpath('//span[@class="detail__date"]')[0].text_content().strip()
            if date:
                releaseDate = parse(date).strftime('%Y-%m-%d')

            score = 100

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s %s' % (PAsearchSites.getSearchSiteName(siteNum), titleNoFormatting, releaseDate), score=score, lang=lang))
    else:
        searchData.encoded = searchData.title.replace(' ', '+')
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded, cookies={
            'sst': 'ulang-en'
        })
        searchResults = HTML.ElementFromString(req.text)
        for searchResult in searchResults.xpath('//ul[@class="cards-list"]//li'):
            titleNoFormatting = searchResult.xpath('.//div[@class="card__footer"]//div[@class="card__h"]/text()')[0]
            curID = PAutils.Encode(searchResult.xpath('.//a/@href')[0])
            releaseDate = parse(searchResult.xpath('.//div[@class="card__date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

            if searchData.date:
                score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)
    art = []

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="detail__title"]')[0].text_content()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class, "detail__txt")]')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteNum)

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="detail__date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[contains(@class, "tag-list")]//a')
    for genre in genres:
        movieGenres.addGenre(genre.text_content().strip())

    # Actors / possible posters
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="detail__models"]//a')
    for actorLink in actors:
        actorName = actorLink.text_content().strip()

        actorPageURL = PAsearchSites.getSearchBaseURL(siteNum) + actorLink.get('href')
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhoto = actorPage.xpath('//div[@class="person__avatar"]//source/@srcset')
        actorPhotoURL = ' '
        if actorPhoto and len(actorPage) == 2:
            actorPhotoURL = actorPhoto[1].replace('.webp', '.jpg')
            art.append(actorPhotoURL)

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters and artwork
    try:
        art.insert(0, detailsPageElements.xpath('//meta[@property="og:image"]/@content')[0].replace('cover', 'hero').replace('medium.jpg', 'large.jpg'))
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
                if width > 1 and height >= width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
