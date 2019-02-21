import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    url = PAsearchSites.getSearchSearchURL(siteNum) + searchTitle.lower().replace(" ","-").replace("'","-")
    searchResults = HTML.ElementFromURL(url)

    searchResult = searchResults.xpath('//div[@class="descrips"]')[0]
    titleNoFormatting = searchResult.xpath('//span[@class="wp-title videotitle"]')[0].text_content()
    curID = searchTitle.lower().replace(" ","-").replace("'","-")
    releaseDate = parse(searchResult.xpath('.//div[@class="row"]//div[@class="col-lg-6 col-sm-6"]//span')[0].text_content().strip()).strftime('%Y-%m-%d')

    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [" + PAsearchSites.getSearchSiteName(siteNum) + "] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    temp = str(metadata.id).split("|")[0]

    url = PAsearchSites.getSearchSearchURL(siteID) + temp
    Log('scene url: ' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    metadata.studio = "Nubiles"

    # Collections / Tagline
    siteName = PAsearchSites.getSearchSiteName(siteID)
    metadata.collections.clear()
    metadata.tagline = siteName
    metadata.collections.add(siteName)

    # Actors
    movieActors.clearActors()
    titleActors = ""
    actors = detailsPageElements.xpath('//span[@class="featuring-modelname model"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPhotoURL = PAactors.actorDBfinder(actorName)
            titleActors = titleActors + actorName + " & "
            Log("actorPhoto: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)
        titleActors = titleActors[:-3]

    # Genres
    movieGenres.clearGenres()
        # Based on site
    #if siteName.lower() == "Lubed".lower():
     #   for genreName in ['Lube', 'Raw', 'Wet']:
      #      movieGenres.addGenre(genreName)
    #elif siteName.lower() == "Holed".lower():
     #   for genreName in ['Anal', 'Ass']:
      #      movieGenres.addGenre(genreName)
    #elif siteName.lower() == "POVD".lower():
     #   for genreName in ['Gonzo', 'POV']:
      #      movieGenres.addGenre(genreName)
    #elif siteName.lower() == "MassageCreep".lower():
     #   for genreName in ['Massage', 'Oil']:
      #      movieGenres.addGenre(genreName)
    #elif siteName.lower() == "DeepThroatLove".lower():
     #   for genreName in ['Blowjob', 'Deep Throat']:
      #      movieGenres.addGenre(genreName)
    #elif siteName.lower() == "PureMature".lower():
     #   for genreName in ['MILF', 'Mature']:
      #      movieGenres.addGenre(genreName)
    # Based on number of actors
    if len(actors) == 3:
        movieGenres.addGenre('Threesome')
    if len(actors) == 4:
        movieGenres.addGenre('Foursome')
    if len(actors) > 4:
        movieGenres.addGenre('Orgy')

    # Posters
    #background = "http:" + detailsPageElements.xpath('//video[@class="vjs-tech"]')[0].get('poster')
    background = "http:" + detailsPageElements.xpath('//div[@id="watchpagevideo"]//div[@class="edgeCMSVideoPlayer"]//video')[0].get('poster')
    #background = background.replace("background-image: url(","").replace("\"","").replace("//","");
    Log("BG DL: " + background)
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    # Date
    date = detailsPageElements.xpath('//div[@class="descrips"]//div[@class="row"]//div[@class="col-lg-6 col-sm-6"]//span')[10].text_content().strip()
    Log('Date: ' + date)
    date_object = datetime.strptime(date, '%b %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Title
    metadata.title = detailsPageElements.xpath('//span[@class="wp-title videotitle"]')[0].text_content().strip()

    return metadata