import PAsearchSites
import PAgenres
import PAactors
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="item-video hover"]'):
        titleNoFormatting = searchResult.xpath('.//a')[0].get('title').strip()
        curID = "http:" + searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        releaseDate = parse(searchResult.xpath('.//div[@class="date"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    metadata.studio = 'BellaPass'
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="videoDetails clear"]/p')[0].text_content().strip()
    
    # Tagline
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="videoDetails clear"]/h3')[0].text_content().strip()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="featuring clear"]/ul/li[@class="label" and contains(text(),"Tags:")]/following-sibling::li/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="featuring clear"]/ul/li[@class="label" and contains(text(),"Featuring:")]/following-sibling::li/a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPage.xpath('//img[@class="model_bio_thumb stdimage thumbs target"]')[0].get("src0_1x")
            movieActors.addActor(actorName,actorPhotoURL)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="videoInfo clear"]/p')[0].text_content().replace('Date Added:','').strip()
    Log('date: ' + str(date))
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Artwork

    # Video background
    setID = detailsPageElements.xpath('//img[@class="update_thumb thumbs stdimage"]')[0].get('id')

    try:
        art.append(PAsearchSites.getSearchBaseURL(siteID) + detailsPageElements.xpath('//img[@class="update_thumb thumbs stdimage"]')[0].get('src0_3x'))
    except:
        pass

    # Search Page
    try:
        Log('searchPageElements: ' + PAsearchSites.getSearchSearchURL(siteID) + metadata.title.replace(' ','+'))
        searchPageElements = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteID) + metadata.title.replace(' ','+'))
        cnt = int(searchPageElements.xpath('//img[@id="'+setID+'"]')[0].get('cnt'))
        for i in range(cnt):
            Log('i: ' + str(i))
            Log('art.append: '+PAsearchSites.getSearchBaseURL(siteID) + searchPageElements.xpath('//img[@id="'+setID+'"]')[0].get('src'+str(i)+'_3x'))
            art.append(PAsearchSites.getSearchBaseURL(siteID) + searchPageElements.xpath('//img[@id="'+setID+'"]')[0].get('src'+str(i)+'_3x'))
    except:
        pass

    # Photo page
    try:
        photoPageElements = HTML.ElementFromURL(url.replace('/trailers/','/preview/'))
        for image in photoPageElements.xpath('//img[@id="'+setID+'"]'):
            art.append(PAsearchSites.getSearchBaseURL(siteID) + image.get('src0_3x'))
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
