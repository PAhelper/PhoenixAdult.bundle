import PAsearchSites
import PAgenres

def posterAlreadyExists(posterUrl,metadata):
    for p in metadata.posters.keys():
        Log(p.lower())
        if p.lower() == posterUrl.lower():
            Log("Found " + posterUrl + " in posters collection")
            return True

    for p in metadata.art.keys():
        if p.lower() == posterUrl.lower():
            return True
    return False

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID):
    searchResults = HTML.ElementFromURL('https://tour.nympho.com/search/' + encodedTitle)
    for searchResult in searchResults.xpath('//h3[@class="title"]//a'):
        Log(str(searchResult.get('href')))
        titleNoFormatting = searchResult.text_content()
        #relDate = searchResults.xpath('//span[@class="fa fa-calendar"]')[0].text_content().strip()
        curID = searchResult.get('href').replace('/','_')
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Nympho]", score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'KB Productions'
    url = str(metadata.id).split("|")[0].replace('_','/')
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    paragraph = detailsPageElements.xpath('//div[@class="desc"]')[0].text_content().strip()
    #paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n','').replace('  ','') + "\n\n"
    metadata.summary = paragraph
    tagline = 'Nympho'
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h2[@class="title"]')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('hardcore')
    movieGenres.addGenre('gonzo')
    movieGenres.addGenre('nympho')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('(//h4[@class="models"])[1]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="model-photo"]//img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="post-date"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    #Posters
    i = 1
    try:
        background = detailsPageElements.xpath('//div[@id="trailer-player"]')[0].get('data-screencap')
        Log("BG DL: " + background)
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass

    posterTemplateURL = actorPage.xpath('//a[@href="' + url + '"]//img')[0].get('src')
    Log("Poster template: " + posterTemplateURL)
    for i in range(1,10):
        posterUrl = posterTemplateURL[:-5] + str(i) + ".jpg"
        Log("Poster URL: " + posterUrl)
        if not posterAlreadyExists(posterUrl,metadata):
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
