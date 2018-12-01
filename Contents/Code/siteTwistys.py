import PAsearchSites
import PAgenres

def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchAll,searchSiteID):
    searchResults = HTML.ElementFromURL('https://www.twistys.com/tour/search/list/keyword/?keyword=' + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="video-ui-wrapper"]'):
        titleNoFormatting = searchResult.xpath('.//div[@class="video-ui"]//div[@class="ui-info-box"]//div[@class="info-box-inner-left"]//h2//a')[0].text_content().strip()
        Log("Result Title: " + titleNoFormatting)
        curID = searchResult.xpath('.//a')[0].get('href').replace('/','_')
        Log("ID: " + curID)
        releasedDate = searchResult.xpath('.//div[@class="video-ui"]//div[@class="ui-info-box"]//div[@class="info-box-inner-right"]//div[@class="info-box-date"]')[0].text_content()

        girlName = searchResult.xpath('.//div[@class="video-ui"]//div[@class="ui-info-box"]//div[@class="info-box-inner-left"]//div[@class="info-box-models-name"]//div//a')[0].text_content()

        Log("CurID" + str(curID))
        lowerResultTitle = str(titleNoFormatting).lower()
        
        titleNoFormatting = girlName + " - " + titleNoFormatting + " [Twistys, " + releasedDate + "]"
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting, score = score, lang = lang))
    return results


def update(metadata, siteID, movieGenres):
    temp = str(metadata.id).split("|")[0].replace('_', '/')

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    Log('url :' + url)
    detailsPageElements = HTML.ElementFromURL(url)

    metadata.studio = "Twistys"

    # Summary
    # paragraph = detailsPageElements.xpath('//p[@class="desc"]')[0].text_content()
    # paragraph = paragraph.replace('&13;', '').strip(' \t\n\r"').replace('\n', '').replace('  ', '') + "\n\n"
    # metadata.summary = paragraph[:-10]
    tagline = detailsPageElements.xpath('//h3[@class="site-name"]//a')[0].text_content()
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    metadata.title = detailsPageElements.xpath('//h1[@class="scene-name"]//span')[0].text_content()

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//div[contains(@class,"tags-date clearfix")]//ul//li//a')

    if len(genres) > 0:
        for genreLink in genres:
            genreName = genreLink.text_content().lower()
            movieGenres.addGenre(genreName)

    date = detailsPageElements.xpath('//h3[@class="date"]')
    if len(date) > 0:
        date = date[0].text_content()[:10]
        date_object = datetime.strptime(date, '%b-%d-%Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    metadata.roles.clear()
    titleActors = ""
    actors = detailsPageElements.xpath('//div[@class="left"]//h2//a')
    if len(actors) > 0:
        for actorLink in actors:
            role = metadata.roles.new()

            actorPageURL = 'https://www.twistys.com' + actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorName = actorPage.xpath('//div[@class="profile-bio-box"]//h1')[0].text_content()
            titleActors = titleActors + actorName + " & "
            role.name = actorName
            actorPhotoURL = "https:" + actorPage.xpath('//div[@class="profile-pic"]//img')[0].get("src")
            role.photo = actorPhotoURL
        titleActors = titleActors[:-3]
        metadata.title = metadata.title


    # Posters
    background = "https://i3-hw.twistyscontent.com/scenes/" + detailsPageElements.xpath('//div[@id="video-player"]')[0].get('data-release-id') + "/s1002x564.jpg"
    Log("BG DL: " + background)
    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    metadata.posters[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)

    return metadata
