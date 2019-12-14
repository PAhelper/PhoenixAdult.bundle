import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('/html/body/div[2]/div[2]/div[1]/div/div[1]/div/ul/li/h5'):
        titleNoFormatting = searchResult.xpath('./a')[0].text_content().strip()
        curID = searchResult.xpath('./a')[0].get('href').replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Playboy Plus] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Playboy Plus'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="fav_in"]/h3')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//meta[@name="description"]')[0].get('content').strip()

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.addGenre("Glamour")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="model_lft col-sm-4 col-xs-12"]/ul[1]/li[3]')[0].text_content().replace("Published:","").strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="modal-links"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    # Director
    director = metadata.directors.new()
    try:
        directors = detailsPageElements.xpath('//div[@class="model_lft col-sm-4 col-xs-12"]/ul[1]/li[2]')
        for dirname in directors:
            director.name = dirname.text_content().replace("Photographer:","").strip()
    except:
        pass

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//div[@class="banner_in inner_banner"]//img')[0].get('src')
        art.append(twitterBG)
    except:
        pass

    # Photos
    photos = detailsPageElements.xpath('//ul[@id="lightgallery"]//a')
    if len(photos) > 0:
        for photoLink in photos:
            photo = photoLink.get('href')
            art.append(photo)

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