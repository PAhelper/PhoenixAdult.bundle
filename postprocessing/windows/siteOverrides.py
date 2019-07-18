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
siteList[1] = ["BrattySis", "New", "New\Bratty Sis"]
siteList[2] = ["CreampieAngels", "New", "New\Creampie-Angels"]
siteList[3] = ["Cum4K", "New", "New\Cum4K"]
siteList[4] = ["DaneJones", "New", "New\Dane Jones"]
siteList[5] = ["FamilyStrokes", "New", "New\Family Strokes"]
siteList[6] = ["JaysPOV", "New", "New\Jays POV"]
siteList[7] = ["Lubed", "New", "New\Lubed"]
siteList[8] = ["MissaX", "New", "New\MissaX"]
siteList[9] = ["MomsBangTeens", "New", "New\Moms Bang Teens"]
siteList[10] = ["DetentionGirls", "New", "New\Nubiles\Detention Girls"]
siteList[11] = ["DriverXXX", "New", "New\Nubiles\Driver XXX"]
siteList[12] = ["MomsTeachSex", "New", "New\Nubiles\Moms Teach Sex"]
siteList[13] = ["MyFamilyPies", "New", "New\Nubiles\My Family Pies"]
siteList[14] = ["NubileFilms", "New", "New\Nubiles\NubileFilms"]
siteList[15] = ["Nubiles", "New", "New\Nubiles\Nubiles"]
siteList[16] = ["NubilesET", "New", "New\Nubiles\Nubiles ET"]
siteList[17] = ["NubilesPorn", "New", "New\Nubiles\Nubiles Porn"]
siteList[18] = ["PetiteHDPorn", "New", "New\Nubiles\Petite HD Porn"]
siteList[19] = ["StepSiblingsCaught", "New", "New\Nubiles\Step Siblings Caught"]
siteList[20] = ["TeacherFucksTeens", "New", "New\Nubiles\Teacher Fucks Teens"]
siteList[21] = ["PassionHD", "New", "New\Passion HD"]
siteList[22] = ["PublicAgent", "New", "New\Public Agent"]
siteList[23] = ["SexArt", "New", "New\SexArt"]
siteList[24] = ["SisLovesMe", "New", "New\Sis Loves Me"]
siteList[25] = ["SpyFam", "New", "New\SpyFam"]
siteList[26] = ["Vixen", "New", "New\Vixen"]
siteList[27] = ["XArt", "New", "New\X-Art"]
siteList[28] = ["LittleCapriceDreams", "New", "New\Little Caprice Dreams"]
siteList[29] = ["ShareMyBF", "New", "New\Share My BF"]
siteList[30] = ["StepSiblings", "New", "New\Step Siblings"]
siteList[31] = ["Tiny4K", "New", "New\Tiny4K"]
siteList[32] = ["NannySpy", "New", "New\NannySpy"]
siteList[33] = ["PrincessCum", "New", "New\Nubiles\Princess Cum"]


def getSiteMatch(site, dir):
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
    logger.debug(" Site: %s" % site)
    logger.debug(" Actor: %s" % actor)
    logger.debug(" Title: %s" % title)
    logger.debug(" Date: %s" % date)
    
    if site.lower() == "brattysis":
        page = requests.get('https://brattysis.com/video/gallery')
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for releaseDate in detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//span[@class= "date"]/text()'):
            sceneID = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//a[@class= "title"]')[i].get("href").split('/')[3]
            title = detailsPageElements.xpath('//div[contains(@class, "content-grid-item")]//a[@class= "title"]/text()')[i].split('-')[0]
            title = sceneID + " - " + title
            #BrattySis date format is (Mon d, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%b %d, %Y')
            releaseDate = datetime_object.strftime('%Y-%m-%d')
            if releaseDate == date:
                return title
            i += 1
    elif site.lower() in ["detentiongirls", "driverxxx", "momsteachsex", "myfamilypies", "nubilefilms", "nubiles", "nubileset", "nubilesporn", "petiteballerinasfucked", "petitehdporn", "princesscum", "stepsiblingscaught", "teacherfucksteens"]:
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
    elif site.lower() == "danejones":
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
            
    logger.info(" No match found in getRename")
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
