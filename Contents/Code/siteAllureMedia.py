import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    Log('****SEARCH*****')
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    # Amateur Allure
    if siteNum == 564:
        for searchResult in searchResults.xpath('//div[@class="update_details"]'):
            titleNoFormatting = searchResult.xpath('.//div[@class="update_title"]/a')[0].text_content().strip()
            releaseDate = parse(searchResult.xpath('.//div[@class="update_date"]')[0].text_content().replace('Added:','').strip()).strftime('%Y-%m-%d')
            curID = searchResult.xpath('.//a[1]')[0].get('href').replace('/','_').replace('?','!')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            if len(titleNoFormatting) > 29:
                titleNoFormatting = titleNoFormatting[:32] + "..."
            results.Append(MetadataSearchResult(id=curID + "|" + str(siteNum), name=titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score=score, lang=lang))

    # Swallow Salon
    if siteNum == 565:
        for searchResult in searchResults.xpath('//div[@class="update_details"]'):
            titleNoFormatting = searchResult.xpath('./a[2]')[0].text_content().strip()
            releaseDate = parse(searchResult.xpath('.//div[@class="cell update_date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
            curID = searchResult.xpath('./a[2]')[0].get('href').replace('/','_').replace('?','!')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            if len(titleNoFormatting) > 29:
                titleNoFormatting = titleNoFormatting[:32] + "..."
            results.Append(MetadataSearchResult(id=curID + "|" + str(siteNum), name=titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score=score, lang=lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Allure Media'
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?').replace('/vids.html','_vids.html')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Summary
    paragraph = detailsPageElements.xpath('//span[@class="update_description"]')[0].text_content().strip()
    metadata.summary = paragraph.strip()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//span[@class="update_tags"]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)
    movieGenres.addGenre("Amateur")

    # Release Date
    date = detailsPageElements.xpath('//div[contains(@class,"update_date")]')[0].text_content().strip()
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
    photoPageURL = None
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
            if i == 5:
                actorPhotoURL = posterUrl
            photos.append(posterUrl)
            i = i + 1
        for x in range(10):
            art.append(photos[random.randint(1,imageCount)])
    except:
        pass

    # Vidcaps page
    try:
        capsPageURL = detailsPageElements.xpath('//div[@class="cell content_tab"]/a[text()="Photos"]')[0].get('href')
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
            if i == 5:
                actorPhotoURL = posterUrl
            vidcaps.append(posterUrl)
            i = i + 1
        for x in range(10):
            art.append(vidcaps[random.randint(1,imageCount)])
    except:
        pass

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="backgroundcolor_info"]/span[@class="update_models"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//div[@class="cell_top cell_thumb"]/img').get('src')
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Manually Add Actors
    # Add Actor Based on Title
    if "Faith" == metadata.title:
        actorName = "Faith"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    # Search for Actor Name in Title and Summary
    if "Nikki Rhodes" in metadata.title or "Nikki Rhodes" in metadata.summary:
        actorName = "Nikki Rhodes"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Talia Tyler" in metadata.title or "Talia Tyler" in metadata.summary:
        actorName = "Talia Tyler"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Hadley" in metadata.title or "Hadley" in metadata.summary:
        actorName = "Hadley"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Evangeline" in metadata.title or "Evangeline" in metadata.summary:
        actorName = "Tanner Mayes"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Zoe Voss" in metadata.title or "Zoe Voss" in metadata.summary:
        actorName = "Zoe Voss"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Raquel Diamond" in metadata.title or "Raquel Diamond" in metadata.summary:
        actorName = "Raquel Diamond"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Shay Golden" in metadata.title or "Shay Golden" in metadata.summary:
        actorName = "Shay Golden"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Emily Grey" in metadata.title or "Emily Grey" in metadata.summary:
        actorName = "Emily Grey"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Allyssa Hall" in metadata.title or "Allyssa Hall" in metadata.summary:
        actorName = "Allyssa Hall"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Alexa Grace" in metadata.title or "Alexa Grace" in metadata.summary:
        actorName = "Alexa Grace"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Remy LaCroix" in metadata.title or "Remy LaCroix" in metadata.summary:
        actorName = "Remy LaCroix"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Nadine Sage" in metadata.title or "Nadine Sage" in metadata.summary:
        actorName = "Nadine Sage"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Chloe Starr" in metadata.title or "Chloe Starr" in metadata.summary:
        actorName = "Chloe Starr"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Melissa Moore" in metadata.title or "Melissa Moore" in metadata.summary:
        actorName = "Melissa Moore"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Taylor Renae" in metadata.title or "Taylor Renae" in metadata.summary:
        actorName = "Taylor Renae"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Veronica Rodriguez" in metadata.title or "Veronica Rodriguez" in metadata.summary:
        actorName = "Veronica Rodriguez"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Naomi Woods" in metadata.title or "Naomi Woods" in metadata.summary:
        actorName = "Naomi Woods"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Amanda Aimes" in metadata.title or "Amanda Aimes" in metadata.summary:
        actorName = "Amanda Aimes"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Alice Green" in metadata.title or "Alice Green" in metadata.summary:
        actorName = "Alice Green"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Kimber Woods" in metadata.title or "Kimber Woods" in metadata.summary:
        actorName = "Kimber Woods"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Alina Li" in metadata.title or "Alina Li" in metadata.summary:
        actorName = "Alina Li"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Holly Michaels" in metadata.title or "Holly Michaels" in metadata.summary:
        actorName = "Holly Michaels"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Layla London" in metadata.title or "Layla London" in metadata.summary:
        actorName = "Layla London"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Dakota Brookes" in metadata.title or "Dakota Brookes" in metadata.summary:
        actorName = "Dakoda Brookes"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Adriana Chechik" in metadata.title or "Adriana Chechik" in metadata.summary:
        actorName = "Adriana Chechik"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Belle Noire" in metadata.title or "Belle Noire" in metadata.summary:
        actorName = "Belle Noire"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Lilly Banks" in metadata.title or "Lilly Banks" in metadata.summary:
        actorName = "Lilly Banks"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Linda Lay" in metadata.title or "Linda Lay" in metadata.summary:
        actorName = "Linda Lay"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Miley May" in metadata.title or "Miley May" in metadata.summary:
        actorName = "Miley May"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Belle Knox" in metadata.title or "Belle Knox" in metadata.summary:
        actorName = "Belle Knox"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Ava Taylor" in metadata.title or "Ava Taylor" in metadata.summary:
        actorName = "Ava Taylor"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Stella May" in metadata.title or "Stella May" in metadata.summary:
        actorName = "Stella May"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Claire Heart" in metadata.title or "Claire Heart" in metadata.summary:
        actorName = "Claire Heart"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Kennedy Leigh" in metadata.title or "Kennedy Leigh" in metadata.summary:
        actorName = "Kennedy Leigh"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Lucy Tyler" in metadata.title or "Lucy Tyler" in metadata.summary:
        actorName = "Lucy Tyler"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Cadence Lux" in metadata.title or "Cadence Lux" in metadata.summary:
        actorName = "Cadence Lux"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Goldie Glock" in metadata.title or "Goldie Glock" in metadata.summary:
        actorName = "Goldie Glock"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Jayma Reid" in metadata.title or "Jayma Reid" in metadata.summary:
        actorName = "Jayma Reid"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Samantha Sin" in metadata.title or "Samantha Sin" in metadata.summary:
        actorName = "Samantha Sin"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Emma Hix" in metadata.title or "Emma Hix" in metadata.summary:
        actorName = "Emma Hix"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Lexi Mansfield" in metadata.title or "Lexi Mansfield" in metadata.summary:
        actorName = "Lexi Mansfield"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Emma Wilson" in metadata.title or "Emma Wilson" in metadata.summary:
        actorName = "Emma Wilson"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Kenzie Reeves" in metadata.title or "Kenzie Reeves" in metadata.summary:
        actorName = "Kenzie Reeves"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Devon Green" in metadata.title or "Devon Green" in metadata.summary:
        actorName = "Devon Green"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Jane Wilde" in metadata.title or "Jane Wilde" in metadata.summary:
        actorName = "Jane Wilde"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Lena Anderson" in metadata.title or "Lena Anderson" in metadata.summary:
        actorName = "Lena Anderson"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Lilly Banks" in metadata.title or "Lilly Banks" in metadata.summary:
        actorName = "Lilly Banks"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Linda Lay" in metadata.title or "Linda Lay" in metadata.summary:
        actorName = "Linda Lay"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Belle Knox" in metadata.title or "Belle Knox" in metadata.summary:
        actorName = "Belle Knox"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    if "Miley May" in metadata.title or "Miley May" in metadata.summary:
        actorName = "Miley May"
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
            try:
                referer = photoPageURL if photoPageURL else url
                req = urllib.Request(posterUrl)
                req.add_header('Referer', referer)
                img_file = urllib.urlopen(req)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': referer}).content, sort_order = j)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': referer}).content, sort_order = j)
                j = j + 1
            except Exception as e:
                Log("posterUrl: "+ posterUrl)
                Log("Error: " + str(e))

    return metadata