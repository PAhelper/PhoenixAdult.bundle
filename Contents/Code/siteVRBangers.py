import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//article'):
        titleNoFormatting = searchResult.xpath('.//a[@rel="bookmark"]')[0].text_content().strip()
        detailsPageElements = HTML.ElementFromURL(searchResult.xpath('.//a[@rel="bookmark"]')[0].get('href'))
        releaseDate = parse(detailsPageElements.xpath('//p[@class="pull-right dates invisible"]')[0].text_content().strip()).strftime('%Y-%m-%d')
        curID = searchResult.xpath('.//a[@rel="bookmark"]')[0].get('href').replace('/','_').replace('?','!')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        if len(titleNoFormatting) > 29:
            titleNoFormatting = titleNoFormatting[:32] + "..."

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ["+PAsearchSites.getSearchSiteName(siteNum)+"] " + releaseDate, score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art=[]

    # Studio
    metadata.studio = "VR Bangers"

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="video-info-title"]//h1[@class="pull-left page-title"]//span')[0].text_content()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="mainContent"]/p')[0].text_content().strip()

    # Tagline and Collection
    tagline = "VR Bangers"
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//p[@class="pull-right dates invisible"]')[0].text_content()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="video-tags"]//a[@class="tags-item"]')
    if len(genres) > 0:
        for genre in genres:
            movieGenres.addGenre(genre.text_content())

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="girls-name"]//div[@class="girls-name-video-space"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().replace(", ","")
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="single-model-featured"]//img')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    for posterLink in detailsPageElements.xpath('//div[@class="single-video-gallery-free"]/a'):
        art.append(posterLink.get('href'))

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