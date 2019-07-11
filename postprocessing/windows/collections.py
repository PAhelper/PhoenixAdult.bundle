#Customise your collections by creating a new entry per site
#Each collection entry needs a Sitename and directory adjustment information.

#In this example sabnzbd downloads the scenes to C:\\Path\to\Porn\New and I want the final content to end up in site folders inside that folder.
#We will keep only the portion of the path before collections field 2
#We will add collections field 3 back onto whatever is remaining of the path

#Examples
#From C:\\Path\to\Porn\New      To: C:\\Path\to\Porn\New\Site       Set: collections[0] = ["Site", "New", "New\Site"]
#                               To: C:\\Path\to\Porn\Site           Set: collections[0] = ["Site", "New", "Site"]
#                               To: C:\\Different\Path\to\Site      Set: collections[0] = ["Site", "Path", "Different\Path\to\Site"]
#                               Leave in same location              Set: collections[0] = ["Site", "", ""]

collections = [None] * 28

collections[0] = ["Babes", "New", "New\Babes"]
collections[1] = ["BrattySis", "New", "New\Bratty Sis"]
collections[2] = ["CreampieAngels", "New", "New\Creampie-Angels"]
collections[3] = ["Cum4K", "New", "New\Cum4K"]
collections[4] = ["DaneJones", "New", "New\Dane Jones"]
collections[5] = ["FamilyStrokes", "New", "New\Family Strokes"]
collections[6] = ["JaysPOV", "New", "New\Jays POV"]
collections[7] = ["Lubed", "New", "New\Lubed"]
collections[8] = ["MissaX", "New", "New\MissaX"]
collections[9] = ["MomsBangTeens", "New", "New\Moms Bang Teens"]
collections[10] = ["DetentionGirls", "New", "New\Nubiles\Detention Girls"]
collections[11] = ["DriverXXX", "New", "New\Nubiles\Driver XXX"]
collections[12] = ["MomsTeachSex", "New", "New\Nubiles\Moms Teach Sex"]
collections[13] = ["MyFamilyPies", "New", "New\Nubiles\My Family Pies"]
collections[14] = ["NubileFilms", "New", "New\Nubiles\NubileFilms"]
collections[15] = ["Nubiles", "New", "New\Nubiles\Nubiles"]
collections[16] = ["NubilesET", "New", "New\Nubiles\Nubiles ET"]
collections[17] = ["NubilesPorn", "New", "New\Nubiles\Nubiles Porn"]
collections[18] = ["PetiteHDPorn", "New", "New\Nubiles\Petite HD Porn"]
collections[19] = ["StepSiblingsCaught", "New", "New\Nubiles\Step Siblings Caught"]
collections[20] = ["TeacherFucksTeens", "New", "New\Nubiles\Teacher Fucks Teens"]
collections[21] = ["PassionHD", "New", "New\Passion HD"]
collections[22] = ["PublicAgent", "New", "New\Public Agent"]
collections[23] = ["SexArt", "New", "New\SexArt"]
collections[24] = ["SisLovesMe", "New", "New\Sis Loves Me"]
collections[25] = ["SpyFam", "New", "New\SpyFam"]
collections[26] = ["Vixen", "New", "New\Vixen"]
collections[27] = ["XArt", "New", "New\X-Art"]


def getSiteMatch(site, dir):
    ID = 0
    for collection in collections:
        if site.lower() == collection[0].lower():
            overrideSite = collections[ID][0]
            overrideSplit = collections[ID][1]
            overrideDir = collections[ID][2]
            return [overrideSite, overrideSplit, overrideDir]
            
        ID += 1
    return 9999
