import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="category_listing_wrapper_updates"]'):
        titleNoFormatting = searchResult.xpath('.//h3')[0].text_content().strip()
        if titleNoFormatting[-3:] == " 4k":
            titleNoFormatting = titleNoFormatting[:-3].strip()
        curID = searchResult.xpath('.//a[@class="ampLink"]')[0].get('href').replace('/','_').replace('?','!')
        try:
            releaseDate = parse(searchResult.xpath('.//div[@class="date-label"]')[0].text_content()[22:].strip()).strftime('%Y-%m-%d')
        except:
            releaseDate = ''
        if searchDate and releaseDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Spizoo] " + releaseDate, score = score, lang = lang))
    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    url = str(metadata.id).split("|")[0].replace('_', '/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = "Spizoo"

    # Title
    title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    if title[-3:] == " 4k":
        title = title[:-3].strip()
    metadata.title = title

    # Summary
    paragraph = detailsPageElements.xpath('//p[@class="description"] | //p[@class="description-scene"]')[0].text_content().strip()
    metadata.summary = paragraph

    #Tagline and Collection(s)
    try:
        tagline = detailsPageElements.xpath('//i[@id="site"]')[0].get('value').strip()
    except:
        if 'rawattack' in url:
            tagline = "RawAttack"
        else:
            tagline = "Spizoo"
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    genres = detailsPageElements.xpath('//div[@id="trailer-data"]//div[@class="col-12 col-md-6"]//div[@class="row"]//div[@class="col-12"]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().lower().strip()
            movieGenres.addGenre(genreName)
    else: #Manual genres for Rawattack
        if siteID == 577:
            movieGenres.addGenre('Unscripted')
            movieGenres.addGenre('Raw')
            movieGenres.addGenre('Hardcore')

    # Release Date
    date = detailsPageElements.xpath('//p[@class="date"]')
    if len(date) > 0:
        date = date[0].text_content()[:10]
        date_object = datetime.strptime(date, '%Y-%m-%d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[@class="row line"]/div[@class="col-3"][1]/a | //p[@class="featuring"]/a')
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().replace('.','').strip()
            actorPageURL = PAsearchSites.getSearchBaseURL(siteID) + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            try:
                try:
                    actorPhotoURL = actorPage.xpath('//div[@class="model-bio-pic"]/img')[0].get("src")
                    if 'http' not in actorPhotoURL:
                        actorPhotoURL = actorPhotoURL + PAsearchSites.getSearchBaseURL(siteID)
                except:
                    actorPhotoURL = actorPage.xpath('//div[@class="model-bio-pic"]/img')[0].get("src0_1x")
                    if 'http' not in actorPhotoURL:
                        actorPhotoURL = actorPhotoURL + PAsearchSites.getSearchBaseURL(siteID)
            except:
                actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//img[contains(@class,"update_thumb thumbs")]')[0].get('src')
        if 'http' not in twitterBG:
            twitterBG = PAsearchSites.getSearchBaseURL(siteID) + "/" + twitterBG
        Log("Background: " + twitterBG)
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
