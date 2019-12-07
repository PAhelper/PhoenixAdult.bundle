import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    try:
        # URL Scene Search
        searchString = searchTitle.replace(" ","-")
        url = PAsearchSites.getSearchSearchURL(siteNum) + "updates/" + searchString + ".html"
        try:
            searchResult = HTML.ElementFromURL(url)
        except:
            Log("Normal url failed, trying with trailing hyphen")
            searchResult = HTML.ElementFromURL(url.replace(".html", "-.html"))
        titleNoFormatting = searchResult.xpath('//div[contains(concat(" ",normalize-space(@class)," "),"title")]//h3')[0].text_content().strip()
        curID = url.replace('/','+').replace('?','!')
        if searchDate:
            releaseDate = parse(searchDate).strftime('%Y-%m-%d')
        else:
            releaseDate = ''
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum) + "|" + releaseDate, name = titleNoFormatting + " [New Sensations] ", score = 100, lang = lang))
    except:
        # URL DVD Search
        searchString = searchTitle.replace(" ","-")
        url = PAsearchSites.getSearchSearchURL(siteNum) + "dvds/" + searchString + ".html"
        searchResult = HTML.ElementFromURL(url)
        titleNoFormatting = searchResult.xpath('//div[@class="dvdSections clear"]/div[1]')[0].text_content().replace("DVDS /","").strip()
        curID = url.replace('/','+').replace('?','!')
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [New Sensations] ", score = 100, lang = lang))
    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('+','/').replace('?','!')
    if "dvds" in url:
        sceneType = "DVD"
        Log("Is DVD")
    else:
        sceneType = "Scene"
        Log("Is Scene")
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'New Sensations'

    if sceneType == "Scene":
        Log("SceneUpdate")
        # Title
        metadata.title = detailsPageElements.xpath('//div[@class="trailerVideos clear"]/div[1]')[0].text_content().strip()

        # Summary
        metadata.summary = detailsPageElements.xpath('//div[@class="trailerInfo"]/p')[0].text_content().strip()

        # Tagline and Collection(s)
        # DVD Name
        dvdName = detailsPageElements.xpath('//div[@class="trailerInfo"]/ul/li[4]')[0].text_content().replace('DVD:','').strip()
        metadata.tagline = dvdName
        metadata.collections.add(dvdName)
        #Site Name
        siteName = PAsearchSites.getSearchSiteName(siteID).strip()
        metadata.collections.add(siteName)

        # Genres
        genres = detailsPageElements.xpath('//div[@class="trailerInfo"]/ul/li[3]/a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip().lower()
                movieGenres.addGenre(genreName)

        # Release Date
        try:
            date = str(metadata.id).split("|")[2]
            if len(date) > 0:
                date_object = parse(date)
                metadata.originally_available_at = date_object
                metadata.year = metadata.originally_available_at.year
                Log("Date from file")
        except:
            pass

        # Actors
        actors = detailsPageElements.xpath('//div[@class="trailerInfo"]/ul/li[1]/span/a')
        if len(actors) > 0:
            if len(actors) == 3:
                movieGenres.addGenre("Threesome")
            if len(actors) == 4:
                movieGenres.addGenre("Foursome")
            if len(actors) > 4:
                movieGenres.addGenre("Orgy")
            for actorLink in actors:
                actorName = str(actorLink.text_content().strip())
                try:
                    actorPageURL = actorLink.get("href")
                    actorPage = HTML.ElementFromURL(actorPageURL)
                    actorPhotoURL = actorPage.xpath('//div[@class="modelPicture"]/div/img')[0].get("src0_3x")
                except:
                    actorPhotoURL = ''
                movieActors.addActor(actorName, actorPhotoURL)

        ### Posters and artwork ###

        # Video trailer background image
        bgnum = 1
        try:
            twitterBG = detailsPageElements.xpath('//span[@id="limit_thumb"]/a/span[1]/img')[0].get('src')
            metadata.art[twitterBG] = Proxy.Preview(HTTP.Request(twitterBG, headers={'Referer': 'http://www.google.com'}).content, sort_order=bgnum)
            metadata.posters[twitterBG] = Proxy.Preview(HTTP.Request(twitterBG, headers={'Referer': 'http://www.google.com'}).content, sort_order=2)
            bgnum += 1
        except:
            pass

        # DVD Page
        try:
            dvdPageLink = detailsPageElements.xpath('//div[@class="trailerInfo"]/ul/li[4]/a')[0].get('href')
            dvdPageElements = HTML.ElementFromURL(dvdPageLink)
            dvdPosterURL = dvdPageElements.xpath('//div[@class="dvdcover"]//img')[0].get("src")
            if dvdPosterURL == None:
                dvdPosterURL = dvdPageElements.xpath('//div[@class="dvdcover"]//img')[0].get("data-src")
            metadata.posters[dvdPosterURL] = Proxy.Preview(HTTP.Request(dvdPosterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order=1)
        except:
            Log("DVD Cover not found")
            pass

    else:
        Log("DVDUpdate")
        # Title
        title = detailsPageElements.xpath('//div[@class="dvdSections clear"]/div[1]')[0].text_content().replace("DVDS /","").strip()
        metadata.title = title

        # Summary
        metadata.summary = detailsPageElements.xpath('//div[@class="dDetails"]/p')[0].text_content().strip()

        # Tagline and Collection(s)
        # DVD Name
        dvdName = title
        metadata.tagline = dvdName
        metadata.collections.add(dvdName)
        # Site Name
        siteName = PAsearchSites.getSearchSiteName(siteID).strip()
        metadata.collections.add(siteName)

        # Genres
        genres = detailsPageElements.xpath('//div[@class="dvdDetails clear"]/ul/li[2]/a')
        if len(genres) > 0:
            for genreLink in genres:
                genreName = genreLink.text_content().strip().lower()
                movieGenres.addGenre(genreName)

        # Release Date
        date = detailsPageElements.xpath('//div[@class="dvdDetails clear"]/ul/li[1]')[0].text_content().replace('Released:','').strip()
        if len(date) > 0:
            try:
                date_object = datetime.strptime(date, '%Y-%m-%d')
            except:
                date_object = datetime.strptime(date, '%m/%d/%y')
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year

        # Actors
        try:
            actors = detailsPageElements.xpath('//span[@class="tour_update_models"]/a')
            if len(actors) > 0:
                for actorLink in actors:
                    actorName = str(actorLink.text_content().strip())
                    try:
                        actorPageURL = actorLink.get("href")
                        actorPage = HTML.ElementFromURL(actorPageURL)
                        actorPhotoURL = actorPage.xpath('//div[@class="modelPicture"]/div/img')[0].get("src0_3x")
                    except:
                        actorPhotoURL = ''
                    movieActors.addActor(actorName, actorPhotoURL)
        except:
            actorsList = detailsPageElements.xpath('//div[@class="dvdDetails clear"]/div[2]/p')[0].text_content().split('Featuring:')[1]
            actors = actorsList.split(",")
            if len(actors) > 0:
                for actorLink in actors:
                    actorName = str(actorLink.strip())
                    actorPhotoURL = ''
                    movieActors.addActor(actorName, actorPhotoURL)

        ### Posters and artwork ###

        # DVD Cover
        posterNum = 1
        try:
            dvdPosterURL = detailsPageElements.xpath('//div[@class="dvdcover"]//img')[0].get("src")
            if dvdPosterURL == None:
                dvdPosterURL = detailsPageElements.xpath('//div[@class="dvdcover"]//img')[0].get("data-src")
            metadata.posters[dvdPosterURL] = Proxy.Preview(HTTP.Request(dvdPosterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order=posterNum)
            posterNum += 1
        except:
            Log("DVD Cover not found")
            pass

    return metadata
