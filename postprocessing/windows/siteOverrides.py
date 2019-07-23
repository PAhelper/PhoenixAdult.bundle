from datetime import datetime
from lxml import html
import requests
import logging

logger = logging.getLogger(__name__)

#Customise your siteList by creating a new entry per site
#Each collection entry needs a Sitename and directory adjustment information.

#In this example sabnzbd downloads the scenes to C:\\Path\to\Porn\New and I want the final content to end up in site folders inside that folder.
#We will keep only the portion of the path before siteList field 2
#We will add siteList field 3 back onto whatever is remaining of the path

#Examples
#From C:\\Path\to\Porn\New      To: C:\\Path\to\Porn\New\Site       Set: siteList[0] = ["Site", "New", "New\Site"]
#                               To: C:\\Path\to\Porn\Site           Set: siteList[0] = ["Site", "New", "Site"]
#                               To: C:\\Different\Path\to\Site      Set: siteList[0] = ["Site", "Path", "Different\Path\to\Site"]
#                               Leave in same location              Set: siteList[0] = ["Site", "", ""]

siteList = [None] * 34

siteList[0] = ["Babes", "New", "New\Babes"]
siteList[1] = ["BrattySis", "New", "Bratty Sis"]
siteList[2] = ["CreampieAngels", "New", "New\Creampie-Angels"]
siteList[3] = ["Cum4K", "New", "Cum4K"]
siteList[4] = ["DaneJones", "New", "Dane Jones"]
siteList[5] = ["FamilyStrokes", "New", "New\Family Strokes"]
siteList[6] = ["JaysPOV", "New", "Jays POV"]
siteList[7] = ["Lubed", "New", "Lubed"]
siteList[8] = ["MissaX", "New", "New\MissaX"]
siteList[9] = ["MomsBangTeens", "New", "Moms Bang Teens"]
siteList[10] = ["DetentionGirls", "New", "Nubiles\Detention Girls"]
siteList[11] = ["DriverXXX", "New", "Nubiles\Driver XXX"]
siteList[12] = ["MomsTeachSex", "New", "Nubiles\Moms Teach Sex"]
siteList[13] = ["MyFamilyPies", "New", "Nubiles\My Family Pies"]
siteList[14] = ["NubileFilms", "New", "Nubiles\Nubile Films"]
siteList[15] = ["Nubiles", "New", "Nubiles\Nubiles"]
siteList[16] = ["NubilesET", "New", "Nubiles\Nubiles ET"]
siteList[17] = ["NubilesPorn", "New", "Nubiles\Nubiles Porn"]
siteList[18] = ["PetiteHDPorn", "New", "Nubiles\Petite HD Porn"]
siteList[19] = ["StepSiblingsCaught", "New", "Nubiles\Step Siblings Caught"]
siteList[20] = ["TeacherFucksTeens", "New", "Nubiles\Teacher Fucks Teens"]
siteList[21] = ["PassionHD", "New", "Passion HD"]
siteList[22] = ["PublicAgent", "New", "New\Public Agent"]
siteList[23] = ["SexArt", "New", "New\SexArt"]
siteList[24] = ["SisLovesMe", "New", "New\Sis Loves Me"]
siteList[25] = ["SpyFam", "New", "SpyFam"]
siteList[26] = ["Vixen", "New", "New\Vixen"]
siteList[27] = ["XArt", "New", "New\X-Art"]
siteList[28] = ["LittleCaprice", "New", "Women\Caprice"]
siteList[29] = ["ShareMyBF", "New", "Share My BF"]
siteList[30] = ["StepSiblings", "New", "New\Step Siblings"]
siteList[31] = ["Tiny4K", "New", "Tiny4K"]
siteList[32] = ["NannySpy", "New", "NannySpy"]
siteList[33] = ["PrincessCum", "New", "Nubiles\Princess Cum"]


def getSiteMatch(site, dir):
    logger.debug(" Before:")
    logger.debug("    Site: %s" % site)
    logger.debug("    Dir: %s" % dir)
    ID = 0
    for item in siteList:
        if site.lower() == item[0].lower():
            overrideSite = siteList[ID][0]
            overrideSplit = siteList[ID][1]
            overrideDir = siteList[ID][2]
            return [overrideSite, overrideSplit, overrideDir]
            
        ID += 1
    return 9999
    
