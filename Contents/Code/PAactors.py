import PAutils
import PAdatabaseActors


class PhoenixActors:
    actorsTable = []

    def addActor(self, newActor, newPhoto):
        newActor = newActor.encode('UTF-8') if isinstance(newActor, unicode) else newActor
        newPhoto = newPhoto.encode('UTF-8') if isinstance(newPhoto, unicode) else newPhoto

        if newActor not in [actorLink['name'] for actorLink in self.actorsTable]:
            self.actorsTable.append({
                'name': newActor,
                'photo': newPhoto,
            })

    def clearActors(self):
        self.actorsTable = []

    def processActors(self, metadata):
        for actorLink in self.actorsTable:
            skip = False
            # Save the potential new Actor or Actress to a new variable, replace &nbsp; with a true space, and strip off any surrounding whitespace
            actorName = actorLink['name'].replace('\xc2\xa0', ' ').replace(',', '').strip().title()
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
                    if metadata.studio in studioList:
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

                        (actorPhoto, gender) = actorDBfinder(displayActorName)
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
                        (actorPhoto, gender) = actorDBfinder(displayActorName)
                        Log('Gender: %s' % gender)
                        if Prefs['gender_enable']:
                            if gender == 'male':
                                continue
                    elif Prefs['gender_enable']:
                        gender = genderCheck(urllib.quote(actorName))
                        Log('Gender: %s' % gender)
                        if gender == 'male':
                            continue

                    if actorPhoto:
                        actorPhoto = PAutils.getClearURL(actorPhoto)

                    Log('Actor: %s %s' % (displayActorName, actorPhoto))
                    role = metadata.roles.new()
                    role.name = actorName
                    role.photo = actorPhoto


def actorDBfinder(actorName):
    actorEncoded = urllib.quote(actorName)

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
        'Local Storage': getFromLocalStorage,
    }

    searchOrder = ['Local Storage', 'Freeones', 'IAFD', 'Indexxx', 'AdultDVDEmpire', 'Boobpedia', 'Babes and Stars', 'Babepedia']
    if Prefs['order_enable']:
        searchOrder = [sourceName.strip() for sourceName in Prefs['order_list'].split(',') if sourceName.strip() in searchResults]

    for sourceName in searchOrder:
        task = searchResults[sourceName]

        url = None
        try:
            (url, gender) = task(actorName, actorEncoded)
        except Exception as e:
            Log.Error(format_exc())

        if url:
            databaseName = sourceName
            actorPhotoURL = url
            break

    if actorPhotoURL:
        Log('%s found in %s ' % (actorName, databaseName))
        Log('PhotoURL: %s' % actorPhotoURL)
    else:
        Log('%s not found' % actorName)

    return actorPhotoURL, gender

def genderCheck(actorEncoded):
    gender = ''

    url = 'http://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=' + actorEncoded
    req = PAutils.HTTPRequest(url)
    actorSearch = HTML.ElementFromString(req.text)
    actorPageURL = actorSearch.xpath('//table[@id="tblFem" or @id="tblMal"]//tbody//a/@href')
    if actorPageURL:
        gender = 'male' if 'gender=m' in actorPageURL[0] else 'female'

    return gender

def getFromFreeones(actorName, actorEncoded):
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


def getFromIndexxx(actorName, actorEncoded):
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


def getFromAdultDVDEmpire(actorName, actorEncoded):
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


def getFromBoobpedia(actorName, actorEncoded):
    actorPhotoURL = ''

    actorPageURL = 'http://www.boobpedia.com/boobs/' + actorName.title().replace(' ', '_')
    req = PAutils.HTTPRequest(actorPageURL)
    actorPage = HTML.ElementFromString(req.text)
    img = actorPage.xpath('//table[@class="infobox"]//a[@class="image"]//img/@src')
    if img:
        actorPhotoURL = 'http://www.boobpedia.com' + img[0]

    return actorPhotoURL, 'female'


def getFromBabesandStars(actorName, actorEncoded):
    actorPhotoURL = ''

    actorPageURL = 'http://www.babesandstars.com/' + actorName[0:1].lower() + '/' + actorName.lower().replace(' ', '-').replace('\'', '-') + '/'
    req = PAutils.HTTPRequest(actorPageURL)
    actorPage = HTML.ElementFromString(req.text)
    img = actorPage.xpath('//div[@class="profile"]//div[@class="thumb"]/img/@src')
    if img:
        actorPhotoURL = img[0]

    return actorPhotoURL, 'female'


def getFromIAFD(actorName, actorEncoded):
    actorPhotoURL = ''
    gender = ''
    req = PAutils.HTTPRequest('http://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=' + actorEncoded)
    actorSearch = HTML.ElementFromString(req.text)
    actorPageURL = actorSearch.xpath('//table[@id="tblFem" or @id="tblMal"]//tbody//a/@href')
    if actorPageURL:
        actorPageURL = 'http://www.iafd.com' + actorPageURL[0]
        req = PAutils.HTTPRequest(actorPageURL)
        actorPage = HTML.ElementFromString(req.text)
        img = actorPage.xpath('//div[@id="headshot"]//img/@src')
        if img and 'nophoto' not in img[0]:
            actorPhotoURL = img[0]

        gender = 'male' if 'gender=m' in actorPageURL else 'female'

    return actorPhotoURL, gender


def getFromBabepedia(actorName, actorEncoded):
    actorPhotoURL = ''

    img = 'http://www.babepedia.com/pics/%s.jpg' % urllib.quote(actorName.title())
    req = PAutils.HTTPRequest(img, 'HEAD', bypass=False)
    if req.ok:
        actorPhotoURL = img

    return actorPhotoURL, 'female'


def getFromLocalStorage(actorName, actorEncoded):
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
