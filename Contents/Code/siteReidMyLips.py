import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchString = searchTitle.lower().replace(' ', '-')
    Log("searchString: " + searchString)
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchString
    searchResult = HTML.ElementFromURL(url)

    titleNoFormatting = searchResult.xpath('//title')[0].text_content().split("|")[-1].strip()
    curID = url.replace('/','_').replace('?','!')
    releaseDate = parse(searchResult.xpath('/html/body/div/div[4]/div[4]/div/main/div[2]/div[2]/div/div/div[2]/div/div/div[4]/p/span')[0].text_content().strip()).strftime('%Y-%m-%d')
    score=100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [ReidMyLips] " + releaseDate, score = score, lang = lang))

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
    metadata.studio = 'ReidMyLips'

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().split("|")[-1].strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//meta[@name="description"]')[0].get('content').strip()

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('/html/body/div/div[4]/div[4]/div/main/div[2]/div[2]/div/div/div[2]/div/div/div[4]/p/span')[0].text_content().strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actorName = "Riley Reid"
    actorPhotoURL = ""
    movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Photos
    photos = detailsPageElements.xpath('//div[@id="pro-gallery-margin-container"]//a[@class="block-fullscreen gallery-item-social-download  pull-right  gallery-item-social-button"]')
    if len(photos) > 0:
        for photoLink in photos:
            photo = photoLink.get('href').split("?")[0]
            art.append(photo)
        # Select 6 random images from art array
        art = [art[0], art[-1]] + random.sample(art, 6)

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