import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    title = encodedTitle.lower().replace("%20","-")
    Log("Media Title: " + title)
    url = PAsearchSites.getSearchSearchURL(siteNum) + title
    searchResults = HTML.ElementFromURL(url)
    titleNoFormatting = searchResults.xpath('//div[(contains(@class,"video-info-left pull-left"))]/h2/a')[0].text_content().strip()
    curID = title
    Log('CURID: ' +  curID)
    releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
	# Due to direct use of the title/url search we have '1-1' unique match with the scene so no mis-matches or 404's can occur. 
    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+ PAsearchSites.getSearchSiteName(siteNum) +"] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0]
    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()

    # Studio/Tagline/Collection
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[(contains(@class,"video-tag-section"))]/a')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content().lower())


    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[(contains(@class,"video-info-left pull-left"))]/h3/span/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[(contains(@class,"single-porn-pic"))]/img/@src')
            movieActors.addActor(actorName,actorPhotoURL[0])
		
    # TITLE
    title = detailsPageElements.xpath('//div[(contains(@class,"video-info-left pull-left"))]/h2/a')[0].text_content().strip()
    metadata.title = title
    Log('Title: ' +  metadata.title)

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[(contains(@class,"video-bottom-txt"))]')[0].text_content().strip()
    Log('summary: ' +  metadata.summary)
	
    # Release Date
    script_text = detailsPageElements.xpath('//script[@type="application/ld+json"][1]')[0].text_content()
    alpha = script_text.find('datePublished')
    omega = script_text.find('"',alpha+16)
    date = script_text[alpha+16:omega]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Posters/Background
    art = []
    xpaths = [
        '//div[(contains(@class,"sub-video"))]/a/@href'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            poster = poster.split('?')[0]

            art.append(poster)

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
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if(width > 100 and idx > 1):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass


    return metadata
