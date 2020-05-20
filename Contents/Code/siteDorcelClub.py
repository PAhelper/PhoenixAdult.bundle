import PAsearchSites
import PAgenres
import PAactors
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    # Scenes by name
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="scene"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="title"]/a')[0].text_content().strip()
        curID = searchResult.xpath('.//div[@class="title"]/a')[0].get('href').replace('/','`').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().replace('Published','').strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))

    # Movies by name
    for searchResult in searchResults.xpath('//div[@class="movie"]'):
        titleNoFormatting = searchResult.xpath('./a/p')[0].text_content().strip()
        movieLink = searchResult.xpath('./a')[0].get('href')
        curID = movieLink.replace('/','`').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " Full Movie ["+PAsearchSites.getSearchSiteName(siteNum)+"]", score = score, lang = lang))

        # Also append all the scenes from matching movies
        moviePageElements = HTML.ElementFromURL(movieLink)
        for movieScene in moviePageElements.xpath('//div[@class="scene"]'):
            titleNoFormatting = movieScene.xpath('.//div[@class="title"]/a')[0].text_content().strip()
            curID = movieScene.xpath('.//div[@class="title"]/a')[0].get('href').replace('/','`').replace('?','!')
            releaseDate = parse(movieScene.xpath('.//span[@class="date"]')[0].text_content().replace('Published','').strip()).strftime('%Y-%m-%d')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Marc Dorcel'
    url = str(metadata.id).split("|")[0].replace('`','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    movieGenres.clearGenres()
    movieActors.clearActors()
    metadata.directors.clear()
    director = metadata.directors.new()
    art = []

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="content_text"]')[0].text_content().strip()
    except:
        pass
    
    # Tagline
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    try:
        movieName = detailsPageElements.xpath('//div[@class="movie"]/a')[0].text_content().strip()
        metadata.collections.add(movieName)
        movieGenres.addGenre("Blockbuster Movie")
    except:
        pass

    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()

    # Genres
    movieGenres.addGenre("French porn")

    # Actors
    try: # For individual scene page
        actors = detailsPageElements.xpath('//section[@id="pornstar"]//a')
        if len(actors) > 0:
            if "porn-movie" not in url and len(actors) == 3:
                movieGenres.addGenre("Threesome")
            if "porn-movie" not in url and len(actors) == 4:
                movieGenres.addGenre("Foursome")
            if "porn-movie" not in url and len(actors) > 4:
                movieGenres.addGenre("Orgy")
            for actorLink in actors:
                actorName = str(actorLink.text_content().strip())
                actorPhotoURL = actorLink.xpath('./img')[0].get('src')
                movieActors.addActor(actorName,actorPhotoURL)
    except:
        pass   
    
    # Release Date
    date = detailsPageElements.xpath('//span[@class="date"]')[0].text_content().replace('Published','').strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Director
    try: # This is for getting from scene page to movie page and grabbing director, if available
        moviePage = detailsPageElements.xpath('//div[@class="movie"]/a')[0].get('href').strip()
        moviePageElements = HTML.ElementFromURL(moviePage)
        movieDirector = moviePageElements.xpath('//div[@class="infos"]/p[2]')[0].text_content().replace('Movie Director:','').strip()
        director.name = movieDirector
    except:
        pass

    try: # This is for getting the director if you're matching a whole movie
        director.name = detailsPageElements.xpath('//div[@class="infos"]/p[2]')[0].text_content().replace('Movie Director:','').strip()
    except:
        pass

    # Country
    metadata.countries.add("French")

    # Video backgrounds
    xpaths = [
        '//ul[@class="vid_rotator_img"]//img/@data-lazy',
        '//div[contains(@class, "pictures_container")]//img[@class="item"]/@src'
    ]

    for xpath in xpaths:
        for img in detailsPageElements.xpath(xpath):
            trash = '_' + img.split('_', 3)[-1].rsplit('.', 1)[0]
            img = img.replace(trash, '', 1)

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
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
