import PAsearchSites
import PAextras
import PAutils


def search(results, lang, siteNum, searchData):
    params = {
        'input_search_sm': searchData.encoded
    }
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum), params=params)
    searchResults = HTML.ElementFromString(req.text)

    for searchResult in searchResults.xpath('//a[contains(@href, "videos")]'):
        link = searchResult.xpath('.//img[contains(@src, "videos")]')
        if link:
            if link[0].get('alt') is not None:
                titleNoFormatting = link[0].get('alt').strip()
                releaseDate = parse(searchResult.xpath('.//h2[2]')[0].text_content().strip()).strftime('%Y-%m-%d')
                curID = PAutils.Encode(searchResult.get('href'))

                if searchData.date:
                    score = 100 - Util.LevenshteinDistance(searchData.date, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    if searchData.title in manualMatch:
        item = manualMatch[searchData.title]
        curID = PAutils.Encode(item['curID'])

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name=item['name'], score=101, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="row info"]//div[@class="small-12 medium-12 large-12 columns"]')[0].text_content().strip()

    # Summary
    paragraphs = detailsPageElements.xpath('//div[@class="small-12 medium-12 large-12 columns info"]//p')
    summary = ''
    for paragraph in paragraphs:
        summary += '\n\n' + paragraph.text_content()
    metadata.summary = summary.strip()

    # Studio
    metadata.studio = 'X-Art'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteNum).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//h2')[2].text_content()[:-1]
    if date:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Genres
    movieGenres.clearGenres()
    movieGenres.addGenre('Artistic')
    movieGenres.addGenre('Glamorous')

    # Actors
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h2//a')
    actorName = ''
    if actors:
        if len(actors) == 3:
            movieGenres.addGenre('Threesome')
        if len(actors) == 4:
            movieGenres.addGenre('Foursome')
        if len(actors) > 4:
            movieGenres.addGenre('Orgy')

        for actorLink in actors:
            actorName = actorLink.text_content()

            actorPageURL = actorLink.get('href')
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            actorPhotoURL = actorPage.xpath('//img[@class="info-img"]/@src')[0]

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    xpaths = [
        '//img[@alt="thumb"]/@src',
        '//div[contains(@class, "video-tour")]//a/img/@src',
        '//div[@class="gallery-item"]//img/@src',
    ]

    elements = [detailsPageElements]

    galleryURL = sceneURL.replace('/videos/', '/galleries/')
    req = PAutils.HTTPRequest(galleryURL)
    if req.ok:
        galleryPageElements = HTML.ElementFromString(req.text)
        elements.insert(0, galleryPageElements)

    for element in elements:
        for xpath in xpaths:
            for poster in element.xpath(xpath):
                if 'videos' in poster:
                    art.append(poster)

                    if poster.endswith('_1.jpg'):
                        poster = poster.replace('_1.jpg', '_2.jpg')
                    elif poster.endswith('_1-lrg.jpg'):
                        poster = poster.replace('_1-lrg.jpg', '_2-lrg.jpg')

                    art.append(poster)

    # Extra Posters
    art_ext = []
    match = 0

    for site in ['XartFan.com', 'HQSluts.com', 'ImagePost.com', 'CoedCherry.com/pics', 'Nude-Gals.com']:
        fanSite = PAextras.getFanArt(site, art_ext, actors, actorName, metadata.title.strip(), match, PAsearchSites.getSearchSiteName(siteNum))
        match = fanSite[2]
        if match is 1:
            break

    if match is 1 or match is 2:
        art.extend(art_ext)

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
                if width > 1 or height > width:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and width > height:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata


manualMatch = {
    'Out of This World': {
        'curID': '/videos/Out_of_This_World',
        'name': 'Out Of This World [X-Art]',
    },
    'Beauteliful Girl': {
        'curID': '/videos/beauteliful_girl',
        'name': 'Beauteliful Girl [X-Art]',
    },
    'Sunset': {
        'curID': '/videos/sunset',
        'name': 'Sunset [X-Art]',
    },
    'Cum Like Crazy': {
        'curID': '/videos/cum_like_crazy',
        'name': 'Cum Like Crazy [X-Art]',
    },
    'Tenderness': {
        'curID': '/videos/tenderness',
        'name': 'Tenderness [X-Art]',
    },
    'My Love': {
        'curID': '/videos/my_love',
        'name': 'My Love [X-Art]',
    },
    'Dream Girl': {
        'curID': '/videos/dream_girl',
        'name': 'Dream Girl [X-Art]',
    },
    'Mutual Orgasm': {
        'curID': '/videos/mutual_orgasm',
        'name': 'Mutual Orgasm [X-Art]',
    },
    'Delicious': {
        'curID': '/videos/delicious',
        'name': 'Delicious [X-Art]',
    },
    'Girlfriends': {
        'curID': '/videos/girlfriends',
        'name': 'Girlfriends [X-Art]',
    },
    'Just for You': {
        'curID': '/videos/just_for_you',
        'name': 'Just for You [X-Art]',
    },
    'True Love': {
        'curID': '/videos/true_love',
        'name': 'True Love [X-Art]',
    },
    'Intimate': {
        'curID': '/videos/intimate',
        'name': 'Intimate [X-Art]',
    },
    'In Bed': {
        'curID': '/videos/in_bed',
        'name': 'In Bed [X-Art]',
    },
    'Angelic': {
        'curID': '/videos/angelic',
        'name': 'Angelic [X-Art]',
    },
    'Her First Time': {
        'curID': '/videos/her_first_time',
        'name': 'Her First Time [X-Art]',
    },
    'Want You': {
        'curID': '/videos/want_you',
        'name': 'Want You [X-Art]',
    },
    'Awakening': {
        'curID': '/videos/Awakening',
        'name': 'Awakening [X-Art]',
    },
    'Rendezvous': {
        'curID': '/videos/Rendezvous',
        'name': 'Rendezvous [X-Art]',
    },
    'Watching': {
        'curID': '/videos/watching',
        'name': 'Watching [X-Art]',
    },
    'First Time': {
        'curID': '/videos/first_time',
        'name': 'First Time [X-Art]',
    },
    'Sapphically Sexy Fucking Lesbians': {
        'curID': '/videos/sapphically_sexy_(fucking_lesbians)',
        'name': 'Sapphically Sexy (Fucking Lesbians) [X-Art]',
    },
    'Je Mappelle Belle': {
        'curID': '/videos/je_m_appelle_belle',
        'name': 'Je M\'Appelle Belle [X-Art]',
    },
    'Sparks': {
        'curID': '/videos/sparks',
        'name': 'Sparks [X-Art]',
    },
    'Hot Orgasm': {
        'curID': '/videos/hot_orgasm',
        'name': 'Hot Orgasm [X-Art]',
    },
    'Group Sex': {
        'curID': '/videos/group_sex',
        'name': 'Group Sex [X-Art]',
    },
    'A Cloudy Hot Day Milas First Lesbian Experience': {
        'curID': '/videos/a_cloudy_hot_day_(mila\'s_first_lesbian_experience)',
        'name': 'A Cloudy Hot Day (Mila\'s First Lesbian Experience) [X-Art]',
    },
    'Our Little Cum Cottage': {
        'curID': '/videos/our_little_(cum)_cottage',
        'name': 'Our Little (Cum) Cottage [X-Art]',
    },
    'Kacey Jordan Does X Art': {
        'curID': '/videos/kacey_jordan_does_x-art',
        'name': 'Kacey Jordan Does X-Art [X-Art]',
    },
    'X Art on TV': {
        'curID': '/videos/x-art_on_tv',
        'name': 'X-Art on TV [X-Art]',
    },
    'Lilys First Time Lesbian Loving': {
        'curID': '/videos/lilys_firsttime_lesbian_loving',
        'name': 'Lily\'s First-time Lesbian Loving [X-Art]',
    },
    'I Love X Art': {
        'curID': '/videos/i_love_x-art',
        'name': 'I Love X-Art [X-Art]',
    },
    'Don\'t Keep Me Waiting Part 1': {
        'curID': '/videos/dont_keep_me_waiting__part_1',
        'name': 'Don\'t Keep Me Waiting - Part 1 [X-Art]',
    },
    'Don\'t Keep Me Waiting Part 2': {
        'curID': '/videos/dont_keep_me_waiting__part_2',
        'name': 'Don\'t Keep Me Waiting - Part 2 [X-Art]',
    },
    'Luminated Sexual Emotions': {
        'curID': '/videos/luminated_(sexual)_emotions',
        'name': 'Luminated (Sexual) Emotions [X-Art]',
    },
    '4 Way in 4k': {
        'curID': '/videos/4way_in_4k',
        'name': '4-Way in 4K [X-Art]',
    },
    'Cut Once More Please': {
        'curID': '/videos/cut!_once_more_please!',
        'name': 'Cut! Once More Please! [X-Art]',
    },
    'Fine Finger Fucking': {
        'curID': '/videos/fine_fingerfucking',
        'name': 'Fine Finger-Fucking [X-Art]',
    },
    'Skin Tillating Sex for Three': {
        'curID': '/videos/skintillating_sex_for_three',
        'name': 'Skin-Tillating Sex For Three [X-Art]',
    },
    'Angelica Hotter Than Ever': {
        'curID': '/videos/angelicahotter_than_ever',
        'name': 'Angelica~Hotter Than Ever [X-Art]',
    },
    'Domination Part 1': {
        'curID': '/videos/domination__part_1',
        'name': 'Domination - Part 1 [X-Art]',
    },
    'The Rich Girl Part One': {
        'curID': '/videos/the_rich_girl_-_part_one',
        'name': 'The Rich Girl - Part One [X-Art]',
    },
    'The Rich Girl Part Two': {
        'curID': '/videos/the_rich_girl_-_part_two',
        'name': 'The Rich Girl - Part Two [X-Art]',
    },
    'Black & White': {
        'curID': '/videos/black_&_white',
        'name': 'Black & White [X-Art]',
    },
    'Fashion Models':{
        'curID': '/videos/fashion_models',
        'name': 'Fashion Models [X-Art]',
    },
    'Francesca Angelic':{
        'curID': '/videos/angelic',
        'name': 'Francesca Angelic [X-Art]',
    },
    'Green Eyes':{
        'curID': '/videos/green_eyes',
        'name': 'Green Eyes [X-Art]',
    },
    'Heart & Soul': {
        'curID': '/videos/heart_&_soul',
        'name': 'Heart & Soul [X-Art]',
    },
    'La Love': {
        'curID': '/videos/l.a._love',
        'name': 'L.A. Love [X-Art]',
    },
    'Naughty & Nice': {
        'curID': '/videos/naughty_&_nice',
        'name': 'Naughty & Nice [X-Art]',
    },
    'One & Only Caprice': {
        'curID': '/videos/one_&_only_caprice',
        'name': 'One & Only Caprice [X-Art]',
    },
    'Young & Hot': {
        'curID': '/videos/young_&_hot',
        'name': 'Young & Hot [X-Art]',
    },
}