def getRename(site, actor, title, date):
    logger.debug("    Actor: %s" % actor)
    logger.debug("    Title: %s" % title)
    logger.debug("    Date: %s" % date)
    
  
    
    #DANE JONES
    if site.lower() == "danejones":
        page = requests.get('https://www.danejones.com/tour/videos')
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for scene in detailsPageElements.xpath('//article'):
            releaseDate = detailsPageElements.xpath('//article//div[@class ="release-date"]/text()')[i]
            title = detailsPageElements.xpath('//article//div[@class ="card-title"]/a')[i].get("title")
            #Danejones date format is (Month d, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%B %d, %Y')
            releaseDate = datetime_object.strftime('%Y-%m-%d')
            if releaseDate == date:
                return title
            i += 1
    #LITTLE CAPRICE
    if site.lower() == "littlecaprice":
        page = requests.get('https://www.littlecaprice-dreams.com/videos/')
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for releaseDate in detailsPageElements.xpath('//div[@class= "meta"]/a/p/text()'):
            title = detailsPageElements.xpath('//div[@class= "meta"]/a/h3/text()')[i]
            #Danejones date format is (Month d, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%B %d, %Y')
            releaseDate = datetime_object.strftime('%Y-%m-%d')
            if releaseDate == date:
                return title
            i += 1
    # NUBILES NETWORK
    elif site.lower() in ["anilos", "brattysis", "hotcrazymess", "nfbusty", "nubilefilms", "nubilesnet", "thatsitcomshow"]:
        if site.lower() == "brattysis":
            page = requests.get('https://brattysis.com/video/gallery')
        elif site.lower() == "nubilefilms":
            page = requests.get('https://nubilefilms.com/video/gallery')
        else:
            url = "https://" + site.lower() + "/video/gallery"
            page = requests.get(url)

        detailsPageElements = html.fromstring(page.content)
        i = 0
        for releaseDate in detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//span[@class= "date"]/text()'):
            sceneID = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//a[@class= "title"]')[i].get("href").split('/')[3]
            title = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//a[@class= "title"]/text()')[i].split('-')[0]
            title = sceneID + " - " + title
            #date format is (Mon d, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
            releaseDate = datetime_object.strftime('%Y-%m-%d')
            if releaseDate == date:
                return title
            i += 1
    elif site.lower() in ["badteenspunished", "bountyhunterporn", "daddyslilangel", "detentiongirls", "driverxxx", "momsteachsex", "myfamilypies", "nubilescasting", "nubileset", "nubilesporn", "nubilesunscripted", "petiteballerinasfucked", "petitehdporn", "princesscum", "stepsiblingscaught", "teacherfucksteens"]:
        #in theory you could add more pages "/30" "/45" etc to do a backdated match
        for url in ["", "/15"]:
            page = requests.get("https://nubiles-porn.com/video/gallery" + url)
            detailsPageElements = html.fromstring(page.content)
            i = 0
            for releaseDate in detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//span[@class= "date"]/text()'):
                sceneID = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//a[@class= "title"]')[i].get("href").split('/')[3]
                title = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//a[@class= "title"]/text()')[i].split('-')[0]
                title = sceneID + " - " + title
                #NubilesPorn date format is (Mon d, yyyy) ... convert it to yyyy-mm-dd
                datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
                releaseDate = datetime_object.strftime('%Y-%m-%d')                
                
                #extra check due to possibility of multiple releases on one date
                releaseSite = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//a[@class= "site-link"]/text()')[i].replace("-", "").strip()
                if releaseDate == date and site.lower() == releaseSite.lower():
                    return title
                i += 1       
        
    #MOFOS NETWORK
    elif site.lower() in ["sharemybf"]:
        if site.lower() == "sharemybf":
            site = "201"
            
        page = requests.get("https://www.mofos.com/scenes?page=1&site=" + site)
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for releaseDate in detailsPageElements.xpath('//div[@class="dtkdna-5 bUqDss"][1]/text()'):
            print releaseDate
            sceneID = detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a')[i].get('href').split("/")[2]
            title = sceneID + " - " + detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a/text()')[i]
            print title
            #Mofos date format is (Mon dd, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
            releaseDate = datetime_object.strftime('%Y-%m-%d')
            if releaseDate == date:
                return title
            i += 1
    # PORN PROS NETWORK
    elif site.lower() in ["cum4k", "lubed", "nannyspy", "passionhd", "spyfam", "tiny4k"]:
        if site.lower() == "cum4k":
            page = requests.get('https://cum4k.com/?page=1')
        elif site.lower() == "holed":
            page = requests.get('https://holed.com/?page=1')
        elif site.lower() == "lubed":
            page = requests.get('https://lubed.com/?page=1')
        elif site.lower() == "nannyspy":
            page = requests.get('https://nannyspy.com/?page=1')
        elif site.lower() == "passionhd":
            page = requests.get('https://passion-hd.com/?page=1')
        elif site.lower() == "spyfam":
            page = requests.get('https://spyfam.com/?page=1')
        elif site.lower() == "tiny4k":
            page = requests.get('https://tiny4k.com/?page=1')
        
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for releaseDate in detailsPageElements.xpath('//p[@class= "date"]/text()'):
            title = detailsPageElements.xpath('//div[@class= "information"]/a')[i].get("href").split("/")[-1].replace('-', ' ')
            #PornPros date format is (Month d, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%B %d, %Y')
            releaseDate = datetime_object.strftime('%Y-%m-%d')
            if releaseDate == date:
                return title
            i += 1
    # REALITY KINGS
    elif site.lower() in ["40inchplus", "8thstreetlatinas", "badtowtruck", "bignaturals", "bigtitsboss", "bikinicrashers", "captainstabbin", "cfnmsecret", "cumfiesta", "cumgirls", "dangerousdongs", "eurosexparties", "extremeasses", "extremenaturals", "firsttimeauditions", "flowertucci", "girlsofnaked", "happytugs", "hdlove", "hotbush", "inthevip", "mikeinbrazil", "mikesapartment", "milfhunter", "milfnextdoor", "momsbangteens", "momslickteens", "moneytalks", "monstercurves", "nofaces", "pure18", "realorgasms", "rkprime", "roundandbrown", "saturdaynightlatinas", "seemywife", "sneakysex", "streetblowjobs", "teamsquirt", "teenslovehugecocks", "topshelfpussy", "trannysurprise", "vipcrew", "welivetogether", "wivesinpantyhose"]:
        for url in ["1", "2"]:
            page = requests.get("https://www.realitykings.com/tour/videos/all-sites/all-categories/all-time/recent/" + url)
            detailsPageElements = html.fromstring(page.content)
            i = 0
            for releaseDate in detailsPageElements.xpath('//span[@class= "card-info__meta-date"]/text()'):
                title = detailsPageElements.xpath('//h2[@class= "card-info__title"]/a')[i].get("title")
                #Reality Kings date format is (Month d, yyyy) ... convert it to yyyy-mm-dd
                datetime_object = datetime.strptime(releaseDate, '%B %d, %Y')
                releaseDate = datetime_object.strftime('%Y-%m-%d')                
                
                #extra check due to possibility of multiple releases on one date
                releaseSite = detailsPageElements.xpath('//div[@class= "card-info__meta"]/a')[i].get("title").replace("-", "").replace(" ", "").strip()
                if releaseDate == date and site.lower() == releaseSite.lower():
                    return title
                i += 1 
    #VIXEN
    elif site.lower() == "vixentest":
        page = requests.get('https://www.vixen.com/search?q=' + title)
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for scene in detailsPageElements.xpath('//div[@data-test-component="VideoThumbnailContainer"]/div/a'):
            scenePage = "https://www.vixen.com" + detailsPageElements.xpath('//div[@data-test-component="VideoThumbnailContainer"]/div/a')[i].get("href")
            scenepage = requests.get(scenePage)
            scenePageElements = html.fromstring(scenepage.content)
            
            #date is hidden by javascript. Json scraper might be able to retriev eit, need to work out how
            releaseDate = scenePageElements.xpath('//button[@title="Release date"]/span')[0].text_content()
            title = scenePageElements.xpath('//h1[@data-test-component="VideoTitle"]/text()')
            #Vixen date format is (Month d, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%B %d, %Y')
            releaseDate = datetime_object.strftime('%Y-%m-%d')
            if releaseDate == date:
                return title
            i += 1
        
        
    logger.info("No match found in getRename")
    return 9999
    
def getMediaInfo(file):
    from pymediainfo import MediaInfo
    media_info = MediaInfo.parse(file)
    for track in media_info.tracks:
        if track.track_type == 'Video':
            logger.debug(" Resolution: %sp, Framerate: %s" % (track.height, track.frame_rate))
            #customise however you wish.
            media_Info = str(track.height) + "p " + str(track.frame_rate).replace('.000', '') + "fps"
            return media_Info
    return 9999  
