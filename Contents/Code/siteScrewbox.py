import PAsearchSites
import PAgenres
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//div[@class="item"]'):
        titleNoFormatting = searchResult.xpath('.//h4//a')[0].text_content().strip()
        Log("Result Title: " + titleNoFormatting)
        curID = "https:" + searchResult.xpath('.//a')[0].get('href').replace('/','_').replace('?','!')
        Log("curID: " + curID)
        actors = searchResult.xpath('.//div[@class="item-featured"]//a')
        Log("# actors: " + str(len(actors)))
        firstActor = actors[0].text_content().strip().title()
        Log("firstActor: " + firstActor)

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [Screwbox] ", score = score, lang = lang))
    return results
def update(metadata,siteID,movieGenres,movieActors):
    url = str(metadata.id).split("|")[0].replace('_','/').replace('!','?')
    detailsPageElements = HTML.ElementFromURL(url)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="item-details-right"]//h1')[0].text_content().strip().title()
    Log("Scene Title: " + metadata.title)

    # Studio/Tagline/Collection
    metadata.studio = "Screwbox"
    metadata.tagline = metadata.studio
    metadata.collections.clear()
    metadata.collections.add(metadata.studio)


    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//p[@class="shorter"]')[0].text_content().strip()
    except:
        Log('No summary found')

    # Date
    date = detailsPageElements.xpath('//ul[@class="more-info"]//li[2]')[0].text_content().replace('RELEASE DATE:','').strip()
    Log("date: " + date)
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//ul[@class="more-info"]//li[1]//a')
    Log("actors #: " + str(len(actors)))
    if len(actors) > 0:
        for actorLink in actors:
            actorName = actorLink.text_content().strip().title()
            Log("Actor: " + actorName)
            actorPageURL = "http:" + actorLink.get('href')
            actorPageElements = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPageElements.xpath('//img[contains(@class,"model_bio_thumb")]')[0].get("src0_1x")
            Log("ActorPhotoURL: " + actorPhotoURL)
            movieActors.addActor(actorName,actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//ul[@class="more-info"]//li[3]//a')
    if len(genres) > 0:
        for genreLink in genres:
            genre = genreLink.text_content().title()
            movieGenres.addGenre(genre)
        # Log("Genre: " + genre)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    try:
        background = detailsPageElements.xpath('//div[@class="fakeplayer"]//img')[0].get("src0_1x")
    except:
        background = detailsPageElements.xpath('//div[@class="fakeplayer"]//img')[0].get("src")

    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)
    Log("BG URL: " + background)


    posterURL = detailsPageElements.xpath('//div[@class="item-details-thumb"]//img')[0].get("src0_1x")
    metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}).content, sort_order = 1)





    return metadata
