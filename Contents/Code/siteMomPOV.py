import PAsearchSites
import PAgenres
import PAactors

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@id="inner_content"]/div'):
        titleNoFormatting = searchResult.xpath('.//div[@class="title_holder"]/h1/a')[0].text_content().strip()
        curID = searchResult.xpath('.//div[@class="title_holder"]/h1/a')[0].get('href').replace('/','_').replace('?','!')
        day = searchResult.xpath('.//div[@class="date_holder"]/span[2]')[0].text_content().strip()
        month = searchResult.xpath('.//div[@class="date_holder"]/span[1]')[0].text_content().replace('2019', '').replace('2018', '').replace('2017', '').replace('2016', '').replace('2015', '').replace('2014', '').replace('2013', '').strip()
        year = searchResult.xpath('.//div[@class="date_holder"]/span[1]/span')[0].text_content().strip()
        date = (month + " " + day + " " + year)
        releaseDate = (parse(date)).strftime('%Y-%m-%d')
        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [MomPOV] " + releaseDate, score = score, lang = lang))

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
    metadata.studio = 'MomPOV'

    # Title
    metadata.title = detailsPageElements.xpath('//a[@class="title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="entry_content"]/p')[0].text_content().strip()

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.addGenre("MILF")

    # Release Date
    date = detailsPageElements.xpath('//div[@class="date_holder"]')[0].text_content().strip()
    Log("Date: " + date)
    if len(date) > 0:
        date_object = datetime.strptime(date, '%b %Y %d')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors

    ### Posters and artwork ###

    # Video trailer background image
    try:
        twitterBG = detailsPageElements.xpath('//div[@id="inner_content"]/div[1]/a/img')[0].get('src')
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