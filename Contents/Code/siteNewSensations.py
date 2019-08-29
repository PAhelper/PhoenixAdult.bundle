import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    try:
        # actress search
        try:
            searchString = searchTitle.replace(" ","-")
            searchResults = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(searchSiteID) + "/tour_ns/models/" + searchString + ".html")
        except:
            try:
                # Random actors have a trailing dash
                searchString = searchString + '-'
                searchResults = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(searchSiteID) + "/tour_ns/models/" + searchString + ".html")
            except:
                try:
                    searchString = searchTitle.replace(" ","")
                    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(searchSiteID) + "/tour_ns/models/" + searchString + ".html")
                except:
                    searchString = searchTitle.replace(" ","")
                    searchInt = int(searchString)
                    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(searchSiteID) + "/tour_ns/sets.php?id=" + searchString)
        for searchResult in searchResults.xpath('//div[contains(@class,"videoBlock")]'):
            titleNoFormatting = searchResult.xpath('.//div[contains(@class,"caption")]//h4//a')[0].text_content()
            Log("titleNoFormatting: " + titleNoFormatting)
            curID = searchResult.xpath('.//div[contains(@class,"caption")]//h4//a')[0].get('href').replace('/', '_').replace('?', '!')
            Log("curID: " + curID)
            results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [New Sensations] ", score = 100, lang = lang))

    except:
        # search by DVD
            searchString = searchTitle.lower().replace(" ","-").replace("#","").replace("'","").replace("vol. ","").replace("volume ","")
            searchResults = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(searchSiteID) + "/tour_ns/dvds/" + searchString + ".html")
            for searchResult in searchResults.xpath('//div[@class="dvdScene"]'):
                titleNoFormatting = searchResult.xpath('.//h4//a')[0].text_content()
                Log("titleNoFormatting: " + titleNoFormatting)
                curID = searchResult.xpath('.//h4//a')[0].get('href').replace('/','_').replace('?','!')
                Log("curID: " + curID)
                releaseDate = parse(searchResult.xpath('.//div[@class="date"]')[0].text_content().split(' l ')[0].replace("Released","").strip()).strftime('%Y-%m-%d')
                Log("releaseDate: " + releaseDate)
                if searchDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [New Sensations] " + releaseDate, score = score, lang = lang))

# From when site had search functionality
    # searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    # for searchResult in searchResults.xpath('//h4//a'):
    #     Log(str(searchResult.get('href')))
    #     titleNoFormatting = searchResult.text_content()
    #     curID = searchResult.get('href').replace('/','_').replace('?','!')
    #     score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
    #
    #     results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [New Sensations]", score = score, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    metadata.studio = 'New Sensations'
    # Scene(details) page
    detailsPageElements = HTML.ElementFromURL(str(metadata.id).split("|")[0].replace('_','/').replace('!','?').replace('tour/ns','tour_ns'))

    # Scene Title
    metadata.title = detailsPageElements.xpath('//div[@class="trailerVideos clear"]//div[@class="title clear"]//h3')[0].text_content()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="trailerInfo"]//p')[0].text_content().strip()

    # DVD name
    tagline = detailsPageElements.xpath('//div[@class="trailerInfo"]//ul//li[4]//a')[0].text_content().strip()
    Log("DVD name/tagline: " + tagline)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # DVD Page
    dvdPageLink = detailsPageElements.xpath('//div[@class="trailerInfo"]//ul//li[4]//a')[0].get("href")
    Log("dvdPageLink: " + dvdPageLink)
    dvdPageElements = HTML.ElementFromURL(dvdPageLink)

    #
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    # Release Date (only available on DVD page)
    date = dvdPageElements.xpath('//div[@class="dvdScene"]//div[@class="date"]')
    if len(date) > 0:
        date = date[0].text_content().strip()
        date = date[10:20]
        try:
            date_object = datetime.strptime(date, '%m/%d/%Y')
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
        except:
            pass


    # DVD Cover as first poster
    posterNum = 1
    try:
        dvdPosterURL = dvdPageElements.xpath('//div[@class="dvdcover"]//img')[0].get("src")
        if dvdPosterURL == None:
            dvdPosterURL = dvdPageElements.xpath('//div[@class="dvdcover"]//img')[0].get("data-src")
        metadata.posters[dvdPosterURL] = Proxy.Preview(HTTP.Request(dvdPosterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
        posterNum += 1
    except:
        Log("DVD Cover not found")


    # Background
    bgNum = 1
    try:
        background = detailsPageElements.xpath('//span[@id="trailer_thumb"]//img')[0].get('src')
        if background != None:
            Log("BG DL: " + background)
            metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = bgNum)
            bgNum += 1
            # also possible poster
            metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
            posterNum +=1
        else:
            Log("BG not found")
    except:
        pass

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[@class="trailerInfo"]//ul//li[3]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip('\n').lower()
            movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//div[@class="trailerInfo"]//ul//li//span[@class="tour_update_models"]//a')
    Log("Actors found: "+str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")

            # Prepend base url if actorPage is a sets.php
            if actorPageURL.startswith("sets.php"):
                actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + "/tour_ns/" + actorPageURL
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//div[@class="modelPicture"]//img')[0].get("src")
            if actorPhotoURL == None:
                actorPhotoURL = actorPage.xpath('//div[@class="modelPicture"]//img')[0].get("data-src")
            movieActors.addActor(actorName,actorPhotoURL)
            # add actor image as possible poster
            try:
                if len(actors) < 3:
                    metadata.posters[actorPhotoURL] = Proxy.Preview(HTTP.Request(actorPhotoURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = posterNum)
                    posterNum += 1
            except:
                pass
    # DVD page only place with more thumbs
    for dvdThumb in dvdPageElements.xpath('//div[@class="dvdScenePic"]//img'):
        dvdThumbURL = dvdThumb.get("src")
        try:
            if dvdThumbURL == None:
                dvdThumbURL = dvdThumb.get("data-src")
            metadata.art[dvdThumbURL] = Proxy.Preview(HTTP.Request(dvdThumbURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = bgNum)
            bgNum += 1
        except:
            pass

    return metadata
