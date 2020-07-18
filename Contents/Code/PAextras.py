import PAutils

# Scenes with No matches but will get false match
noMatch = [None] * 26
noMatch[0] = ['Close to The Edge']
noMatch[1] = ['After Sunset']
noMatch[2] = ['No Turning Back Part Two']
noMatch[3] = ['Dont Keep Me Waiting  Part 2']
noMatch[4] = ['Drinks for 2']
noMatch[5] = ['From 3 to 4 part 1']
noMatch[6] = ['Girlfriends']
noMatch[7] = ['Intimo']
noMatch[8] = ['Perfect Girls']
noMatch[9] = ['Stairway to Heaven']
noMatch[10] = ['Through the Looking Glass']
noMatch[11] = ['For your Enyes Only']
noMatch[12] = ['Like the First Time']
noMatch[13] = ['Little Play Thing']
noMatch[14] = ['Lovers Quarrel']
noMatch[15] = ['No Turning Back Part One']
noMatch[16] = ['Private Tutor']
noMatch[17] = ['Red Hot Christmas']
noMatch[18] = ['Young Passion']
noMatch[19] = ['Classic beauty']
noMatch[20] = ['If Only']
noMatch[21] = ['Poolside Pleasure']
noMatch[22] = ['She Bad']
noMatch[23] = ['The Rich Girl - part one']
noMatch[24] = ['She Cums in Colors']
noMatch[25] = ['Hot Fitness Sex']


