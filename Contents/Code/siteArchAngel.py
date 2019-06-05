import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="item-video hover"]'):
        titleNoFormatting = searchResult.xpath('./div[@class="item-thumb"]/a')[0].get('title')
        curID = searchResult.xpath('./div[@class="item-thumb"]/a')[0].get('href').replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [ArchAngel] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'ArchAngel Video'

    # Title
    metadata.title = detailsPageElements.xpath('//h4/a')[0].text_content().strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//p[@class="description"]')[0].text_content().strip()
    except:
        pass

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres

    # Release Date
    date = detailsPageElements.xpath('//ul[@class="item-meta"]/li')[0].text_content().replace('Release Date:','').strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//h5/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    photos = detailsPageElements.xpath('//img[contains(@class, "update_thumb thumbs stdimage")]')
    if len(photos) > 0:
        for photoLink in photos:
            photo = PAsearchSites.getSearchBaseURL(siteID) + photoLink.get('src0_3x')
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