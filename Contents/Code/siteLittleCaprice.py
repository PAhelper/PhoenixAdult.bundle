import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@id="left-area"]/article'):
        titleNoFormatting = searchResult.xpath('.//h2[@class="entry-title"]/a')[0].text_content().strip()
        curID = searchResult.xpath('.//h2[@class="entry-title"]/a')[0].get('href').replace('_','*').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//span[@class="published"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [LittleCaprice] " + releaseDate, score = score, lang = lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!').replace('*','_')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'LittleCaprice'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="entry-title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="et_pb_text et_pb_module et_pb_bg_layout_light et_pb_text_align_left"]/p')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//meta[11]')[0].get("content").split("T")[0]
    if len(date) > 0:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[contains(@class,"et_pb_text_align_left")]/ul/li[contains(.,"Models")]/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = ""
            #actorPhotoURL = actorPage.xpath('//img[@class="model-page"]')[0].get("src")
            #if 'http' not in actorPhotoURL:
            #    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//meta[13]')[0].get('content')
        art.append(twitterBG)
    except:
        pass

    # Photos
    photos = detailsPageElements.xpath('//span[@class="et_pb_image_wrap "]/img')
    if len(photos) > 0:
        for photoLink in photos:
            photo = PAsearchSites.getSearchBaseURL(siteID) + photoLink.get('src')
            art.append(photo)

    # Scene photos page
    try:
        photoPageUrl = PAsearchSites.getSearchBaseURL(siteID)+detailsPageElements.xpath('//div[contains(@class,"et_pb_text_align_left")]/ul/li[contains(.,"Pictures:")]/a')[0].get('href')
        photoPage = HTML.ElementFromURL(photoPageUrl)
        unlockedPhotos = photoPage.xpath('//div[@class="et_pb_gallery_image landscape"]/a')
        for unlockedPhoto in unlockedPhotos:
            if 'http' not in unlockedPhoto.get('href'):
                art.append(PAsearchSites.getSearchBaseURL(siteID) + unlockedPhoto.get('href'))
            else:
                art.append(unlockedPhoto.get('href'))
    except:
        pass

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                j = j + 1
            except:
                pass

    return metadata