# Scenes with incorrect matches
# if actorName needs fixing replace second field with correct name
badMatch = [None] * 61
badMatch[0] = ['Twice The Fun', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/aubrey-in-twice-the-fun-7688.html']
badMatch[1] = ['Party of Three', None, 'XartFan.com', 'https://xartfan.com/party-of-three/']
badMatch[2] = ['Fun for Three', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/angelica-heidi-in-fun-for-three-5994.html']
badMatch[3] = ['One Show For Each', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/katherine-angelica-in-one-show-for-each-7018.html']
badMatch[4] = ['Fucking Goddesses', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/caprice-angelica-in-fucking-goddesses-6814.html']
badMatch[5] = ['Should Have Seen Your Face', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/jenna-aubrey-in-should-have-seen-your-face-7719.html']
badMatch[6] = ['The Sleepover', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/leila-caprice-angelica-in-the-sleepover-3879.html']
badMatch[7] = ['Three in the Morning', None, 'XartFan.com', 'https://xartfan.com/x-art-francesca-caprice-tiffany-suite-19/']
badMatch[8] = ['Triple Play', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/kenna-alex-grey-blake-in-triple-play-8281.html']
badMatch[9] = ['Tropical Fantasy', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/leila-caprice-in-tropical-fantasy-1974.html']
badMatch[10] = ['Alex Greys First Lesbian Experience', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/aubrey-alex-grey-in-first-lesbian-experience-8196.html']
badMatch[11] = ['Come to me now', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/naomi-the-red-fox-in-come-to-me-now-5971.html']
badMatch[12] = ['Above the Air', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/addison-c-in-above-the-air-8148.html']
badMatch[13] = ['Back for More', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/aubrey-in-back-for-more-7389.html']
badMatch[14] = ['Bound By Desire', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/aubrey-in-bound-by-desire-8228.html']
badMatch[15] = ['Deep inside Gina', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/gina-in-deep-inside-gina-9700.html']
badMatch[16] = ['Double Tease', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/caprice-in-double-tease-5957.html']
badMatch[17] = ['Hot Coffee', None, 'XartFan.com', 'https://xartfan.com/hot-cofee-with-alina-edward']
badMatch[18] = ['Into The Lions Mouth', None, 'XartFan.com', 'https://xartfan.com/x-art-cayla-into-the-lions-mouth']
badMatch[19] = ['Just Watch Part 2', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/kate-in-just-watch-part-ii-6206.html']
badMatch[20] = ['Raw Passion', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/scarlet-in-raw-passion-5982.html']
badMatch[21] = ['Sneaking In', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/angelica-in-sneaking-in-4495.html']
badMatch[22] = ['The Studio Part II', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/angelica-in-the-studio-part-ii-7558.html']
badMatch[23] = ['They Meet Again', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/silvie-in-they-meet-again-4932.html']
badMatch[24] = ['Together Again', None, 'XartFan.com', 'https://xartfan.com/x-art-baby-waking-up-from-a-dream/']
badMatch[25] = ['Heaven Sent', 'XartFan.com', None, 'https://xartfan.com/x-art-ivy-dare-to-dream/']
badMatch[26] = ['Angelica Means Angel', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/angelica-in-angelica-means-angel-6456.html']
badMatch[27] = ['Big Toy Orgasm Video', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/carlie-in-big-toy-orgasm-588.html']
badMatch[28] = ['Fashion Fantasy', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/mila-k-in-fashion-fantasy-7460.html']
badMatch[29] = ['Girl in a Room', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/mila-k-in-girl-in-a-room-4499.html']
badMatch[30] = ['I will See You In the Morning', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/tiffany-in-i-will-see-you-in-the-morning-5690.html']
badMatch[31] = ['Just Watch Part 1', None, 'XartBeauties.com/galleries', 'http://www.xartbeauties.com/galleries/kate-in-just-watch-part-i-6432.html']
badMatch[32] = ['A Pleasing Pussy', 'Rebel Lynn', 'HQSluts.com', 'https://www.hqsluts.com/Rebel+Lynn+-+A+Pleasing+Pussy-404357/']
badMatch[33] = ['Little Firecracker', 'Ariela', 'HQSluts.com', 'https://www.hqsluts.com/Ariela+B+-+Little+Firecracker-400815/']
badMatch[34] = ['Close Shave', None, 'HQSluts.com', 'https://www.hqsluts.com/Ivy+Wolfe+-+Close+Shave-405025/']
badMatch[35] = ['Slippery Pool Sex', None, 'ImagePost.com', 'https://www.imagepost.com/videos/rebel-lynn-on-lubed-in-slippery-pool-sex/']
badMatch[36] = ['Lubed For St. Patty’s Day', None, 'ImagePost.com', 'https://www.imagepost.com/movies/katie-kush-on-lubed-in-st-pattys-day/']
badMatch[37] = ['Busy GF? At Least Stepmom Wants To Fuck!', None, 'SkeetScenes.com', 'https://skeetscenes.com/video/Fucking%20Stepmom%20Like%20Its%20A%20Game/i60021/']
badMatch[38] = ['Fucking My Mothers Sisters Husband (?!)', None, 'TeamSkeetFans.com', 'https://teamskeetfans.com/family-strokes-averie-moore-fucking-mothers-sisters-husband/']
badMatch[39] = ['The Secrets Of Seduction', None, 'TeamSkeetFans.com', 'https://teamskeetfans.com/family-strokes-gia-vendetti-in-the-secrets-of-seduction/']
badMatch[40] = ['The Sex Crazed Stepkids', None, 'SkeetScenes.com', 'http://skeetscenes.com/video/The%20Sex%20Crazed%20Stepkids/i68557/']
badMatch[41] = ['What Mommy Says Daughter Performs!', None, 'SkeetScenes.com', 'http://skeetscenes.com/video/Following%20Stepmoms%20Instructions/i59185/']
badMatch[42] = ['Stepdad Zaps Stepdaughter\'s Pussy', None, 'ImagePost.com', 'https://www.imagepost.com/videos/jada-doll-on-spy-fam/']
badMatch[43] = ['Stepsister Walks In On Stepbro Jerkin It', None, 'ImagePost.com', 'https://www.imagepost.com/videos/natalia-nix-on-spy-fame-walking-in-on-step-brother/']
badMatch[44] = ['Purely Perfect Pink', None, 'XartFan.com', 'https://xartfan.com/naomi-b-purely-perfect-pink/']
badMatch[45] = ['Thinking of You', None, 'Nude-Gals.com', 'https://nude-gals.com/photoshoot.php?photoshoot_id=22220']
badMatch[46] = ['Sexy movies Cum Inside', None, 'Nude-Gals.com', 'https://nude-gals.com/photoshoot.php?photoshoot_id=22652']
badMatch[47] = ['Hot Fucking with Sexy Sybil and Jake', None, 'Nude-Gals.com', 'https://nude-gals.com/photoshoot.php?photoshoot_id=22850']
badMatch[48] = ['New Year’s Party', None, 'ImagePost.com', 'https://www.imagepost.com/movies/scarlett-bloom-on-passion-hd-in-new-years-party/']
badMatch[49] = ['Couch Coach', None, 'ImagePost.com', 'https://www.imagepost.com/videos/jada-doll-couch-coach-passion-hd/']
badMatch[50] = ['Honey, I’m Home', None, 'ImagePost.com', 'https://www.imagepost.com/movies/kyler-quinn-on-passion-hd-in-honey-im-home/']
badMatch[51] = ['A Stepdaughter’s Gift', None,  'ImagePost.com', 'https://www.imagepost.com/videos/emily-willis-on-passion-hd-in-a-stepdaughters-gift/']
badMatch[52] = ['Picnic At The Park', None, 'ImagePost.com', 'https://www.imagepost.com/videos/emily-willis-on-passion-hd-in-picnic-at-the-park/']
badMatch[53] = ['Horny StepDaughter Begs StepDad To Make Her Cum', None, 'ImagePost.com', 'https://www.imagepost.com/movies/mia-collins-on-spy-fam-begs-stepdad-to-make-her-cum/']
badMatch[54] = ['Dear Diary: Stepsister’s Confessions', None, 'CoedCherry.com/pics', 'https://www.coedcherry.com/pics/jenni-jordan-dear-diary---stepsisters-confession']
badMatch[55] = ['Horny Stepsis Gets Stepbro To Massage Her Pussy', None, 'CoedCherry.com/pics', 'https://www.coedcherry.com/pics/charity-crawford-puts-out-stepbro']
badMatch[56] = ['Injured Stepbro Needs Sexual Healing', None, 'CoedCherry.com/pics', 'https://www.coedcherry.com/pics/eliza-ibarra-injuured-stepbro-needs-sexual-healing']
badMatch[57] = ['New Years Resolution: Blackmail Stepsister', None, 'CoedCherry.com/pics', 'https://www.coedcherry.com/pics/adriana-chechik-new-years-resolution-blackmail-stepbro']
badMatch[58] = ['Stepbro Shocked By Stepsister’s Wet Pussy', None, 'CoedCherry.com/pics', 'https://www.coedcherry.com/pics/emma-starletto-bangs-stepbro']
badMatch[59] = ['Stepdaughter Caught Stealing Easter Egg Money', None, 'CoedCherry.com/pics', 'https://www.coedcherry.com/pics/allie-nicole-stepdaughter-caught-stealing']
badMatch[60] = ['Stepsisters Sexual Message', None, 'CoedCherry.com/pics', 'https://www.coedcherry.com/site/sis-loves-me/pics/hot-coed-autumn-belle-has-pov-sex-with-stepbrother']


def getNoMatchID(scene):
    matchID = 0
    for match in noMatch:
        if scene.lower().replace(' ', '').replace('\'', '').replace('’', '').replace('\\', '').replace('&', 'and').replace(',', '').strip() == match[0].lower().replace(' ', '').replace('\'', '').replace('’', '').replace('&', 'and').replace(',', '').strip():
            Log('Title Registered as having no fansite matches.')
            return 0

        matchID += 1
    return 9999


def getBadMatchID(scene):
    badID = 0
    for match in badMatch:
        if scene.lower().replace(' ', '').replace('\'', '').replace('\\', '').replace('&', 'and').strip() == match[0].lower().replace(' ', '').replace('\'', '').replace('&', 'and').strip():
            overrideActor = badMatch[badID][1]
            overrideSite = badMatch[badID][2]
            overrideURL = badMatch[badID][3]
            return [overrideActor, overrideSite, overrideURL]
        badID += 1
    return 9999


# HQ Sluts Fansite Search
def getFanArt(site, art, actors, actorName, title, match, siteName):

    summary = ''
    actress = 'notarealperson'
    validSites = ['AnalPornFan.com', 'CoedCherry.com/pics', 'EroticBeauties.net/pics', 'HQSluts.com', 'ImagePost.com', 'LubedFan.com', 'Nude-Gals.com', 'PassionHDFan.com', 'PinkWorld.com', 'PornGirlsErotica.com', 'SkeetScenes.com', 'SpyFams.com', 'TeamSkeetFans.com', 'Tiny4KFan.com', 'XartBeauties.com/galleries', 'XartFan.com']
    backupMatch = match

    if site not in validSites:
        Log('CAUTION: ' + site + ' is not an accepted PAextras search term. Sites are case sensitive: PassionHDFan.com is acceptable, Passionhdfan.com is not.')
        return (art, summary, match)

    overrideSettings = getBadMatchID(title)

    if getNoMatchID(title) == 9999:
        try:
            if match is 0 or match is 2:
                urls = PAutils.getFromGoogleSearch(actorName + ' ' + title, site, stop=2)
                if overrideSettings != 9999:
                    urls = [None] * 1
                    urls[0] = ['test.com']
                # coed cherry needs extra help
                elif site == 'CoedCherry.com/pics':
                    cherryurls = []
                    # include any original google matches
                    try:
                        cherryurls.append(urls[0])
                    except:
                        Log('no good')
                        pass
                    # try direct match
                    temp = ('https://' + site + '/' + actorName + ' ' + title.replace('’', '').replace('\'', '').replace(':', '')).replace(' ', '-')
                    Log('DirectURL: ' + temp)
                    cherryurls.append(temp)
                    # built-in site search
                    try:
                        searchurl = ('https://' + site + '/search/' + actorName + ' ' + title.replace('’', '').replace('\'', '').split(':')[0]).replace(' ', '+')
                        Log('SearchURL: ' + searchurl)
                        req = PAutils.HTTPRequest(searchurl)
                        searchPageElements = HTML.ElementFromString(req.text)
                        for result in searchPageElements.xpath('//div[@class="thumbs "]//a'):
                            cherryurls.append(result.get('href'))
                    except:
                        pass
                    # actor search match
                    try:
                        for sitename in ['Cum 4K', 'Passion HD', 'Spy Fam', 'Tiny 4K']:
                            if sitename.lower().replace(' ', '').replace('-', '') == siteName.lower().replace(' ', '').replace('-', ''):
                                break
                            else:
                                sitename = siteName
                        searchurl = ('https://' + site + '/search/' + actorName + ' ' + sitename + '?sort=newest').replace(' ', '+')
                        Log('SearchURL: ' + searchurl)
                        req = PAutils.HTTPRequest(searchurl)
                        searchPageElements = HTML.ElementFromString(req.text)
                        for result in searchPageElements.xpath('//div[@class="thumbs "]//a'):
                            result = result.get('href')
                            cherryurls.append(result)
                    except:
                        pass

                    urls = cherryurls

                for url in urls:
                    if match is 0 or match is 2:
                        if overrideSettings != 9999:
                            site = overrideSettings[1]
                            url = overrideSettings[2]
                            Log('Title known for bad fan match. URL/actress set manually.')
                            if overrideSettings[0] is not None:
                                actress = overrideSettings[0]
                                actorName = actress

                            # found one example of a badmatch not working because the actress match failed. this forces it to proceed.
                            match = 1
                            backupmatch = match

                        try:
                            googleSearchURL = url
                            req = PAutils.HTTPRequest(sceneURL)
                            fanPageElements = HTML.ElementFromString(req.text)
                        except:
                            pass

                        try:
                            if overrideSettings == 9999:
                                # Determine where to look for the Actor Name/s
                                try:
                                    if site in ['AnalPornFan.com', 'PassionHDFan.com', 'LubedFan.com', 'Tiny4KFan.com']:
                                        nameinheader = fanPageElements.xpath('//div[@class="page-title pad group"]//a[not(contains(@href, "respond"))][not(contains(@href, "comments"))]/text()')
                                    elif site == 'CoedCherry.com/pics':
                                        nameinheader = fanPageElements.xpath('//div[@class="models"]//figcaption/text()')
                                    elif site == 'EroticBeauties.net/pics':
                                        nameinheader = fanPageElements.xpath('//div[@class="clearfix"]//a[contains(@href, "model")]/text()')
                                    elif site == 'HQSluts.com':
                                        nameinheader = fanPageElements.xpath('//p[@class="details"]//a[contains(@href, "sluts")]/text()')
                                    elif site == 'ImagePost.com':
                                        try:
                                            nameinheader = fanPageElements.xpath('//h3/a[contains(@href, "star")]/text()')
                                        except:
                                            pass
                                        if len(nameinheader) < 1:
                                            try:
                                                nameinheader = fanPageElements.xpath('//h3//strong/text()')
                                            except:
                                                pass
                                    elif site == 'Nude-Gals.com':
                                        nameinheader = fanPageElements.xpath('//div[@class="row photoshoot-title row_margintop"]//a[contains(@href, "model")]/text()')
                                    elif site == 'PinkWorld.com':
                                        nameinheader = fanPageElements.xpath('//div[@class="clearfix"]//a[contains(@href, "pornstar")]/text()')
                                    elif site == 'PornGirlsErotica.com':
                                        nameinheader = fanPageElements.xpath('//h2[@class="title"]')[0].text_content()
                                    elif site == 'SkeetScenes.com':
                                        nameinheader = fanPageElements.xpath('//div[@class="card-body"]//h1/a[contains(@href, "model")]')
                                    elif site in ['SpyFams.com', 'TeamSkeetFans.com']:
                                        nameinheader = fanPageElements.xpath('//span[@itemprop="articleSection"][not(contains(text(), "Family"))][not(contains(text(), "Sis Loves Me"))]/text()')
                                        if nameinheader == 'Uncategorized' or nameinheader[0].text_content() == 'Uncategorized' or nameinheader[0] == 'Uncategorized':
                                            Log('Uncategorized name found, checking against title!')
                                            fanTitle = fanPageElements.xpath('//h1/text()')[0].strip()
                                            if actorName in fanTitle:
                                                nameinheader = actorName
                                            elif actress in fanTitle:
                                                nameinheader = actress
                                    elif site == 'XartBeauties.com/galleries':
                                        nameinheader = fanPageElements.xpath('//a[contains(@href, "models")][not(contains(text(), "Models"))]/text()')
                                    elif site == 'XartFan.com':
                                        nameinheader = fanPageElements.xpath('//header[@class="entry-header"]/p//a//text()')

                                    if len(nameinheader) <= 1:
                                        try:
                                            nameinheader = nameinheader[0].text_content()
                                        except:
                                            nameinheader = nameinheader[0]
                                        Log('Actress name in fansite header: ' + nameinheader)
                                    else:
                                        Log('Actress names in fansite header: ' + str(nameinheader))
                                except:
                                    Log('No Actress found in the fansite header')

                            # CHECK IF WE HAVE A FANSITE MATCH USING ACTOR NAMES
                                if actorName.lower() in nameinheader.lower() or actress.lower() in nameinheader.lower():
                                    Log('Fansite Match Found on ' + site)
                                    match = 1
                                else:
                                    # When there are multiple actors listed we need to check all of them.
                                    try:
                                        for actorLink in actors:
                                            if site == 'TeamSkeetFans.com':
                                                actorName = actorLink
                                            else:
                                                actorName = actorLink.text_content().strip()
                                            try:
                                                Log(actorName + ' vs ' + nameinheader)
                                            except:
                                                pass

                                            try:
                                                if actorName.lower() in nameinheader.lower() or actress.lower() in nameinheader.lower():
                                                    Log(site + ' Fansite Match Found')
                                                    match = 1
                                                    break
                                            except:
                                                pass
                                            try:
                                                for name in nameinheader:
                                                    if match is 1:
                                                        break
                                                    Log('Comparing with: ' + actorName)
                                                    if actorName.lower() in name.lower() or actress.lower() in name.lower():
                                                        Log(site + ' Fansite Match Found')
                                                        match = 1
                                                        break
                                            except:
                                                pass
                                    except:
                                        Log('No Actress Match')

                                if match is 1:
                                    # try to avoid bad matches based on title check also
                                    try:
                                        if site in ['AnalPornFan.com', 'LubedFan.com', 'PassionHDFan.com', 'Tiny4KFan.com']:
                                            fanTitle = fanPageElements.xpath('//h1[@class= "post-title"]/text()')[0].strip()
                                        elif site == 'CoedCherry.com/pics':
                                            fanTitle = url.split('/')[-1].replace('-', ' ')
                                        elif site == 'EroticBeauties.net/pics':
                                            fanTitle = fanPageElements.xpath('//div[contains(@class, "gallery-title")]/h1/text()')[0].strip()
                                        elif site == 'HQSluts.com':
                                            fanTitle = fanPageElements.xpath('//p[@class="desc"]/span/text()')[0].strip()
                                        elif site == 'ImagePost.com':
                                            fanTitle = fanPageElements.xpath('//h1/text()')[0].strip()
                                        elif site == 'Nude-Gals.com':
                                            fanTitle = fanPageElements.xpath('//h1/small/text()')[0].strip()
                                        elif site in ['SpyFams.com', 'TeamSkeetFans.com']:
                                            fanTitle = fanPageElements.xpath('//h1/text()')[0].strip()
                                        elif site == 'PinkWorld.com':
                                            fanTitle = fanPageElements.xpath('//h1/text()')[0].strip()
                                        elif site == 'PornGirlsErotica.com':
                                            fanTitle = fanPageElements.xpath('//h2[@class="title"]/text()')[0].strip()
                                        elif site == 'SkeetScenes.com':
                                            fanTitle = fanPageElements.xpath('//h1/text()')[0].strip()
                                        elif site == 'XartBeauties.com/galleries':
                                            fanTitle = fanPageElements.xpath('//div[@id="header-text"]/p[not(@class="promo")]/text()')[0].strip()
                                        elif site == 'XartFan.com':
                                            fanTitle = fanPageElements.xpath('//h1/text()')[0].strip()

                                        Log(title.strip() + ' vs ' + str(fanTitle))
                                        # try percentage calculation of how many words match
                                        a = [x for x in title.replace('’', '').replace('\'', '').replace(':', '').replace(',', '').strip().lower().split(' ')]
                                        b = [x for x in fanTitle.replace('’', '').replace('\'', '').replace(':', '').replace(',', '').strip().lower().split(' ')]
                                        c = len(a)
                                        count = 0
                                        for word in a:
                                            if word in b:
                                                Log(word)
                                                count += 1
                                        percentage = (float(count) / float(c)) * 100
                                        Log('Percentage of words that match: %s' % percentage)
                                        threshold = 40

                                        if not title.strip().lower() in str(fanTitle).lower() and not title.replace('’', '').replace('\'', '').replace(':', ' -').strip().lower() in str(fanTitle).lower() and percentage < threshold:
                                            Log('Title Mismatch: ' + str(fanTitle))
                                            match = backupMatch
                                        # coedCherry titles are often poor, try to confirm site also
                                        # if site == 'CoedCherry.com/pics':
                                        #    fanTitle = fanPageElements.xpath('//div[@class= 'paysite_link ']/a/text()').replace('Continue to ', '').replace(' ', '').split()
                                        #    if fanTitle == Originalsite?

                                    except:
                                        Log('Something went wrong when trying to compare scene title:')
                                        Log(str(fanTitle))

                            # POSTERS
                            if match is 1:
                                try:
                                    # Various Poster xpaths needed for different sites
                                    Log('Searching ' + site)
                                    if site in ['AnalPornFan.com', 'LubedFan.com']:
                                        for posterURL in fanPageElements.xpath('//div[contains(@class, "rgg-imagegrid")]//a'):
                                            art.append(posterURL.get('href'))
                                    elif site == 'CoedCherry.com/pics':
                                        for posterURL in fanPageElements.xpath('//div[@class="thumbs "]//a[@class="track"]'):
                                            art.append(posterURL.get('href'))
                                    elif site == 'EroticBeauties.net/pics':
                                        for posterURL in fanPageElements.xpath('//div[contains(@class, "my-gallery")]//a'):
                                            art.append(posterURL.get('href'))
                                    elif site == 'HQSluts.com':
                                        for posterURL in fanPageElements.xpath('//li[@class="item i"]//a'):
                                            art.append(posterURL.get('href'))
                                    elif site == 'ImagePost.com':
                                        counter = 1
                                        try:
                                            for posterURL in fanPageElements.xpath('//div[@id="theGallery"]//a'):
                                                sceneTypeSegment = str(googleSearchURL.split('/')[-3:-2]).split('\'')[1]
                                                sceneTitleSegment = str(googleSearchURL.split('/')[-2:-1]).split('\'')[1]
                                                if counter > 9:
                                                    finalurl = 'https://www.imagepost.com/' + str(sceneTypeSegment) + '/' + str(sceneTitleSegment) + '/' + str(sceneTitleSegment) + '-' + '0' + str(counter) + '.jpg'
                                                else:
                                                    finalurl = 'https://www.imagepost.com/' + str(sceneTypeSegment) + '/' + str(sceneTitleSegment) + '/' + str(sceneTitleSegment) + '-' + '00' + str(counter) + '.jpg'
                                                art.append(str(finalurl))
                                                counter += 1
                                        except:
                                            Log('Issue Creating Image URL')
                                    elif site == 'Nude-Gals.com':
                                        for posterURL in fanPageElements.xpath('(//div[@class="row row_margintop"]//a)[not(contains(@title, "#"))]'):
                                            art.append('https://nude-gals.com/' + posterURL.get('href'))
                                    elif site in ['PassionHDFan.com', 'SpyFams.com', 'TeamSkeetFans.com', 'Tiny4KFan.com']:
                                        for posterURL in fanPageElements.xpath('//div[contains(@class, "tiled-gallery")]//a/img'):
                                            art.append(posterURL.get('data-orig-file'))
                                    elif site == 'PinkWorld.com':
                                        for posterURL in fanPageElements.xpath('//div[contains(@class, "my-gallery")]//a'):
                                            art.append(posterURL.get('href'))
                                    elif site == 'PornGirlsErotica.com':
                                        for posterURL in fanPageElements.xpath('//div[@class="ngg-galleryoverview"]//a'):
                                            art.append(posterURL.get('href'))
                                    elif site == 'SkeetScenes.com':
                                        Log('here')
                                        for posterURL in fanPageElements.xpath('//div[@class="row"]/div[contains(@class, "col-xl-2")]//img'):
                                            Log('here')
                                            artlink = 'https:' + posterURL.get('data-srcset').replace('_thumb', '').replace('.webp', '.jpg')
                                            Log(artlink)
                                            art.append(artlink)
                                    elif site == 'XartBeauties.com/galleries':
                                        for posterURL in fanPageElements.xpath('//div[@id="gallery-thumbs"]//img'):
                                            art.append(posterURL.get('src').replace('images.', 'www.').replace('/tn', ''))
                                    elif site == 'XartFan.com':
                                        for posterURL in fanPageElements.xpath('//div[contains(@class, "tiled-gallery")]//a//img'):
                                            art.append(posterURL.get('data-orig-file').replace('images.', ''))
                                except:
                                    Log('No Images Found')

                            Log('Artwork found: ' + str(len(art)))
                            if len(art) < 9 and match is 1 and overrideSettings == 9999:
                                match = 2

                        except:
                            Log('No Fan site Match')

                        if match is 1 or match is 2:
                            # Summary
                            try:
                                if site in ['AnalPornFan.com', 'LubedFan.com', 'PassionHDFan.com', 'Tiny4KFan.com']:
                                    summary = fanPageElements.xpath('//div[@class="entry-inner"]//p')[0].text_content().replace('---->Click Here to Download<----', '').replace('Click Here for More Wet & Oiled Up Sex!', '').strip()
                                elif site == 'ImagePost.com':
                                    summary = fanPageElements.xpath('//div[@class="central-section-content"]/p')[0].text_content().strip()
                                elif site == 'SpyFams.com':
                                    paragraphs = fanPageElements.xpath('(//div[@class="entry-content g1-typography-xl"]//p)[not(*[contains(@class, "jp-relatedposts-post")])]')
                                    if len(paragraphs) > 3:
                                        pNum = 1
                                        for paragraph in paragraphs:
                                            if pNum >= 1 and pNum <= 7:
                                                summary = summary + '\n\n' + paragraph.text_content()
                                            pNum += 1
                                        summary = summary.strip()
                                    else:
                                        summary = fanPageElements.xpath('(//div[@class="entry-content g1-typography-xl"]//p)[position()=1]')[0].text_content().strip()
                                elif site == 'TeamSkeetFans.com':
                                    paragraphs = fanPageElements.xpath('//div[@class="entry-content g1-typography-xl"]')[0].text_content().split('\n')
                                    if len(paragraphs) > 13:
                                        for paragraph in paragraphs:
                                            summary = (summary + '\n\n' + paragraph).replace('LinkEmbedCopy and paste this HTML code into your webpage to embed.', '').replace('CLICK HERE FOR MORE FAMILY STROKES', '').replace('--> Click Here for More Sis Loves Me! <--', '').strip()
                                    else:
                                        summary = fanPageElements.xpath('(//div[@class="entry-content g1-typography-xl"]//p)[position()=1]')[0].text_content().strip()
                            except:
                                Log('Error grabbing fansite summary')
        except:
            Log('No Fansite Match')
    return (art, summary, match)
