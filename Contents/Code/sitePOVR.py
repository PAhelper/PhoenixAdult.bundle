import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="thumbnail-wrap"]/div'):
        titleNoFormatting = searchResult.xpath('.//div/h6[@class="thumbnail__title"]')[0].text_content()
        curID = PAutils.Encode(searchResult.xpath('.//a[@class="thumbnail__link"]/@href')[0])
        subSite = searchResult.xpath('.//div/div/a[@class="thumbnail__footer-link"]')[0].text_content()

        siteScore = 80 - (Util.LevenshteinDistance(subSite.lower(), PAsearchSites.getSearchSiteName(siteNum).lower()) * 8 / 10)
        titleScore = 20 - (Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower()) * 2 / 10)
        score = siteScore + titleScore

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, subSite), name='%s [%s]' % (titleNoFormatting, subSite), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    script_text = detailsPageElements.xpath('//script[@type="application/ld+json"]')[0].text_content()
    scene_data = json.loads(script_text)

    # Title
    metadata.title = scene_data['name']

    # Summary
    metadata.summary = scene_data['description']

    # Studio
    metadata.studio = metadata_id[2]

    # Release Date
    date = scene_data['datePublished']
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actor_link in scene_data['actor']:
        actor_name = actor_link['name']
        actor_page = actor_link['@id']
        actor_req = PAutils.HTTPRequest(actor_page)
        actor_page_elements = HTML.ElementFromString(actor_req.text)
        actor_script = actor_page_elements.xpath('//script[@type="application/ld+json"]')[0].text_content()
        actor_data = json.loads(actor_script)
        actor_photo_url = actor_data['image']
        movieActors.addActor(actor_name, actor_photo_url)

    # Genres
    movieGenres.clearGenres()
    for genre_link in detailsPageElements.xpath('//ul[@class="category-link mb-2"]/li/a'):
        genre_name = genre_link.text_content().strip()
        movieGenres.addGenre(genre_name)

    art = []
    # Posters/Background
    background = scene_data['thumbnailUrl'].replace('tiny', 'large')
    art.append(background)


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
