import PAsearchSites
import PAgenres
import json


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//a[contains(@class,"movies")]'):
        Log("****SEARCH")
        titleNoFormatting = searchResult.xpath('.//img')[0].get('alt').strip()
        curID = searchResult.get('href').replace('/','_').replace('?','!')

        try:
            detailsPageElements = HTML.ElementFromURL(PAsearchSites.getSearchBaseURL(siteNum) + searchResult.get('href'))
            releaseDate = parse(detailsPageElements.xpath('//div[@class="col-xs-12 col-md-6 with-margin"]/div[@class="entries"]/div[@class="entries"]')[0].text_content().strip().replace("Production year:", ""))
        except:
            releaseDate = ''
            
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " ("+releaseDate.strftime('%Y')+") ["+PAsearchSites.getSearchSiteName(siteNum)+"]", score = score, lang = lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    temp = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    url = (PAsearchSites.getSearchBaseURL(siteID) + temp).replace("https:","http:")
    detailsPageElements = HTML.ElementFromURL(url)
    art = []

    # Summary
    try:
        paragraph = detailsPageElements.xpath('//meta[@name="twitter:description"]')[0].get("content").strip()
    except:
        try:
            paragraph = detailsPageElements.xpath('//div[@id="summaryList"]')[0].text_content().strip()
        except:
            paragraph = ''
    metadata.summary = paragraph.replace('</br>','\n').replace('<br>','\n').strip()

    # Tagline
    metadata.collections.clear()
    try:
        taglineFirst = detailsPageElements.xpath('//div[@class="col-xs-12 col-md-6 with-margin"]//div[@class="entries"]/div')
        tagline = tagline[0].xpath('//a')[0].text_content().strip()
        metadata.collections.add('Dorcel Vision')
    except:
        tagline = 'Dorcel Vision'
    metadata.tagline = tagline
    metadata.studio = tagline
    metadata.collections.add(tagline)

    # Title
    try:
        title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    except:
        title = "I couldn't find the title, please report this on github: https://github.com/PAhelper/PhoenixAdult.bundle/issues"
    metadata.title = title

    # Director
    metadata.directors.clear()

    # Genres
    movieGenres.clearGenres()

    # Release Date
    try:
        date = parse(detailsPageElements.xpath('//div[@class="col-xs-12 col-md-6 with-margin"]/div[@class="entries"]/div[@class="entries"]')[0].text_content().strip().replace("Production year:", ""))
   
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year
    except:
        date = ''

    # Actors
    movieActors.clearActors()

    Log("Initial try for actors")
    actorsBox = detailsPageElements.xpath('//div[@class="col-xs-12 casting"]')[0].xpath('//div[contains(@class,"slider-xl")]')[0]
    actors = actorsBox.xpath('//div[@class="col-xs-2"]/a[@class="link oneline"]')
    Log("actors found: " + str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = str(actorLink.text_content().strip())
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL((PAsearchSites.getSearchBaseURL(siteID)+actorPageURL).replace("https:","http:"))
            actorBoxA = actorPage.xpath('//div[@class="slider-part screenshots"]')[0]
            actorBoxB = actorBoxA.xpath('//div[contains(@class,"slider-xl")]/div[@class="slides"]/a')[0]
            actorPhoto = actorBoxB.get("href").strip()
            actorPhotoURL = (PAsearchSites.getSearchBaseURL(siteID)+actorPhoto).replace("https:","http:")
            movieActors.addActor(actorName,actorPhotoURL)
    else:
        Log("No actor found")
        pass

    #DVD Cover
    try:
        poster = detailsPageElements.xpath('//div[contains(@class,"covers")]/a[contains(@class,"cover")]')[0].get('href').strip()
        coverURL = (PAsearchSites.getSearchBaseURL(siteID)+poster).replace("https:","http:")
        art.append(coverURL)
    except:
        Log("No cover found")
        coverURL = ''
        pass

    # Screen
    try:
        photoBoxA = detailsPageElements.xpath('//div[@class="slider-part screenshots"]')[0]
        photoBoxB = photoBoxA.xpath('//div[contains(@class,"slider-xl")]/div[@class="slides"]/div[@class="col-xs-2"]/a')
        Log("Screen: " + str(len(photoBoxB)))
        
        for photo in photoBoxB:
            photoURL = (PAsearchSites.getSearchBaseURL(siteID)+photo.get("href").strip()).replace("https:","http:").replace("blur9/","/")
            art.append(photoURL)
    except:
        pass


    j = 1
    for posterUrl in art:
        if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if(width > 1):
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': coverURL}).content, sort_order = j)
                if(width > 100):
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': coverURL}).content, sort_order = j)
                j = j + 1
            except Exception as e:
                Log("Error: " + str(e))

    return metadata
