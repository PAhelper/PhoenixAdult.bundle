import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    userID = searchTitle.split(' ', 1)[0]
    sceneTitle = searchTitle.split(' ', 1)[1]
    encodedTitle = urllib.quote(sceneTitle)

    url = PAsearchSites.getSearchSearchURL(siteNum) + userID + '/*/Cat0-AllCategories/Page1/SortBy-bestmatch/Limit50/search/' + encodedTitle
    req = PAutils.HTTPRequest(url)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="clipWrapper"]'):
        titleNoFormatting = searchResult.xpath('.//a[@class="clipTitleLink"]')[0].text_content().replace('(HD MP4)', '').replace('(WMV)', '').strip()
        curID = PAutils.Encode(searchResult.xpath('.//a[@class="clipTitleLink"]/@href')[0])
        subSite = searchResult.xpath('//title')[0].text_content().strip()

        score = 100 - Util.LevenshteinDistance(sceneTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [Clips4Sale/%s]' % (titleNoFormatting, subSite), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteID) + sceneURL
    userID = sceneURL.split('/')[-3]
    sceneID = sceneURL.split('/')[-2]
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    art = []
    movieGenres.clearGenres()
    movieActors.clearActors()

    # Title
    metadata.title = detailsPageElements.xpath('//div[@class="clipTitle"]')[0].text_content().replace('(HD MP4)', '').replace('(WMV)', '').strip()

    # Summary
    summary = detailsPageElements.xpath('//div[contains(@class, "dtext dheight")]')[0].text_content().strip()
    summary = summary.split('--SCREEN SIZE')[0].strip()  # K Klixen
    summary = summary.split('Description:')[1].split('window.NREUM')[0].replace('**TOP 50 CLIP**', '').replace('1920x1080 (HD1080)', '').strip()  # MHBHJ
    metadata.summary = summary

    # Studio
    metadata.studio = 'Clips4Sale'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = detailsPageElements.xpath('//title')[0].text_content().split('-')[0].strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="clearfix infoRow2 clip_details"]/div/div[2]/div[3]/span/span')[0].text_content().strip()[:-8]
    if date:
        date_object = datetime.strptime(date, '%m/%d/%y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors / Genres
    # Main Category
    cat = detailsPageElements.xpath('//div[@class="clipInfo clip_details"]/div[1]/a')[0].text_content().strip().lower()
    movieGenres.addGenre(cat)
    # Related Categories / Keywords
    genreList = []
    genres = detailsPageElements.xpath('//span[@class="relatedCatLinks"]/span/a')
    for genre in detailsPageElements.xpath('//span[@class="relatedCatLinks"]/span/a'):
        genreName = genre.text_content().strip().lower()

        genreList.append(genreName)
    # Add Actors

    #  CherryCrush
    if 'My cherry crush' in tagline:
        genreList.remove('cherry')
        genreList.remove('cherrycrush')

    #  Klixen
    elif 'KLIXEN' in tagline:
        actors = detailsPageElements.xpath('//div[@class="clipInfo clip_details"]/div[3]/span[2]/span/a')
        for actor in actors:
            actorName = str(actor.text_content().strip())
            actorPhotoURL = ''
            genreList.remove(actorName)
            movieActors.addActor(actorName, actorPhotoURL)

    #  AAA wicked
    elif 'AAA wicked' in tagline:
        if 'mistress candide' in genreList:
            movieActors.addActor('Mistress Candice', '')
            genreList.remove('mistress candice')

    #  Aballs and cock crushing sexbomb
    elif 'Aballs and cock crushing sexbomb' in tagline:
        if 'Alina' in metadata.title or 'Alina' in metadata.summary:
            movieActors.addActor('Mistress Alina', '')

    #  Adrienne Adora
    elif 'Adrienne Adora' in tagline:
        movieActors.addActor('Adrienne Adora', '')

    #  Amazon Goddess Harley
    elif 'Amazon Goddess Harley' in tagline:
        if 'goddess harley' in genreList:
            movieActors.addActor('Goddess Harley', '')
            genreList.remove('goddess harley')
        if 'amazon goddess harley' in genreList:
            movieActors.addActor('Goddess Harley', '')
            genreList.remove('amazon goddess harley')

    #  AnikaFall
    elif 'AnikaFall' in tagline:
        movieActors.addActor('Anika Fall', '')
        if 'anikafall' in genreList:
            movieActors.addActor('Anika Fall', '')
            genreList.remove('anikafall')
        if 'anika fall' in genreList:
            movieActors.addActor('Anika Fall', '')
            genreList.remove('anika fall')
        if 'goddess anika fall' in genreList:
            movieActors.addActor('Anika Fall', '')
            genreList.remove('goddess anika fall')

    #  Ashley Albans Fetish Fun
    elif 'Ashley Albans Fetish Fun' in tagline:
        if 'ashley alban' in genreList:
            movieActors.addActor('Ashley Alban', '')
            genreList.remove('ashley alban')

    #  AstroDomina
    elif 'AstroDomina' in tagline:
        if 'astrodomina' in genreList:
            movieActors.addActor('Astro Domina', '')
            genreList.remove('astrodomina')
        if 'Astrodomina' in metadata.title or 'AstroDomina' in metadata.title:
            movieActors.addActor('Astro Domina', '')
        if 'StellarLoving' in metadata.title:
            movieActors.addActor('Stellar Loving', '')

    #  Ball Busting Chicks
    elif 'Ball Busting Chicks' in tagline:
        if 'hera' in genreList:
            movieActors.addActor('Domina Hera', '')
            genreList.remove('hera')
        if 'amy' in genreList:
            movieActors.addActor('Domina Amy', '')
            genreList.remove('amy')

    #  Ballbusting World PPV
    elif 'Ballbusting World PPV' in tagline:
        if 'Tasha Holz' in metadata.summary or 'Tasha' in metadata.summary:
            movieActors.addActor('Tasha Holz', '')

    #  Best Latin ASS on the WEB!
    elif 'Best Latin ASS on the WEB!' in tagline:
        if 'goddess sandra' in genreList:
            movieActors.addActor('Sandra Latina', '')
            genreList.remove('goddess sandra')
        if 'sandra latina' in genreList:
            movieActors.addActor('Sandra Latina', '')
            genreList.remove('sandra latina')
        if 'latinsandra' in genreList:
            movieActors.addActor('Sandra Latina', '')
            genreList.remove('latinsandra')
        if 'latin sandra' in genreList:
            movieActors.addActor('Sandra Latina', '')
            genreList.remove('latin sandra')
        if 'latina sandra' in genreList:
            movieActors.addActor('Sandra Latina', '')
            genreList.remove('latina sandra')
        if 'hotwife sandra' in genreList:
            movieActors.addActor('Sandra Latina', '')
            genreList.remove('hotwife sandra')

    #  Bikini Blackmail Ballbust Lyne
    elif 'Bikini Blackmail Ballbust Lyne' in tagline:
        if 'princess lyne' in genreList.summary:
            movieActors.addActor('Princess Lyne', '')
            genreList.remove('princess lyne')

    #  Brat Doll Amanda Powers
    elif 'Brat Doll Amanda Powers' in tagline:
        movieActors.addActor('Amanda Powers', '')

    #  Brat Princess 2
    elif 'Brat Princess 2' in tagline:
        #  Genre list match
        if 'natalya vega' in genreList:
            movieActors.addActor('Natalya Vega', '')
            genreList.remove('natalya vega')
        if 'kat soles' in genreList:
            movieActors.addActor('Kat Soles', '')
            genreList.remove('kat soles')
        if 'macy cartel' in genreList:
            movieActors.addActor('Macy Cartel', '')
            genreList.remove('macy cartel')
        if 'amadahy' in genreList:
            movieActors.addActor('Goddess Amadahy', '')
            genreList.remove('amadahy')
        if 'goddess amadahy' in genreList:
            movieActors.addActor('Goddess Amadahy', '')
            genreList.remove('amadahy')
            genreList.remove('goddess amadahy')
        if 'jennifer' in genreList:
            movieActors.addActor('Empress Jennifer', '')
            genreList.remove('jennifer')
        if 'empress jennifer' in genreList:
            movieActors.addActor('Empress Jennifer', '')
            genreList.remove('empress jennifer')
        #  Metadata match
        if 'Cali Carter' in metadata.summary:
            movieActors.addActor('Cali Carter', '')
        if 'Kenzie Taylor' in metadata.summary:
            movieActors.addActor('Kenzie Taylor', '')
        if 'Alexa' in metadata.summary:
            movieActors.addActor('Alexa', '')
        if 'Natalya' in metadata.summary:
            movieActors.addActor('Natalya Vega', '')
        if 'Jessica' in metadata.summary:
            movieActors.addActor('Jessica', '')

    #  Brat Princess Natalya
    elif 'Brat Princess Natalya' in tagline:
        movieActors.addActor('Princess Natalya', '')
        #  Genre list match
        if 'princess natalya' in genreList:
            movieActors.addActor('Princess Natalya', '')
            genreList.remove('princess natalya')

    #  Brat Princess POV
    elif 'Brat Princess POV' in tagline:
        #  Genre list match
        if 'brandi' in genreList:
            movieActors.addActor('Princess Brandi', '')
            genreList.remove('brandi')
        if 'kelli' in genreList:
            movieActors.addActor('Princess Kelli', '')
            genreList.remove('kelli')

        #  Metadata match
        if 'Brandi' in metadata.summary:
            movieActors.addActor('Princess Brandi', '')
        if 'Princess Kelli' in metadata.summary:
            movieActors.addActor('Princess Kelli', '')
        if 'Jennifer' in metadata.summary:
            movieActors.addActor('Jennifer', '')
        if 'Mia' in metadata.summary:
            movieActors.addActor('Mia', '')

    #  Bratty Ashley Sinclair and Friends
    elif 'Bratty Ashley Sinclair and Friends' in tagline:
        movieActors.addActor('Ashley Sinclair', '')

    #  Bratty Foot Girls
    elif 'Bratty Foot Girls' in tagline:
        #  metadata match
        if 'Sasha Foxxx' in metadata.summary:
            movieActors.addActor('Sasha Foxxx', '')

    #  Bratty Jamie Productions
    elif 'Bratty Jamie Productions' in tagline:
        movieActors.addActor('Bratty Jamie', '')

    #  Bratty Princess Lisa
    elif 'Bratty Princess Lisa' in tagline:
        if 'bratty princess lisa' in genreList:
            movieActors.addActor('Lisa Jordan', '')
            genreList.remove('bratty princess lisa')
        if 'lisa jordan' in genreList:
            movieActors.addActor('Lisa Jordan', '')
            genreList.remove('lisa jordan')

    #  Brie White
    elif 'Brie White' in tagline:
        movieActors.addActor('Brie White', '')
        if 'brie white' in genreList:
            movieActors.addActor('Brie White', '')
            genreList.remove('brie white')
        if 'larkin love' in genreList:
            movieActors.addActor('Larkin Love', '')
            genreList.remove('larkin love')

    #  British Bratz
    elif 'British Bratz' in tagline:
        #  Genre list match
        if 'lizzie murphy' in genreList:
            movieActors.addActor('Lizzie Murphy', '')
            genreList.remove('lizzie murphy')
        if 'goddess melissa' in genreList:
            movieActors.addActor('Goddess Melissa', '')
            genreList.remove('goddess melissa')
        if 'princess chloe' in genreList:
            movieActors.addActor('Princess Chloe', '')
            genreList.remove('princess chloe')
        if 'princess rosie' in genreList:
            movieActors.addActor('Princess Rosie Lee', '')
            genreList.remove('princess rosie')
        if 'princess rosie lee' in genreList:
            movieActors.addActor('Princess Rosie Lee', '')
            genreList.remove('princess rosie lee')
        if 'rosie lee' in genreList:
            movieActors.addActor('Princess Rosie Lee', '')
            genreList.remove('rosie lee')
        if 'jasmine jones' in genreList:
            movieActors.addActor('Jasmine Jones', '')
            genreList.remove('jasmine jones')
        if 'elle pharrell' in genreList:
            movieActors.addActor('Elle Pharrel', '')
            genreList.remove('elle pharrell')
        if 'danni maye' in genreList:
            movieActors.addActor('Danni Maye', '')
            genreList.remove('danni maye')
        if 'princess danni' in genreList:
            movieActors.addActor('Princess Danni', '')
            genreList.remove('princess danni')
        if 'princess stephanie' in genreList:
            movieActors.addActor('Princess Stephanie', '')
            genreList.remove('princess stephanie')
        if 'jessie jenson' in genreList:
            movieActors.addActor('Jessie Jenson', '')
            genreList.remove('jessie jenson')
        if 'diva boss ivy' in genreList:
            movieActors.addActor('Diva Boss Ivy', '')
            genreList.remove('diva boss ivy')
        if 'stephanie wright' in genreList:
            movieActors.addActor('Stephanie Wright', '')
            genreList.remove('stephanie wright')
        if 'lady natt' in genreList:
            movieActors.addActor('Lady Natt', '')
            genreList.remove('lady natt')
        #  Metadata match
        if 'Princess Stephanie' in metadata.title or 'Princess Stephanie' in metadata.summary:
            movieActors.addActor('Princess Stephanie', '')
        if 'Princess Kiki' in metadata.title or 'Princess Kiki' in metadata.summary:
            movieActors.addActor('Princess Kiki', '')
        if 'Vicky' in metadata.title or 'Vicky' in metadata.summary:
            movieActors.addActor('Vicky Narni', '')

    #  Brittany Marie
    elif 'Brittany Marie' in tagline:
        if 'brittany marie' in genreList:
            movieActors.addActor('Brittany Marie', '')
            genreList.remove('brittany marie')

    #  Brooke Marie's Fantasies
    elif 'Brooke Marie\'s Fantasies' in tagline:
        movieActors.addActor('Brooke Marie', '')
        if 'brooke marie' in genreList:
            movieActors.addActor('Brooke Marie', '')
            genreList.remove('brooke marie')

    #  Butt3rflyforU Fantasies
    elif 'Butt3rflyforU Fantasies' in tagline:
        if 'rae knight' in genreList:
            movieActors.addActor('Rae Knight', '')
            genreList.remove('rae knight')
        if 'butt3rflyforu' in genreList:
            genreList.remove('butt3rflyforu')

    #  Candy Glitter
    elif 'Candy Glitter' in tagline:
        if 'candyglitter' in genreList:
            movieActors.addActor('Candy Glitter', '')
            genreList.remove('candyglitter')
        if 'candy glitter' in genreList:
            movieActors.addActor('Candy Glitter', '')
            genreList.remove('candy glitter')

    #  Carlie
    elif 'Carlie' in tagline:
        movieActors.addActor('Carlie', '')

    #  Ceara Lynch Humiliatrix
    elif 'Ceara Lynch Humiliatrix' in tagline:
        movieActors.addActor('Ceara Lynch', '')
        if 'ceara' in genreList:
            movieActors.addActor('Ceara Lynch', '')
            genreList.remove('ceara')
        if 'ceara lynch' in genreList:
            movieActors.addActor('Ceara Lynch', '')
            genreList.remove('ceara lynch')
        if 'princess ceara' in genreList:
            movieActors.addActor('Ceara Lynch', '')
            genreList.remove('princess ceara')
        if 'bratty bunny' in genreList:
            movieActors.addActor('Bratty Bunny', '')
            genreList.remove('bratty bunny')

    #  Charlotte Stokely
    elif 'Charlotte Stokely' in tagline:
        if 'goddess charlotte stokely' in genreList:
            movieActors.addActor('Charlotte Stokely', '')
            genreList.remove('goddess charlotte stokely')

    elif 'chicks' in tagline:
        #  Metadata match
        if 'Sophia' in metadata.summary:
            movieActors.addActor('Mistress Sophia', '')

    #  Christy Berrie
    elif 'Christy Berrie' in tagline:
        movieActors.addActor('Christy Berrie', '')

    #  Club Stiletto Femdom
    elif 'Club Stiletto FemDom' in tagline:
        #  Genre list match
        if 'mistress kandy kink' in genreList:
            movieActors.addActor('Mistress Kandy Kink', '')
            genreList.remove('mistress kandy kink')
        if 'mistress kandy' in genreList:
            movieActors.addActor('Mistress Kandy', '')
            genreList.remove('mistress kandy')
        if 'princess lily' in genreList:
            movieActors.addActor('Princess Lily', '')
            genreList.remove('princess lily')
        if 'miss jasmine' in genreList:
            movieActors.addActor('Miss Jasmine', '')
            genreList.remove('miss jasmine')

        #  Summary match
        if 'Princess Jemma' in metadata.summary:
            movieActors.addActor('Princess Jemma', '')

    #  Countess Crystal Knight
    elif 'Countess Crystal Knight' in tagline:
        if 'crystal knight' in genreList:
            movieActors.addActor('Crystal Knight', '')
            genreList.remove('crystal knight')

    #  Cruel City
    elif 'Cruel City' in tagline:
        if 'Mistress Julia' in metadata.summary:
            movieActors.addActor('Mistress Julia', '')

    #  Cruel Girlfriend
    elif 'Cruel Girlfriend' in tagline:
        if 'jessie jensen' in genreList:
            movieActors.addActor('Jessie Jensen', '')
            genreList.remove('jessie jensen')

    #  CRUEL MISTRESSES
    elif 'CRUEL MISTRESSES' in tagline:
        if 'Lady Ann' in metadata.summary:
            movieActors.addActor('Lady Ann', '')
        if 'Mistress Anette' in metadata.summary:
            movieActors.addActor('Mistress Anette', '')
        if 'Mistress Amanda' in metadata.summary:
            movieActors.addActor('Mistress Amanda', '')
        if 'Mistress Ariel' in metadata.summary:
            movieActors.addActor('Mistress Ariel', '')
        if 'Mistress Kittina' in metadata.summary:
            movieActors.addActor('Mistress Kittina', '')

    #  Cruel Seductress
    elif 'Cruel Seductress' in tagline:
        movieActors.addActor('Goddess Victoria', '')

    #  Cruel  Unusual FemDom
    elif 'Cruel  Unusual FemDom' in tagline:
        #  Genre List
        if 'kiki klout' in genreList:
            movieActors.addActor('Kiki Klout', '')
            genreList.remove('kiki klout')
        if 'megan jones' in genreList:
            movieActors.addActor('Megan Jones', '')
            genreList.remove('megan jones')
        if 'kylie rogue' in genreList:
            movieActors.addActor('Kylie Rogue', '')
            genreList.remove('kylie rogue')
        if 'dava foxx' in genreList:
            movieActors.addActor('Dava Foxx', '')
            genreList.remove('dava foxx')
        if 'alexis grace' in genreList:
            movieActors.addActor('Alexis Grace', '')
            genreList.remove('alexis grace')
        if 'jean bardot' in genreList:
            movieActors.addActor('Jean Bardot', '')
            genreList.remove('jean Bardot')
        if 'stevie shae' in genreList:
            movieActors.addActor('Stevie Shae', '')
            genreList.remove('stevie shae')
        if 'stevie shay' in genreList:
            movieActors.addActor('Stevie Shay', '')
            genreList.remove('stevie shay')
        if 'goddess stevie shae' in genreList:
            movieActors.addActor('Goddess Stevie Shae', '')
            genreList.remove('goddess stevie shae')
        if 'victoria saphire' in genreList:
            movieActors.addActor('Victoria Saphire', '')
            genreList.remove('victoria saphire')
        if 'victoria sapphire' in genreList:
            movieActors.addActor('Victoria Saphire', '')
            genreList.remove('victoria sapphire')
        if 'hailey young' in genreList:
            movieActors.addActor('Hailey Young', '')
            genreList.remove('hailey young')
        if 'holly halston' in genreList:
            movieActors.addActor('Holly Halston', '')
            genreList.remove('holly halston')
        if 'mistress holly halston' in genreList:
            movieActors.addActor('Mistress Holly Halston', '')
            genreList.remove('mistress holly halston')
        if 'mistress holly' in genreList:
            movieActors.addActor('Mistress Holly', '')
            genreList.remove('mistress holly')
        if 'randy moore' in genreList:
            movieActors.addActor('Randy Moore', '')
            genreList.remove('randy moore')
        if 'deanna storm' in genreList:
            movieActors.addActor('Deanna Storm', '')
            genreList.remove('deanna storm')
        if 'ashley edmunds' in genreList:
            movieActors.addActor('Ashley Edmunds', '')
            genreList.remove('ashley edmunds')
        if 'ashely edmunds' in genreList:
            movieActors.addActor('Ashely Edmunds', '')
            genreList.remove('ashely edmunds')
        if 'ashley edmonds' in genreList:
            movieActors.addActor('Ashley edmonds', '')
            genreList.remove('ashley edmonds')
        if 'goddess ashley edmunds' in genreList:
            movieActors.addActor('Goddess Ashley Edmunds', '')
            genreList.remove('goddess ashley edmunds')
        if 'mistress ashley' in genreList:
            movieActors.addActor('Mistress Ashley', '')
            genreList.remove('mistress ashley')
        if 'shay evans' in genreList:
            movieActors.addActor('Shay Evans', '')
            genreList.remove('shay evans')
        if 'kelly diamond' in genreList:
            movieActors.addActor('Kelly Diamond', '')
            genreList.remove('kelly diamond')
        if 'bella reese' in genreList:
            movieActors.addActor('Bella Reese', '')
            genreList.remove('bella reese')
        if 'bella ink' in genreList:
            movieActors.addActor('Bella Ink', '')
            genreList.remove('bella ink')
        if 'raven eve' in genreList:
            movieActors.addActor('Raven Eve', '')
            genreList.remove('raven eve')
        if 'kitty carrera' in genreList:
            movieActors.addActor('Kitty Carrera', '')
            genreList.remove('kitty carrera')
        if 'goddess brianna' in genreList:
            movieActors.addActor('Goddess Brianna', '')
            genreList('goddess brianna')
        if 'kendra james' in genreList:
            movieActors.addActor('Kendra James', '')
            genreList.remove('kendra james')

        #  Summary List
        if 'Goddess Brianna' in metadata.summary:
            movieActors.addActor('Goddess Brianna', '')
        if 'Goddess Hailey' in metadata.summary:
            movieActors.addActor('Goddess Hailey', '')
        if 'Jean Bardot' in metadata.summary:
            movieActors.addActor('Jean Bardot', '')
        if 'Simone Kross' in metadata.summary:
            movieActors.addActor('Simone Kross', '')
        if 'Mistress Alexis' in metadata.summary:
            movieActors.addActor('Mistress Alexis', '')
        if 'Mistress Candance' in metadata.summary:
            movieActors.addActor('Mistress Candence', '')
        if 'Mistress Allison' in metadata.summary:
            movieActors.addActor('Mistress Allison', '')
        if 'Mistress Megan' in metadata.summary or 'Megan' in metadata.summary:
            movieActors.addActor('Mistress Megan', '')
        if 'Kendra James' in metadata.summary:
            movieActors.addActor('Kendra James', '')
        if 'Goddess Victoria' in metadata.summary or 'Victoria Saphire' in metadata.summary or 'Victoria Sapphire' in metadata.summary:
            movieActors.addActor('Goddess Victoria', '')
        if 'Mistress Coral' in metadata.summary:
            movieActors.addActor('Mistress Coral', '')
        if 'Mistress Megan Jones' in metadata.summary:
            movieActors.addActor('Mistress Megan jones', '')
        if 'Princess Stevie' in metadata.summary or 'Stevie' in metadata.summary:
            movieActors.addActor('Princess Stevie', '')
        if 'Goddess Holly' in metadata.summary or 'Holly' in metadata.summary:
            movieActors.addActor('Goddess Holly', '')
        if 'Alexis Grace' in metadata.summary:
            movieActors.addActor('Alexis Grace', '')
        if 'Mistress Heidi' in metadata.summary or 'Heidi' in metadata.summary:
            movieActors.addActor('Mistress Heidi', '')
        if 'Mistress Varla' in metadata.summary:
            movieActors.addActor('Mistress Varla', '')
        if 'Goddess Skyler' in metadata.summary or 'Skyler' in metadata.summary:
            movieActors.addActor('Goddess Skyler', '')
        if 'Goddess Hailey' in metadata.summary or 'Hailey' in metadata.summary:
            movieActors.addActor('Goddess Hailey', '')
        if 'Mistress Raina' in metadata.summary or 'Raina' in metadata.summary:
            movieActors.addActor('Mistress Raina', '')
        if 'Goddess Ashley' in metadata.summary or 'Princess Ashley' in metadata.summary or 'Mistress Ashley' in metadata.summary or 'Ashley' in metadata.summary:
            movieActors.addActor('Mistress Ashley', '')
        if 'Stevie Shay' in metadata.summary:
            movieActors.addActor('Stevie Shay', '')
        if 'Kelly Diamon' in metadata.summary:
            movieActors.addActor('Kelly Diamond', '')
        if 'Tatiana' in metadata.summary:
            movieActors.addActor('Mistress Tatiana', '')
        if 'Mistress Bella' in metadata.summary:
            movieActors.addActor('Mistress Bella', '')

    #  CUCKOLD BRAZIL
    elif 'CUCKOLD BRAZIL' in tagline:
        if 'Mistress Megan' in metadata.summary:
            movieActors.addActor('Mistress Megan', '')

    #  Cuckoldress Cameron and Friends
    elif 'Cuckoldress Cameron and Friends' in tagline:
        #  Genre list match
        if 'cali carter' in genreList:
            movieActors.addActor('Cali Carter', '')
            genreList.remove('cali carter')
        if 'sadie holmes' in genreList:
            movieActors.addActor('Sadie Holmes', '')
            genreList.remove('sadie holmes')
        if 'vienna' in genreList:
            movieActors.addActor('Vienna', '')
            genreList.remove('vienna')

    #  DANGEROUS TEMPTATION
    elif 'DANGEROUS TEMPTATION' in tagline:
        if 'goddess celine' in genreList:
            movieActors.addActor('Goddess Celine', '')
            genreList.remove('goddess celine')

    #  DANIELLE MAYE XXX
    elif 'DANIELLE MAYE XXX' in tagline:
        if 'dani' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('dani')
        if 'danielle' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('danielle')
        if 'dani maye' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('dani maye')
        if 'danielle maye' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('danielle maye')

    #  Darias Fetish KingDom
    elif 'Darias Fetish KingDom' in tagline:
        movieActors.addActor('Goddess Daria', '')
        if 'goddess daria' in genreList:
            movieActors.addActor('Goddess Daria', '')
            genreList.remove('goddess daria')

    #  Diane Andrews
    elif 'Diane Andrews' in tagline:
        movieActors.addActor('Diane Andrews', '')
        if 'milf diane' in genreList:
            genreList.remove('milf diane')
        if 'milf diane andrews vids' in genreList:
            genreList.remove('milf diane andrews vids')
        if 'diane andrews' in genreList:
            genreList.remove('diane andrews')

    #  Divine Goddess Jessica
    elif 'Divine Goddess Jessica' in tagline:
        movieActors.addActor('Goddess Jessica', '')

    #  DomNation
    elif 'DomNation' in tagline:
        if 'snow mercy' in genreList:
            movieActors.addActor('Snow Mercy', '')
            genreList.remove('snow mercy')

    #  Empress Elle
    elif 'Empress Elle' in tagline:
        movieActors.addActor('Empress Elle', '')

    #  EMPRESS JENNIFER
    elif 'EMPRESS JENNIFER' in tagline:
        movieActors.addActor('Empress Jennifer')

    #  Eva de Vil
    elif 'Eva de Vil' in tagline:
        movieActors.addActor('Eva de Vil', '')

    #  Explore With Ivy Starshyne
    elif 'Explore With Ivy Starshyne' in tagline:
        movieActors.addActor('Ivy Starshyne', '')
        if 'ivy starshyne' in genreList:
            genreList.remove('ivy starshyne')
        if 'khandi redd' in genreList:
            movieActors.addActor('Khandi Redd', '')
            genreList.remove('khandi redd')
        if 'vera price' in genreList:
            movieActors.addActor('Vera Price', '')
            genreList.remove('vera price')
        if 'bianca baker' in genreList:
            movieActors.addActor('Bianca Baker', '')
            genreList.remove('bianca baker')

    #  Exquisite Goddess
    elif 'Exquisite Goddess' in tagline:
        movieActors.addActor('Exquisite Goddess', '')

    #  femdomuncut Store
    elif 'femdomuncut Store' in tagline:
        if 'Princess Nikki' in metadata.summary or 'Nikki' in metadata.summary:
            movieActors.addActor('Princess Nikki', '')
        if 'Zazie' in metadata.summary:
            movieActors.addActor('Zazie Skymm', '')

    #  Fetish By LucySkye
    elif 'Fetish By LucySkye' in tagline:
        movieActors.addActor('Lucy Skye', '')

    #  Fetish Princess Kristi
    elif 'Fetish Princess Kristi' in tagline:
        movieActors.addActor('Princess Kristi', '')
        if 'princess kristi' in genreList:
            genreList.remove('princess kristi')
        if 'kinky kristi' in genreList:
            genreList.remove('kinky kristi')

    #  FIlth Syndicate
    elif 'FIlth Syndicate' in tagline:
        if 'robin ray' in genreList:
            movieActors.addActor('Robin Ray', '')
            genreList.remove('robin ray')
        if 'ryan keely' in genreList:
            movieActors.addActor('Ryan Keely', '')
            genreList.remove('ryan keely')
        if 'ashley paige' in genreList:
            movieActors.addActor('Ashley Paige', '')
            genreList.remove('ashley paige')
        if 'sophie monroe' in genreList:
            movieActors.addActor('Sophie Monroe', '')
            genreList.remove('sophie monroe')
        if 'cherry torn' in genreList:
            movieActors.addActor('Cherry Torn', '')
            genreList.remove('cherry torn')
        if 'barbary rose' in genreList:
            movieActors.addActor('Barbary Rose', '')
            genreList.remove('barbary rose')

    #  Galactic Goddess
    elif 'Galactic Goddess' in tagline:
        movieActors.addActor('Galactic Goddess', '')

    #  Glam Worship
    elif 'Glam Worship' in tagline:
        if 'mikaela witt' in genreList:
            movieActors.addActor('Mikaela Witt', '')
            genreList.remove('mikaela witt')
        if 'mikaela' in genreList:
            movieActors.addActor('Mikaela Witt', '')
            genreList.remove('mikaela')
        if 'jessie jensen' in genreList:
            movieActors.addActor('Jessie Jensen', '')
            genreList.remove('jessie jensen')
        if 'jessie' in genreList:
            movieActors.addActor('Jessie Jensen', '')
            genreList.remove('jessie')
        if 'lizzie murphy' in genreList:
            movieActors.addActor('Lizzie Murphy', '')
            genreList.remove('lizzie murphy')
        if 'lizzie' in genreList:
            movieActors.addActor('Lizzie Murphy', '')
            genreList.remove('lizzie')
        if 'lucy zara' in genreList:
            movieActors.addActor('Lucy Zara', '')
            genreList.remove('lucy zara')
        if 'lucy' in genreList:
            movieActors.addActor('Lucy Zara', '')
            genreList.remove('lucy')
        if 'lilly roma' in genreList:
            movieActors.addActor('Lilly Roma', '')
            genreList.remove('lilly roma')
        if 'lilly' in genreList:
            movieActors.addActor('Lilly Roma', '')
            genreList.remove('lilly')
        if 'dannii harwood' in genreList:
            movieActors.addActor('Dannii Harwood', '')
            genreList.remove('dannii harwood')
        if 'dannii' in genreList:
            movieActors.addActor('Dannii Harwood', '')
            genreList.remove('dannii')
        if 'vicky narni' in genreList:
            movieActors.addActor('Vicky Narni', '')
            genreList.remove('vicky narni')
        if 'vicky' in genreList:
            movieActors.addActor('Vicky Narni', '')
            genreList.remove('vicky')
        if 'dani maye' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('dani maye')
        if 'dani' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('dani')
        if 'danielle maye' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('danielle maye')
        if 'danielle' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('danielle')
        if 'nina leigh' in genreList:
            movieActors.addActor('Nina Leigh', '')
            genreList.remove('nina leigh')
        if 'nina' in genreList:
            movieActors.addActor('Nina Leigh', '')
            genreList.remove('nina')

    #  Goddess Alexandra Snow
    elif 'Goddess Alexandra Snow' in tagline:
        movieActors.addActor('Alexandra Snow', '')

    #  Goddess Bs Slave Training 101
    elif 'Goddess Bs Slave Training 101' in tagline:
        movieActors.addActor('Brandon Areana', '')
        if 'brandon areana' in genreList:
            genreList.remove('brandon areana')
        if 'goddess brandon' in genreList:
            genreList.remove('goddess brandon')

    #  Goddess Cheyenne
    elif 'Goddess Cheyenne' in tagline:
        if 'goddess cheyenne' in genreList:
            movieActors.addActor('Goddess Cheyenne', '')
            genreList.remove('goddess cheyenne')
        if 'jewell marceau' in genreList:
            movieActors.addActor('Jewell Marceau', '')
            genreList.remove('jewell marceau')
        if 'lady kyra' in genreList:
            movieActors.addActor('Lady Kyra', '')
            genreList.remove('lady kyra')
        if 'jean bardot' in genreList:
            movieActors.addActor('Jean Bardot', '')
            genreList.remove('jean bardot')

    #  Goddess Christina
    elif 'Goddess Christina' in tagline:
        movieActors.addActor('Goddess Cristina', '')
        if 'goddess christina' in genreList:
            genreList.remove('goddess christina')
        if 'erotic goddess christina' in genreList:
            genreList.remove('erotic goddess christina')
        if 'eroticgoddessxxx' in genreList:
            genreList.remove('eroticgoddessxxx')
        if 'erotic goddess' in genreList:
            genreList.remove('erotic goddess')

    #  Goddess Ella Kross
    elif 'Goddess Ella Kross' in tagline:
        movieActors.addActor('Ella Kross', '')

    #  Goddess Eris Temple
    elif 'Goddess Eris Temple' in tagline:
        movieActors.addActor('Eris Temple', '')
        #  Metadata match
        if 'Nikki Nyx' in metadata.title or 'Nikki Nyx' in metadata.summary:
            movieActors.addActor('Nikki Nyx', '')

    #  Goddess Femdom
    elif 'Goddess Femdom' in tagline:
        movieActors.addActor('Madame Amiee', '')
        if 'madame amiee' in genreList:
            genreList.remove('madame amiee')
        if 'johnny rifle' in genreList:
            movieActors.addActor('Johnny Rifle', '')
            genreList.remove('johnny rifle')

    #  Goddess Foot Domination
    elif 'Goddess Foot Domination' in tagline:
        if 'goddess brianna' in genreList:
            movieActors.addActor('Goddess Brianna', '')
            genreList.remove('goddess brianna')
        if 'vicky vixxx' in genreList:
            movieActors.addActor('Vicky Vixxx', '')
            genreList.remove('vicky vixxx')
        if 'nicki blake' in genreList:
            movieActors.addActor('Nicki Blake', '')
            genreList.remove('nicki blake')

    #  Goddess Gemma
    elif 'Goddess Gemma' in tagline:
        movieActors.addActor('Goddess Gemma', '')

    #  Goddess Gwen the Princess Boss
    elif 'Goddess Gwen the Princess Boss' in tagline:
        movieActors.addActor('Goddess Gwen', '')

    #  Goddess Idelsy
    elif 'Goddess Idelsy' in tagline:
        movieActors.addActor('Idelsy Love', '')
        if 'idelsy love' in genreList:
            genreList.remove('idelsy love')
        if 'goddess idelsy' in genreList:
            genreList.remove('goddess idelsy')

    #  Goddess JessiBelle
    elif 'Goddess JessiBelle' in tagline:
        movieActors.addActor('Jessi Belle', '')
        if 'jessibelle' in genreList:
            genreList.remove('jessibelle')
        if 'jessi belle' in genreList:
            genreList.remove('jessi belle')

    #  Goddess Kendall
    elif 'Goddess Kendall' in tagline:
        movieActors.addActor('Kendall Olsen', '')

    #  Goddess Kims Fantasies
    elif 'Goddess Kims Fantasies' in tagline:
        movieActors.addActor('Young Goddess Kim', '')
        if 'young goddess kim' in genreList:
            genreList.remove('young goddess kim')

    #  Goddess Kittys Findom Fuckery
    elif 'Goddess Kittys Findom Fuckery' in tagline:
        movieActors.addActor('Goddess Kitty', '')
        if 'goddess blonde kitty' in genreList:
            genreList.remove('goddess blonde kitty')

    #  Goddess Madam Violet
    elif 'Goddess Madam Violet' in tagline:
        movieActors.addActor('Madam Violet', '')
        if 'madam violet' in genreList:
            genreList.remove('madam violet')

    #  Goddess Mira
    elif 'Goddess Mira' in tagline:
        movieActors.addActor('Goddess Mira', '')

    #  Goddess Misha Mystique
    elif 'Goddess Misha Mystique' in tagline:
        movieActors.addActor('Misha Mystique', '')
        if 'misha mystique' in genreList:
            genreList.remove('misha mystique')

    #  Goddess Nikki
    elif 'Goddess Nikki' in tagline:
        movieActors.addActor('Nikki Ashton', '')
        if 'nikki ashton' in genreList:
            genreList.remove('nikki ashton')
        if 'goddess nikki' in genreList:
            genreList.remove('goddess nikki')
        if 'erotic nikki' in genreList:
            genreList.remove('erotic nikki')
        if 'eroticnikki' in genreList:
            genreList.remove('eroticnikki')

    #  Goddess Paige
    elif 'Goddess Paige' in tagline:
        movieActors.addActor('Paige Orion', '')
        if 'paige orion' in genreList:
            genreList.remove('paige orion')
        if 'goddess paige' in genreList:
            genreList.remove('goddess paige')
        if 'goddess paige orion' in genreList:
            genreList.remove('goddess paige orion')

    #  Goddess Saffron
    elif 'Goddess Saffron' in tagline:
        movieActors.addActor('Goddess Saffron', '')
        if 'goddess saffron' in genreList:
            genreList.remove('goddess saffron')
        if 'saffronism' in genreList:
            genreList.remove('saffronism')
        if 'saffmas' in genreList:
            genreList.remove('saffmas')

    #  Goddess Stella Sol
    elif 'Goddess Stella Sol' in tagline:
        movieActors.addActor('Stella Sol', '')

    #  Goddess Tangent World of Femdom
    elif 'Goddess Tangent World of Femdom' in tagline:
        movieActors.addActor('Goddess Tangent', '')
        if 'tangent' in genreList:
            genreList.remove('tangent')
        if 'goddess tangent' in genreList:
            genreList.remove('goddess tangent')

    #  Goddess Valora
    elif 'Goddess Valora' in tagline:
        movieActors.addActor('Goddess Valora', '')
        if 'goddess valora' in genreList:
            genreList.remove('goddess valora')

    #  Goddess Venus
    elif 'Goddess Venus' in tagline:
        movieActors.addActor('Goddess Venus', '')
        if 'goddess venus' in genreList:
            genreList.remove('goddess venus')
        if 'venus' in genreList:
            genreList.remove('venus')

    #  Goddess Vivian Leigh
    elif 'Goddess Vivian Leigh' in tagline:
        movieActors.addActor('Vivian Leigh', '')
        if 'goddess vivian leigh' in genreList:
            genreList.remove('goddess vivian leigh')

    #  Goddess Zenova Controls Your Mind
    elif 'Goddess Zenova Controls Your Mind' in tagline:
        movieActors.addActor('Goddess Zenova', '')

    #  Goddess Zephy
    elif 'Goddess Zephy' in tagline:
        movieActors.addActor('Goddess Zephy', '')
        if 'zephy' in genreList:
            genreList.remove('Zephy')
        if 'zephyanna' in genreList:
            genreList.remove('zephianna')

    #  Harley LaVey
    elif 'Harley LaVey' in tagline:
        movieActors.addActor('Harley LaVey', '')

    #  HollyDomme
    elif 'HollyDomme' in tagline:
        movieActors.addActor('Holly Webster', '')
        if 'hollydomme' in genreList:
            genreList.remove('hollydomme')
        if 'hollywebster' in genreList:
            genreList.remove('hollywebster')

    #  HomSmother
    elif 'HomSmother' in tagline:
        if 'liana' in genreList:
            movieActors.addActor('Liana', '')
            genreList.remove('Liana')
        if 'amy' in genreList:
            movieActors.addActor('Amy', '')
            genreList.remove('amy')
        if 'sabrina' in genreList:
            movieActors.addActor('Sabrina', '')
            genreList.remove('sabrina')
        if 'sabrina a' in genreList:
            movieActors.addActor('Sabrina', '')
            genreList.remove('sabrina a')
        if 'anna' in genreList:
            movieActors.addActor('Anna', '')
            genreList.remove('anna')
        if 'anna b' in genreList:
            movieActors.addActor('Anna', '')
            genreList.remove('anna a')
        if 'cindy' in genreList:
            movieActors.addActor('Cindy', '')
            genreList.remove('cindy')
        if 'cindy c' in genreList:
            movieActors.addActor('Cindy', '')
            genreList.remove('cindy c')
        if 'florence' in genreList:
            movieActors.addActor('Florence', '')
            genreList.remove('florence')
        if 'rayana' in genreList:
            movieActors.addActor('Rayana', '')
            genreList.remove('rayana')
        if 'sara' in genreList:
            movieActors.addActor('Sara', '')
            genreList.remove('sara')
        if 'adriana' in genreList:
            movieActors.addActor('Adriana', '')
            genreList.remove('adriana')
        if 'felicitas' in genreList:
            movieActors.addActor('Felicitas', '')
            genreList.remove('felicitas')

    #  Hot Juls Fetishes
    elif 'Hot Juls Fetishes' in tagline:
        movieActors.addActor('Goddess Juls', '')
        if 'goddess juls' in genreList:
            genreList.remove('goddess juls')
        if 'hot juls fetishes' in genreList:
            genreList.remove('hot juls fetishes')
        if 'juls' in genreList:
            genreList.remove('juls')

    #  Humiliation Brat Girls
    elif 'Humiliation Brat Girls' in tagline:
        if 'Jolene' in metadata.summary:
            movieActors.addActor('Jolene', '')
        if 'Bobbi Dylan' in metadata.summary:
            movieActors.addActor('Bobbi Dylan', '')
        if 'Cydel' in metadata.summary:
            movieActors.addActor('Cydel', '')

    #  Humiliation POV
    elif 'Humiliation POV' in tagline:
        if 'Goddess Carissa' in metadata.summary or 'Carissa Montgomery' in metadata.summary:
            movieActors.addActor('Carissa Montgomery', '')
        if 'Princess Ellie' in metadata.summary:
            movieActors.addActor('Ellie Idol', '')
        if 'Miss Tiffany' in metadata.summary:
            movieActors.addActor('Miss Tiffany', '')
        if 'Goddess Alexa' in metadata.summary:
            movieActors.addActor('Goddess Alexa', '')
        if 'Goddess Isabel' in metadata.summary:
            movieActors.addActor('Goddess Isabel', '')
        if 'Kelle Martina' in metadata.summary:
            movieActors.addActor('Kelle Martina', '')
        if 'Bratty Bunny' in metadata.summary:
            movieActors.addActor('Bratty Bunny', '')
        if 'Macey Jade' in metadata.summary:
            movieActors.addActor('Macey Jade', '')
        if 'Princess Kaelin' in metadata.summary:
            movieActors.addActor('Princess Kaelin', '')
        if 'Princess Kate' in metadata.summary:
            movieActors.addActor('Princess Kate', '')
        if 'Megan Foxx' in metadata.summary:
            movieActors.addActor('Megan Foxx', '')
        if 'Nikki Next' in metadata.summary:
            movieActors.addActor('Nikki Next', '')
        if 'Goddess Sahrye' in metadata.summary:
            movieActors.addActor('Goddess Sahrye', '')
        if 'Amai Liu' in metadata.summary:
            movieActors.addActor('Amai Liu', '')
        if 'London Lix' in metadata.summary:
            movieActors.addActor('London Lix', '')

    #  Humiliation Princess Rene's Clips!
    elif 'Humiliation Princess Rene\'s Clips!' in tagline:
        movieActors.addActor('Princess Rene', '')
        if 'princess rene' in genreList:
            genreList.remove('princess rene')
        if 'worship rene' in genreList:
            genreList.remove('worship rene')
        if 'renee' in genreList:
            genreList.remove('renee')
        if 'rene' in genreList:
            genreList.remove('rene')

    #  HUMILIATRIX CLIPSTORE
    if 'HUMILIATRIX CLIPSTORE' in tagline:
        #  Genre list match
        if 'princess selena' in genreList:
            movieActors.addActor('Princess Selana', '')
            genreList.remove('princess selana')
        if 'princess ashleigh' in genreList:
            movieActors.addActor('Princess Ashleigh', '')
            genreList.remove('princess ashleigh')
        if 'princess missy' in genreList:
            movieActors.addActor('Princess Missy', '')
            genreList.remove('princess missy')
        if 'princess tiffani' in genreList:
            movieActors.addActor('Princess Tiffani', '')
            genreList.remove('princess tiffani')
        if 'kendra james' in genreList:
            movieActors.addActor('Kendra James', '')
            genreList.remove('kendra james')

        #  Metadata match
        if 'Princess Becky' in metadata.title or 'Princess Becky' in metadata.summary:
            movieActors.addActor('Princess Becky', '')
        if 'Kendra James' in metadata.title or 'Kendra James' in metadata.summary:
            movieActors.addActor('Kendra James', '')
        if 'Princess luna' in metadata.title or 'princess luna' in metadata.summary:
            movieActors.addActor('Princess Luna', '')
        if 'Princess Tiffani' in metadata.title or 'Princess Tiffani' in metadata.summary:
            movieActors.addActor('Princess Tiffani', '')
        if 'Ashleigh' in metadata.title or 'Ashleigh' in metadata.summary:
            movieActors.addActor('Princess Ashleigh', '')
        if 'Princess Tessa' in metadata.title or 'Princess Tessa' in metadata.summary:
            movieActors.addActor('Princess Tessa', '')
        if 'Princess Remi' in metadata.title or 'Princess Remi' in metadata.summary or 'Remi' in metadata.title or 'remi' in metadata.summary:
            movieActors.addActor('Princess Remi', '')
        if 'Goddess Rhianna' in metadata.title or 'Goddess Rhianna' in metadata.summary:
            movieActors.addActor('Goddess Rhianna', '')
        if 'Princess Ashley' in metadata.title or 'Princess Ashley' in metadata.summary:
            movieActors.addActor('Princess Ashley', '')
        if 'Princess Jade' in metadata.title or 'Princess Jade' in metadata.summary:
            movieActors.addActor('Princess Jade', '')
        if 'Princess Missy' in metadata.title or 'Princess Missy' in metadata.summary:
            movieActors.addActor('Princess Missy', '')
        if 'Pimpstress Sari' in metadata.title or 'Pimpstress Sari' in metadata.summary:
            movieActors.addActor('Pimpstress Sari', '')

        #  Italian Empress Daria
        elif 'Italian Empress Daria' in tagline:
            movieActors.addActor('Empress Daria', '')
            if 'daria' in genreList:
                genreList.remove('daria')

        #  Jasmine Mendez  LatinAss Locas
        elif 'Jasmine Mendez  LatinAss Locas' in tagline:
            movieActors.addActor('Jasmine Mendez', '')

        #  Jerk Off Instructions
        elif 'Jerk Off Instructions' in tagline:
            #  Genre list match
            if 'amai liu' in genreList:
                movieActors.addActor('Amai Liu', '')
                genreList.remove('amai liu')
            if 'lacy lennon' in genreList:
                movieActors.addActor('Lacy Lennon', '')
                genreList.remove('lacy lennon')
            if 'katie kush' in genreList:
                movieActors.addActor('Katie Kush', '')
                genreList.remove('katie kush')
            if 'veronica valentine' in genreList:
                movieActors.addActor('Veronica Valentine', '')
                genreList.remove('veronica valentine')
            if 'victoria voxxx' in genreList:
                movieActors.addActor('Victoria Voxxx', '')
                genreList.remove('victoria voxxx')
            if 'licey sweet' in genreList:
                movieActors.addActor('Licey Sweet', '')
                genreList.remove('licey sweet')
            if 'lily adams' in genreList:
                movieActors.addActor('Lily Adams', '')
                genreList.remove('lily adams')
            if 'ryder skye' in genreList:
                movieActors.addActor('Ryder Sky', '')
                genreList.remove('ryder skye')
            if 'violet starr' in genreList:
                movieActors.addActor('Violet Starr', '')
                genreList.remove('violet starr')
            if 'kasey warner' in genreList:
                movieActors.addActor('Kasey Warner', '')
                genreList.remove('kasey warner')
            if 'aiden ashley' in genreList:
                movieActors.addActor('Aiden Ashley', '')
                genreList.remove('aiden ashley')
            if 'olivia glass' in genreList:
                movieActors.addActor('Olivia Glass', '')
                genreList.remove('olivia glass')
            if 'carolina sweets' in genreList:
                movieActors.addActor('Carolina Sweets', '')
                genreList.remove('carolina sweets')
            if 'jillian janson' in genreList:
                movieActors.addActor('Jillian Janson', '')
                genreList.remove('jillian janson')
            if 'raven hart' in genreList:
                movieActors.addActor('Raven Hart', '')
                genreList.remove('raven hart')
            if 'jayden cole' in genreList:
                movieActors.addActor('Jayden Cole', '')
                genreList.remove('jayden cole')
            if 'anna graham' in genreList:
                movieActors.addActor('Anna Graham', '')
                genreList.remove('anna graham')

                #  Metadata match
            if 'Anna' in metadata.summary:
                movieActors.addActor('Anna Graham', '')

    #  Jerk4PrincessUK
    elif 'Jerk4PrincessUK' in tagline:
        if 'axa jay' in genreList:
            movieActors.addActor('Axa Jay', '')
            genreList.remove('axa jay')
        if 'axajay' in genreList:
            movieActors.addActor('Axa Jay', '')
            genreList.remove('axajay')
        if 'cherry blush' in genreList:
            movieActors.addActor('Cherry Blush', '')
            genreList.remove('cherry blush')
        if 'raven lee' in genreList:
            movieActors.addActor('Raven Lee', '')
            genreList.remove('raven lee')
        if 'bonnie bellotti' in genreList:
            movieActors.addActor('Bonnie Bellotti', '')
            genreList.remove('bonnie bellotti')
        if 'charn' in genreList:
            movieActors.addActor('Charn', '')
            genreList.remove('charn')
        if 'natalia forrest' in genreList:
            movieActors.addActor('Natalia Forrest', '')
            genreList.remove('natalia forrest')
        if 'michelle hush' in genreList:
            movieActors.addActor('Michelle Hush', '')
            genreList.remove('michelle hush')
        if 'carmen' in genreList:
            movieActors.addActor('Carmen', '')
            genreList.remove('carmen')
        if 'jessica fox' in genreList:
            movieActors.addActor('Jessica Fox', '')
            genreList.remove('jessica fox')
        if 'kacie james' in genreList:
            movieActors.addActor('Kacie James', '')
            genreList.remove('kacie james')
        if 'volkova' in genreList:
            movieActors.addActor('Volkova', '')
            genreList.remove('volkova')
        if 'setina rose' in genreList:
            movieActors.addActor('Setina Rose', '')
            genreList.remove('setina rose')

    #  KEBRANOZES BRAZILIAN BALLBUSTING
    elif 'KEBRANOZES BRAZILIAN BALLBUSTING' in tagline:
        #  Genre list match
        if 'barbara inked' in genreList:
            movieActors.addActor('Barbara Inked', '')
            genreList.remove('barbara inked')
        if 'tygra' in genreList:
            movieActors.addActor('Tygra', '')
            genreList.remove('tygra')
        if 'renata' in genreList:
            movieActors.addActor('Renata', '')
            genreList.remove('renata')
        if 'leona' in genreList:
            movieActors.addActor('Leona', '')
            genreList.remove('leona')
        if 'yoko' in genreList:
            movieActors.addActor('Yoko', '')
            genreList.remove('yoko')
        if 'alexa' in genreList:
            movieActors.addActor('Alexa', '')
            genreList.remove('alexa')

        #  Metadata match
        if 'Tygra' in metadata.summary:
            movieActors.addActor('Tygra', '')
        if 'Yoko' in metadata.summary:
            movieActors.addActor('Yoko', '')
        if 'Sandy' in metadata.summary:
            movieActors.addActor('Sandy', '')
        if 'Renata' in metadata.summary:
            movieActors.addActor('Renata', '')
        if 'Leona' in metadata.summary:
            movieActors.addActor('Leona', '')

    #  Kerri King's Naughty Pleasures
    elif 'Kerri King\'s Naughty Pleasures' in tagline:
        movieActors.addActor('Kerri King', '')
        if 'kerri king' in genreList:
            genreList.remove('kerri king')

    #  KIMBERLY KANES KANEARMY
    elif 'KIMBERLY KANES KANEARMY' in tagline:
        movieActors.addActor('Kimberly Kane', '')
        if 'kimberly kane' in genreList:
            genreList.remove('kimberly kane')
        if 'syren demer' in genreList:
            movieActors.addActor('Syren Demer', '')
            genreList.remove('syren demer')
        if 'dee williams' in genreList:
            movieActors.addActor('Dee Williams', '')
            genreList.remove('dee williams')
        if 'natalia mars' in genreList:
            movieActors.addActor('Natalia Mars', '')
            genreList.remove('natalia mars')
        if 'mandy mitchell' in genreList:
            movieActors.addActor('Mandy Mitchell', '')
            genreList.remove('mandy mitchell')

    #  Kitzis Clown Fetish
    elif 'Kitzis Clown Fetish' in tagline:
        movieActors.addActor('Kitzi Klown', '')

    #  Kyaa's Empire
    elif 'Kyaa\'s Empire' in tagline:
        movieActors.addActor('Kyaa Chimera', '')
        if 'goddess kyaa' in genreList:
            genreList.remove('goddess kyaa')
        if 'domme kyaa' in genreList:
            genreList.remove('domme kyaa')
        if 'kyaa chimera' in genreList:
            genreList.remove('kyaa chimera')
        if 'kyaaism' in genreList:
            genreList.remove('kyaaism')
        if 'sarah diavola' in genreList:
            movieActors.addActor('Sarah Diavola', '')
            genreList.remove('sarah diavola')
        if 'laila delight' in genreList:
            movieActors.addActor('Laila Delight', '')
            genreList.remove('laila delight')
        if 'jessica doll' in genreList:
            movieActors.addActor('Jessica Doll', '')
            genreList.remove('jessica doll')

    #  Lady Bellatrix
    elif 'Lady Bellatrix' in tagline:
        movieActors.addActor('Lady Bellatrix', '')
        if 'lady bellatrix' in genreList:
            genreList.remove('lady bellatrix')
        if 'mistress nikki whiplash' in genreList:
            movieActors.addActor('Nikki Whiplash', '')
            genreList.remove('mistress nikki whiplash')
        if 'miss xi' in genreList:
            movieActors.addActor('Miss Xi', '')
            genreList.remove('miss xi')
        if 'miss jasmine' in genreList:
            movieActors.addActor('Miss Jasmine', '')
            genreList.remove('miss jasmine')
        if 'gaelle lagalle' in genreList:
            movieActors.addActor('Gaelle Lagalle', '')
            genreList.remove('gaelle lagalle')
        if 'mistress esme' in genreList:
            movieActors.addActor('Mistress Esme', '')
            genreList.remove('mistress esme')
        if 'miss tiffany naylor' in genreList:
            movieActors.addActor('Tiffany Naylor', '')
            genreList.remove('miss tiffany naylor')

    #  Lady Fyre Femdom
    elif 'Lady Fyre Femdom' in tagline:
        #  Genre list match
        if 'lady fyre' in genreList:
            movieActors.addActor('Lady Fyre', '')
            genreList.remove('lady fyre')
        if 'kenzie madison' in genreList:
            movieActors.addActor('Kenzie Madison', '')
            genreList.remove('kenzie madison')
        if 'indica flower' in genreList:
            movieActors.addActor('Indica Flower', '')
            genreList.remove('indica flower')
        if 'laney grey' in genreList:
            movieActors.addActor('Laney Grey', '')
            genreList.remove('laney grey')
        if 'katie kush' in genreList:
            movieActors.addActor('Katie Kush', '')
            genreList.remove('katie kush')
        if 'violet starr' in genreList:
            movieActors.addActor('Violet Starr', '')
            genreList.remove('violet starr')
        if 'laz fyre' in genreList:
            movieActors.addActor('Laz Fyre')
            genreList.remove('laz fyre')
        if 'mandy muse' in genreList:
            movieActors.addActor('Mandy Muse', '')
            genreList.remove('mandy muse')
        if 'house of fyre' in genreList:
            genreList.remove('house of fyre')

        #  Metadata Match
        if 'Cali Carter' in metadata.summary:
            movieActors.addActor('Cali Carter', '')

    #  Lady Karame
    elif 'Lady Karame' in tagline:
        movieActors.addActor('Lady Karame', '')
        if 'lady karame' in genreList:
            genreList.remove('lady karame')

    #  Lady Nina Leighs Royal Domination
    elif 'Lady Nina Leighs Royal Domination' in tagline:
        movieActors.addActor('Nina Leigh', '')
        if 'ladyninaleigh' in genreList:
            genreList.remove('ladyninaleigh')
        if 'loveladynina' in genreList:
            genreList.remove('loveladynina')
        if 'lady nina leigh' in genreList:
            genreList.remove('lady nina leigh')

    #  Latex Barbie Land
    elif 'Latex Barbie Land' in tagline:
        movieActors.addActor('Latex Barbie', '')
        if 'latexbarbie' in genreList:
            genreList.remove('latexbarbie')
        if 'latex barbie' in genreList:
            genreList.remove('latex barbie')
        if 'barbie' in genreList:
            genreList.remove('barbie')
        if 'latex' in genreList:
            genreList.remove('latex')

    #  Lelu Love
    elif 'Lelu Love' in tagline:
        movieActors.addActor('Lelu Love', '')
        if 'lelu' in genreList:
            genreList.remove('lelu')
        if 'lelu-love' in genreList:
            genreList.remove('lelu-love')
        if 'lelu love' in genreList:
            genreList.remove('lelu love')

    #  Lindsey Leigh Addiction
    elif 'Lindsey Leigh Addiction' in tagline:
        movieActors.addActor('Lindsey Leigh', '')

    #  Luna Sapphire
    elif 'Luna Sapphire' in tagline:
        movieActors.addActor('Luna Sapphire', '')
    if 'luna sapphire' in genreList:
        genreList.remove('luna sapphire')
    if 'goddess luna' in genreList:
        genreList.remove('goddess luna')
    if 'goddess ellie' in genreList:
        movieActors.addActor('Ellie Boulder', '')
        genreList.remove('goddess ellie')
    if 'ellie boulder' in genreList:
        movieActors.addActor('Ellie Boulder', '')
        genreList.remove('ellie boulder')

    #  Majesty Natalie
    elif 'Majesty Natalie' in tagline:
        movieActors.addActor('Majesty Natalie', '')
        if 'majesty natalie' in genreList:
            genreList.remove('majesty natalie')
        if 'majestynatalie' in genreList:
            genreList.remove('majestynatalie')

    #  Makayla Divine Busty Latina Goddess
    elif 'Makayla Divine Busty Latina Goddess' in tagline:
        movieActors.addActor('Makayla Divine', '')

    #  Mandy Flores
    elif 'Mandy Flores' in tagline:
        movieActors.addActor('Mandy Flores', '')
        if 'mandy flores' in genreList:
            genreList.remove('mandy flores')
        if 'new mandy flores video' in genreList:
            genreList.remove('new mandy flores video')
        if 'mymandygirl' in genreList:
            genreList.remove('mymandygirl')

    #  MARKS HEAD BOBBERS  HAND JOBBERS
    elif 'MARKS HEAD BOBBERS  HAND JOBBERS' in tagline:
        movieActors.addActor('Mark Rockwell', '')
        #  Genre list match
        if 'mark rockwell' in genreList:
            genreList.remove('mark rockwell')
        if 'alexa grace' in genreList:
            movieActors.addActor('Alexa Grace', '')
            genreList.remove('alexa grace')
        if 'remy lacroix' in genreList:
            movieActors.addActor('Remy LaCroix', '')
            genreList.remove('remy lacroix')
        if 'jade indica' in genreList:
            movieActors.addActor('Jade Indica', '')
            genreList.remove('jade indica')
        if 'dillion carter' in genreList:
            movieActors.addActor('Dillion Carter', '')
            genreList.remove('dillion carter')
        if 'sierra cure' in genreList:
            movieActors.addActor('Sierra Cure', '')
            genreList.remove('sierra cure')
        if 'britney stevens' in genreList:
            movieActors.addActor('Britney Stevens', '')
            genreList.remove('britney stevens')
        if 'megan piper' in genreList:
            movieActors.addActor('Megan Piper', '')
            genreList.remove('megan piper')
        if 'alexis venton' in genreList:
            movieActors.addActor('Alexis Venton', '')
            genreList.remove('alexis venton')
        if 'jessica rayne' in genreList:
            movieActors.addActor('Jessica Rayne', '')
            genreList.remove('jessica rayne')
        if 'mandy haze' in genreList:
            movieActors.addActor('Mandy Haze', '')
            genreList.remove('mandy haze')

        #  Metadata match
        if 'Alexa Grace' in metadata.summary:
            movieActors.addActor('Alexa Grace', '')
        if 'Remy LaCroix' in metadata.summary:
            movieActors.addActor('Remy LaCroix', '')
        if 'Jade Indica' in metadata.summary:
            movieActors.addActor('Jade Indica', '')
        if 'Dillion Carter' in metadata.summary:
            movieActors.addActor('Dillion Carter', '')
        if 'Sierra Cure' in metadata.summary:
            movieActors.addActor('Sierra Cure', '')
        if 'Britney Stevens' in metadata.summary:
            movieActors.addActor('Britney Stevens', '')
        if 'Megan Piper' in metadata.summary:
            movieActors.addActor('Megan Piper', '')
        if 'Alexis Venton' in metadata.summary:
            movieActors.addActor('Alexis Venton', '')
        if 'Jessica Rayne' in metadata.summary:
            movieActors.addActor('Jessica Rayne', '')
        if 'Mandy Haze' in metadata.summary:
            movieActors.addActor('Mandy Haze', '')

    #  Meana Wolf
    elif 'Meana Wolf' in tagline:
        movieActors.addActor('Meana Wolf', '')
        #  Genre list match
        if 'meana wolf' in genreList:
            genreList.remove('meana wolf')
        if 'liv revamped' in genreList:
            movieActors.addActor('Liv Revamped', '')
            genreList.remove('liv revamped')
        #  Metadata match
        if 'Liv Revamped' in metadata.summary:
            movieActors.addActor('Liv Revamped')

    #  MeanBitches POV Slave Orders
    elif 'MeanBitches POV Slave Orders' in tagline:
        #  Genre list match
        if 'valentina jewels' in genreList:
            movieActors.addActor('Valentina Jewels', '')
            genreList.remove('valentina jewels')
        if 'gia dimarco' in genreList:
            movieActors.addActor('Gia Dimarco', '')
            genreList.remove('gia dimarco')
        if 'kimber woods' in genreList:
            movieActors.addActor('Kimber Woods', '')
            genreList.remove('kimber woods')
        if 'alura jenson' in genreList:
            movieActors.addActor('Alura Jenson', '')
            genreList.remove('alura jenson')
        if 'lala ivey' in genreList:
            movieActors.addActor('Lala Ivey', '')
            genreList.remove('lala ivey')
        if 'alexis fawx' in genreList:
            movieActors.addActor('Alexis Fawx', '')
            genreList.remove('alexis fawx')
        if 'london rivers' in genreList:
            movieActors.addActor('London Rivers', '')
            genreList.remove('london rivers')
        if 'victoria voxxx' in genreList:
            movieActors.addActor('Victoria Voxxx', '')
            genreList.remove('victoria voxxx')
        if 'sofia rose' in genreList:
            movieActors.addActor('Sofia Rose', '')
            genreList.remove('sofia rose')
        if 'lana violet' in genreList:
            movieActors.addActor('Lana Violet', '')
            genreList.remove('lana violet')
        #  Metadata match
        if 'Holly Wellin' in metadata.title or 'Holly Wellin' in metadata.summary:
            movieActors.addActor('Holly Wellin', '')
        if 'Holly Michael' in metadata.title or 'Holly Michael' in metadata.summary:
            movieActors.addActor('Holly Michael', '')
        if 'Kristina rose' in metadata.title or 'Kristina Rose' in metadata.summary:
            movieActors.addActor('Kristina Rose', '')
        if 'Phoenix Marie' in metadata.title or 'Phoenix Marie' in metadata.summary:
            movieActors.addActor('Phoenix Marie', '')
        if 'Alexis Texas' in metadata.title or 'Alexis Texas' in metadata.summary:
            movieActors.addActor('Alexis Texas', '')
        if 'Bree Olson' in metadata.title or 'Bree Olson' in metadata.summary:
            movieActors.addActor('Bree Olson', '')

    #  Meggerz
    elif 'Meggerz' in tagline:
        movieActors.addActor('Meggerz', '')
        #  Genre list match
        if 'meggerz' in genreList:
            genreList.remove('meggerz')
        if 'sarah diavola' in genreList:
            movieActors.addActor('Sarah Diavola', '')
            genreList.remove('sarah diavola')
        if 'ninja jason' in genreList:
            movieActors.addActor('Ninja Jason', '')
            genreList.remove('ninja jason')
        if 'mz devious' in genreList:
            movieActors.addActor('Mz Devious', '')
            genreList.remove('mz devious')
        if 'evelyn milano' in genreList:
            movieActors.addActor('Evelyn Milano', '')
            genreList.remove('evelyn milano')
        #  Metadata Match
        if 'Mz Devious' in metadata.summary:
            movieActors.addActor('Mz Devious', '')

    #  Men Are Slaves
    elif 'Men Are Slaves' in tagline:
        #  Genre list match
        if 'cadence st. john' in genreList:
            movieActors.addActor('Cadence St. John', '')
            genreList.remove('cadence st.john')
        if 'mistress cadence' in genreList:
            movieActors.addActor('Cadence St. John', '')
            genreList.remove('mistress cadence')
        if 'edyn blair' in genreList:
            movieActors.addActor('Edyn Blair', '')
            genreList.remove('edyn blair')
        if 'miley mae' in genreList:
            movieActors.addActor('Miley Mae', '')
            genreList.remove('miley mae')
        if 'kay carter' in genreList:
            movieActors.addActor('Kay Carter', '')
            genreList.remove('kay carter')
        if 'kendall faye' in genreList:
            movieActors.addActor('Kendall Faye', '')
            genreList.remove('kendall faye')
        if 'sara luvv' in genreList:
            movieActors.addActor('Sara Luvv', '')
            genreList.remove('sara luvv')

        #  Metadata match
        if 'Cadence' in metadata.title or 'Cadence' in metadata.summary:
            movieActors.addActor('Cadence St. John', '')
        if 'Katrina' in metadata.title or 'Katrina' in metadata.summary:
            movieActors.addActor('Goddess Katrina', '')
        if 'Sara Luvv' in metadata.title or 'Sara Luvv' in metadata.summary:
            movieActors.addActor('Sara Luvv', '')
        if 'Kendall Faye' in metadata.title or 'Kendall Faye' in metadata.summary:
            movieActors.addActor('Kendall Faye', '')

    #  Merciless Dominas
    elif 'Merciless Dominas' in tagline:
        #  Genre list match
        if 'lady tiger' in genreList:
            movieActors.addActor('Lady Tiger', '')
            genreList.remove('lady tiger')
        if 'princess mckenzie' in genreList:
            movieActors.addActor('Princess Mckenzie', '')
            genreList.remove('princess mckenzie')
        if 'mistress athena' in genreList:
            movieActors.addActor('Mistress Athena', '')
            genreList.remove('mistress athena')
        if 'lady deluxe' in genreList:
            movieActors.addActor('Lady Deluxe', '')
            genreList.remove('lady deluxe')
        if 'chloe lovette' in genreList:
            movieActors.addActor('Chloe Lovette', '')
            genreList.remove('chloe lovette')
        if 'mistress chloe' in genreList:
            movieActors.addActor('Chloe Lovette', '')
            genreList.remove('mistress chloe')
        if 'mistress chloe lovette' in genreList:
            movieActors.addActor('Chloe Lovette', '')
            genreList.remove('mistress chloe lovette')
        if 'miss jessica wood' in genreList:
            movieActors.addActor('Jessica Wood', '')
            genreList.remove('miss jessica wood')

    #  Miss Jade
    elif 'Miss Jade' in tagline:
        movieActors.addActor('Macey Jade', '')
        if 'miss jade' in genreList:
            genreList.remove('miss jade')

    #  Miss Kelle Martina
    elif 'Miss Kelle Martina' in tagline:
        movieActors.addActor('Kelle Martina', '')
        if 'kelle martina' in genreList:
            genreList.remove('kelle martina')
        if 'kinky kelle' in genreList:
            genreList.remove('kinky kelle')
        if 'miss kelle' in genreList:
            genreList.remove('miss kelle')

    #  Miss Kira Star
    elif 'Miss Kira Star' in tagline:
        movieActors.addActor('Kira Star', '')
        if 'kira star' in genreList:
            genreList.remove('kira star')

    #  Miss London Lix Femdom and Fetish
    elif 'Miss London Lix Femdom and Fetish' in tagline:
        movieActors.addActor('London Lix', '')
        #  Metadata match
        if 'Bratty Bunny' in metadata.title or 'Bratty Bunny' in metadata.summary:
            movieActors.addActor('Bratty Bunny', '')

    #  Miss Melissa
    elif 'Miss Melissa' in tagline:
        movieActors.addActor('Miss Melissa', '')

    #  Miss Noel Knight
    elif 'Miss Noel Knight' in tagline:
        movieActors.addActor('Noel Knight', '')

    #  Miss Roper
    elif 'Miss Roper' in tagline:
        movieActors.addActor('Raquel Roper', '')
        if 'miss roper' in genreList:
            genreList.remove('miss roper')
        if 'raquel roper' in genreList:
            genreList.remove('raquel roper')
        if 'lizzy lamb' in genreList:
            movieActors.addActor('Lizzy Lamb', '')
            genreList.remove('lizzy lamb')
        if 'sasha fox' in genreList:
            movieActors.addActor('Sasha Fox', '')
            genreList.remove('sasha fox')
        if 'anatasia rose' in genreList:
            movieActors.addActor('Anatasia Rose', '')
            genreList.remove('anatasia rose')
        if 'nikki brooks' in genreList:
            movieActors.addActor('Nikki Brooks', '')
            genreList.remove('nikki brooks')
        if 'reagan lush' in genreList:
            movieActors.addActor('Reagan Lush', '')
            genreList.remove('reagan lush')
        if 'carmen velentina' in genreList:
            movieActors.addActor('Carmen Valentina', '')
            genreList.remove('carmen valentina')

    #  Miss Suzanna Maxwell
    elif 'Miss Suzanna Maxwell' in tagline:
        movieActors.addActor('Suzanna Maxwell', '')
        #  Genre list match
        if 'suzanna' in genreList:
            genreList.remove('suzanna')
        if 'miss suzanna' in genreList:
            genreList.remove('miss suzanna')
        if 'miss suzanna maxwell' in genreList:
            genreList.remove('miss suzanna maxwell')
        if 'mistress krush' in genreList:
            movieActors.addActor('Mistress Krush', '')
            genreList.remove('mistress krush')
        if 'goddess serena' in genreList:
            movieActors.addActor('Goddess Serana', '')
            genreList.remove('goddess serena')
        if 'mistress courtney' in genreList:
            movieActors.addActor('Mistress Courtney', '')
            genreList.remove('mistress courtney')
        if 'mistress inka' in genreList:
            movieActors.addActor('Mistress Inka', '')
            genreList.remove('mistress inka')
        if 'inka' in genreList:
            movieActors.addActor('Mistress Inka', '')
            genreList.remove('inka')
        if 'ruby marks' in genreList:
            movieActors.addActor('Ruby Marks', '')
            genreList.remove('ruby marks')
        if 'miss ruby marks' in genreList:
            movieActors.addActor('Ruby Marks', '')
            genreList.remove('miss ruby marks')
        if 'ruby' in genreList:
            movieActors.addActor('Ruby Marks', '')
            genreList.remove('ruby')
        #  Metadata match
        if 'Goddess Serena' in metadata.title or 'Goddess Serena' in metadata.summary:
            movieActors.addActor('Goddess Serena', '')
        if 'Mistress Krush' in metadata.title or 'Mistress Krush' in metadata.summary:
            movieActors.addActor('Mistress Krush', '')
        if 'Mistress Marks' in metadata.title or 'Mistress Marks' in metadata.summary:
            movieActors.addActor('Ruby Marks', '')

    #  Miss Untamed FemDom Fetish Clips
    elif 'Miss Untamed FemDom Fetish Clips' in tagline:
        movieActors.addActor('Andrea Untamed', '')
        if 'miss untamed' in genreList:
            genreList.remove('miss untamed')
        if 'andrea untamed' in genreList:
            genreList.remove('andrea untamed')
        if 'stella liberty' in genreList:
            movieActors.addActor('Stella Liberty', '')
            genreList.remove('stella liberty')
        if 'cybill troy' in genreList:
            movieActors.addActor('Cybill Troy', '')
            genreList.remove('cybill troy')
        if 'cupcake sinclair' in genreList:
            movieActors.addActor('Cupcake Sinclair', '')
            genreList.remove('cupcake sinclair')

    #  Mistress - T - Fetish Fuckery
    elif '23869' in userID:
        movieActors.addActor('Mistress T', '')
        if 'astrodomina' in genreList:
            movieActors.addActor('Astro Domina', '')
            genreList.remove('astrodomina')

    #  Mistress Ayn
    elif 'Mistress Ayn' in tagline:
        movieActors.addActor('Mistress Ayn', '')
        #  Genre list match
        if 'mistress ayn' in genreList:
            genreList.remove('mistress ayn')
        #  Metadata match
        if 'Ultra Violet' in metadata.summary:
            movieActors.addActor('Mistress Ultra Violet', '')
        if 'Kellie Bardot' in metadata.summary:
            movieActors.addActor('Kellie Bardot', '')

    #  Mistress Chantel
    elif 'Mistress Chantel' in tagline:
        movieActors.addActor('Mistress Chantel', '')

    elif 'Mistress Ezada Sinn' in tagline:
        movieActors.addActor('Ezada Sinn', '')
        if 'ezada' in genreList:
            genreList.remove('ezada')
        if 'sinn' in genreList:
            genreList.remove('sinn')
        if 'ezada sinn' in genreList:
            genreList.remove('ezada sinn')
        if 'domina dinah' in genreList:
            movieActors.addActor('Domina Dinah', '')
            genreList.remove('domina dinah')
        if 'ambra' in genreList:
            movieActors.addActor('Goddess Ambra', '')
        if 'tess' in genreList:
            movieActors.addActor('Mistress Tess', '')
            genreList.remove('tess')
        if 'eris martinet' in genreList:
            movieActors.addActor('Eris Martinet', '')
            genreList.remove('eris martinet')

    #  Mistress Harley Studio
    elif 'Mistress Harley Studio' in tagline:
        movieActors.addActor('Mistress Harley', '')

    #  Mistress Jessica Starling
    elif 'Mistress Jessica Starling' in tagline:
        movieActors.addActor('Jessica Starling', '')

    #  Mistress Kawaii
    elif 'Mistress Kawaii' in tagline:
        movieActors.addActor('Mistress Kawaii', '')
        if 'mistress kawaii' in genreList:
            genreList.remove('mistress kawaii')
        if 'jasmine mendez' in genreList:
            movieActors.addActor('Jasmine Mendez', '')
            genreList.remove('jasmine mendez')

    #  Mistress Lady Renee
    elif 'Mistress Lady Renee' in tagline:
        movieActors.addActor('Lady Renee', '')
        if 'mistress lady renee' in genreList:
            genreList.remove('mistress lady renee')
        if 'lady renee' in genreList:
            genreList.remove('lady renee')
        if 'renee' in genreList:
            genreList.remove('renee')
        if 'mistress bliss' in genreList:
            movieActors.addActor('Mistress Bliss', '')
            genreList.remove('mistress bliss')
        if 'fetish liza' in genreList:
            movieActors.addActor('Fetish Liza', '')
            genreList.remove('fetish liza')

    #  Mistress Lola Ruin FemDom Fetish
    elif 'Mistress Lola Ruin FemDom Fetish' in tagline:
        movieActors.addActor('Lola Ruin', '')
        if 'lola' in genreList:
            genreList.remove('lola')

    #  Mistress Nikki Whiplash
    elif 'Mistress Nikki Whiplash' in tagline:
        movieActors.addActor('Nikki Whiplash', '')
        #  Genre list match
        if 'chloe lovette' in genreList:
            movieActors.addActor('Chloe Lovette', '')
            genreList.remove('chloe lovette')
        if 'mistresschloeuk' in genreList:
            genreList.remove('mistresschloeuk')
        if 'fetish nikki' in genreList:
            movieActors.addActor('Fetish Nikki', '')
            genreList.remove('fetish nikki')
        #  Metadata Match
        if 'Mistress Axa' in metadata.summary:
            movieActors.addActor('Mistress Axa', '')
        if 'Fetish Nikki' in metadata.summary:
            movieActors.addActor('Fetish Nikki', '')
        if 'Chloe' in metadata.summary:
            movieActors.addActor('Chloe Lovette', '')
        if 'Jessica' in metadata.summary:
            movieActors.addActor('Mistress Jessica', '')

    #  Mistress Petra Hunter
    elif 'Mistress Petra Hunter' in tagline:
        movieActors.addActor('Petra Hunter', '')
        #  Genre list match
        if 'mistress petra hunter' in genreList:
            genreList.remove('mistress petra hunter')
        if 'petra hunter' in genreList:
            genreList.remove('petra hunter')
        #  Metadata match
        if 'Elan Kane' in metadata.summary:
            movieActors.addActor('Elan Kane', '')

    #  Mistress Salem
    elif 'Mistress Salem' in tagline:
        movieActors.addActor('Mistress Salem', '')
        if 'mistress salem' in genreList:
            genreList.remove('mistress salem')

    #  MistressVictoria
    elif 'MistressVictoria' in tagline:
        movieActors.addActor('Vikki Lynn', '')
        if 'mistressvictoria' in genreList:
            genreList.remove('mistressvictoria')
        if 'missvikki' in genreList:
            genreList.remove('missvikki')
        if 'missvikkilynn' in genreList:
            genreList.remove('missvikkilynn')
        if 'twins brooke and vikki' in genreList:
            genreList.remove('twins brooke and vikki')
        if 'twin brooke and vikki' in genreList:
            genreList.remove('twin brooke and vikki')
        if 'mistress vikki lynn' in genreList:
            genreList.remove('mistress vikki lynn')
        if 'twin nikki' in genreList:
            genreList.remove('twin nikki')

    #  Morgan Rain
    elif 'Morgan Rain' in tagline:
        movieActors.addActor('Morgan Rain', '')
        if 'morgan rain' in genreList:
            genreList.remove('morgan rain')
        if 'morgan' in genreList:
            genreList.remove('morgan')
        if 'caitlyn brooks' in genreList:
            movieActors.addActor('Caitlyn Brooks', '')
            genreList.remove('caitlyn brooks')
        if 'jaycee starr' in genreList:
            movieActors.addActor('Jaycee Starr', '')
            genreList.remove('jaycee starr')

    #  My Fetish Addictions
    elif 'My Fetish Addictions' in tagline:
        movieActors.addActor('Maya Sintress', '')
        if 'miss maya sintress' in genreList:
            genreList.remove('miss maya Sintress')
        if 'maya sintress' in genreList:
            genreList.remove('maya sintress')
        if 'julie rocket' in genreList:
            movieActors.addActor('Julie Rocket', '')
            genreList.remove('julie rocket')
        if 'kendra james' in genreList:
            movieActors.addActor('Kendra James', '')
            genreList.remove('kendra james')
        if 'sully savage' in genreList:
            movieActors.addActor('Sully Savage', '')
            genreList.remove('sully savage')
        if 'princess seva' in genreList:
            movieActors.addActor('Princess Seva', '')
            genreList.remove('princess seva')
        if 'queen vanity' in genreList:
            movieActors.addActor('Queen Vanity', '')
            genreList.remove('queen vanity')
        if 'queen paris' in genreList:
            movieActors.addActor('Queen Paris', '')
            genreList.remove('queen paris')

    #  Mz Devious Fetish Clips
    elif 'Mz Devious Fetish Clips' in tagline:
        movieActors.addActor('Mz Devious', '')
        if 'mz devious' in genreList:
            genreList.remove('mz devious')
        if 'princess danni' in genreList:
            genreList.remove('princess danni')

    #  Natashas Bedroom
    elif 'Natashas Bedroom' in tagline:
        movieActors.addActor('Goddess Natasha', '')
        if 'natasha' in genreList:
            genreList.remove('natasha')
        if 'natasha\'s bedroom' in genreList:
            genreList.remove('natasha\'s bedroom')
        if 'goddess natasha' in genreList:
            genreList.remove('goddess natasha')

    #  Obey Miss Tiffany
    elif 'Obey Miss Tiffany' in tagline:
        movieActors.addActor('Miss Tiffany')

    #  Play With Amai
    elif 'Play With Amai' in tagline:
        movieActors.addActor('Amai Liu', '')
        if 'amai' in genreList:
            genreList.remove('amai')
        if 'liu' in genreList:
            genreList.remove('liu')
        if 'amai liu' in genreList:
            genreList.remove('amai liu')

    #  Princess Alexa Findom and Fetish
    elif 'Princess Alexa Findom and Fetish' in tagline:
        movieActors.addActor('Princess Alexa', '')
        if 'alexa' in genreList:
            genreList.remove('alexa')
        if 'alexaholic' in genreList:
            genreList.remove('alexaholic')

    #  Princess Amy Latina
    elif 'Princess Amy Latina' in tagline:
        movieActors.addActor('Amy Latina', '')

    #  Princess Ashley's Clip Store
    elif 'Princess Ashley\'s Clip Store' in tagline:
        movieActors.addActor('Princess Ashley', '')
        if 'princess ashley' in genreList:
            genreList.remove('princess ashley')

    #  Princess Beverly
    elif 'Princess Beverly' in tagline:
        movieActors.addActor('Princess Beverly', '')

    #  PRINCESS BREANNA'S STORE FOR LOSERS
    elif 'PRINCESS BREANNA\'S STORE FOR LOSERS' in tagline:
        movieActors.addActor('Princess Breanna', '')
        if 'princess breanna' in genreList:
            genreList.remove('princess breanna')

    #  Princess Brook Humiliatrix
    elif 'Princess Brook Humiliatrix' in tagline:
        movieActors.addActor('Princess Brook', '')

    #  Princess Camryn
    elif 'Princess Camryn' in tagline:
        movieActors.addActor('Princess Camryn', '')

    #  Princess Ellie Idol
    elif 'Princess Ellie Idol' in tagline:
        movieActors.addActor('Ellie Idol', '')
        if 'princess ellie idol' in genreList:
            genreList.remove('princess ellie idol')
        if 'london lix' in genreList:
            movieActors.addActor('London Lix', '')

    #  Princess Fierce
    elif 'Princess Fierce' in tagline:
        movieActors.addActor('Princess Fierce', '')

    #  Princess Jessy Belle
    elif 'Princess Jessy Belle' in tagline:
        movieActors.addActor('Jessy Belle', '')

    #  Princess Kimber Lee
    elif 'Princess Kimber Lee' in tagline:
        movieActors.addActor('Kimber Lee', '')
        if 'kimber lee' in genreList:
            genreList.remove('kimber lee')
        if 'princess kimber lee' in genreList:
            genreList.remove('princess kimber lee')
        if 'kimberleelive' in genreList:
            genreList.remove('kimberleelive')

    #  Princess Larkin
    elif 'Princess Larkin' in tagline:
        movieActors.addActor('Larkin Love', '')
        if 'larkin love' in genreList:
            genreList.remove('larkin love')
        if 'queen bitch larkin' in genreList:
            genreList.remove('queen bitch larkin')
        if 'princess larkin' in genreList:
            genreList.remove('princess larkin')

    #  Princess Lexie's Clip Store
    elif 'Princess Lexie\'s Clip Store' in tagline:
        movieActors.addActor('Princess Lexie', '')

    #  Princess Lucy
    elif 'Princess Lucy' in tagline:
        movieActors.addActor('Princess Lucy', '')

    #  Princess Mackaylas Sinpire
    elif 'Princess Mackaylas Sinpire' in tagline:
        movieActors.addActor('Princess Mackayla', '')
        if 'princess mackayla' in genreList:
            genreList.remove('princess mackayla')

    #  Princess Samantha
    elif 'Princess Samantha' in tagline:
        movieActors.addActor('Princess Samantha', '')

    #  Princess Shaye
    elif 'Princess Shaye' in tagline:
        movieActors.addActor('Princess Shay', '')

    #  Princess Tammie
    elif 'Princess Tammie' in tagline:
        movieActors.addActor('Tammie Madison', '')
        if 'princess tammie' in genreList:
            genreList.remove('princess tammie')
        if 'tammie madison' in genreList:
            genreList.remove('tammie madison')
        if 'tammie_' in genreList:
            genreList.remove('tammie_')

    #  Psyche Abuse - Goddess Eliza
    elif '89304' in userID:
        movieActors.addActor('Goddess Eliza', '')
        if 'goddess eliza' in genreList:
            genreList.remove('goddess eliza')

    #  Queen Amber Mae
    elif 'Queen Amber Mae' in tagline:
        movieActors.addActor('Amber Mae', '')
        if 'amber mae' in genreList:
            genreList.remove('amber mae')
        if 'goddess amber mae' in genreList:
            genreList.remove('goddess amber mae')

    #  Queen Brea
    elif 'Queen Brea' in tagline:
        movieActors.addActor('Queen Brea', '')

    #  QUEEN JENNIFER MARIE
    elif 'QUEEN JENNIFER MARIE' in tagline:
        movieActors.addActor('Jennifer Marie', '')
        if 'queenjennifermarie' in genreList:
            genreList.remove('queenjennifermarie')

    #  Raptures Fetish Playground
    elif 'Raptures Fetish Playground' in tagline:
        #  Genre list match
        if 'bella ink' in genreList:
            movieActors.addActor('Bella Ink', '')
            genreList.remove('bella ink')
        if 'bella' in genreList:
            genreList.remove('bella')
        if 'cameron dee' in genreList:
            movieActors.addActor('Cameron Dee', '')
            genreList.remove('cameron dee')
        #  Metadata match
        if 'Lilith' in metadata.title or 'Lilith' in metadata.summary:
            movieActors.addActor('Lilith', '')

    #  reiinapop
    elif 'reiinapop' in tagline:
        movieActors.addActor('Reiinapop', '')

    #  Ruby Rousson
    elif 'Ruby Rousson' in tagline:
        movieActors.addActor('Ruby Rousson', '')
        if 'ruby rousson' in genreList:
            genreList.remove('ruby rousson')
        if 'mistress rousson' in genreList:
            genreList.remove('mistress rousson')

    #  Sadurnus New Moon
    elif 'Sadurnus New Moon' in tagline:
        #  Metadata match
        if 'Mistress Tatjana' in metadata.title or 'Mistress Tatjana' in metadata.summary or 'Tatjana' in metadata.title or 'Tatjana' in metadata.summary:
            movieActors.addActor('Mistress Tatjana', '')
        if 'Darcia Lee' in metadata.title or 'Darcia Lee' in metadata.summary:
            movieActors.addActor('Darcia Lee', '')

    #  Sarah DiAvola
    elif 'Sarah DiAvola' in tagline:
        movieActors.addActor('Sarah DiAvola', '')
        if 'brat princess sarah' in genreList:
            genreList.remove('brat princess sarah')
        if 'sarah diavola' in genreList:
            genreList.remove('sarah diavola')
        if 'andrea dipre' in genreList:
            movieActors.addActor('Andrea Dipre', '')
            genreList.remove('andrea dipre')
        if 'maria marley' in genreList:
            movieActors.addActor('Maria Marley', '')
            genreList.remove('maria marley')

    #  Savannahs Fetish Fantasies
    elif 'Savannahs Fetish Fantasies' in tagline:
        movieActors.addActor('Savannah Fox', '')
        if 'skylar renee' in genreList:
            movieActors.addActor('Skylar Renee', '')
            genreList.remove('skylar renee')
        if 'lauren phillips' in genreList:
            movieActors.addActor('Lauren Phillips', '')
            genreList.remove('lauren phillips')
        if 'andrea roso' in genreList:
            movieActors.addActor('Andrea roso', '')
            genreList.remove('andrea roso')
        if 'anrea rosu' in genreList:
            movieActors.addActor('Andrea Roso', '')
            genreList.remove('andrea rosu')
        if 'arena rome' in genreList:
            movieActors.addActor('Arena Rome', '')
            genreList.remove('arena rome')
        if 'brandie mae' in genreList:
            movieActors.addActor('Brandie Mae', '')
            genreList.remove('brandie mae')
        if 'monica mynx' in genreList:
            movieActors.addActor('Monica Mynx', '')
            genreList.remove('monica mynx')
        if 'jasmeen lafleaur' in genreList:
            movieActors.addActor('Jasmeen Lafleaur', '')
            genreList.remove('jasmeen lafleaur')
        if 'jasmmen lafleur' in genreList:
            movieActors.addActor('Jasmeen Lafleaur', '')
            genreList.remove('jasmmen lafleur')
        if 'lux lives' in genreList:
            movieActors.addActor('Lux Lives', '')
            genreList.remove('lux lives')
        if 'cali carter' in genreList:
            movieActors.addActor('Cali Carter', '')
            genreList.remove('cali carter')
        if 'cali logan' in genreList:
            movieActors.addActor('Cali Logan', '')
            genreList.remove('cali logan')

    #  She Owns Your Manhood
    elif 'She Owns Your Manhood' in tagline:
        #  Genre list match
        if 'lily lane' in genreList:
            movieActors.addActor('Lily Lane', '')
            genreList.remove('lily lane')
        if 'sharron small' in genreList:
            movieActors.addActor('Sharron Small', '')
            genreList.remove('sharron small')
        if 'alexa ray' in genreList:
            movieActors.addActor('Alexa Ray', '')
            genreList.remove('alexa ray')
        if 'vivienne lamour' in genreList:
            movieActors.addActor('Vivienne Lamour', '')
            genreList.remove('vivienne lamour')
        if 'lance hart' in genreList:
            movieActors.addActor('Lance Hart', '')
            genreList.remove('lance hart')
        #  Metadata Match
        if 'Vivenne LAmours' in metadata.summary or 'VIVIENNE LAMOUR' in metadata.summary:
            movieActors.addActor('Vivienne Lamour', '')

    #  Siren Thorn Inked Asian Goddess
    elif 'Siren Thorn Inked Asian Goddess' in tagline:
        movieActors.addActor('Siren Thorn', '')
        #  Genre list match
        if 'siren thorn' in genreList:
            genreList.remove('siren thorn')
        if 'miss xi' in genreList:
            movieActors.addActor('Miss Xi', '')
            genreList.remove('miss xi')
        if 'latex barbie' in genreList:
            movieActors.addActor('Latex Barbie', '')
            genreList.remove('latex barbie')
        #  Metadata match
        if 'Miss Xi' in metadata.summary:
            movieActors.addActor('Miss Xi', '')

    #  Slutty Magic
    elif 'Slutty Magic' in tagline:
        if 'chanel santini' in genreList:
            movieActors.addActor('Chanel Santini', '')
            genreList.remove('chanel santini')
        if 'cory chase' in genreList:
            movieActors.addActor('Cory Chase', '')
            genreList.remove('cory chase')
        if 'cory chase pegging' in genreList:
            genreList.remove('cory chase pegging')
        if 'alex adams' in genreList:
            movieActors.addActor('Alex Adams', '')
            genreList.remove('alex adams')
        if 'lance hart' in genreList:
            movieActors.addActor('Lance Hart', '')
            genreList.remove('lance hart')
        if 'charlotte sartre' in genreList:
            movieActors.addActor('Charlotte Sartre', '')
            genreList.remove('charlotte sartre')
        if 'alex cole' in genreList:
            movieActors.addActor('Alex Cole', '')
            genreList.remove('alex cole')
        if 'lily lane' in genreList:
            movieActors.addActor('Lily Lane', '')
            genreList.remove('lily lane')
        if 'whitney morgan' in genreList:
            movieActors.addActor('Whitney Morgan', '')
            genreList.remove('whitney morgan')
        if 'sarah diavola' in genreList:
            movieActors.addActor('Sarah DiAvola', '')
            genreList.remove('sarah diavola')
        if 'nikki hearts' in genreList:
            movieActors.addActor('Nikki Hearts', '')
            genreList.remove('nikki hearts')

    #  SparklyHots hot clips
    elif 'SparklyHots hot clips' in tagline:
        movieActors.addActor('SparklyHot', '')

    #  SpittingBitches
    elif 'SpittingBitches' in tagline:
        if 'serena' in genreList:
            movieActors.addActor('Serena Ice', '')
            genreList.remove('serena')
        if 'serena ice' in genreList:
            movieActors.addActor('Serana Ice', '')
            genreList.remove('serena ice')
        if 'ice' in genreList:
            movieActors.addActor('Serana Ice', '')
            genreList.remove('ice')
        if 'trinity' in genreList:
            movieActors.addActor('Trinity', '')
            genreList.remove('trinity')
        if 'amber' in genreList:
            movieActors.addActor('Amber', '')
            genreList.remove('amber')

    #  Stella Liberty
    elif 'Stella Liberty' in tagline:
        movieActors.addActor('Stella Liberty', '')
        if 'stella liberty' in genreList:
            genreList.remove('stella liberty')
        if 'andrea untamed' in genreList:
            movieActors.addActor('Andrea Untamed', '')
            genreList.remove('andrea untamed')

    #  Strapon Encouragement - Dirty TalkS
    elif '7640' in userID:
        #  Genre list match
        if 'brea bennette' in genreList:
            movieActors.addActor('Brea Bennette', '')
            genreList.remove('brea bennette')
        if 'lexi belle' in genreList:
            movieActors.addActor('Lexi Belle', '')
            genreList.remove('lexi belle')
        #  Metadata match
        if 'Tiffany Brookes' in metadata.summary or 'Tiffany' in metadata.summary:
            movieActors.addActor('Tiffany Brookes', '')

    #  Tammie Madison
    elif 'Tammie Madison' in tagline:
        movieActors.addActor('Tammie Madison', '')
        if 'tammie madison' in genreList:
            genreList.remove('tammie madison')
        if 'tammie_' in genreList:
            genreList.remove('tammie_')

    #  Tara Tainton
    elif 'Tara Tainton' in tagline:
        movieActors.addActor('Tara Tainton', '')
        if 'tara tainton' in genreList:
            genreList.remove('tara tainton')
        if 'the real tara tainton' in genreList:
            genreList.remove('the real tara tainton')

    #  The AnnabelFatalecom store
    elif 'The AnnabelFatalecom store' in tagline:
        movieActors.addActor('Annabel Fatale', '')
        if 'annabellefatale' in genreList:
            genreList.remove('annabellefatale')
        if 'annabelle' in genreList:
            genreList.remove('annabelle')

    #  THE MEAN GIRLS
    elif 'THE MEAN GIRLS' in tagline:
        #  Genre list match
        if 'goddess harley' in genreList:
            movieActors.addActor('Goddess Harley', '')
            genreList.remove('goddess harley')
        if 'princess carmela' in genreList:
            movieActors.addActor('Princess Carmela', '')
            genreList.remove('princess carmela')
        if 'carmela' in genreList:
            movieActors.addActor('Princess Carmela', '')
            genreList.remove('carmela')
        if 'cindi' in genreList:
            movieActors.addActor('Princess Cindi', '')
            genreList.remove('cindi')
        if 'princess bella' in genreList:
            movieActors.addActor('Princess Bella', '')
            genreList.remove('princess bella')
        if 'queen grace' in genreList:
            movieActors.addActor('Queen Grace', '')
            genreList.remove('queen grace')
        if 'goddess platinum' in genreList:
            movieActors.addActor('Goddess Platinum', '')
            genreList.remove('goddess platinum')
        if 'princess amber' in genreList:
            movieActors.addActor('Princess Amber', '')
            genreList.remove('princess amber')
        if 'goddess draya' in genreList:
            movieActors.addActor('Goddess Draya', '')
            genreList.remove('goddess draya')
        if 'tina' in genreList:
            movieActors.addActor('Goddess Tina', '')
            genreList.remove('tina')
        if 'princess tia' in genreList:
            movieActors.addActor('Princess Tia', '')
            genreList.remove('princess tia')
        if 'princess arianna' in genreList:
            movieActors.addActor('Princess Arianna', '')
            genreList.remove('princess arianna')
        if 'princess natalia' in genreList:
            movieActors.addActor('Princess Natalia', '')
            genreList.remove('princess natalia')
        if 'princess beverly' in genreList:
            movieActors.addActor('Princess Beverly', '')
            genreList.remove('princess beverly')
        if 'princess chanel' in genreList:
            movieActors.addActor('Princess Chanel', '')
            genreList.remove('princess chanel')
        if 'princess ashley' in genreList:
            movieActors.addActor('Princess Ashley', '')
            genreList.remove('princess ashley')
        if 'goddess charlotte' in genreList:
            movieActors.addActor('Charlotte Stokely', '')
            genreList.remove('goddess charlotte')
        if 'goddess rodea' in genreList:
            movieActors.addActor('Goddess Rodea', '')
            genreList.remove('goddess rodea')
        if 'tasha reign' in genreList:
            movieActors.addActor('Tasha Reign', '')
            genreList.remove('tasha reign')

        #  Metadata match
        if 'Goddess Suvana' in metadata.summary or 'GODDESS SUVANA' in metadata.summary:
            movieActors.addActor('Goddess Suvana', '')
        if 'Empress Jennifer' in metadata.summary or 'EMPRESS JENNIFER' in metadata.summary or 'P. Jenn' in metadata.summary or 'PJenn' in metadata.summary:
            movieActors.addActor('Empress Jennifer', '')
        if 'Goddess Charlotte Stokely' in metadata.summary:
            movieActors.addActor('Charlotte Stokely', '')
        if 'QUEEN KASEY' in metadata.summary:
            movieActors.addActor('Queen Kasey', '')
        if 'Princess Cindi' in metadata.summary:
            movieActors.addActor('Princess Cindi', '')
        if 'Ash Hollywood' in metadata.summary:
            movieActors.addActor('Ash Hollywood', '')

        # Metadata match (would not work in the "elif 71196" block)
        if 'P-Jenn' in metadata.title:
            movieActors.addActor('Empress Jennifer', '')
        if 'Princess PERFECTION' in metadata.summary: 
            movieActors.addActor('Princess Perfection', '')
        if 'Goddess Farrah' in metadata.summary:
            movieActors.addActor('Goddess Farrah', '')
        if 'Goddess Alexis' in metadata.summary:
            movieActors.addActor('Goddess Alexis', '')
        if 'Goddess Nina' in metadata.summary:
            movieActors.addActor('Goddess Nina', '')
        if 'Goddess Randi' in metadata.summary:
            movieActors.addActor('Goddess Randi', '')

    #  THE MEAN GIRLS- P O V
    elif '71196' in userID:
        #  Genre list match
        if 'goddess harley' in genreList:
            movieActors.addActor('Goddess Harley', '')
            genreList.remove('goddess harley')
        if 'princess nikkole' in genreList:
            movieActors.addActor('Princess Nikkole', '')
            genreList.remove('princess nikkole')
        if 'princess beverly' in genreList:
            movieActors.addActor('Princess Beverly', '')
            genreList.remove('princess beverly')
        if 'princess ashley' in genreList:
            movieActors.addActor('Princess Ashley', '')
            genreList.remove('princess ashley')
        if 'princess chanel' in genreList:
            movieActors.addActor('Princess Chanel', '')
            genreList.remove('princess chanel')
        if 'princess amber' in genreList:
            movieActors.addActor('Princess Amber', '')
            genreList.remove('princess amber')
        if 'ash hollywood' in genreList:
            movieActors.addActor('Ash Hollywood', '')
            genreList.remove('ash hollywood')
        #  Metadata match
        if 'Queen Kasey' in metadata.summary:
            movieActors.addActor('Queen Kasey', '')

    #  The Mistress B
    elif 'The Mistress B' in tagline:
        movieActors.addActor('Mistress B', '')

    #  The Princess Miki
    elif 'The Princess Miki' in tagline:
        movieActors.addActor('Princess Miki', '')
        if 'princess miki' in genreList:
            genreList.remove('princess miki')
        if 'miki' in genreList:
            genreList.remove('miki')

    #  Trixie Miss
    elif 'Trixie Miss' in tagline:
        movieActors.addActor('Trixis Miss', '')
        if 'trixie miss' in genreList:
            genreList.remove('trixie miss')

    #  Tsarina Baltic
    elif 'Tsarina Baltic' in tagline:
        movieActors.addActor('Tsarina Baltic', '')

    #  valeriesins
    elif 'valeriesins' in tagline:
        movieActors.addActor('Valerie Sins', '')
        if 'valeriesins' in genreList:
            genreList.remove('valeriesins')

    #  Verbal Humiliatrix Princess Lacey
    elif 'Verbal Humiliatrix Princess Lacey' in tagline:
        movieActors.addActor('Princess Lacey', '')

    #  Vixen Palace
    elif 'Vixen Palace' in tagline:
        movieActors.addActor('Miss Vixen', '')

    #  Welcome to Smutty Vallie
    elif 'Welcome to Smutty Vallie' in tagline:
        movieActors.addActor('Vallie Beuys', '')
        if 'vallie beuys' in genreList:
            genreList.remove('vallie beuys')
        if 'vallie' in genreList:
            genreList.remove('vallie')
        if 'mistress vallie' in genreList:
            genreList.remove('mistress vallie')
        if 'miss vallie' in genreList:
            genreList.remove('miss vallie')

    #  Worship Amanda
    elif 'Worship Amanda' in tagline:
        movieActors.addActor('Goddess Amanda', '')

    #  Worship Goddess Jasmine
    elif 'Worship Goddess Jasmine' in tagline:
        movieActors.addActor('Jasmine Jones', '')
        if 'jasmine jones' in genreList:
            genreList.remove('jasmine jones')
        if 'goddess jasmine' in genreList:
            genreList.remove('goddess jasmine')
        if 'princess danielle' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('princess danielle')
        if 'danni maye' in genreList:
            movieActors.addActor('Danielle Maye', '')
            genreList.remove('danni maye')

    #  WORSHIP Princess NINA
    elif 'WORSHIP Princess NINA' in tagline:
        movieActors.addActor('Princess Nina', '')
        if 'worship princess nina' in genreList:
            genreList.remove('worship princess nina')
        if 'bratty princess nina' in genreList:
            genreList.remove('bratty princess nina')

    #  Worship The Wolfe
    elif 'Worship The Wolfe' in tagline:
        movieActors.addActor('Janira Wolfe', '')
        if 'janira wolfe' in genreList:
            genreList.remove('janira wolfe')
        if 'worship the wolfe' in genreList:
            genreList.remove('worship the wolfe')
        if 'elis ataxxx' in genreList:
            movieActors.addActor('Elis Ataxxx', '')
            genreList.remove('elis ataxxx')
        if 'rick fantana' in genreList:
            movieActors.addActor('Rick Fantana', '')
            genreList.remove('rick fantana')

    #  Worship Violet Doll
    elif 'Worship Violet Doll' in tagline:
        movieActors.addActor('Violet Doll', '')
        if 'violet doll' in genreList:
            genreList.remove('violet doll')
        if 'violet doll joi' in genreList:
            genreList.remove('violet doll joi')
        if 'violet doll ass worship' in genreList:
            genreList.remove('violet doll ass worship')

    #  xRussianBeautyx Clip Store
    elif 'xRussianBeautyx Clip Store' in tagline:
        movieActors.addActor('Russian Beauty', '')

    #  Young Goddess Kim
    elif 'Young Goddess Kim' in tagline:
        movieActors.addActor('Young Goddess Kim', '')
        if 'young goddess kim' in genreList:
            genreList.remove('young goddess kim')

    else:
        actorName = tagline
        actorPhotoURL = ''
        movieActors.addActor(actorName, actorPhotoURL)
    # Add Genres
    for genre in genreList:
        movieGenres.addGenre(genre)

    # Posters
    art = [
        'http://imagecdn.clips4sale.com/accounts99/%s/clip_images/previewlg_%s.jpg' % (userID, sceneID)
    ]

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
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
