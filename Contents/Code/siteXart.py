import PAsearchSites
import PAgenres
import PAextras
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    xartpost = {
        "input_search_sm" : encodedTitle
    }
    searchResults = HTML.ElementFromURL('https://www.x-art.com/search/', values = xartpost)

    for searchResult in searchResults.xpath('//a[contains(@href,"videos")]'):
        link = searchResult.xpath('.//img[contains(@src,"videos")]')
        if len(link) > 0:
            if link[0].get("alt") is not None:
                
                titleNoFormatting = link[0].get("alt").strip()
                releaseDate = parse(searchResult.xpath('.//h2[2]')[0].text_content().strip()).strftime('%Y-%m-%d')
                curID = searchResult.get("href")[21:]
                curID = curID.replace('/','+')
                Log(str(curID))
                if searchDate:
                    score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
                else:
                    score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())
                results.Append(MetadataSearchResult(id=curID + "|" + str(siteNum), name=titleNoFormatting + " [X-Art] " + releaseDate, score=score, lang=lang))

    if searchTitle == "Naughty  Nice":
        Log("Manual Search Match")
        curID = ("/videos/Naughty_&_Nice")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Naughty & Nice" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Out Of This World":
        Log("Manual Search Match")
        curID = ("/videos/Out_of_This_World")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Out Of This World" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Beautiful Girl":
        Log("Manual Search Match")
        curID = ("/videos/beautiful_girl")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Beautiful Girl" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Sunset":
        Log("Manual Search Match")
        curID = ("/videos/sunset")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Sunset" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Cum Like Crazy":
        Log("Manual Search Match")
        curID = ("/videos/cum_like_crazy")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Cum Like Crazy" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Tenderness":
        Log("Manual Search Match")
        curID = ("/videos/tenderness")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Tenderness" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "My Love":
        Log("Manual Search Match")
        curID = ("/videos/my_love")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "My Love" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Dream Girl":
        Log("Manual Search Match")
        curID = ("/videos/dream_girl")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Dream Girl" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Mutual Orgasm":
        Log("Manual Search Match")
        curID = ("/videos/mutual_orgasm")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Mutual Orgasm" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Delicious":
        Log("Manual Search Match")
        curID = ("/videos/delicious")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Delicious" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Girlfriends":
        Log("Manual Search Match")
        curID = ("/videos/girlfriends")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Girlfriends" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Just for You":
        Log("Manual Search Match")
        curID = ("/videos/just_for_you")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Just for You" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "True Love":
        Log("Manual Search Match")
        curID = ("/videos/true_love")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "True Love" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Intimate":
        Log("Manual Search Match")
        curID = ("/videos/intimate")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Intimate" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "One  Only Caprice":
        Log("Manual Search Match")
        curID = ("/videos/one_&_only_caprice")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "One & Only Caprice" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "In Bed":
        Log("Manual Search Match")
        curID = ("/videos/in_bed")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "In Bed" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Angelic":
        Log("Manual Search Match")
        curID = ("/videos/angelic")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Angelic" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Her First Time":
        Log("Manual Search Match")
        curID = ("/videos/her_first_time")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Her First Time" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Out of This World":
        Log("Manual Search Match")
        curID = ("/videos/out_of_this_world")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Out of This World" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Want You":
        Log("Manual Search Match")
        curID = ("/videos/want_you")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Want You" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Awakening":
        Log("Manual Search Match")
        curID = ("/videos/Awakening")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Awakening" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Warm  Fuzzy Little Miracles":
        Log("Manual Search Match")
        curID = ("/videos/warm_&_fuzzy_(little_miracles)")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Warm & Fuzzy (Little Miracles)" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Blindfold Me  Tie Me Up":
        Log("Manual Search Match")
        curID = ("/videos/blindfold_me_&_tie_me_up")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Blindfold Me & Tie Me Up" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "First  Forever":
        Log("Manual Search Match")
        curID = ("/videos/first_&_forever")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "First & Forever" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Black  White":
        Log("Manual Search Match")
        curID = ("/videos/black_&_white")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Black & White" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Rendezvous":
        Log("Manual Search Match")
        curID = ("/videos/Rendezvous")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Rendezvous" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Watching":
        Log("Manual Search Match")
        curID = ("/videos/watching")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Watching" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "First Time":
        Log("Manual Search Match")
        curID = ("/videos/first_time")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "First Time" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Sapphically Sexy Fucking Lesbians":
        Log("Manual Search Match")
        curID = ("/videos/sapphically_sexy_(fucking_lesbians)")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Sapphically Sexy (Fucking Lesbians)" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Je M'appelle Belle":
        Log("Manual Search Match")
        curID = ("/videos/je_m_appelle_belle")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Je M'Appelle Belle" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Sparks":
        Log("Manual Search Match")
        curID = ("/videos/sparks")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Sparks" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Hot Orgasm":
        Log("Manual Search Match")
        curID = ("/videos/hot_orgasm")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Hot Orgasm" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Group Sex":
        Log("Manual Search Match")
        curID = ("/videos/group_sex")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Group Sex" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "A Cloudy Hot Day Mila's First Lesbian Experience":
        Log("Manual Search Match")
        curID = ("/videos/a_cloudy_hot_day_(mila's_first_lesbian_experience)")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "A Cloudy Hot Day (Mila's First Lesbian Experience)" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Our Little Cum Cottage":
        Log("Manual Search Match")
        curID = ("/videos/our_little_(cum)_cottage")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Our Little (Cum) Cottage" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Kacey Jordan Does X Art":
        Log("Manual Search Match")
        curID = ("/videos/kacey_jordan_does_x-art")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Kacey Jordan Does X-Art" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "X Art on Tv":
        Log("Manual Search Match")
        curID = ("/videos/x-art_on_tv")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "X-Art on TV" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Lily's First Time Lesbian Loving":
        Log("Manual Search Match")
        curID = ("/videos/lilys_firsttime_lesbian_loving")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Lily's First-time Lesbian Loving" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Cock Sucking  Fucking Competition":
        Log("Manual Search Match")
        curID = ("/videos/cock_sucking__fucking_competition")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Cock Sucking (& Fucking) Competition" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Beauty  the Beast Video":
        Log("Manual Search Match")
        curID = ("/videos/beauty_beast_video")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Beauty & the Beast Video" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Yoga Master  Student":
        Log("Manual Search Match")
        curID = ("/videos/yoga_master_&_teacher")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Yoga Master & Student" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "I Love X Art":
        Log("Manual Search Match")
        curID = ("/videos/i_love_x-art")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "I Love X-Art" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Clean  Wet":
        Log("Manual Search Match")
        curID = ("/videos/clean_&_wet")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Clean & Wet" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Erotic Stretching  Sex":
        Log("Manual Search Match")
        curID = ("/videos/erotic_stretching_&_sex")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Erotic Stretching & Sex" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Don't Keep Me Waiting Part 1":
        Log("Manual Search Match")
        curID = ("/videos/dont_keep_me_waiting__part_1")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Don't Keep Me Waiting - Part 1" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Don't Keep Me Waiting Part 2":
        Log("Manual Search Match")
        curID = ("/videos/dont_keep_me_waiting__part_2")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Don't Keep Me Waiting - Part 2" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Luminated Sexual Emotions":
        Log("Manual Search Match")
        curID = ("/videos/luminated_(sexual)_emotions")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Luminated (Sexual) Emotions" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "4 Way in 4k":
        Log("Manual Search Match")
        curID = ("/videos/4way_in_4k")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "4-Way in 4K" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Cut Once More Please":
        Log("Manual Search Match")
        curID = ("/videos/cut!_once_more_please!")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Cut! Once More Please!" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Fine Finger Fucking":
        Log("Manual Search Match")
        curID = ("/videos/fine_fingerfucking")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Fine Finger-Fucking" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Skin Tillating Sex for Three":
        Log("Manual Search Match")
        curID = ("/videos/skintillating_sex_for_three")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Skin-Tillating Sex For Three" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Angelica Hotter Than Ever":
        Log("Manual Search Match")
        curID = ("/videos/angelicahotter_than_ever")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Angelica~Hotter Than Ever" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "Domination Part 1":
        Log("Manual Search Match")
        curID = ("/videos/domination__part_1")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "Domination - Part 1" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "The Rich Girl Part One":
        Log("Manual Search Match")
        curID = ("/videos/the_rich_girl_-_part_one")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "The Rich Girl - Part One" + " [X-Art]", score = 101, lang = lang))
    if searchTitle == "The Rich Girl Part Two":
        Log("Manual Search Match")
        curID = ("/videos/the_rich_girl_-_part_two")
        curID = curID.replace('/','+')
        Log(str(curID))
        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = "The Rich Girl - Part Two" + " [X-Art]", score = 101, lang = lang))

    return results

def update(metadata,siteID,movieGenres,movieActors):
    Log('******UPDATE CALLED*******')
    temp = str(metadata.id).split("|")[0].replace('+','/')  

    url = PAsearchSites.getSearchBaseURL(siteID) + temp
    detailsPageElements = HTML.ElementFromURL(url)

    # Summary
    metadata.studio = "X-Art"
    paragraphs = detailsPageElements.xpath('//div[@class="small-12 medium-12 large-12 columns info"]//p')
    summary = ""
    for paragraph in paragraphs:
        summary = summary + '\n\n' + paragraph.text_content()
    metadata.summary = summary.strip()
    metadata.title = detailsPageElements.xpath('//div[@class="row info"]//div[@class="small-12 medium-12 large-12 columns"]')[0].text_content().strip()
    date = detailsPageElements.xpath('//h2')[2].text_content()[:-1]
    date_object = datetime.strptime(date, '%b %d, %Y')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    #Tagline and Collection(s)
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)
    
    # Genres
    movieGenres.clearGenres()
    # No Source for Genres, add manual
    movieGenres.addGenre("Artistic")
    movieGenres.addGenre("Glamorous")

    # Actors 
    movieActors.clearActors()
    actors = detailsPageElements.xpath('//h2//a')
    if len(actors) > 0:
        if len(actors) == 3:
            movieGenres.addGenre("Threesome")
        if len(actors) == 4:
            movieGenres.addGenre("Foursome")
        if len(actors) > 4:
            movieGenres.addGenre("Orgy")
        for actorLink in actors:
            actorName = actorLink.text_content()
            actorPageURL = actorLink.get("href")
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//img[@class="info-img"]')[0].get("src")
            movieActors.addActor(actorName,actorPhotoURL)


    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)
    thumbs = []
    try:
        for posterURL in detailsPageElements.xpath('//div[@class="gallery-item"]//img'):
            thumbs.append((posterURL.get('src')).replace(" ", "_"))
    except:
        Log("No Thumbnails found")
    background = detailsPageElements.xpath('//img[contains(@src,"/videos")]')[0].get("src")
    metadata.art[background] = Proxy.Preview(HTTP.Request(background).content, sort_order = 1)
    try:
        posterURL = str((thumbs[0]))[:-5] + "2.jpg"
    except:
        posterURL = background.replace("1.jpg", "2.jpg").replace("1-lrg.jpg", "2-lrg.jpg")
    metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL).content, sort_order = 1)


    #Extra Posters
    import random
    art=[]
    match = 0
    siteName = PAsearchSites.getSearchSiteName(siteID)
            
    for site in ["XartFan.com", "HQSluts.com", "ImagePost.com", "CoedCherry.com/pics", "Nude-Gals.com"]:
        fanSite = PAextras.getFanArt(site, art, actors, actorName, metadata.title.strip(), match, siteName)
        match = fanSite[2]
        if match is 1:	
            break
    #try:
        #art = thumbs
    #except:
        #pass
 
    if match is 1 or match is 2:
        # Return, first few, last one and randóm selection of images
        # If you want more or less posters edít the value in random.sample below or refresh metadata to get a different sample.	
        try:
            sample = [art[0], art[1], art[2], art[3], art[-1]] + random.sample(art, 4)     
            art = sample
            Log("Selecting subset of " + str(len(art)) + " images from the set.")
        except:
            pass
            
        try:
            j = 1
                                                              
            for posterUrl in art:
                Log("Trying next Image")
                Log(posterUrl)
                if not PAsearchSites.posterAlreadyExists(posterUrl,metadata):            
                #Download image file for analysis
                    try:
                        #hdr needed to get images from some fansites. No adverse effects seen so far.
                        hdr = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
                        req = urllib.Request(posterUrl, headers=hdr)
                        img_file = urllib.urlopen(req)
                        im = StringIO(img_file.read())
                        resized_image = Image.open(im)
                        width, height = resized_image.size
                        #Add the image proxy items to the collection
                        if width > 1 or height > width:
                            # Item is a poster
                            metadata.posters[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                        if width > 100 and width > height:
                            # Item is an art item
                            metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
                        j = j + 1
                    except:
                        Log("there was an issue")
                        #metadata.art[posterUrl] = Proxy.Preview(HTTP.Request(posterUrl, headers={'Referer': 'http://www.google.com'}).content, sort_order = j)
        except:
            pass

    return metadata
