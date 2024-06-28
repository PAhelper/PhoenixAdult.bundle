import PAutils
import PAdatabaseActors
import PAsearchSites


class PhoenixActors:
    actorsTable = []
    directorsTable = []
    producersTable = []

    def addActor(self, newActor, newPhoto):
        newActor = newActor.encode('UTF-8') if isinstance(newActor, unicode) else newActor
        newPhoto = newPhoto.encode('UTF-8') if isinstance(newPhoto, unicode) else newPhoto

        if newActor not in [actorLink['name'] for actorLink in self.actorsTable]:
            self.actorsTable.append({
                'name': newActor,
                'photo': newPhoto,
            })

    def addDirector(self, newDirector, newPhoto):
        newDirector = newDirector.encode('UTF-8') if isinstance(newDirector, unicode) else newDirector
        newPhoto = newPhoto.encode('UTF-8') if isinstance(newPhoto, unicode) else newPhoto

        if newDirector not in [directorLink['name'] for directorLink in self.directorsTable]:
            self.directorsTable.append({
                'name': newDirector,
                'photo': newPhoto,
            })

    def addProducer(self, newProducer, newPhoto):
        newProducer = newProducer.encode('UTF-8') if isinstance(newProducer, unicode) else newProducer
        newPhoto = newPhoto.encode('UTF-8') if isinstance(newPhoto, unicode) else newPhoto

        if newProducer not in [producerLink['name'] for producerLink in self.producersTable]:
            self.producersTable.append({
                'name': newProducer,
                'photo': newPhoto,
            })

    def clearActors(self):
        self.actorsTable = []

    def clearDirectors(self):
        self.directorsTable = []

    def clearProducers(self):
        self.producersTable = []

    def processActors(self, metadata, siteNum):
        for actorLink in self.actorsTable:
            skip = False
            # Save the potential new Actor or Actress to a new variable, replace &nbsp; with a true space, and strip off any surrounding whitespace
            actorName = PAutils.parseTitle(actorLink['name'].replace('\xc2\xa0', ' ').replace(',', '').strip().lower(), 0)
            actorPhoto = actorLink['photo'].strip()

            actorName = ' '.join(actorName.split())

            # Skip an actor completely; this could be used to filter out male actors if desired
            if not actorName:
                skip = True
            elif actorName == 'Bad Name':
                skip = True
            elif actorName == 'Test Model Name':
                skip = True

            if not skip:
                searchStudioIndex = None
                for studioIndex, studioList in PAdatabaseActors.ActorsStudioIndexes.items():
                    if not siteNum == 684 and metadata.studio.lower() in map(str.lower, studioList) or PAsearchSites.getSearchSiteName(siteNum).lower() in map(str.lower, studioList):
                        searchStudioIndex = studioIndex
                        break

                searchActorName = actorName.lower()
                if searchStudioIndex is not None and searchStudioIndex in PAdatabaseActors.ActorsReplaceStudios:
                    for newActorName, aliases in PAdatabaseActors.ActorsReplaceStudios[searchStudioIndex].items():
                        if searchActorName == newActorName.lower() or searchActorName in map(str.lower, aliases):
                            actorName = newActorName

                            if searchStudioIndex == 32 and actorName != 'QueenSnake':
                                actorName = '%s QueenSnake' % actorName

                            break

                for newActorName, aliases in PAdatabaseActors.ActorsReplace.items():
                    if searchActorName == newActorName.lower() or searchActorName in map(str.lower, aliases):
                        actorName = newActorName
                        break

                if ',' in actorName:
                    for newActor in actorName.split(','):
                        actorName = newActor.strip()
                        displayActorName = actorName.replace('\xc2\xa0', '').strip()

                        (actorPhoto, gender) = actorDBfinder(displayActorName, metadata)
                        Log('Actor: %s %s' % (displayActorName, actorPhoto))
                        Log('Gender: %s' % gender)
                        if Prefs['gender_enable']:
                            if gender == 'male':
                                continue

                        role = metadata.roles.new()
                        role.name = actorName
                        role.photo = actorPhoto
                else:
                    displayActorName = actorName.replace('\xc2\xa0', '').strip()
                    req = None
                    if actorPhoto:
                        req = PAutils.HTTPRequest(actorPhoto, 'HEAD', bypass=False)

                    if not req or not req.ok:
                        (actorPhoto, gender) = actorDBfinder(displayActorName, metadata)
                        Log('Gender: %s' % gender)
                        if Prefs['gender_enable']:
                            if gender == 'male':
                                continue
                    elif Prefs['gender_enable']:
                        gender = genderCheck(actorName)
                        Log('Gender: %s' % gender)
                        if gender == 'male':
                            continue

                    if actorPhoto:
                        actorPhoto = PAutils.getClearURL(actorPhoto)

                    Log('Actor: %s %s' % (displayActorName, actorPhoto))
                    role = metadata.roles.new()
                    role.name = actorName
                    role.photo = actorPhoto

    def processDirectors(self, metadata, siteNum):
        for directorLink in self.directorsTable:
            skip = False
            # Save the potential new Director to a new variable, replace &nbsp; with a true space, and strip off any surrounding whitespace
            directorName = PAutils.parseTitle(directorLink['name'].replace('\xc2\xa0', ' ').replace(',', '').strip().lower(), 0)
            directorPhoto = directorLink['photo'].strip()

            directorName = ' '.join(directorName.split())

            # Skip an Director completely
            if not directorName:
                skip = True
            elif directorName == 'Bad Name':
                skip = True
            elif directorName == 'Test Model Name':
                skip = True

            if not skip:
                searchStudioIndex = None
                for studioIndex, studioList in PAdatabaseActors.ActorsStudioIndexes.items():
                    if not siteNum == 684 and metadata.studio.lower() in map(str.lower, studioList) or PAsearchSites.getSearchSiteName(siteNum).lower() in map(str.lower, studioList):
                        searchStudioIndex = studioIndex
                        break

                searchDirectorName = directorName.lower()
                if searchStudioIndex is not None and searchStudioIndex in PAdatabaseActors.ActorsReplaceStudios:
                    for newDirectorName, aliases in PAdatabaseActors.ActorsReplaceStudios[searchStudioIndex].items():
                        if searchDirectorName == newDirectorName.lower() or searchDirectorName in map(str.lower, aliases):
                            directorName = newDirectorName

                            if searchStudioIndex == 32 and directorName != 'QueenSnake':
                                directorName = '%s QueenSnake' % directorName

                            break

                for newDirectorName, aliases in PAdatabaseActors.ActorsReplace.items():
                    if searchDirectorName == newDirectorName.lower() or searchDirectorName in map(str.lower, aliases):
                        directorName = newDirectorName
                        break

                if ',' in directorName:
                    for newDirector in directorName.split(','):
                        directorName = newDirector.strip()
                        displayDirectorName = directorName.replace('\xc2\xa0', '').strip()

                        (directorPhoto, gender) = actorDBfinder(displayDirectorName, metadata)

                        Log('Director: %s %s' % (displayDirectorName, directorPhoto))
                        director = metadata.directors.new()
                        director.name = directorName
                        director.photo = directorPhoto
                else:
                    displayDirectorName = directorName.replace('\xc2\xa0', '').strip()
                    req = None
                    if directorPhoto:
                        req = PAutils.HTTPRequest(directorPhoto, 'HEAD', bypass=False)

                    if not req or not req.ok:
                        (directorPhoto, gender) = actorDBfinder(displayDirectorName, metadata)

                    if directorPhoto:
                        directorPhoto = PAutils.getClearURL(directorPhoto)

                    Log('Director: %s %s' % (displayDirectorName, directorPhoto))
                    director = metadata.directors.new()
                    director.name = directorName
                    director.photo = directorPhoto

    def processProducers(self, metadata, siteNum):
        for producerLink in self.producersTable:
            skip = False
            # Save the potential new producer to a new variable, replace &nbsp; with a true space, and strip off any surrounding whitespace
            producerName = PAutils.parseTitle(producerLink['name'].replace('\xc2\xa0', ' ').replace(',', '').strip().lower(), 0)
            producerPhoto = producerLink['photo'].strip()

            producerName = ' '.join(producerName.split())

            # Skip an producer completely
            if not producerName:
                skip = True
            elif producerName == 'Bad Name':
                skip = True
            elif producerName == 'Test Model Name':
                skip = True

            if not skip:
                searchStudioIndex = None
                for studioIndex, studioList in PAdatabaseActors.ActorsStudioIndexes.items():
                    if not siteNum == 684 and metadata.studio.lower() in map(str.lower, studioList) or PAsearchSites.getSearchSiteName(siteNum).lower() in map(str.lower, studioList):
                        searchStudioIndex = studioIndex
                        break

                searchProducerName = producerName.lower()
                if searchStudioIndex is not None and searchStudioIndex in PAdatabaseActors.ActorsReplaceStudios:
                    for newProducerName, aliases in PAdatabaseActors.ActorsReplaceStudios[searchStudioIndex].items():
                        if searchProducerName == newProducerName.lower() or searchProducerName in map(str.lower, aliases):
                            producerName = newProducerName

                            if searchStudioIndex == 32 and producerName != 'QueenSnake':
                                producerName = '%s QueenSnake' % producerName

                            break

                for newProducerName, aliases in PAdatabaseActors.ActorsReplace.items():
                    if searchProducerName == newProducerName.lower() or searchProducerName in map(str.lower, aliases):
                        producerName = newProducerName
                        break

                if ',' in producerName:
                    for newProducer in producerName.split(','):
                        producerName = newProducer.strip()
                        displayProducerName = producerName.replace('\xc2\xa0', '').strip()

                        (producerPhoto, gender) = actorDBfinder(displayProducerName, metadata)
                        Log('Producer: %s %s' % (displayProducerName, producerPhoto))

                        producer = metadata.producers.new()
                        producer.name = producerName
                        producer.photo = producerPhoto
                else:
                    displayProducerName = producerName.replace('\xc2\xa0', '').strip()
                    req = None
                    if producerPhoto:
                        req = PAutils.HTTPRequest(producerPhoto, 'HEAD', bypass=False)

                    if not req or not req.ok:
                        (producerPhoto, gender) = actorDBfinder(displayProducerName, metadata)

                    if producerPhoto:
                        producerPhoto = PAutils.getClearURL(producerPhoto)

                    Log('Producer: %s %s' % (displayProducerName, producerPhoto))
                    producer = metadata.producers.new()
                    producer.name = producerName
                    producer.photo = producerPhoto


def actorDBfinder(actorName, metadata):
    actorEncoded = urllib.quote(re.sub(r'(?<=\w)\.\s(?=\w\.)', '', actorName).replace('.', ''))

    actorPhotoURL = ''
    databaseName = ''

    searchResults = {
        'Freeones': getFromFreeones,
        'IAFD': getFromIAFD,
        'Indexxx': getFromIndexxx,
        'AdultDVDEmpire': getFromAdultDVDEmpire,
        'Boobpedia': getFromBoobpedia,
        'Babes and Stars': getFromBabesandStars,
        'Babepedia': getFromBabepedia,
        'JAVBus': getFromJavBus,
        'JAVDatabase': getFromJAVDatabase,
        'Local Storage': getFromLocalStorage,
    }

    searchOrder = ['Local Storage', 'Freeones', 'IAFD', 'Indexxx', 'AdultDVDEmpire', 'Boobpedia', 'Babes and Stars', 'Babepedia', 'JAVBus', 'JAVDatabase']
    if Prefs['order_enable']:
        searchOrder = [sourceName.strip() for sourceName in Prefs['order_list'].split(',') if sourceName.strip() in searchResults]

    for sourceName in searchOrder:
        task = searchResults[sourceName]

        url = None
        try:
            (url, gender) = task(actorName, actorEncoded, metadata)
        except Exception as e:
            Log.Error(format_exc())

        if url:
            databaseName = sourceName
            actorPhotoURL = url
            break

    if actorPhotoURL:
        Log('%s found in %s ' % (actorName, databaseName))
        Log('PhotoURL: %s' % actorPhotoURL)
    elif Prefs['gender_enable']:
        gender = genderCheck(actorName)
        Log('%s image not found' % actorName)
    else:
        Log('%s not found' % actorName)

    return actorPhotoURL, gender


def genderCheck(actorName):
    actorEncoded = urllib.quote(re.sub(r'(?<=\w)\.\s(?=\w\.)', '', actorName).replace('.', ''))
    period_corrections = {
        (r'^dr%20', 'Dr%2E%20'), (r'%20st%20', '%20St.%20'), (r'^j%20', 'J%2E%20')
    }

    for value in period_corrections:
        actorEncoded = re.sub(value[0], value[1], actorEncoded, flags=re.IGNORECASE)

    gender = ''

    url = 'http://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=' + actorEncoded
    req = PAutils.HTTPRequest(url)

    actorSearch = HTML.ElementFromString(req.text)
    actorResults = actorSearch.xpath('//table[@id="tblFem" or @id="tblMal"]//tbody//td[2]//a')
    actorAlias = actorSearch.xpath('//table[@id="tblFem" or @id="tblMal"]//tbody//td[@class="text-left"]')
    maleActorURLs = actorSearch.xpath('//table[@id="tblMal"]//tbody//td[2]//a/@href')

    if actorResults:
        score = Util.LevenshteinDistance(actorName.lower(), actorResults[0].text_content().strip().lower()) + 1

        results = []
        for idx, actor in enumerate(actorResults, 0):
            resultScore = Util.LevenshteinDistance(actorName.lower(), actor.text_content().strip().lower())

            if resultScore != 0:
                if actorName.lower() in actorAlias[idx].text_content().lower():
                    resultScore = resultScore - 1

            if resultScore == score:
                results.append(actor)
            elif resultScore < score:
                score = resultScore
                results = [actor]

        if results:
            actor = random.choice(results)
            actorPageURL = actor.xpath('./@href')[0]

        gender = 'male' if actorPageURL in maleActorURLs else 'female'

    return gender


def getFromFreeones(actorName, actorEncoded, metadata):
    actorPhotoURL = ''

    req = PAutils.HTTPRequest('https://www.freeones.com/babes?q=' + actorEncoded)
    actorSearch = HTML.ElementFromString(req.text)
    actorPageURL = actorSearch.xpath('//div[contains(@class, "grid-item")]//a/@href')
    if actorPageURL:
        actorPageURL = actorPageURL[0].replace('/feed', '/bio', 1)
        actorPageURL = 'https://www.freeones.com' + actorPageURL
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)

        DBactorName = actorPage.xpath('//h1')[0].text_content().lower().replace(' bio', '').strip()
        aliases = actorPage.xpath('//p[contains(., "Aliases")]/following-sibling::div/p')
        if aliases:
            aliases = aliases[0].text_content().strip()
            if aliases:
                aliases = [alias.strip().lower() for alias in aliases.split(',')]
            else:
                aliases = []

        aliases.append(DBactorName)

        img = actorPage.xpath('//div[contains(@class, "image-container")]//a/img/@src')

        is_true = False
        professions = actorPage.xpath('//p[contains(., "Profession")]/following-sibling::div/p')
        if professions:
            professions = professions[0].text_content().strip()

            for profession in professions.split(','):
                profession = profession.strip()
                if profession in ['Porn Stars', 'Adult Models']:
                    is_true = True
                    break

        if img and actorName.lower() in aliases and is_true:
            actorPhotoURL = img[0]

    return actorPhotoURL, 'female'


def getFromIndexxx(actorName, actorEncoded, metadata):
    actorPhotoURL = ''

    req = PAutils.HTTPRequest('https://www.indexxx.com/search/?query=' + actorEncoded)
    actorSearch = HTML.ElementFromString(req.text)
    actorPageURL = actorSearch.xpath('//div[contains(@class, "modelPanel")]//a[@class="modelLink3"]/@href')
    if actorPageURL:
        actorPageURL = actorPageURL[0]
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        img = actorPage.xpath('//img[@class="model-img"]/@src')
        if img:
            actorPhotoURL = img[0]
            actorPhotoURL = cacheActorPhoto(actorPhotoURL, actorName, headers={'Referer': actorPageURL})

    return actorPhotoURL, 'female'


def getFromAdultDVDEmpire(actorName, actorEncoded, metadata):
    actorPhotoURL = ''

    req = PAutils.HTTPRequest('https://www.adultdvdempire.com/performer/search?q=' + actorEncoded)
    actorSearch = HTML.ElementFromString(req.text)
    actorPageURL = actorSearch.xpath('//div[@id="performerlist"]/div//a/@href')
    if actorPageURL:
        actorPageURL = 'https://www.adultdvdempire.com' + actorPageURL[0]
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        img = actorPage.xpath('//div[contains(@class, "performer-image-container")]/a/@href')
        if img:
            actorPhotoURL = img[0]

    return actorPhotoURL, ''


def getFromBoobpedia(actorName, actorEncoded, metadata):
    actorPhotoURL = ''

    actorPageURL = 'http://www.boobpedia.com/boobs/' + actorName.title().replace(' ', '_')
    req = PAutils.HTTPRequest(actorPageURL)
    actorPage = HTML.ElementFromString(req.text)
    img = actorPage.xpath('//table[@class="infobox"]//a[@class="image"]//img/@src')
    if img:
        actorPhotoURL = 'http://www.boobpedia.com' + img[0]

    return actorPhotoURL, 'female'


def getFromBabesandStars(actorName, actorEncoded, metadata):
    actorPhotoURL = ''

    actorPageURL = 'http://www.babesandstars.com/' + actorName[0:1].lower() + '/' + actorName.lower().replace(' ', '-').replace('\'', '-') + '/'
    req = PAutils.HTTPRequest(actorPageURL)
    actorPage = HTML.ElementFromString(req.text)
    img = actorPage.xpath('//div[@class="profile"]//div[@class="thumb"]/img/@src')
    if img:
        actorPhotoURL = img[0]

    return actorPhotoURL, 'female'


def getFromIAFD(actorName, actorEncoded, metadata):
    actorPhotoURL = ''
    gender = ''
    period_corrections = {
        (r'^dr%20', 'Dr%2E%20'), (r'%20st%20', '%20St.%20'), (r'^j%20', 'J%2E%20')
    }

    for value in period_corrections:
        actorEncoded = re.sub(value[0], value[1], actorEncoded, flags=re.IGNORECASE)

    req = PAutils.HTTPRequest('http://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=' + actorEncoded)

    actorSearch = HTML.ElementFromString(req.text)
    actorResults = actorSearch.xpath('//table[@id="tblFem" or @id="tblMal"]//tbody//td[2]//a')
    actorAlias = actorSearch.xpath('//table[@id="tblFem" or @id="tblMal"]//tbody//td[@class="text-left"]')
    maleActorURLs = actorSearch.xpath('//table[@id="tblMal"]//tbody//td[2]//a/@href')

    actorPageURL = ''
    if actorResults:
        score = Util.LevenshteinDistance(actorName.lower(), actorResults[0].text_content().strip().lower()) + 1

        results = []
        for idx, actor in enumerate(actorResults, 0):
            resultScore = Util.LevenshteinDistance(actorName.lower(), actor.text_content().strip().lower())

            if resultScore != 0:
                if actorName.lower() in actorAlias[idx].text_content().lower():
                    resultScore = resultScore - 1

                if metadata.studio.replace(' ', '').lower() in actorAlias[idx].text_content().replace(' ', '').lower():
                    resultScore = 0

            if resultScore == score:
                results.append(actor)
            elif resultScore < score:
                score = resultScore
                results = [actor]

        if results:
            actor = random.choice(results)
            actorPageURL = actor.xpath('./@href')[0]

    if actorPageURL:
        req = PAutils.HTTPRequest('http://www.iafd.com' + actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        img = actorPage.xpath('//div[@id="headshot"]//img/@src')
        if img and 'nophoto' not in img[0] and 'th_iafd_ad' not in img[0]:
            actorPhotoURL = img[0]

        gender = 'male' if actorPageURL in maleActorURLs else 'female'

    return actorPhotoURL, gender


def getFromBabepedia(actorName, actorEncoded, metadata):
    actorPhotoURL = ''

    img = 'http://www.babepedia.com/pics/%s.jpg' % urllib.quote(actorName.title())
    req = PAutils.HTTPRequest(img, 'HEAD', bypass=False)
    if req.ok:
        actorPhotoURL = img

    return actorPhotoURL, 'female'


def getFromJavBus(actorName, actorEncoded, metadata):
    actorPhotoURL = ''
    actorID = ''

    for id, names in PAdatabaseActors.ActorsReplaceJavBusSearch.items():
        if actorName.lower() in map(str.lower, names):
            actorID = id
            break

    if actorID:
        req = PAutils.HTTPRequest('https://www.javbus.com/en/star/' + actorID)
    else:
        req = PAutils.HTTPRequest('https://www.javbus.com/en/searchstar/' + actorEncoded)

    actorSearch = HTML.ElementFromString(req.text)
    results = actorSearch.xpath('//div[@class="photo-frame"]//img')
    score = 100
    for actor in results:
        img = actor.xpath('./@src')[0]
        actorSeachName = actor.xpath('./@title')[0].strip()

        if actorID:
            actorPhotoURL = 'https://www.javbus.com' + img
            break
        elif Util.LevenshteinDistance(actorName, actorSeachName) < int(score):
            score = Util.LevenshteinDistance(actorName, actorSeachName)

            if 'nowprinting' not in img and 'dmm' not in img:
                if 'http' not in img:
                    actorPhotoURL = 'https://www.javbus.com' + img
                else:
                    actorPhotoURL = img

                if int(score) == 0:
                    break

    return actorPhotoURL, 'female'


def getFromJAVDatabase(actorName, actorEncoded, metadata):
    actorPhotoURL = ''
    actorEncoded = actorName.replace(' ', '+')

    req = PAutils.HTTPRequest('https://www.javdatabase.com/?wpessid=391488&s=' + actorEncoded)

    actorSearch = HTML.ElementFromString(req.text)
    results = actorSearch.xpath('//div[@class="idol-thumb"]//img[@class]')
    lastScore = 100
    for actor in results:
        actorSeachName = actor.xpath('./@alt')[0].strip()

        score = Util.LevenshteinDistance(actorName, actorSeachName)

        if score < lastScore or not actorPhotoURL:
            lastScore = score
            actorPhotoURL = actor.xpath('./@data-src')[0]

            req = PAutils.HTTPRequest(actorPhotoURL)
            if 'unknown.' in req.url:
                actorPhotoURL = ''

        if actorPhotoURL and int(score) == 0:
            break

    return actorPhotoURL, 'female'


def getFromLocalStorage(actorName, actorEncoded, metadata):
    actorPhotoURL = ''

    actorsResourcesPath = os.path.join(Core.bundle_path, 'Contents', 'Resources')
    filename = filename = 'actor.' + actorName.replace(' ', '-').lower()
    for root, dirs, files in os.walk(actorsResourcesPath):
        for file in files:
            if file.startswith(filename):
                filename = file
                break
        break

    localPhoto = Resource.ExternalPath(filename)
    if localPhoto:
        actorPhotoURL = localPhoto

    return actorPhotoURL, ''


# fetches a copy of an actor image and stores it locally, then returns a URL from which Plex can fetch it later
def cacheActorPhoto(url, actorName, **kwargs):
    localPhoto = ''

    req = PAutils.HTTPRequest(url, **kwargs)

    actorsResourcesPath = os.path.join(Core.bundle_path, 'Contents', 'Resources')
    if not os.path.exists(actorsResourcesPath):
        os.makedirs(actorsResourcesPath)

    extension = mimetypes.guess_extension(req.headers['Content-Type'])
    if extension:
        filename = 'actor.' + actorName.replace(' ', '-').lower() + extension
        filepath = os.path.join(actorsResourcesPath, filename)

        Log('Saving actor image as: "%s"' % filename)
        with codecs.open(filepath, 'wb+') as file:
            file.write(req.content)

        localPhoto = Resource.ExternalPath(filename)
        if not localPhoto:
            localPhoto = ''

    return localPhoto, ''
