import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    sceneInfo = getSceneInfo(searchData.title)
    if not sceneInfo:
        return

    req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteNum), 'HEAD', allow_redirects=False)
    cookies = {
        'start_session_galleria': req.cookies['start_session_galleria']
    }

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + sceneInfo['modelID'], cookies=cookies)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="movie-wrap-index img-polaroid left"]'):
        titleNoFormatting = searchResult.xpath('.//h1[@class="video-title-model"]')[0].text_content().strip()
        titleNoFormattingID = PAutils.Encode(titleNoFormatting)

        try:
            description = searchResult.xpath('.//div[@class="col-lg-7"]')[0].text_content().split('Description:')[1].strip()
        except:
            description = ''

        descriptionID = PAutils.Encode(description)

        poster = searchResult.xpath('.//img[@class="img-responsive"]/@src')[0]
        posterID = PAutils.Encode(poster)

        actor = searchResult.xpath('//h1[@class="page-title col-lg-12"]')[0].text_content().strip()
        releaseDate = searchData.dateFormat()

        curID = PAutils.Encode(searchResult.xpath('.//a[@class="thumbnail left"]/@href')[0])

        compareSearchStrings = []
        compareResultStrings = []

        if sceneInfo['title']:
            compareSearchStrings.append(sceneInfo['title'].lower())
            compareResultStrings.append(titleNoFormatting.lower())

        if searchData.duration:
            compareSearchStrings.append(searchData.durationFormat())
            compareResultStrings.append(searchResult.xpath('.//div[@class="movie-duration"]')[0].text_content().strip())

        compareSearch = ' - '.join(compareSearchStrings)
        compareResult = ' - '.join(compareResultStrings)
        score = 100 - Util.LevenshteinDistance(compareSearch, compareResult)

        results.Append(MetadataSearchResult(id='%s|%d|%s|%s|%s|%s|%s' % (curID, siteNum, titleNoFormattingID, descriptionID, releaseDate, actor, posterID), name='%s [ATKGirlfriends]' % titleNoFormatting, score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    sceneTitle = PAutils.Decode(metadata_id[2])
    sceneDescription = PAutils.Decode(metadata_id[3])
    sceneDate = metadata_id[4]
    sceneActor = metadata_id[5]
    scenePoster = PAutils.Decode(metadata_id[6])

    # Title
    metadata.title = sceneTitle

    # Summary
    metadata.summary = sceneDescription

    # Studio
    metadata.studio = 'ATK'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date_object = parse(sceneDate)
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()

    actorName = sceneActor
    actorPhotoURL = ''

    movieActors.addActor(actorName, actorPhotoURL)

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Girlfriend Experience')
    # If scenePage is valid, try to load it to scrape genres
    try:
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        genreText = detailsPageElements.xpath('//div[@class="movie-wrap img-polaroid"]')[0].text_content().split('Tags :')[1].strip()
        for genreLink in genreText.split(','):
            genreName = genreLink.strip()

            movieGenres.addGenre(genreName)
    except:
        pass

    # Posters
    art = []
    scenePoster = scenePoster.replace('sm_', '').split('1.jpg')[0]
    for photoNum in range(1, 8):
        photo = scenePoster + str(photoNum) + '.jpg'

        art.append(photo)

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
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata


def getSceneInfo(searchTitle):
    models = {
        'Aaliyah Love': 'aal003',
        'Abby Adams': 'abb017',
        'Addee Kate': 'add007',
        'Addison Ryder': 'add006',
        'Adria Rae': 'adr042',
        'Adriana Chechik': 'adr035',
        'Adriana Maya': 'adr041',
        'Aften Opal': 'aft001',
        'Aimee Black': 'aim007',
        'Alaina Dawson': 'ala027',
        'Alex Blake': 'ale167',
        'Alex Coal': 'ale170',
        'Alexa Grace': 'ale152',
        'Alexa Nova': 'ale156',
        'Alexa Raye': 'ale163',
        'Alexia Anders': 'ale173',
        'Alexia Gold': 'ale147',
        'Alexis Adams': 'ale138',
        'Alexis Blaze': 'ale112',
        'Alexis Rodriquez': 'ale151',
        'Alice March': 'ali097',
        'Alice Pink': 'ali126',
        'Alina West': 'ali106',
        'Alison Faye': 'ali099',
        'Alison Rey': 'ali105',
        'Aliya Brynn': 'ali127',
        'Allie Addison': 'all049',
        'Allie James': 'all029',
        'Amanda Bryant': 'ama034',
        'Amanda Tate': 'ama045',
        'Amara Romani': 'ama047',
        'Amarna Miller': 'ama046',
        'Amirah Adara': 'ami007',
        'Ana Foxxx': 'ana027',
        'Andy San Dimas': 'and098',
        'Angel Smalls': 'ang181',
        'Anikka Albrite': 'ani045',
        'Anissa Kate': 'ani049',
        'Anna Mae': 'ann135',
        'Anya Olsen': 'any009',
        'April Brookes': 'apr022',
        'April Snow': 'apr023',
        'Aria Banks': 'ari060',
        'Aria Skye': 'ari051',
        'Ariana Aimes': 'ari053',
        'Ariana Marie': 'ari037',
        'Ariel Grace': 'ari046',
        'Arielle Faye': 'ari047',
        'Arietta Adams': 'ari059',
        'Chloe Foster': 'chl033',
        'Chloe Love': 'chl037',
        'Chloe Skyy': 'chl039',
        'Chloe Temple': 'chl046',
        'Cindy Starfall': 'cin030',
        'Cleo Vixen': 'cle017',
        'Compilation': 'com001',
        'Daisy Haze': 'dai020',
        'Dakota James': 'dak008',
        'Danni Rivers': 'dan096',
        'Daya Knight': 'day002',
        'Dee Dee Lynn': 'dee020',
        'Demi Lopez': 'dem005',
        'Devon Green': 'dev015',
        'Dillion Harper': 'dil003',
        'Dixie Comet': 'dix003',
        'Dixie Lynn': 'dix006',
        'Dolly Leigh': 'dol011',
        'Eden Sin': 'ede006',
        'Edyn Blair': 'edy002',
        'Ela Darling': 'ela002',
        'Elaina Raye': 'kyl018',
        'Elektra Rose': 'ele039',
        'Elena Koshka': 'ele041',
        'Eliza Jane': 'eli059',
        'Ella Nova': 'ell035',
        'Ella Woods': 'ell031',
        'Elsa Jean': 'els004',
        'Ember Stone': 'emb005',
        'Emily Cash': 'emi033',
        'Emily Willis': 'emi035',
        'Emma Evins': 'emm030',
        'Emma Hix': 'emm032',
        'Emma Ryder': 'emm031',
        'Emma Starletto': 'emm035',
        'Emma Stoned': 'emm028',
        'Erin Grey': 'eri071',
        'Eva Sedona': 'eva073',
        'Gabbie Carter': 'gab033',
        'Gabriela Lopez': 'gab032',
        'Gia Paige': 'gia022',
        'Gianna Nicole': 'gia020',
        'Giaoni Whiley': 'gia021',
        'Gina Valentina': 'gin058',
        'Goldie Rush': 'gol006',
        'Gracie Green': 'gra025',
        'Haley Reed': 'hal021',
        'Halle Von': 'hal020',
        'Hanna Lay': 'han026',
        'Hannah Hawthorne': 'han030',
        'Hannah Hays': 'han029',
        'Harley Jade': 'har019',
        'Harmony Wonder': 'har021',
        'Hazel Grace': 'haz015',
        'Henley Hart': 'hen009',
        'Hime Marie': 'him001',
        'Hollie Mack': 'hol045',
        'Holly Hendrix': 'hol046',
        'Hope Howell': 'hop004',
        'Iggy Amore': 'igg001',
        'Indica Monroe': 'ind012',
        'Iris Ivy': 'pap001',
        'Isabel Moon': 'isa042',
        'Ivy Aura': 'ivy018',
        'Ivy Sherwood': 'ivy016',
        'Ivy Wolfe': 'emm034',
        'Izzy Bell': 'izz003',
        'Izzy Champayne': 'izz002',
        'Jackie Marie': 'jac038',
        'Jackie Rogen': 'jac040',
        'Jada Doll': 'jad048',
        'Jade Amber': 'jad044',
        'Jade Jantzen': 'jad038',
        'Jade Kush': 'jad047',
        'Jade Nile': 'jad042',
        'Jamie Marleigh': 'jam036',
        'Jane Wilde': 'jan148',
        'Janice Griffith': 'jan144',
        'Jayde Symz': 'lac025',
        'Jaye Summers': 'jay045',
        'Jenna Ivory': 'jen142',
        'Jenna Reid': 'jen149',
        'Jericha Jem': 'jer019',
        'Jessica Malone': 'jes754',
        'Jessica Rex': 'jes760',
        'Jessie Parker': 'mat009',
        'Jessie Wylde': 'jes763',
        'Jezabel Vessir': 'jez012',
        'Jill Kassidy': 'jil022',
        'Jillian Janson': 'jil021',
        'Joey White': 'joe017',
        'Jojo Kiss': 'joj004',
        'Joseline Kelly': 'jos038',
        'Kacey Jordan': 'kac002',
        'Kacie Castle': 'kac010',
        'Kacy Lane': 'kac009',
        'Kali Roses': 'kal018',
        'Kalina Ryu': 'kal014',
        'Kandace Kayne': 'kan019',
        'Kara Lee': 'kar120',
        'Karla Kush': 'kar100',
        'Karlee Grey': 'kar105',
        'Karly Baker': 'kar115',
        'Karmen Bella': 'kar107',
        'Karmen Karma': 'kar102',
        'Karter Foxx': 'kar110',
        'Kasey Miller': 'kas011',
        'Kasey Warner': 'kas007',
        'Kate Bloom': 'kat245',
        'Kate England': 'kat225',
        'Kate Wolf': 'kat219',
        'Katerina Kay': 'kat222',
        'Katie St Ives': 'kat165',
        'Keisha Grey': 'kei016',
        'Kelsi Monroe': 'kel067',
        'Kendall White': 'ken031',
        'Kennedy Kressler': 'ken013',
        'Kenzie Kai': 'ken043',
        'Kenzie Reeves': 'ken044',
        'Kharlie Stone': 'kha002',
        'Khloe Kapri': 'khl004',
        'Kiara Cole': 'kia007',
        'Kiera Daniels': 'khl002',
        'Kiera Winters': 'kie005',
        'Kierra Wilde': 'kie008',
        'Kimber Woods': 'kim061',
        'Kimberly Brix': 'kim058',
        'Kimmy Granger': 'kim060',
        'Kristen Scott': 'kri081',
        'Kristina Bell': 'kri078',
        'Kyler Quinn': 'kyl035',
        'Kylie Foxx': 'kyl033',
        'Kylie Nicole': 'kay038',
        'Kylie Sinner': 'kyl032',
        'Lacy Lennon': 'lac032',
        'Lana Rhoades': 'lan034',
        'Lana Sharapova': 'lan035',
        'Lara Brookes': 'lar019',
        'Leah Lee': 'lea048',
        'Lenna Lux': 'len058',
        'Lilly Ford': 'lil088',
        'Lily Adams': 'lil089',
        'Lily Jordan': 'lil086',
        'Lily LaBeau': 'lil043',
        'Lily Larimar': 'lil092',
        'Lily Love': 'lil072',
        'Lily Rader': 'lil085',
        'Liv Revamped': 'liv005',
        'Liza Rowe': 'liz039',
        'Lola Fae': 'lol042',
        'Lolli Lane': 'lol043',
        'Lucie Kline': 'luc106',
        'Lucy Valentine': 'luc109',
        'Luna Kitsuen': 'lun007',
        'Lyra Law': 'lyr003',
        'Maci Winslett': 'mac012',
        'Mackenzie Lohan': 'mac015',
        'Maddy Rose': 'mad046',
        'Madelyn Monroe': 'mad029',
        'Maia Davis': 'mai013',
        'Makenna Blue': 'mak008',
        'Malory Malibu': 'mal025',
        'Mandy Muse': 'xyl001',
        'Marina Angel': 'mar406',
        'Marina Woods': 'mar421',
        'Marley Brinx': 'mar416',
        'Marley Matthews': 'mar408',
        'Mary Jane Mayhem': 'mar329',
        'Maya Bijou': 'may022',
        'Maya Kendrick': 'may021',
        'Megan Hughes': 'meg050',
        'Megan Marx': 'meg049',
        'Megan Rain': 'meg042',
        'Megan Sage': 'meg043',
        'Megan Winters': 'meg048',
        'Melanee Star': 'mel112',
        'Melody Marks': 'mel116',
        'Mi Ha Doan': 'mih002',
        'Miko Dai': 'mik036',
        'Miranda Mills': 'mir038',
        'Misty Anderson': 'mis032',
        'Moka Mora': 'mok001',
        'Molly Manson': 'mol035',
        'Monica Rise': 'mon111',
        'Nala Nova': 'nal002',
        'Naomi Swann': 'nao022',
        'Natalia Nix': 'nat148',
        'Natalia Queen': 'nat150',
        'Natalie Brooks': 'nat147',
        'Natalie Monroe': 'nat137',
        'Natalie Porkman': 'nat149',
        'Natasha White': 'nat134',
        'Nickey Huntsman': 'nic093',
        'Nicole Bexley': 'nic097',
        'Niki Snow': 'nik122',
        'Nikki Daniels': 'nik086',
        'Nikki Next': 'nik111',
        'Nikki Peach': 'nik129',
        'Nikki Simmons': 'nik128',
        'Nikole Nash': 'nik130',
        'Nina Nirvana': 'nin038',
        'Nina North': 'nin037',
        'Noemie Bilas': 'noe011',
        'Norah Nova': 'nor013',
        'Odette Delacroix': 'ode001',
        'Olive': 'oli027',
        'Olivia Lua': 'oli029',
        'Olivia Nova': 'oli033',
        'Onyx': 'ony002',
        'Paisley Rae': 'pai016',
        'Paris White': 'par028',
        'Penelope Reed': 'pen027',
        'Penny Pax': 'pen026',
        'Pepper Hart': 'pep010',
        'Pepper XO': 'pep009',
        'Peyton Coast': 'ver098',
        'Piper Perri': 'pip007',
        'Pressley Carter': 'ari033',
        'Rachel James': 'rac059',
        'Rachel Rivers': 'rac061',
        'Rachele Richey': 'rac055',
        'Rahyndee James': 'rah002',
        'Raven Orion': 'rav015',
        'Raven Rockette': 'rav013',
        'Raven Wylde': 'rav016',
        'Raylin Ann': 'ray015',
        'Rayna Rose': 'ray016',
        'Rebecca Blue': 'reb020',
        'Rebecca Vanguard': 'sai003',
        'Renee Roulette': 'ren055',
        'Rhaya Shyne': 'rha001',
        'Rikki Rumor': 'rik006',
        'Riley Reid': 'ril009',
        'Riley Reyes': 'ril015',
        'Riley Star': 'ril018',
        'Rina Ellis': 'rin004',
        'Rococo Royalle': 'roc013',
        'Rosalyn Sphinx': 'ros075',
        'Rose Red': 'ros064',
        'Rosie Reefer': 'ros076',
        'Sabrina Banks': 'sab037',
        'Sadie Blair': 'sad027',
        'Sadie Blake': 'sad029',
        'Sadie Pop': 'sad028',
        'Sally Squirt': 'sal023',
        'Samantha Bentley': 'sam047',
        'Samantha Hayes': 'sam080',
        'Samantha Rone': 'sam078',
        'Sami Parker': 'sam083',
        'Sami White': 'sam085',
        'Sara Luvv': 'sar089',
        'Sativa Verte': 'sat007',
        'Savannah Sixx': 'sav018',
        'Scarlet Red': 'sca034',
        'Scarlett Fever': 'sca032',
        'Scarlett Minx': 'sca040',
        'Scarlett Sage': 'sca036',
        'Selina Bentz': 'sel016',
        'Sera Ryder': 'ser030',
        'Shane Blair': 'sha111',
        'Shauna Skye': 'sha112',
        'Sierra Moon': 'sie024',
        'Sierra Nicole': 'sie023',
        'Simone Delilah': 'sim034',
        'Sinn Sage': 'ric002',
        'Skin Diamond': 'ski001',
        'Sky Pierce': 'sky033',
        'Skye Blue': 'sky034',
        'Skye West': 'sky024',
        'Skylar Green': 'sky022',
        'Sofia Banks': 'man031',
        'Sophia Grace': 'sop047',
        'Sophia Leone': 'sop048',
        'Sophia Lux': 'sop050',
        'Sophie Sativa': 'sop049',
        'Stephanie Saint': 'ste073',
        'Stevie Shae': 'blo005',
        'Summer Carter': 'sum024',
        'Susan Ayn': 'sus025',
        'Sydney Cole': 'syd005',
        'Tali Dova': 'tal017',
        'Tara Ashley': 'tar031',
        'Tara Lynn Foxx': 'tar024',
        'Taylor Blake': 'tay048',
        'Taylor Reed': 'tay043',
        'Taylor Whyte': 'tay040',
        'Tegan Riley': 'teg001',
        'Tia Cyrus': 'tia020',
        'Tiffany Doll': 'tif052',
        'Tiffany Watson': 'tif059',
        'Tina Kay': 'tin053',
        'Trillium': 'tri049',
        'Trisha Parks': 'abi012',
        'Tysen Rich': 'tys001',
        'Valentina Nappi': 'val054',
        'Vera King': 'lex046',
        'Veronica Rodriguez': 'ver077',
        'Veronica Vella': 'ver107',
        'Veruca James': 'ver097',
        'Victoria Gracen': 'vic064',
        'Victoria Rae Black': 'vic044',
        'Vienna Black': 'vie002',
        'Vina Sky': 'vin002',
        'Violet Monroe': 'meg016',
        'Violet Rain': 'vio028',
        'Violet Winters': 'vio023',
        'Whitney Westgate': 'whi008',
        'Whitney Wright': 'whi009',
        'Willow Hayes': 'wil017',
        'Winter Jade': 'win006',
        'Winter Marie': 'win005',
        'Yara Skye': 'yar002',
        'Zaya Cassidy': 'zay003',
        'Zoe Bloom': 'zoe046',
        'Zoe Parker': 'zoe042',
        'Zoey Foxx': 'zoe030',
    }

    searchTitleLower = searchTitle.lower()

    for modelName, modelID in models.items():
        modelNameLower = modelName.lower()
        if searchTitleLower.startswith(modelNameLower):
            return splitModelAndTitle(modelID, modelName, searchTitleLower, modelNameLower)

    # just in case the modelID was specified
    for modelName, modelID in models.items():
        if searchTitleLower.startswith(modelID):
            return splitModelAndTitle(modelID, modelName, searchTitleLower, modelID)

    return ''


def splitModelAndTitle(modelID, modelName, searchTitle, splitter):
    split = searchTitle.lower().split(splitter)
    return {
        'modelID': modelID,
        'modelName': modelName,
        'title': split[1].strip()
    }
