from datetime import datetime
from lxml import html
import requests
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

siteList = [None] * 33

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
    
def getRename(site, actor, date):
    
    if site.lower() == "danejones":
        page = requests.get('https://www.danejones.com/tour/videos')
        detailsPageElements = html.fromstring(page.content)
        i = 0
        for scene in detailsPageElements.xpath('//article'):
            releaseDate = detailsPageElements.xpath('//article//div[@class ="release-date"]/text()')[i]
            title = detailsPageElements.xpath('//article//div[@class ="card-title"]/a')[i].get("title")
            #Danejones Date format is (Month d, yyyy) ... convert it to yyyy-mm-dd
            datetime_object = datetime.strptime(releaseDate, '%B %d, %Y')
            siteDate = datetime_object.strftime('%Y-%m-%d')
            if siteDate == date:
                return title
            i += 1

    return 9999
