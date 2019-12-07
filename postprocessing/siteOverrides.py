from datetime import datetime
from lxml import html
import requests
import logging
from siteConfig import siteList

logger = logging.getLogger(__name__)

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
    
  
    
    
   
    # FAKEHUB NETWORK
    if site.lower() in ["fakeagent", "fakeagentuk", "fakecop", "fakedrivingschool", "fakehospital", "fakehostel", "fakehuboriginals", "faketaxi", "femaleagent", "femalefaketaxi", "publicagent"]:
        if site.lower() == "fakeagent":
            site = "281"
        elif site.lower() == "fakeagentuk":
            site = "277"
        elif site.lower() == "fakecop":
            site = "278"
        elif site.lower() == "fakedrivingschool":
            site = "285"
        elif site.lower() == "fakehospital":
            site = "279"
        elif site.lower() == "fakehostel":
            site = "288"
        elif site.lower() == "fakehuboriginals":
            site = "287"
        elif site.lower() == "faketaxi":
            site = "281"
        elif site.lower() == "femaleagent":
            site = "283"
        elif site.lower() == "femalefaketaxi":
            site = "284"
        elif site.lower() == "publicagent":
            site = "282"
        
        for pagenumber in range(1, 10):
        
            page = requests.get("https://www.fakehub.com/scenes?page=" + str(pagenumber) + "&site=" + site)
            detailsPageElements = html.fromstring(page.content)
            i = 0
            for releaseDate in detailsPageElements.xpath('//div[@class="dtkdna-5 bUqDss"][1]/text()'):
                sceneID = detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a')[i].get('href').split("/")[2]
                title = sceneID + " - " + detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a/text()')[i]
                #FakeHub date format is (Mon dd, yyyy) ... convert it to yyyy-mm-dd
                datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
                releaseDate = datetime_object.strftime('%Y-%m-%d')
                if releaseDate == date:
                    return title
                i += 1
    # FAMILY STROKES
    elif site.lower() == "familystrokes":
        page = requests.get('https://www.familystrokes.com/scenes')
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for releaseDate in detailsPageElements.xpath('//div[@class="scene-date"]/text()'):
            releaseDate = releaseDate.strip()
            title = detailsPageElements.xpath('//div[@class="title"]//span/text()')[i]
            #Danejones date format is (dd/mm/yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%m/%d/%Y')
            releaseDate = datetime_object.strftime('%Y-%m-%d')
            if releaseDate == date:
                return title
            i += 1
    
    # LITTLE CAPRICE DREAMS
    elif site.lower() == "littlecapricedreams":
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
    elif site.lower() in ["anilos", "badteenspunished", "brattysis", "bountyhunterporn", "daddyslilangel", "detentiongirls", "driverxxx", "hotcrazymess", "momsteachsex", "myfamilypies", "nfbusty", "nubilefilms", "nubilescasting", "nubileset", "nubilesnet", "nubilesporn", "nubilesunscripted", "petiteballerinasfucked", "petitehdporn", "princesscum", "stepsiblingscaught", "teacherfucksteens", "thatsitcomshow"]:
        #in theory you could add more pages "/30" "/45" etc to do a backdated match
        for pagenumber in ["", "12", "24", "36", "48", "60", "72"]:
            if site.lower() in ["nubilesnet", "nubilesporn"]:
                site = "nubiles-porn"
            elif site.lower() == "nubilescasting":
                site = "nubiles-casting"
                
            url = "https://" + site.lower() + ".com/video/gallery/" + pagenumber
            page = requests.get(url)
            detailsPageElements = html.fromstring(page.content)
            i = 0
            for releaseDate in detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//span[@class= "date"]/text()'):
                sceneID = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//span[@class= "title"]/a')[i].get("href").split('/')[3]
                title = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//span[@class= "title"]/a/text()')[i].split('-')[0]
                title = sceneID + " - " + title
                #NubilesPorn date format is (Mon d, yyyy) ... convert it to yyyy-mm-dd
                datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
                releaseDate = datetime_object.strftime('%Y-%m-%d')                
                
                #extra check due to possibility of multiple releases on one date
                if site == "nubile-porn":
                    releaseSite = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//a[@class= "site-link"]/text()')[i].replace("-", "").strip()
                else:
                    releaseSite = site
                    
                if releaseDate == date and site.lower() == releaseSite.lower():
                    return title
                i += 1       
        
    # MOFOS NETWORK
    elif site.lower() in ["sharemybf"]:
        if site.lower() == "sharemybf":
            site = "201"
            
        for pagenumber in range(1,10):
            page = requests.get("https://www.mofos.com/scenes?page=" + str(pagenumber) + "&site=" + site)        
            detailsPageElements = html.fromstring(page.content)
            i = 0
            for releaseDate in detailsPageElements.xpath('//div[@class="dtkdna-5 bUqDss"][1]/text()'):
                sceneID = detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a')[i].get('href').split("/")[2]
                title = sceneID + " - " + detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a/text()')[i]
                #Mofos date format is (Mon dd, yyyy) ... convert it to yyyy-mm-dd
                datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
                releaseDate = datetime_object.strftime('%Y-%m-%d')
                if releaseDate == date:
                    return title
                i += 1

    # PORN PROS NETWORK
    elif site.lower() in ["cum4k", "lubed", "nannyspy", "passionhd", "spyfam", "tiny4k"]:
        for pagenumber in range(1,10):
            if site.lower() == "cum4k":
                page = requests.get('https://cum4k.com/?page=' + str(pagenumber))
            elif site.lower() == "holed":
                page = requests.get('https://holed.com/?page=' + str(pagenumber))
            elif site.lower() == "lubed":
                page = requests.get('https://lubed.com/?page=' + str(pagenumber))
            elif site.lower() == "nannyspy":
                page = requests.get('https://nannyspy.com/?page=' + str(pagenumber))
            elif site.lower() == "passionhd":
                page = requests.get('https://passion-hd.com/?page=' + str(pagenumber))
            elif site.lower() == "spyfam":
                page = requests.get('https://spyfam.com/?page=' + str(pagenumber))
            elif site.lower() == "tiny4k":
                page = requests.get('https://tiny4k.com/?page=' + str(pagenumber))
            
            detailsPageElements = html.fromstring(page.content)
            i = 0
            for releaseDate in detailsPageElements.xpath('//p[@class= "date"]/text()'):
                title = detailsPageElements.xpath('//div[contains(@class,"video-releases")][position()=last()]//div[@class= "information"]/a')[i].get("href").split("/")[-1].replace('-', ' ')
                #PornPros date format is (Month d, yyyy) ... convert it to yyyy-mm-dd
                datetime_object = datetime.strptime(releaseDate, '%B %d, %Y')
                releaseDate = datetime_object.strftime('%Y-%m-%d')
                if releaseDate == date:
                    return title
                i += 1
    # REALITY KINGS
    elif site.lower() in ["40inchplus", "8thstreetlatinas", "badtowtruck", "bignaturals", "bigtitsboss", "bikinicrashers", "captainstabbin", "cfnmsecret", "cumfiesta", "cumgirls", "dangerousdongs", "eurosexparties", "extremeasses", "extremenaturals", "firsttimeauditions", "flowertucci", "girlsofnaked", "happytugs", "hdlove", "hotbush", "inthevip", "mikeinbrazil", "mikesapartment", "milfhunter", "milfnextdoor", "momsbangteens", "momslickteens", "moneytalks", "monstercurves", "nofaces", "pure18", "realorgasms", "rkprime", "roundandbrown", "saturdaynightlatinas", "seemywife", "sneakysex", "streetblowjobs", "teamsquirt", "teenslovehugecocks", "topshelfpussy", "trannysurprise", "vipcrew", "welivetogether", "wivesinpantyhose"]:
        if site.lower() == "40inchplus":
            sitenum = "4"
        elif site.lower() == "8thstreetlatinas":
            sitenum = "1"
        elif site.lower() == "badtowtruck":
            sitenum = "44"
        elif site.lower() == "bignaturals":
            sitenum = "5"
        elif site.lower() == "bigtitsboss":
            sitenum = "6"
        
        elif site.lower() == "momsbangteens":
            sitenum = "27"
            
        elif site.lower() == "rkprime":
            sitenum = "45"
        
        else:
            sitenum = ""
        
        for pagenumber in range(1,10):
            page = requests.get("https://www.realitykings.com/scenes?page=" + str(pagenumber) + "&site=" + sitenum)        
            detailsPageElements = html.fromstring(page.content)
            i = 0
            for releaseDate in detailsPageElements.xpath('//div[@class="dtkdna-5 bUqDss"][1]/text()'):
                sceneID = detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a')[i].get('href').split("/")[2]
                title = sceneID + " - " + detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a/text()')[i]
                #reality kings date format is (Mon dd, yyyy) ... convert it to yyyy-mm-dd
                datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
                releaseDate = datetime_object.strftime('%Y-%m-%d')
                
                #extra check due to possibility of multiple releases on one date
                if sitenum == "":
                    releaseSite = detailsPageElements.xpath('//a[@class="sc-11m21lp-0-n jRqcyg"]/div[position()=2]/text()')[i].strip()
                else:
                    releaseSite = site
                    
                if releaseDate == date and site.lower() == releaseSite.lower():
                    return title
                i += 1
    # SEXYHUB NETWORK
    elif site.lower() in ["danejones", "fitnessrooms", "girlfriends", "lesbea", "massagerooms", "momxxx"]:
        if site.lower() == "danejones":
            site = "290"
        elif site.lower() == "fitnessrooms":
            site = "294"
        elif site.lower() == "girlfriends":
            site = "289"
        elif site.lower() == "lesbea":
            site = "291"
        elif site.lower() == "massagerooms":
            site = "292"
        elif site.lower() == "momxxx":
            site = "293"
        
        for pagenumber in range(1,10):
            page = requests.get("https://www.sexyhub.com/scenes?page=" + str(pagenumber) + "&site=" + site)        
            detailsPageElements = html.fromstring(page.content)
            i = 0
            for releaseDate in detailsPageElements.xpath('//div[@class="dtkdna-5 bUqDss"][1]/text()'):
                sceneID = detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a')[i].get('href').split("/")[2]
                title = sceneID + " - " + detailsPageElements.xpath('//span[contains(@class, "dtkdna-5")]/a/text()')[i]
                #sexyhub date format is (Mon dd, yyyy) ... convert it to yyyy-mm-dd
                datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
                releaseDate = datetime_object.strftime('%Y-%m-%d')
                if releaseDate == date:
                    return title
                i += 1
    # SISLOVESME
    elif site.lower() == "sislovesme":
        page = requests.get("https://www.sislovesme.com/")
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for releaseDate in detailsPageElements.xpath('//div[@class="thumb"]/div/a/div[@class="title_black pull-left"]/text()'):
            sceneID = detailsPageElements.xpath('//div[@class="thumb"]/div/a[@class="seo-thumb"]')[i].get('href').split('/')[3]
            title = sceneID + ' - ' + detailsPageElements.xpath('//div[@class="thumb"]/div/a/div[@class="title red pull-left"]/text()')[i]
            #SisLovesMe date format is (Mon d, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%b %d, %Y ')
            releaseDate = datetime_object.strftime('%Y-%m-%d')
            if releaseDate == date:
                return title
            i += 1
    # VIXEN
    elif site.lower() == "vixen":
        page = requests.get('https://www.vixen.com/search?q=' + title)
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for scene in detailsPageElements.xpath('//div[@data-test-component="VideoThumbnailContainer"]/div/a'):
            scenePage = "https://www.vixen.com" + detailsPageElements.xpath('//div[@data-test-component="VideoThumbnailContainer"]/div/a')[i].get("href")
            scenepage = requests.get(scenePage)
            scenePageElements = html.fromstring(scenepage.content)
            
            #date is hidden by javascript.
            tmp = scenePageElements.xpath('//script[contains(text(), "uploadDate")]')[0].text_content()
            k = tmp.find("uploadDate")
            releaseDate = tmp[k+13:k+23]
            title = scenePageElements.xpath('//h1[@data-test-component="VideoTitle"]/text()')[0]
            print title
           
            if releaseDate == date:
                return title
            i += 1
    # XART
    elif site.lower() == "xart":
        page = requests.get("https://www.x-art.com/videos/recent/all/")
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for releaseDate in detailsPageElements.xpath('//div[@class="item-header"]//h2[not(contains(text(),"HD Video"))][not(contains(text(),"4K Video"))]/text()'):
            title = detailsPageElements.xpath('//div[@class="item-header"]/h1/text()')[i]
            #Xart date format is (Mon d, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
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
