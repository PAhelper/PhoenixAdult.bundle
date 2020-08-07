import PAsearchSites
import PAgenres
import PAextras
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    params = {
        'input_search_sm': encodedTitle
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

                if searchDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

                results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    if searchTitle == 'Naughty Nice':
        curID = PAutils.Encode('/videos/Naughty_&_Nice')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Naughty & Nice [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Out Of This World':
        curID = PAutils.Encode('/videos/Out_of_This_World')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Out Of This World [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Beauteliful Girl':
        curID = PAutils.Encode('/videos/beauteliful_girl')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Beauteliful Girl [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Sunset':
        curID = PAutils.Encode('/videos/sunset')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Sunset [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Cum Like Crazy':
        curID = PAutils.Encode('/videos/cum_like_crazy')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Cum Like Crazy [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Tenderness':
        curID = PAutils.Encode('/videos/tenderness')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Tenderness [X-Art]', score=101, lang=lang))
    elif searchTitle == 'My Love':
        curID = PAutils.Encode('/videos/my_love')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='My Love [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Dream Girl':
        curID = PAutils.Encode('/videos/dream_girl')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Dream Girl [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Mutual Orgasm':
        curID = PAutils.Encode('/videos/mutual_orgasm')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Mutual Orgasm [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Delicious':
        curID = PAutils.Encode('/videos/delicious')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Delicious [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Girlfriends':
        curID = PAutils.Encode('/videos/girlfriends')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Girlfriends [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Just for You':
        curID = PAutils.Encode('/videos/just_for_you')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Just for You [X-Art]', score=101, lang=lang))
    elif searchTitle == 'True Love':
        curID = PAutils.Encode('/videos/true_love')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='True Love [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Intimate':
        curID = PAutils.Encode('/videos/intimate')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Intimate [X-Art]', score=101, lang=lang))
    elif searchTitle == 'One  Only Caprice':
        curID = PAutils.Encode('/videos/one_&_only_caprice')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='One & Only Caprice [X-Art]', score=101, lang=lang))
    elif searchTitle == 'In Bed':
        curID = PAutils.Encode('/videos/in_bed')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='In Bed [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Angelic':
        curID = PAutils.Encode('/videos/angelic')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Angelic [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Her First Time':
        curID = PAutils.Encode('/videos/her_first_time')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Her First Time [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Out of This World':
        curID = PAutils.Encode('/videos/out_of_this_world')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Out of This World [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Want You':
        curID = PAutils.Encode('/videos/want_you')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Want You [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Awakening':
        curID = PAutils.Encode('/videos/Awakening')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Awakening [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Warm  Fuzzy Little Miracles':
        curID = PAutils.Encode('/videos/warm_&_fuzzy_(little_miracles)')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Warm & Fuzzy (Little Miracles) [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Blindfold Me  Tie Me Up':
        curID = PAutils.Encode('/videos/blindfold_me_&_tie_me_up')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Blindfold Me & Tie Me Up [X-Art]', score=101, lang=lang))
    elif searchTitle == 'First  Forever':
        curID = PAutils.Encode('/videos/first_&_forever')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='First & Forever [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Black  White':
        curID = PAutils.Encode('/videos/black_&_white')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Black & White [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Rendezvous':
        curID = PAutils.Encode('/videos/Rendezvous')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Rendezvous [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Watching':
        curID = PAutils.Encode('/videos/watching')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Watching [X-Art]', score=101, lang=lang))
    elif searchTitle == 'First Time':
        curID = PAutils.Encode('/videos/first_time')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='First Time [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Sapphically Sexy Fucking Lesbians':
        curID = PAutils.Encode('/videos/sapphically_sexy_(fucking_lesbians)')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Sapphically Sexy (Fucking Lesbians) [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Je Mappelle Belle':
        curID = PAutils.Encode('/videos/je_m_appelle_belle')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Je M\'Appelle Belle [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Sparks':
        curID = PAutils.Encode('/videos/sparks')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Sparks [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Hot Orgasm':
        curID = PAutils.Encode('/videos/hot_orgasm')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Hot Orgasm [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Group Sex':
        curID = PAutils.Encode('/videos/group_sex')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Group Sex [X-Art]', score=101, lang=lang))
    elif searchTitle == 'A Cloudy Hot Day Milas First Lesbian Experience':
        curID = PAutils.Encode('/videos/a_cloudy_hot_day_(mila\'s_first_lesbian_experience)')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='A Cloudy Hot Day (Mila\'s First Lesbian Experience) [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Our Little Cum Cottage':
        curID = PAutils.Encode('/videos/our_little_(cum)_cottage')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Our Little (Cum) Cottage [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Kacey Jordan Does X Art':
        curID = PAutils.Encode('/videos/kacey_jordan_does_x-art')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Kacey Jordan Does X-Art [X-Art]', score=101, lang=lang))
    elif searchTitle == 'X Art on Tv':
        curID = PAutils.Encode('/videos/x-art_on_tv')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='X-Art on TV [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Lilys First Time Lesbian Loving':
        curID = PAutils.Encode('/videos/lilys_firsttime_lesbian_loving')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Lily\'s First-time Lesbian Loving [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Cock Sucking  Fucking Competition':
        curID = PAutils.Encode('/videos/cock_sucking__fucking_competition')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Cock Sucking (& Fucking) Competition [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Beauty  the Beast Video':
        curID = PAutils.Encode('/videos/beauty_beast_video')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Beauty & the Beast Video [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Yoga Master  Student':
        curID = PAutils.Encode('/videos/yoga_master_&_teacher')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Yoga Master & Student [X-Art]', score=101, lang=lang))
    elif searchTitle == 'I Love X Art':
        curID = PAutils.Encode('/videos/i_love_x-art')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='I Love X-Art [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Clean  Wet':
        curID = PAutils.Encode('/videos/clean_&_wet')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Clean & Wet [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Erotic Stretching  Sex':
        curID = PAutils.Encode('/videos/erotic_stretching_&_sex')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Erotic Stretching & Sex [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Dont Keep Me Waiting Part 1':
        curID = PAutils.Encode('/videos/dont_keep_me_waiting__part_1')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Don\'t Keep Me Waiting - Part 1 [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Dont Keep Me Waiting Part 2':
        curID = PAutils.Encode('/videos/dont_keep_me_waiting__part_2')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Don\'t Keep Me Waiting - Part 2 [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Luminated Sexual Emotions':
        curID = PAutils.Encode('/videos/luminated_(sexual)_emotions')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Luminated (Sexual) Emotions [X-Art]', score=101, lang=lang))
    elif searchTitle == '4 Way in 4k':
        curID = PAutils.Encode('/videos/4way_in_4k')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='4-Way in 4K [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Cut Once More Please':
        curID = PAutils.Encode('/videos/cut!_once_more_please!')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Cut! Once More Please! [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Fine Finger Fucking':
        curID = PAutils.Encode('/videos/fine_fingerfucking')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Fine Finger-Fucking [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Skin Tillating Sex for Three':
        curID = PAutils.Encode('/videos/skintillating_sex_for_three')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Skin-Tillating Sex For Three [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Angelica Hotter Than Ever':
        curID = PAutils.Encode('/videos/angelicahotter_than_ever')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Angelica~Hotter Than Ever [X-Art]', score=101, lang=lang))
    elif searchTitle == 'Domination Part 1':
        curID = PAutils.Encode('/videos/domination__part_1')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='Domination - Part 1 [X-Art]', score=101, lang=lang))
    elif searchTitle == 'The Rich Girl Part One':
        curID = PAutils.Encode('/videos/the_rich_girl_-_part_one')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='The Rich Girl - Part One [X-Art]', score=101, lang=lang))
    elif searchTitle == 'The Rich Girl Part Two':
        curID = PAutils.Encode('/videos/the_rich_girl_-_part_two')
        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='The Rich Girl - Part Two [X-Art]', score=101, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
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
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
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
        '//div[@class="gallery-item"]//img/@src',
        '//img[contains(@src, "/videos")]/@src',
        '//section[@id="product-gallery"]//img/@data-src'
    ]
    for xpath in xpaths:
        for poster in detailsPageElements.xpath(xpath):
            poster.replace(' ', '_')

            art.append(poster)

    # Extra Posters
    art_ext = []
    match = 0

    for site in ['XartFan.com', 'HQSluts.com', 'ImagePost.com', 'CoedCherry.com/pics', 'Nude-Gals.com']:
        fanSite = PAextras.getFanArt(site, art_ext, actors, actorName, metadata.title.strip(), match, PAsearchSites.getSearchSiteName(siteID))
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
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.google.com'})
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
