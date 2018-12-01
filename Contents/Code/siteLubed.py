import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    url = 'https://lubed.com/video/' + searchTitle.lower().replace(" ","-")
    searchResults = HTML.ElementFromURL(url)

    searchResult = searchResults.xpath('//div[@class="details col-sm-6 col-md-3 order-md-2 mb-2"]')[0]
    titleNoFormatting = searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//h1')[0].text_content()
    Log("Result Title: " + titleNoFormatting)
    cur = "/video/" + searchTitle.lower().replace(" ","-")
    curID = cur.replace('/','_')
    Log("ID: " + curID)
    releasedDate = searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//p')[0].text_content()

    girlName = searchResult.xpath('.//div[@class="row"]//div[@class="col-6 col-md-12"]//a')[0].text_content()

    Log("CurID" + str(curID))
    lowerResultTitle = str(titleNoFormatting).lower()

    titleNoFormatting = girlName + " - " + titleNoFormatting + " [Lubed, " + releasedDate +"]"
    score = 100
    results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    return results


def update(metadata, siteID, movieGenres):
    temp = str(metadata.id).split("|")[0].replace('_', '/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    Log('url :' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    metadata.studio = "Lubed"

    # Summary
    # paragraph = detailsPageElements.xpath('//p[@class="desc"]')[0].text_content()
    # paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n', '').replace('  ', '') + "\n\n"
    # metadata.summary = paragraph[:-10]
    tagline = "Lubed"
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//div[@class="details col-sm-6 col-md-3 order-md-2 mb-2"]//div[@class="row"]//div[@class="col-6 col-md-12"]//h1')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    for genreName in ['60FPS', 'Lube', 'Raw', 'Wet', 'Sex', 'Ass', 'Pussy', 'Sex', 'Cumshot']:
        movieGenres.addGenre(genreName)

    # Actors
    metadata.roles.clear()
    titleActors = ""
    actors = detailsPageElements.xpath('//div[@class="details col-sm-6 col-md-3 order-md-2 mb-2"]//div[@class="row"]//div[@class="col-6 col-md-12"]//a')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()

            actorPageURL = 'https://lubed.com' + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorName = actorPage.xpath('//div[@class="col-md-3 order-md-2 mb-2 details"]//h1')[0].text_content()
            titleActors = titleActors + actorName + " & "
            role.name = actorName
            actorPhotoURL = "https:" + actorPage.xpath('//div[@class="col-md-6 order-md-1 mb-4 image"]//a//img')[0].get("src")
            role.photo = actorPhotoURL
        titleActors = titleActors[:-3]
        metadata.title = metadata.title


    # Posters

    background = "https:" + detailsPageElements.xpath('//video[@id="player"]')[0].get('poster')
    Log("BG DL: " + background)
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata
