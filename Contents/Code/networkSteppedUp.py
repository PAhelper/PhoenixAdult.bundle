import PAsearchSites
import PAgenres
import PAactors


def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchDate):
    searchString = searchTitle.replace(" ", "-").replace(",", "").replace("’","").replace("'","").replace("--","-").lower()
    if "/" not in searchString:
        searchString = searchString.replace("-", "/", 1)

    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + searchString
    detailsPageElements = HTML.ElementFromURL(sceneURL)

    curID = String.Encode(sceneURL)
    titleNoFormatting = detailsPageElements.xpath('//h1[@class="title"] | //h2[@class="title"]')[0].text_content().strip()

    date = detailsPageElements.xpath('//span[contains(@class,"date")] | //span[contains(@class,"hide")]')
    if date:
        releaseDate = parse(date[0].text_content().strip()).strftime('%Y-%m-%d')
    else:
        releaseDate = parse(searchDate).strftime('%Y-%m-%d') if searchDate else ''
    displayDate = releaseDate if date else ''

    if searchDate and displayDate:
        score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
    else:
        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

    results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')

    metadata_id = str(metadata.id).split('|')
    sceneURL = String.Decode(metadata_id[0])
    sceneDate = metadata_id[1]
    detailsPageElements = HTML.ElementFromURL(sceneURL)

    # Studio
    metadata.studio = 'Stepped Up Media'

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="title"] | //h2[@class="title"]')[0].text_content().strip()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[contains(@class,"desc")]')[0].text_content().strip()

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    if tagline == "Swallowed":
        movieGenres.addGenre('blowjob')
        movieGenres.addGenre('cum swallow')
    elif tagline == "TrueAnal" or "AllAnal":
        movieGenres.addGenre('anal')
        movieGenres.addGenre('gaping')
    elif tagline == "Nympho":
        movieGenres.addGenre('nympho')
    movieGenres.addGenre('hardcore')
    movieGenres.addGenre('heterosexual')

    # Release Date
    if sceneDate:
        date_object = parse(sceneDate)
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('(//h4[@class="models"])[1]//a')
    for actorLink in actors:
        actorName = str(actorLink.text_content().strip())

        actorPageURL = actorLink.get("href")
        actorPage = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPage.xpath('//div[contains(@class,"model")]/img')[0].get("src")

        movieActors.addActor(actorName, actorPhotoURL)
    movieActors.addActor('Mike Adriano', 'https://imgs1cdn.adultempire.com/actors/470003.jpg')

    # Posters
    art = []

    try:
        art.append(detailsPageElements.xpath('//div[@id="trailer-player"]')[0].get('data-screencap'))
    except:
        art.append(detailsPageElements.xpath('//video[@id="ypp-player"]')[0].get('poster'))

    for poster in actorPage.xpath('//a[@href="' + sceneURL + '"]//img'):
        art.append(poster.get('src'))
    for poster in actorPage.xpath('//div[@class="thumb-mouseover"] | //div[@class="thumb-bottom"] | //div[@class="thumb-top"]'):
        theStyle = poster.get('style')
        alpha = theStyle.find('http')
        omega = theStyle.find(');',alpha)
        art.append(theStyle[alpha:omega].strip())

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            #Download image file for analysis
            try:
                img_file = urllib.urlopen(posterUrl)
                im = StringIO(img_file.read())
                resized_image = Image.open(im)
                width, height = resized_image.size
                #Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order=idx)
            except:
                pass

    return metadata
