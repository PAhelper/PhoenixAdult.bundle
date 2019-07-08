import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="videos-list"]/article'):
        titleNoFormatting = searchResult.xpath('.//a')[0].get('title').strip()
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        if searchDate:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d')
        else:
            releaseDate = ''
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate , name = titleNoFormatting + " [WowPorn/WowGirls] ", score = score, lang = lang))

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
    metadata.studio = 'WowGirls'

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="title-views"]/h1')[0].text_content().strip().rsplit(" ",3)[0]

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="desc "]/p')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@class="tags-list"]/a[i[@class="fa fa-folder"]]')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    try:
        date = detailsPageElements.xpath('//meta[@property="article:published_time"]')[0].get('content')
    except:
        date = str(metadata.id).split("|")[2]
        Log("Date from file")

    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    
    # Actors
    actors = detailsPageElements.xpath('//div[@class="tags-list"]/a[i[@class="fa fa-tag"]]')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)


    ### Posters and artwork ###

    # Video trailer background image
    twitterBG = detailsPageElements.xpath('//meta[@property="og:image"]')[0].get('content')
    Log("TwitterBG: " + twitterBG)
    art.append(twitterBG)

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=j)
            j = j + 1

    return metadata