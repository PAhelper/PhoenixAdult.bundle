#VARIABLES

#real or test rename
dryrun=False
#delete extra files and empty folder after rename
cleanup=True
sab_cleanup=True
#debug logging
debug=True

#Permission Error if doing a batch file rename? set to true
batch=False

#How will we handle Duplicates
overwrite_duplicate = False
keep_duplicate = True
#Folder where duplicate files will placed if keep_duplicate = true
#Set to "" for original folder
duplicate_location = "C:\Path\to\Duplicates"

log_location = 'C:\Program Files\SABnzbd\scripts\pa_post.log'
#linux example '/usr/local/sabnzbd/var/logs/pa_post.log'

use_filename=False


#Media Info is a beta option and will require you to install two things.
# install pymedia info -> pip install pymediainfo
# https://mediaarea.net/en/MediaInfo the MediaInfo.DLL file for your system (NOTE: I did find this must have already been installed on my system and was not nedded)

#add mediainfo to folder name
mediainfo=False
sab_mediainfo=False
#add media info to file name
mediainfo2=False
sab_mediainfo2=False

#Customise your siteList by creating a new entry per site
#Each collection entry needs a Sitename and directory adjustment information.

#In this example sabnzbd downloads the scenes to C:\\Path\to\Porn\Downloads and I want the final content to end up in site folders inside that folder.
#We will keep only the portion of the path before siteList field 2
#We will add siteList field 3 back onto whatever is remaining of the path

#Example folder structure             Move to:                            In siteList set as follows:
#C:\\Path\to\Porn\Downloads           C:\\Path\to\Porn\Downloads\Site     Set: siteList[0] = ["Site", "Downloads", "Downloads\Site"]
#                                     C:\\Path\to\Porn\Site               Set: siteList[0] = ["Site", "Downloads", "Site"]
#                                     C:\\Different\Path\to\Site          Set: siteList[0] = ["Site", "Path", "Different\Path\to\Site"]
#                                     Leave in same location              Set: siteList[0] = ["Site", "", ""]

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
siteList[22] = ["PublicAgent", "New", "Public Agent"]
siteList[23] = ["SexArt", "New", "New\SexArt"]
siteList[24] = ["SisLovesMe", "New", "Sis Loves Me"]
siteList[25] = ["SpyFam", "New", "SpyFam"]
siteList[26] = ["Vixen", "New", "New\Vixen"]
siteList[27] = ["XArt", "New", "X-Art"]
siteList[28] = ["LittleCapriceDreams", "New", "Women\Caprice"]
siteList[29] = ["ShareMyBF", "New", "Share My BF"]
siteList[30] = ["StepSiblings", "New", "New\Step Siblings"]
siteList[31] = ["Tiny4K", "New", "Tiny4K"]
siteList[32] = ["NannySpy", "New", "NannySpy"]
siteList[33] = ["PrincessCum", "New", "Nubiles\Princess Cum"]
