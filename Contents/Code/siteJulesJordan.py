import PAsearchSites
import PAgenres
import math

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="update_details"]'):
        titleNoFormatting = searchResult.xpath('./a[last()]')[0].text_content().strip()
        releaseDate = searchResult.xpath('.//div[@class="cell update_date"]')[0].text_content().strip()
        if releaseDate == '':
            try:
                releaseDate = str(searchResult.xpath('.//div[@class="cell update_date"]/comment()')[0]).strip()
                releaseDate = releaseDate[releaseDate.find('OFF')+4:releaseDate.find('D',releaseDate.find('OFF')+4)].strip()
            except:
                pass
        releaseDate = parse(releaseDate).strftime('%Y-%m-%d')
        Log("releaseDate: " + releaseDate)
        curID = searchResult.xpath('./a[last()]')[0].get('href').replace('/','_').replace('?','!')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate , score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!').replace('/vids.html','_vids.html')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Jules Jordan'

    # Title
    metadata.title = detailsPageElements.xpath('//span[@class="title_bar_hilite"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//span[@class="update_description"]')[0].text_content().strip()

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID)
    tagline = tagline.strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    try:
        dvdName = detailsPageElements.xpath('//span[@class="update_dvds"]')[0].text_content().replace('Movie:','').strip()
        metadata.collections.add(dvdName)
    except:
        pass

    # Genres
    genres = detailsPageElements.xpath('//span[@class="update_tags"]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="cell update_date"]')[0].text_content().strip()
    if date == '':
        try:
            date = str(detailsPageElements.xpath('.//div[@class="cell update_date"]/comment()')[0]).strip()
            date = date[date.find('OFF')+4:date.find('D',date.find('OFF')+4)].strip()
        except:
            pass
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    if PAsearchSites.getSearchSiteName(siteID) == "GirlGirl":
        actors = detailsPageElements.xpath('//div[@class="item"]/span/div/a')
    else:
        actors = detailsPageElements.xpath('//div[@class="backgroundcolor_info"]/span[@class="update_models"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            try:
                actorPhotoURL = actorPage.xpath('//img[@class="model_bio_thumb stdimage thumbs target"]')[0].get("src0_3x")
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters

    # Video trailer background
    try:
        bigScript = detailsPageElements.xpath('//script[contains(text(),"df_movie")]')[0].text_content()
        alpha = bigScript.find('useimage = "')+12
        omega = bigScript.find('";',alpha)
        background = bigScript[alpha:omega]
        if 'http' not in background:
            background = PAsearchSites.getSearchBaseURL(siteID) + background
        Log("background: "+background)
        art.append(background)
    except:
        pass

    # Slideshow of images from the Search page
    try:
        bigScript = detailsPageElements.xpath('//script[contains(text(),"df_movie")]')[0].text_content()
        alpha = bigScript.find('setid:"')+7
        omega = bigScript.find('",',alpha)
        setID = bigScript[alpha:omega]
        Log("setID: "+setID)
        searchPageElements = HTML.ElementFromURL((PAsearchSites.getSearchSearchURL(siteID) + metadata.title).replace(' ','%20'))
        posterUrl = searchPageElements.xpath('//img[@id="set-target-'+setID+'"]')[0].get('src')
        if 'http' not in posterUrl:
            posterUrl = PAsearchSites.getSearchBaseURL(siteID) + posterUrl
        Log("slideshow: "+posterUrl)
        art.append(posterUrl)
        i = 0
        for i in range(0,7):
            try:
                posterUrl = searchPageElements.xpath('//img[@id="set-target-'+setID+'"]')[0].get('src'+i+'_1x')
                if 'http' not in posterUrl:
                    posterUrl = PAsearchSites.getSearchBaseURL(siteID) + posterUrl
                Log("slideshow: "+posterUrl)
                art.append(posterUrl)
            except:
                pass
    except:
        pass

    # Photos page
    try:
        photoPageURL = detailsPageElements.xpath('//div[@class="cell content_tab"]/a[text()="Photos"]')[0].get('href')
        photoPageElements = HTML.ElementFromURL(photoPageURL)
        bigScript = photoPageElements.xpath('//script[contains(text(),"var ptx")]')[0].text_content()
        ptx1600starts = bigScript.find('1600')
        ptx1600ends = bigScript.find('togglestatus', ptx1600starts)
        ptx1600 = bigScript[ptx1600starts:ptx1600ends]
        photos = []
        i = 1
        alpha = 0
        omega = 0
        imageCount = ptx1600.count('ptx["1600"][')
        Log("Photos found: "+str(imageCount))
        while i <= imageCount:
            alpha = ptx1600.find('{src: "',omega)+7
            omega = ptx1600.find('"',alpha)
            posterUrl = ptx1600[alpha:omega]
            if 'http' not in posterUrl:
                posterUrl = PAsearchSites.getSearchBaseURL(siteID) + posterUrl
            photos.append(posterUrl)
            i = i + 1
        for x in range(10):
            art.append(photos[random.randint(1,imageCount)])
    except:
        pass

    # Vidcaps page
    try:
        capsPageURL = detailsPageElements.xpath('//div[@class="cell content_tab"]/a[text()="Caps"]')[0].get('href')
        capsPageElements = HTML.ElementFromURL(capsPageURL)
        bigScript = capsPageElements.xpath('//script[contains(text(),"var ptx")]')[0].text_content()
        ptxjpgstarts = bigScript.find('ptx["jpg"] = {};')
        ptxjpgends = bigScript.find('togglestatus', ptxjpgstarts)
        ptxjpg = bigScript[ptxjpgstarts:ptxjpgends]
        vidcaps = []
        i = 1
        alpha = 0
        omega = 0
        imageCount = ptxjpg.count('ptx["jpg"][')
        Log("Vidcaps found: "+str(imageCount))
        while i <= imageCount:
            alpha = ptxjpg.find('{src: "',omega)+7
            omega = ptxjpg.find('"',alpha)
            posterUrl = ptxjpg[alpha:omega]
            if 'http' not in posterUrl:
                posterUrl = PAsearchSites.getSearchBaseURL(siteID) + posterUrl
            vidcaps.append(posterUrl)
            i = i + 1
        for x in range(10):
            art.append(vidcaps[random.randint(1,imageCount)])
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