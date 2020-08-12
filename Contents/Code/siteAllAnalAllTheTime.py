import PAsearchSites
import PAgenres
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    sceneID = None
    splited = searchTitle.split(' ')
    if unicode(splited[0], 'utf8').isdigit():
        sceneID = splited[0]
        searchTitle = searchTitle.replace(sceneID, '', 1).strip()
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + sceneID)
        searchResults = HTML.ElementFromString(req.text)
        titleNoFormatting = searchResults.xpath('//h1[@class="customhcolor"]')[0].text_content()
        curID = PAutils.Encode(PAsearchSites.getSearchSearchURL(siteNum) + sceneID)

        releaseDate = ''
        date = searchResults.xpath('//div[@class="date"]')[0].text_content().strip()
        if date:
            releaseDate = parse(date).strftime('%Y-%m-%d')

        score = 100
        
    results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s %s' % (PAsearchSites.getSearchSiteName(siteNum), titleNoFormatting, releaseDate), score=score, lang=lang))

    return results

def StringToList(string): 
    li = list(string.split(",")) 
    return li 

def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)
    art = []

    # Title
    metadata.title = detailsPageElements.xpath('//h1[@class="customhcolor"]')[0].text_content()

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="customhcolor2"]')[0].text_content().strip()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = metadata.studio
    metadata.collections.add(metadata.studio)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="date"]')[0].text_content().strip()
    date_object = parse(date)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    genrestring = detailsPageElements.xpath('//h4[@class="customhcolor"]')[0].text_content().strip()
    genres = StringToList(genrestring)
    for genre in genres:
        movieGenres.addGenre(genre)

    # Actors / possible posters
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h3[@class="customhcolor"]')
    for actor in actors:
        actorName = actor.text_content().strip()
        actorPhotoURL = ''
        art.append(actorPhotoURL)
        movieActors.addActor(actorName, actorPhotoURL)

    return metadata
