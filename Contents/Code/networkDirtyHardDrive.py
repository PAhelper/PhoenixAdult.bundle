import PAsearchSites
import PAgenres
import PAactors
import PAutils

def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    url = PAsearchSites.getSearchSearchURL(siteNum)
    req = PAutils.HTTPRequest(url)
    sitemapElements = HTML.ElementFromString(req.text)

    sceneResults = sitemapElements.xpath('//loc[contains(text(), "/tour1/")][contains(text(), ".html")]')
    Log('Found ' + str(len(sceneResults)) + ' results.')

    for result in sceneResults:
        filename = os.path.splitext(os.path.basename(result.text_content()))[0]
        
        title = filename.replace('_', ' ').title()

        curID = PAutils.Encode(filename)

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), title.lower())

        if score > 80:
            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s]' % (title, 'Dirty Hard Drive'), score=score, lang=lang))

    return results

def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = 'http://bangmyhand.com/tour1/' + PAutils.Decode(metadata_id[0]) + '.html'

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    m = re.search("'playlistfile': '(.+playlist\.xml)'", req.text)
    playListUrl = ''
    tagline = ''
    if m:
        playListUrl = m.group(1)
        Log('Playlist file found.')

        if '/dhd_' in playListUrl:
            tagline = 'Dirty Sluts and Studs'
        elif '/bmh_' in playListUrl:
            tagline = 'Bang My Hand'
        elif '/kk_' in playListUrl:
            tagline = 'Katie Kox'
        elif '/lb_' in playListUrl:
            tagline = 'Lee Bang XXX'
        elif '/sdaf_' in playListUrl:
            tagline = 'Sophie Dee and Friends'
        elif '/kkng_' in playListUrl:
            tagline = 'Kiera King'
        elif '/gin_' in playListUrl:
            tagline = 'Girls in Nylon'

        xmlPlaylistElements = XML.ElementFromURL(playListUrl)
        poster = xmlPlaylistElements.xpath('//channel/item/*[name()="media:group"]/*[name()="media:thumbnail"]')[0].get('url')
    else:
        Log('Playlist file NOT found.')
        m = re.search("'image': '(.+bookend\.jpg)'", req.text)
        if m:
            poster = m.group(1)
    
    if 'The Squirt Instructor' in req.text:
        tagline = 'The Squirt Instructor'

    if tagline == '': # Default
        tagline = 'Dirty Sluts and Studs'
    
    # Title
    metadata.title = detailsPageElements.xpath('//h1')[0].text_content().strip()
    
    # Summary
    metadata.summary = detailsPageElements.xpath('.//div[@id="video-page-desc"]')[0].text_content()
    
    metadata.studio = 'Dirty Hard Drive'

    # Tagline and Collection(s)
    metadata.collections.clear()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//a[starts-with(@href, "pornstar_")]'):
        actorName = actorLink.get('href')[9:-5].replace('_', ' ').title()

        actorPageURL = actorLink.get('href')
        req = PAutils.HTTPRequest('http://bangmyhand.com/tour1/' + actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        actorPhotoURL = actorPage.xpath('//div[@id="global-model-img"]//img/@src')[0]

        movieActors.addActor(actorName, actorPhotoURL)
    
    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    
    posters = []
    posters.append(poster)

    posterNum = 1
    for posterUrl in posters:
        metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl).content, sort_order = posterNum)
        posterNum = posterNum + 1

    return metadata