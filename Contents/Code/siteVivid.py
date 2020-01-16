import PAsearchSites
import PAgenres
import PAactors
import json

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
    }
    for sceneType in ['videos', 'dvds']:
        url = PAsearchSites.getSearchSearchURL(siteNum) + sceneType + '/api/?flagType=video&search=' + encodedTitle
        req = urllib.Request(url, headers=headers)
        data = urllib.urlopen(req).read()
        searchResults = json.loads(data)
        for searchResult in searchResults['responseData']:
            titleNoFormatting = searchResult['name']
            curID = searchResult['url'].replace('/','_').replace('?','!')
            if 'site' in searchResult:
                subSite = searchResult['site']['name']
            else:
                subSite = 'DVD'
            releaseDate = parse(searchResult['release_date']).strftime('%Y-%m-%d')
            videoBG = searchResult['placard_800'].replace('/','_').replace('?','!')
            if searchDate:
                score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
            else:
                score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
            results.Append(MetadataSearchResult(id='%s|%d|%s|%s' % (curID, siteNum, subSite, videoBG), name='%s [Vivid/%s] %s' % (titleNoFormatting, subSite, releaseDate), score=score, lang=lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = PAsearchSites.getSearchBaseURL(siteID) + str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'Vivid Entertainment'

    # Title
    metadata.title = detailsPageElements.xpath('//h2[@class="scene-h2-heading"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//p[@class="indie-model-p"]')[0].text_content().strip()

    # Tagline and Collection(s)
    tagline = str(metadata.id).split("|")[2]
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//h5[contains(text(),"Categories:")]/a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().strip().lower()
            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//h5[contains(text(),"Released:")]')[0].text_content().replace("Released:","").strip()
    if len(date) > 0:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//h4[contains(text(),"Starring:")]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPhotoURL = ""
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = str(metadata.id).split("|")[3]
        twitterBG = twitterBG.replace('_', '/').replace('!', '?')
        art.append(twitterBG)
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