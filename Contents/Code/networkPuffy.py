import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@style="position:relative; background:black;"]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].get('title')
        SubSite = searchResult.xpath('.//img')[0].get('src')
        if 'wetandpissy' in SubSite:
            SubSite = 'Wet and Pissy'
        if 'weliketosuck' in SubSite:
            SubSite = 'We Like To Suck'
        if 'wetandpuffy' in SubSite:
            SubSite = 'Wet and Puffy'
        if 'simplyanal' in SubSite:
            SubSite = 'Simply Anal'
        if 'eurobabefacials' in SubSite:
            SubSite = 'Euro Babe Facials'
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        #releaseDate = parse(searchResult.xpath('.//span[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Puffy Network/" + SubSite + "] ", score = score, lang = lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    temp = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    url = 'https://www.puffynetwork.com/' + temp
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Puffy Network'

    # Title
    metadata.title = detailsPageElements.xpath('//div/section[1]/div[2]/h2/span')[0].text_content().strip()

    # Summary
    all_summary = detailsPageElements.xpath('//div/section[3]/div[2]')[0].text_content().strip()
    tags_summary = detailsPageElements.xpath('//div/section[3]/div[2]/p')[0].text_content().strip()
    summary = all_summary.replace(tags_summary, '')
    summary = summary.split("Show more...")[0].strip()
    metadata.summary = summary
    # Log("Summary:" + metadata.summary)
    
    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div/section[3]/div[2]/p/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div/section[2]/dl/dt[2]')[0].text_content().strip("Released on:")
    Log("Date:" + date)
    if len(date) > 0:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div/section[2]/dl/dd[1]/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = actorLink.get("href")
                if 'http' not in actorPageURL:
                    actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorPageURL
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//div/section[1]/div/div[1]/img')[0].get("src")
                if 'http' not in actorPhotoURL:
            	    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    # Director

    ### Posters and artwork ###

    # Video trailer background image

    try:
        if 'Wet and Pissy' in tagline:
           temp2 = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
           temp2 = temp2.split("-video-")[1]
           twitterBG = 'https://media.wetandpissy.com/videos/video-' + temp2 + 'cover/hd.jpg'
           art.append(twitterBG)
        if 'We Like To Suck' in tagline:
           temp2 = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
           temp2 = temp2.split("-video-")[1]
           twitterBG = 'https://media.weliketosuck.com/videos/video-' + temp2 + 'cover/hd.jpg'
           art.append(twitterBG)
        if 'Wet and Puffy' in tagline:
           temp2 = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
           temp2 = temp2.split("-video-")[1]
           twitterBG = 'https://media.wetandpuffy.com/videos/video-' + temp2 + 'cover/hd.jpg'
           art.append(twitterBG)
        if 'Simply Anal' in tagline:
           temp2 = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
           temp2 = temp2.split("-video-")[1]
           twitterBG = 'https://media.simplyanal.com/videos/video-' + temp2 + 'cover/hd.jpg'
           art.append(twitterBG)
        if 'Euro Babe Facials' in tagline:
           temp2 = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
           temp2 = temp2.split("-video-")[1]
           twitterBG = 'https://media.eurobabefacials.com/videos/video-' + temp2 + 'cover/hd.jpg'
           art.append(twitterBG)
    except:
        pass

    # Posters
    posters = detailsPageElements.xpath('//div[contains(@id, "pics")]//div//ul//li//div//div//img')
    posterNum = 1
    Log(str(len(posters)))
    for poster in posters:
        posterURL = poster.get("src")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum += 1
    

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
                    # and Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                j = j + 1
            except:
                pass

    return metadata
