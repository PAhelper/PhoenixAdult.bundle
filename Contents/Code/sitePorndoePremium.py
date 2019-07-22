import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="col col-33 t-col-50 m-col-100"]'):
        #Log(searchResult.text_content())
        titleNoFormatting = searchResult.xpath('.//a[@class="main-url"]')[0].get('title')
        subSite = searchResult.xpath('.//a[@class="uppercase"]')[0].get('title')
        curID = searchResult.xpath('.//a[@class="main-url"]')[0].get('href').replace('/','_').replace('?','!')

        score = 102 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        titleNoFormatting = titleNoFormatting + " [LetsDoeIt/"+subSite+"]"
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    url = str(metadata.id).split("|")[0].replace('_','/').replace('?','!')

    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "Porndoe Premium"

    metadata.summary = detailsPageElements.xpath('//meta[@itemprop="description"]')[0].get('content')
    metadata.title = detailsPageElements.xpath('//div[@itemprop="video"]/meta[@itemprop="name"]')[0].get('content')
    releaseDate = detailsPageElements.xpath('//meta[@itemprop="uploadDate"]')[0].get('content')
    date_object = parse(releaseDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year 
    metadata.tagline = detailsPageElements.xpath('//h4[@class="h5 no-space"]/a/strong')[0].text_content()
    metadata.collections.clear()
    metadata.collections.add(metadata.tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[contains(@href,"/videos/category/")]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)
    
    genres = detailsPageElements.xpath('//a[contains(@href,"/videos/tag/")]')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//a[@class="secondary-color links"]')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="avatar"]/picture/img[@class="lazy"]')[0].get("data-src")
            movieActors.addActor(actorName,actorPhotoURL)

    # Posters/Background
    try:
        background = detailsPageElements.xpath('//div[@class="swiper-slide gallery-swiper-slide"]/a/picture/source')[0].get("data-srcset").replace("/0x250/", "/1920x1080/").replace(".webp",".jpg")
        metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    except:
        pass


    posters = detailsPageElements.xpath('//div[@class="swiper-slide gallery-swiper-slide"]/a/picture/source')
    posterNum = 1
    for poster in posters:
        posterURL = poster.get("data-srcset").replace("/0x250/", "/1920x1080/").replace(".webp",".jpg")
        metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        metadata.art[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum + 1)
        posterNum += 1



    return metadata
