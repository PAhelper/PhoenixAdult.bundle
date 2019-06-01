import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class=" grid__item  "]'):
        titleNoFormatting = searchResult.xpath('//img')[0].get('alt')
        curID = searchResult.xpath('//a[@class="movie-cover movie-cover--landscape"]')[0].get('href').replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [XConfessions] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    url = "http://www.xconfessions.com" + (str(metadata.id).split("|"))[0].replace('_','/').replace('?','!')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Erika Lust Films'

    # Title
    metadata.title = detailsPageElements.xpath('//title')[0].text_content().strip()[:-14]

    # Summary
    Description = detailsPageElements.xpath('//div[@class="film__details-description-title"]')[0].text_content().strip()
    try:
        Erika = "Erika's Comment: " + detailsPageElements.xpath('//div[@class="film__erika-comment-text"]//p')[0].text_content().strip()
        metadata.summary = Description + "\n" + Erika
    except:
        metadata.summary = Description

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.addGenre("Artistic")

    # Release Date
    year = detailsPageElements.xpath('//div[@class="video-new-design__overview-data"]//p[1]')[0].text_content().strip()[:4]
    date = "January 1, " + year
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="video-new-design__overview-data"]/p[3]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Director
    director = metadata.directors.new()
    try:
        directors = detailsPageElements.xpath('//a[@class="video-new-design__description-highlight"]')
        for dirname in directors:
            director.name = dirname.text_content().strip()
    except:
        pass

    ### Posters and artwork ###

    # Poster
    try:
        poster = detailsPageElements.xpath('//div[@class="film__details-cover-image"]//img')[0].get('src')
        art.append(poster)
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