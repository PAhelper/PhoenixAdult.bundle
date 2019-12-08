import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    Log("siteNum: " + str(siteNum))
    
    if unicode(searchTitle.split(" ")[0], 'utf-8').isnumeric():
        url = PAsearchSites.getSearchBaseURL(siteNum) + "/scenes/view/id/" + searchTitle.split(" ")[0]
        Log(url)
        searchResult = HTML.ElementFromURL(url)
        titleNoFormatting = searchResult.xpath('//h1')[0].text_content().strip()
        curID = (PAsearchSites.getSearchBaseURL(int(siteNum)) + searchResult.xpath('//meta[@name= "dti.url"]')[0].get('content')).replace('/','_').replace('?','!')
        Log(curID)
        subSite = searchResult.xpath('//span[@class="label-text"]')[0].text_content().strip()
        Log(subSite)
        releaseDate = parse(searchResult.xpath('//aside[@class= "scene-date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        Log(releaseDate)

        score = 100
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Brazzers/" + subSite + "] " + releaseDate, score = score, lang = lang))
        return results

    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="scene-card-info"]'):
        titleNoFormatting = searchResult.xpath('.//a[1]')[0].get('title')
        curID = (PAsearchSites.getSearchBaseURL(int(siteNum)) + searchResult.xpath('.//a[1]')[0].get('href')).replace('/','_').replace('?','!')
        subSite = searchResult.xpath('.//span[@class="label-text"]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('.//time')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Brazzers/" + subSite + "] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'Brazzers'
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//p[@itemprop="description"]')[0].text_content()
    paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = paragraph[:-10]
    tagline = detailsPageElements.xpath('//span[@class="label-text"]')[0].text_content()
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[contains(@class,"tag-card-container")]//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            # If it's part of a series, add an extra Collection tag with the series name... Trouble is there's no standard for locating the series name, so this might not work 100% of the time
            if "series" in genreName or "800 Phone Sex: Line " in metadata.title or ": Part" in metadata.title or "Porn Logic" in metadata.title or "- Ep" in metadata.title or tagline == "ZZ Series":
                seriesName = metadata.title
                if (seriesName.rfind(':')):
                    metadata.collections.add(seriesName[:seriesName.rfind(':')])
                elif (seriesName.rfind('- Ep')):
                    metadata.collections.add(seriesName[:seriesName.rfind('- Ep')])
                else:
                    metadata.collections.add(seriesName.rstrip('1234567890 '))
            if "office 4-play" in metadata.title.lower() or "office 4-play" in genreName:
                metadata.collections.add("Office 4-Play")

            # But we don't need a genre tag named "3 part series", so exclude that genre itself
            if "series" not in genreName and "office 4-play" not in genreName:
                movieGenres.addGenre(genreName)


    # Release Date
    date = detailsPageElements.xpath('//aside[contains(@class,"scene-date")]')
    if len(date) > 0:
        date = date[0].text_content()
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    
    # Actors
    movieActors.clearActors()
    #starring = detailsPageElements.xpath('//p[contains(@class,"related-model")]//a')
    actors = detailsPageElements.xpath('//div[@class="model-card"]/div[@class="card-image"]/a/img[@class="lazy card-main-img"]')
    if len(actors) > 0:
        # Check if member exists in the maleActors list as either a string or substring
        #if any(member.text_content().strip() in m for m in maleActors) == False:
        for actorLink in actors:
            actorName = actorLink.get('alt')
            actorPhotoURL = "http:" + actorLink.get('data-src').replace("model-medium.jpg","model-small.jpg")
            movieActors.addActor(actorName,actorPhotoURL)
    
    #Posters
    i = 1
    try:
        background = "http:" + detailsPageElements.xpath('//*[@id="trailer-player"]/img')[0].get('src')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass
    for poster in detailsPageElements.xpath('//a[@rel="preview"]'):
        posterUrl = "http:" + poster.get('href').strip()
        thumbUrl = "http:" + detailsPageElements.xpath('//img[contains(@data-src,"thm")]')[i-1].get('data-src')
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #posterUrl = posterUrl[:-6] + "01.jpg"
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i)
                if(width > 100):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = i+1)
                i = i + 1
            except:
                pass


    return metadata
