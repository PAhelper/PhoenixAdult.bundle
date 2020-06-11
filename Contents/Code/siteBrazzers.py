import PAsearchSites
import PAgenres
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    sceneID = searchTitle.split()[0]
    if unicode(sceneID, 'UTF-8').isdigit():
        sceneURL = '%s/scenes/view/id/%s' % (PAsearchSites.getSearchBaseURL(siteNum), sceneID)
        detailsPageElements = HTML.ElementFromURL(sceneURL)

        titleNoFormatting = detailsPageElements.xpath('//h1')[0].text_content().strip()
        curID = String.Encode(sceneURL)
        subSite = detailsPageElements.xpath('//span[@class="label-text"]')[0].text_content().strip()
        releaseDate = parse(detailsPageElements.xpath('//aside[@class="scene-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Brazzers/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=100, lang=lang))
    else:
        cookies = {
            'textSearch': encodedTitle
        }
        data = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum), cookies=cookies)
        searchResults = HTML.ElementFromString(data)
        for searchResult in searchResults.xpath('//div[@class="scene-card-info"]'):
            sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + searchResult.xpath('.//a[1]/@href')[0]
            curID = String.Encode(sceneURL)
            titleNoFormatting = searchResult.xpath('.//a[1]/@title')[0]
            subSite = searchResult.xpath('.//span[@class="label-text"]')[0].text_content().strip()
            releaseDate = parse(searchResult.xpath('.//time')[0].text_content().strip()).strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Brazzers/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneURL = String.Decode(metadata_id[0])
    detailsPageElements = HTML.ElementFromURL(sceneURL)

    # Summary
    paragraph = detailsPageElements.xpath('//p[@itemprop="description"]')[0].text_content()
    paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n', '').replace('  ', '') + "\n\n"
    metadata.summary = paragraph[:-10]

    # Studio
    metadata.studio = 'Brazzers'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//span[@class="label-text"]')[0].text_content()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[contains(@class,"tag-card-container")]//a')

    for genreLink in genres:
        genreName = genreLink.text_content().strip().lower()
        # If it's part of a series, add an extra Collection tag with the series name... Trouble is there's no standard for locating the series name, so this might not work 100% of the time
        if "series" in genreName or "800 Phone Sex: Line " in metadata.title or ": Part" in metadata.title or "Porn Logic" in metadata.title or "- Ep" in metadata.title or tagline == "ZZ Series":
            seriesName = metadata.title
            if (seriesName.rfind(':')):
                metadata.collections.add(seriesName[:seriesName.rfind(':')])
            elif (seriesName.rfind('- Ep')):
                metadata.collections.add(seriesName[:seriesName.rfind('- Ep')])
            else:
                metadata.collections.add(seriesName.rstrip('1234567890 '))
        if "office 4-play" in metadata.title.lower() or "office 4-play" in genreName:
            metadata.collections.add("Office 4-Play")

        # But we don't need a genre tag named "3 part series", so exclude that genre itself
        if "series" not in genreName and "office 4-play" not in genreName:
            movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//aside[contains(@class,"scene-date")]')
    if date:
        date = date[0].text_content()
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    
    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="model-card"]')
    for actorLink in actors:
        actorName = actorLink.xpath('.//h2[@class="model-card-title"]//a/@title')[0]
        actorPhotoURL = actorLink.xpath('.//div[@class="card-image"]//img/@data-src')[0]
        if not actorPhotoURL.startswith('http'):
            actorPhotoURL = 'http:' + actorPhotoURL

        movieActors.addActor(actorName, actorPhotoURL)
    
    # Posters
    art = []
    xpaths = [
        '//*[@id="trailer-player"]/img/@src',
        '//a[@rel="preview"]/@href'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            if not img.startswith('http'):
                img = 'http:' + img
            art.append(img)

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
                if idx > 1 and width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
