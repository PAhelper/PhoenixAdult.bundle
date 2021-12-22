import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    searchJAVID = None
    splitSearchTitle = searchData.title.split()
    if len(splitSearchTitle) > 1:
        if unicode(splitSearchTitle[1], 'UTF-8').isdigit():
            searchJAVID = '%s%%2B%s' % (splitSearchTitle[0], splitSearchTitle[1])

    if searchJAVID:
        searchData.encoded = searchJAVID

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//li[contains(@class, "item-list")]'):
        titleNoFormatting = searchResult.xpath('.//dt')[0].text_content().strip()
        JAVID = searchResult.xpath('.//img/@alt')[0]

        sceneURL = searchResult.xpath('.//a/@href')[0].rsplit('/', 1)[0]
        curID = PAutils.Encode(sceneURL)

        if searchJAVID:
            score = 100 - Util.LevenshteinDistance(searchJAVID.lower(), JAVID.lower())
        else:
            score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='[%s] %s' % (JAVID, titleNoFormatting), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    scene_id = sceneURL.split('id=')[1]
    dataURL = PAsearchSites.getSearchBaseURL(siteNum) + '/api/v4f/contents/' + scene_id
    dataReq = PAutils.HTTPRequest(dataURL)
    dataElements = json.loads(dataReq.text)['data']

    javID = dataElements['dvd_id']

    # Title
    JavTitle = dataElements['title']

    # Undoing the Self Censoring R18.com does to their tags and titles
    if '**' in JavTitle:
        JavTitle = JavTitle.replace('R**e', 'Rape')
        JavTitle = JavTitle.replace('S********l', 'Schoolgirl')
        JavTitle = JavTitle.replace('S***e', 'Slave')
        JavTitle = JavTitle.replace('M****t', 'Molest')
        JavTitle = JavTitle.replace('F***e', 'Force')
        JavTitle = JavTitle.replace('G*******g', 'Gang Bang')
        JavTitle = JavTitle.replace('G******g', 'Gangbang')
        JavTitle = JavTitle.replace('K*d', 'Descendant')
        JavTitle = JavTitle.replace('C***d', 'Descendant')
        JavTitle = JavTitle.replace('T*****e', 'Torture')
        JavTitle = JavTitle.replace('T******e', 'Tentacle')
        JavTitle = JavTitle.replace('D**g', 'Drug')
        JavTitle = JavTitle.replace('P****h', 'Punish')
        JavTitle = JavTitle.replace('S*****t', 'Student')
        JavTitle = JavTitle.replace('V*****e', 'Violate')
        JavTitle = JavTitle.replace('V*****t', 'Violent')
        JavTitle = JavTitle.replace('B***d', 'Blood')
        JavTitle = JavTitle.replace('M************n', 'Mother and Son')

    metadata.title = javID + ' ' + JavTitle

    # Summary
    try:
        metadata.summary = detailsPageElements.xpath('//meta[@name="description"]/@content"]')[0].text_content()
    except:
        pass

    # Studio
    metadata.studio = dataElements['maker']['name']

    # Director
    director = metadata.directors.new()
    directorName = dataElements['director']
    if directorName != '----':
        director.name = directorName

    # Release Date
    date = dataElements['release_date']
    date_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    if dataElements['actresses']:
        for actorLink in dataElements['actresses']:
            fullActorName = actorLink['name']
            if fullActorName != '----':
                splitActorName = fullActorName.split('(')
                mainName = splitActorName[0].strip()

                actorPhotoURL = actorLink['image_url']

                if len(splitActorName) > 1 and mainName == splitActorName[1][:-1]:
                    actorName = mainName
                else:
                    actorName = fullActorName

                movieActors.addActor(actorName, actorPhotoURL)

    else:
        alternateSceneUrl = 'https://www.javlibrary.com/en/vl_searchbyid.php?keyword=' + scene_id
        alternateSceneReq = PAutils.HTTPRequest(alternateSceneUrl)
        alternateDetailsPageElements = HTML.ElementFromString(alternateSceneReq.text)

        if alternateDetailsPageElements.xpath('.//span[@class="cast"]/span/a'):
            for actress in alternateDetailsPageElements.xpath('.//span[@class="cast"]/span/a'):
                actorName = actress.text_content().strip()

                movieActors.addActor(actorName, '')
        else:
            if javID.startswith('3DSVR'):
                javID = javID.replace('3DSVR', 'DSVR')
                
            alternateSceneUrl = 'https://www.javlibrary.com/en/vl_searchbyid.php?keyword=' + javID

            alternateSceneReq = PAutils.HTTPRequest(alternateSceneUrl)
            alternateDetailsPageElements = HTML.ElementFromString(alternateSceneReq.text)
            if alternateDetailsPageElements.xpath('.//span[@class="cast"]/span/a'):
                for actress in alternateDetailsPageElements.xpath('.//span[@class="cast"]/span/a'):
                    actorName = actress.text_content().strip()

                    movieActors.addActor(actorName, '')

    # Genres
    movieGenres.clearGenres()

    for genreLink in dataElements['categories']:
        genreName = genreLink['name']

        if '**' in genreName:
            genreName = genreName.replace('r**e', 'rape')
            genreName = genreName.replace('s********l', 'schoolgirl')
            genreName = genreName.replace('s***e', 'slave')
            genreName = genreName.replace('m****ter', 'molester')
            genreName = genreName.replace('g*******g', 'gang bang')
            genreName = genreName.replace('g******g', 'gangbang')
            genreName = genreName.replace('k*d', 'descendant')
            genreName = genreName.replace('c***d', 'descendant')
            genreName = genreName.replace('f***e', 'force')
            genreName = genreName.replace('t*****e', 'torture')
            genreName = genreName.replace('t******e', 'tentacle')
            genreName = genreName.replace('d**g', 'drug')
            genreName = genreName.replace('p****h', 'punish')
            genreName = genreName.replace('s*****t', 'student')
            genreName = genreName.replace('v*****e', 'violate')
            genreName = genreName.replace('v*****t', 'violent')
            genreName = genreName.replace('b***d', 'blood')

        movieGenres.addGenre(genreName)

    metadata.collections.add('Japan Adult Video')

    # Posters
    art = []
    for photo in dataElements['gallery']:
        photoURL = photo['large']

        art.append(photoURL)

    for poster in dataElements['images']:
        poster_idx = poster.index('jacket_image')
        if poster_idx:
            posterURL = poster[poster_idx]['large']

            art.append(posterURL)

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
