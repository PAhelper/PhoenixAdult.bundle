import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[4]/div/div[3]/div/div'):
        titleNoFormatting = searchResult.xpath('.//a')[0].get('title').title()
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [SinsLife] ", score = score, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    temp = str(metadata.id).split("=")[-1].replace('_','/').replace('?','!')
    url = 'https://nats.thesinslife.com/signup/signup.php?&setID=' + temp
    detailsPageElements = HTML.ElementFromURL(url)
    art = []
    metadata.collections.clear()
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Studio
    metadata.studio = 'SinsLife'

    # Title
    metadata.title = detailsPageElements.xpath('//div[4]/div/div[2]/div/div/div[2]/div[1]/div/h3')[0].text_content().strip().title()

    # Summary
    summary = detailsPageElements.xpath('//div[4]/div/div[2]/div/div/div[2]/div[2]/p')[0].text_content().strip()
#    tags_summary = detailsPageElements.xpath('//div/section[4]/div/p')[0].text_content().strip()
#    summary = all_summary.replace(tags_summary, '')
#    summary = summary.split("Show more...")[0].strip()
    metadata.summary = summary
    # Log("Summary:" + metadata.summary)
    
    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
#    genres = detailsPageElements.xpath('//div/section[4]/div/p/a')
#    if len(genres) > 0:
#        for genreLink in genres:
#            genreName = genreLink.text_content().strip().lower()
#            movieGenres.addGenre(genreName)

    # Release Date
    date = detailsPageElements.xpath('//div[4]/div/div[2]/div/div/div[2]/div[1]/div/div[1]')[0].text_content().strip("Release Date:")
    Log("Date:" + date)
    if len(date) > 0:
        date_object = datetime.strptime(date, '%B %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    actors = detailsPageElements.xpath('//div[4]/div/div[2]/div/div/div[2]/div[3]/ul/li/a/..')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            #actorPageURL = actorLink.get("src")
    # can't get this to work, below is temp fix
            if len(actors) == 1:
                actorPageURL = detailsPageElements.xpath('//div[4]/div/div[2]/div/div/div[2]/div[3]/ul/li/a/img[@class="category_model_thumb stdimage thumbs target"]')[0].get("src")
                actorPageURL = 'https:' + actorPageURL
                actorPhotoURL = actorPageURL
            if len(actors) > 1:
                actorPhotoURL = ''
            movieActors.addActor(actorName,actorPhotoURL)

    # Director

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//div[4]/div/div[2]/div/div/div[1]/div[2]/div/div[1]/img')[0].get('src')
        twitterBG = 'https:' + twitterBG
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