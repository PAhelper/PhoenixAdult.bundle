import PAsearchSites
import PAgenres


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//article'):
        titleNoFormatting = searchResult.xpath('.//a[@rel="bookmark"]')[0].text_content().strip()
        Log("Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        Log("curID: " + curID)
        # Removing date search (not on results page) to speed search and cut down page openings (as it was it opened each search result to check date)
        # detailsPageElements = HTML.ElementFromURL(curID.replace('_','/').replace('!','?'))
        # releaseDate = parse(detailsPageElements.xpath('//div[@class="video-content__download-info"]//div[@class="section__item-title-download-space"][2]')[0].text_content().replace("Release date:","").strip()).strftime('%Y-%m-%d')
        # Log("Release date: " + releaseDate)
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        if len(titleNoFormatting) > 29:
            titleNoFormatting = titleNoFormatting[:32] + "..."
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] ", score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art=[]

    # Studio
    metadata.studio = "VR Bangers"

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="less-text d-block"]/p[2]')[0].text_content().strip()
    except:
        pass

    # Tagline and Collection
    tagline = "VR Bangers"
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="video-content__download-info"]//div[@class="section__item-title-download-space"][2]')[0].text_content().replace("Release date:","").strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[contains(@class,"video-item-info-tags")]//a')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="video-content__download-info"]//div[contains(@class,"video-item-info--starring")]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip()
            Log("actor: " + actorName)
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[contains(@class, "single-model__featured-img")]/@src')[0]
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    for posterLink in detailsPageElements.xpath('//a[contains(@class, "justified__item")]/@href'):
        art.append(posterLink)
        Log("poster: " + posterLink)

    ## Banner
    banner = detailsPageElements.xpath('//section[@class="banner"]//img')[0].get("src")
    Log("banner: " + banner)
    art.append(banner)

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