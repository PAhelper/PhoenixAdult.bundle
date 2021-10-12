import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum))
    detailsPageElements = HTML.ElementFromString(req.text)
    parent = ''

    if searchData.date:
        Log('*** date search')
        parent = detailsPageElements.xpath('//tr[.//span[@class="videodate" and text()=\'Date: %s\']]' % searchData.dateFormat('%B %d, %Y'))
    elif searchData.title:
        Log('*** title search')
        m = re.search(r'([a-z0-9\&\; ]+) (masturbation|photoshoot|interview|girl-girl action|pov lapdance)', searchData.title, re.IGNORECASE)
        if m:
            parent = detailsPageElements.xpath('//tr[.//h2[@class="videomodel" and contains(text(), "%s")] and .//span[@class="videotype" and contains(text(), "%s")]]' % (m.group(1), m.group(2)))

    if parent:
        for elem in parent:
            model = re.sub(r'Models?: (.+)', r'\1', elem.xpath('.//h2[@class="videomodel"]')[0].text_content().strip())
            genre = re.sub(r'Video Type: (.+)', r'\1', elem.xpath('.//span[@class="videotype"]')[0].text_content().strip())
            releaseDate = parse(re.sub(r'Date: (.+)', r'\1', elem.xpath('.//span[@class="videodate"]')[0].text_content().strip())).strftime('%Y-%m-%d')
            sceneID = re.sub(r'graphics/videos/(.+)\.jpg', r'\1', elem.xpath('.//td[@class="videothumbnail"]/a/img/@src')[0].strip())
            results.Append(MetadataSearchResult(id='%s|%s|%s' % (sceneID, siteNum, releaseDate), name='%s %s %s [ALSAngels/%s]' % (model, genre, releaseDate, sceneID), score=100, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')

    sceneID = metadata_id[0]
    m = re.search(r'([^0-9]+)([0-9-]+)', sceneID)
    modelID = m.group(1)
    sceneNum = m.group(2)

    sceneURL = '%s/profiles/%s.html#videoupdate' % (PAsearchSites.getSearchBaseURL(siteNum), modelID)

    sceneDate = metadata_id[2]
    dateObject = parse(sceneDate)
    dateString = dateObject.strftime('%B %d, %Y')
    searchBaseUrl = PAsearchSites.getSearchBaseURL(siteNum).strip()

    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)
    parentElement = detailsPageElements.xpath('//tr[.//span[@class="videodate" and text()=\'Date: %s\']]' % dateString)[0]

    # Components
    model = re.sub(r'ALSAngels.com - (.+)', r'\1', detailsPageElements.xpath('//title')[0].text_content().strip(), flags=re.IGNORECASE)
    subject = re.sub(r'Video Type: (.+)', r'\1', parentElement.xpath('.//span[@class="videotype"]')[0].text_content().strip(), flags=re.IGNORECASE)

    # Title
    metadata.title = '%s #%d: %s' % (model, int(sceneNum), subject)

    # Summary
    metadata.summary = parentElement.xpath('.//span[@class="videodescription"]')[0].text_content().strip()

    # Studio
    metadata.studio = 'ALSAngels'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    metadata.originally_available_at = dateObject
    metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre(subject)

    # Actors
    movieActors.clearActors()
    actorPhotoURL = detailsPageElements.xpath('.//div[@id="modelbioheadshot"]/img/@src')[0].replace('..', searchBaseUrl)
    movieActors.addActor(model, actorPhotoURL)

    # Posters/Background
    art = []
    xpaths = [
        '//td[@class="videothumbnail"]//img/@src',
        '//td[@class="videothumbnail"]//a/@href',
    ]
    for xpath in xpaths:
        for img in parentElement.xpath(xpath):
            art.append(img.replace('..', searchBaseUrl))

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if (width > 1 or height > width) and width < height:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
