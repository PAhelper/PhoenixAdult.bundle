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
    for searchResult in searchResults.xpath('//div[@class="content-card-info"]'):
        titleNoFormatting = searchResult.xpath('./h4[@class="content-title-wrap"]/a')[0].text_content().strip()
        curID = searchResult.xpath('./h4[@class="content-title-wrap"]/a')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('./span[@class="date hidden-xs"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        lowerResultTitle = str(titleNoFormatting).lower()
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Nympho] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'KB Productions'
    url = str(metadata.id).split("|")[0].replace('_','/')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Summary
    paragraph = detailsPageElements.xpath('//div[contains(@class,"desc")]')[0].text_content().strip()
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
            actorPhotoURL = actorPage.xpath('//div[contains(@class,"wrap-model")]//img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="date hidden-xs"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    #Posters
    art.append(detailsPageElements.xpath('//video[@id="ypp-player"]')[0].get('poster'))

    for poster in actorPage.xpath('//a[@href="' + url + '"]//img'):
        art.append(poster.get('src'))
    for poster in actorPage.xpath('//div[@class="thumb-mouseover"]'):
        theStyle = poster.get('style')
        alpha = theStyle.find('http')
        omega = theStyle.find(');',alpha)
        art.append(theStyle[alpha:omega].strip())

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                if(width > 100):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                j = j + 1
            except:
                pass

    return metadata
