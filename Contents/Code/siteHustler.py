import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + '"' + encodedTitle + '"')
    for searchResult in searchResults.xpath('//div[@class="item hover videoThumb"]'):
        titleNoFormatting = searchResult.xpath('./div/a')[0].get('title').strip()
        curID = searchResult.xpath('./div/a')[0].get('href').replace('/','_').replace('?','!')
        actorNames = ""
        actors = searchResult.xpath('.//h5/a')
        for actor in actors:
            actorName = actor.text_content()
            actorNames = actorNames + actorName + ", "
            Log("actorNames: " + actorNames)
        if actorNames != "":
            actorNames = actorNames[:-2]
            actorNames = str(actorNames) + " in "
        img = searchResult.xpath('./div/a/img')[0].get('src0_3x').replace('/','_').replace('?','!')
        if searchDate:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d')
        else:
            releaseDate = ''
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate + "|" + img, name = actorNames + titleNoFormatting + " [Hustler] ", score = score, lang = lang))

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
    metadata.studio = 'Hustler'

    # Title
    title = detailsPageElements.xpath('//div[@class="gallery-info"]/h1')[0].text_content()
    metadata.title = title.split('featuring')[0].strip()

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//div[@class="gallery-info"]/p')[0].text_content().strip()
    except:
        pass

    # Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//span[@class="gallery-meta"]/span/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = str(metadata.id).split("|")[2]
    if len(date) > 0:
        date_object = parse(date)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
        Log("Date from file")

    # Actors
    actors = detailsPageElements.xpath('//div[@class="gallery-info"]/h4/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            try:
                actorPageURL = actorLink.get("href")
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//div[@class="section-box profile-pic"]/img')[0].get("src0_3x")
                if 'http' not in actorPhotoURL:
                    actorPhotoURL = PAsearchSites.getSearchBaseURL(siteID) + actorPhotoURL
            except:
                actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = str(metadata.id).split("|")[3].replace('_','/').replace('!','?')
        art.append(twitterBG)
    except:
        pass

    j = 1
    Log("Artwork found: " + str(len(art)))
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):
            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
            j = j + 1

    return metadata