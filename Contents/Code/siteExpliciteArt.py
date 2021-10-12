import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchData.encoded = searchData.title.replace(' ', '-').lower()
    searchURL = '%s%s/page1.html' % (PAsearchSites.getSearchSearchURL(siteNum), searchData.encoded)
    req = PAutils.HTTPRequest(searchURL)
    searchResults = HTML.ElementFromString(req.text)

    for searchResult in searchResults.xpath('//div[@class="content"][.//*[contains(@src, "video")]]'):
        titleNoFormatting = PAutils.parseTitle(searchResult.xpath('.//div[@class="vtitle"]')[0].text_content().strip(), siteNum)
        sceneURL = searchResult.xpath('.//a/@href')[0]
        curID = PAutils.Encode(sceneURL)

        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = PAutils.parseTitle(detailsPageElements.xpath('//title')[0].text_content().strip(), siteNum)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="player-info-desc"]')[0].text_content().strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.studio = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//span[@class="tags"]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="player-info-row"]/a'):
        actorName = actorLink.text_content().strip()

        modelURL = actorLink.xpath('.//@href')[0]
        req = PAutils.HTTPRequest(modelURL)
        actorPageElements = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPageElements.xpath('//div[@class="pornstar-bio-left"]//@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//div[@id="player"]//script',
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            match = re.search(r'(?<=(image: ")).*(?=")', img.text_content())
            if match:
                img = match.group(0)

                art.append(img)

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
                if height > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
