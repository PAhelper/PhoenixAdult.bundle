import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    Log("siteNum: " + str(siteNum))
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

    if "how to handle your students 101" in searchTitle.lower():
        if "angelica heart" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7007/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Angelica Heart" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "jessica bangkok" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7008/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Jessica Bangkok" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "morgan ray" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7009/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Morgan Ray" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "kerry louise" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7011/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Kerry Louise" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "tanya tate" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7012/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Tanya Tate" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "veronica avluv" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7013/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Veronica Avluv" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "katie kox" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7014/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Katie Kox" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "britney amber" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7015/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Britney Amber" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "sophie dee" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7016/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Sophie Dee" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "julia ann" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7017/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Julia Ann" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
        elif "rachel roxx" in searchTitle.lower() or "sienna west" in searchTitle.lower():
            Log("Manual Search Match")
            curID = ("https://www.brazzers.com/scenes/view/id/7018/how-to-handle-your-students-101/")
            curID = curID.replace('/','_')
            Log(str(curID))
            subSite = "Brazzers Vault"
            releaseDate = "2012-12-03"
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "How To Handle Your Students: 101 - Rachel Roxx & Sienna West" + " [Brazzers/" + subSite + "] " + releaseDate, score = 101, lang = lang))
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
