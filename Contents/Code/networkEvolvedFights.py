import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    directURL = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.replace(' ', '-').lower() + '.html'

    searchResults = [directURL]
    googleResults = PAutils.getFromGoogleSearch(searchTitle, siteNum)
    for sceneURL in googleResults:
        if ('/updates/' in sceneURL and sceneURL not in searchResults):
            searchResults.append(sceneURL)

    for sceneURL in searchResults:
        detailsPageElements = None
        try:
            detailsPageElements = HTML.ElementFromURL(sceneURL)
        except:
            pass

        if detailsPageElements:
            curID = PAutils.Encode(sceneURL)
            Log("curID: " +curID)
            titleNoFormatting = detailsPageElements.xpath('//title')[0].text_content().strip()
            date = detailsPageElements.xpath('//span[(contains(@class, "update_date"))]')[0].text_content().strip()
            releaseDate = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    detailsPageElements = HTML.ElementFromURL(sceneURL)

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[(contains(@class, "latest_update_description"))]')[0].text_content().strip()

    # Studio/Tagline/Collection
    metadata.collections.clear()
    metadata.studio = "Evolved Fights Network"
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Genres
    movieGenres.clearGenres()
    for genreLink in detailsPageElements.xpath('//span[(contains(@class, "tour_update_tags"))]/a'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[(contains(@class, "update_block_info model_update_block_info"))]/span[(contains(@class, "tour_update_models"))]/a'):
        actorName = actorLink.text_content().strip()
        actorPageURL = actorLink.get('href')

        actorPage = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPage.xpath('//img[(contains(@class, "model_bio_thumb stdimage thumbs target"))]/@src0_3x')[0]
        actorPhotoURLFixed = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
        movieActors.addActor(actorName, actorPhotoURLFixed)
	
    # Release Date
    date = detailsPageElements.xpath('//span[@class="update_date"]')[0].text_content().strip()
    date_object = datetime.strptime(date, '%m/%d/%Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Posters/Background
    art = []
    poster = PAsearchSites.getSearchBaseURL(siteID) + '/' + detailsPageElements.xpath('//span[(contains(@class, "model_update_thumb"))]/img/@src0_4x')[0]
    poster2 = poster.replace('0-4x','1-4x')
    art.append(poster)
    art.append(poster2)
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
                if width > 100 and idx > 5:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
