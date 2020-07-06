import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@id="left-area"]/article'):
        titleNoFormatting = searchResult.xpath('.//h2[@class="entry-title"]/a')[0].text_content().strip()
        curID = PAutils.Encode(searchResult.xpath('.//h2[@class="entry-title"]/a/@href')[0])
        releaseDate = parse(searchResult.xpath('.//span[@class="published"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [LittleCaprice] " + releaseDate, score = score, lang = lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    detailsPageElements = HTML.ElementFromURL(sceneURL)
    movieGenres.clearGenres()

    # Studio
    metadata.studio = 'LittleCaprice'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="entry-title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="et_pb_text et_pb_module et_pb_bg_layout_light et_pb_text_align_left"]/p')[0].text_content().strip()

    #Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//meta[@property="article:published_time"]')[0].get("content").split("T")[0]
    if date:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[contains(@class,"et_pb_text_align_left")]/ul/li[contains(.,"Models")]/a')
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)

            actorName = actorLink.text_content().strip()
            actorPhotoURL = actorPage.xpath('//img[@class="model-page"]')[0].get("src")
            actorPhotoURL = actorPhotoURL.replace("media.",'')
            if 'http' not in actorPhotoURL:
                actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL

            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###
    art = []
    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//meta[@property="og:image"]/@content')[0]
        art.append(twitterBG)
    except:
        pass

    # Photos
    photos = detailsPageElements.xpath('//span[@class="et_pb_image_wrap "]/img/@src')
    for photoLink in photos:
        art.append(PAsearchSites.getSearchBaseURL(siteID) + photoLink)

    # Scene photos page
    try:
        photoPageUrl = PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//div[contains(@class, "et_pb_text_align_left")]/ul/li[contains(., "Pictures:")]/a/@href')[0]
        photoPage = HTML.ElementFromURL(photoPageUrl)
        for unlockedPhoto in photoPage.xpath('//div[@class="et_pb_gallery_image landscape"]/a/@href'):
            if not unlockedPhoto.startswith('http'):
                unlockedPhoto = PAsearchSites.getSearchBaseURL(siteID) + unlockedPhoto

            art.append(unlockedPhoto)
    except:
        pass

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
