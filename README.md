
PhoenixAdult metadata agent
===========================
This metadata agent helps fill Plex with information for your adult videos by pulling from the original site.

Features
--------
Currently the features of this metadata agent are:
- Grabs all available Metadata
- Video title
- Studio
- Originating site (saved as the Tagline, and also a Collection for easy searching)
- Release Date
- Genres/Categories/Tags
- Porn Stars stored as Actors with photo
- Scene director (if available)
- Movie Poster(s) / Background art (if available)

- Function to strip common "scene" tags from filenames to assist with matching
- Function to help replace abbreviations in filenames with the full names to assist with matching
- Function to help clean up extraneous Genres
- Function to map actresses with aliases on different sites together (e.g. Doris Ivy is Gina Gerson)
- Function to locate an image for actresses where the original site doesn't provide one

File Naming
-----------
The agent will try to match your file automatically, usually based on the filename. You can help it match by renaming your video appropriately (see below).
If the video is not successfully matched, you can manually try to match it using the [Match...] function in Plex, and entering as much information as you have in the format examples below.
Which type of search each site accepts is listed at the bottom of this README.
**Plex Video Files Scanner needs to be set as the library scanner for best results.

The release date can optionally be added to the filename or search terms for more accurate matching. Date can use a 2-digit year or 4-digit year.

###### Title Search

- Site - YYYY-MM-DD - Scene Title.[ext]

Examples:
- Blacked - Hot Vacation Adventures.mp4
- Blacked - 2018-12-11 - The Real Thing.mp4
- Blackedraw - Pass Me Around.mp4

###### Actor Search

- Site - YYYY-MM-DD - Porn Star Names.[ext]
- Site - Porn Star Name Porn Star Name.[ext]

Examples:
- Blacked - 2018-09-07 - Alecia Fox.mp4
- Blacked - 18-09-07 - Alecia Fox Joss Lescaf.mp4
- Blacked - 18-09-04 - Haley Reed.mp4
- Blacked - 2018-09-04 - Haley Reed Jason Luv.mp4

###### Direct Match

Some sites do not have a search function available, but are still supported through direct matching.
These usually don't make the most intuitive filenames, so it is often better to use the [Match...] function in Plex and enter a specific ID number or a part of the URL from the original site.

Examples:
- PornPros - **eager-hands** (taken from the URL [https://pornpros.com/video/**eager-hands**](https://linkthe.net/?https://pornpros.com/video/eager-hands) to direct match)
- MomsTeachSex - **314082** (taken from the URL [https://momsteachsex.com/tube/watch/**314082**](https://linkthe.net/?https://momsteachsex.com/tube/watch/314082) to direct match)

Installation
------------
Here is how to find the plug-in folder location:
[https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-](https://linkthe.net/?https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-)

Plex main folder location:

    * '%LOCALAPPDATA%\Plex Media Server\'                                        # Windows Vista/7/8
    * '%USERPROFILE%\Local Settings\Application Data\Plex Media Server\'         # Windows XP, 2003, Home Server
    * '$HOME/Library/Application Support/Plex Media Server/'                     # Mac OS
    * '$PLEX_HOME/Library/Application Support/Plex Media Server/',               # Linux
    * '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/', # Debian,Fedora,CentOS,Ubuntu
    * '/usr/local/plexdata/Plex Media Server/',                                  # FreeBSD
    * '/usr/pbi/plexmediaserver-amd64/plexdata/Plex Media Server/',              # FreeNAS
    * '${JAIL_ROOT}/var/db/plexdata/Plex Media Server/',                         # FreeNAS
    * '/c/.plex/Library/Application Support/Plex Media Server/',                 # ReadyNAS
    * '/share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/',        # QNAP
    * '/volume1/Plex/Library/Application Support/Plex Media Server/',            # Synology, Asustor
    * '/raid0/data/module/Plex/sys/Plex Media Server/',                          # Thecus
    * '/raid0/data/PLEX_CONFIG/Plex Media Server/'                               # Thecus Plex community    

Get the latest source zip in GitHub release at https://github.com/PAhelper/PhoenixAdult.bundle > "Clone or download > Download Zip
- Open PhoenixAdult.bundle-master.zip and copy the folder inside (PhoenixAdult.bundle-master) to the plug-ins folders
- Rename folder to "PhoenixAdult.bundle" (remove -master)

Notice
------
I try to maintain bug-free code, but sometimes bugs happen. If you are having difficulty matching a scene, [create an issue on Github](https://github.com/PAhelper/PhoenixAdult.bundle/issues) and I will do my best to address it.

** Plex Video Files Scanner needs to be set as the library scanner for best results. **

Known Limitations
-----------------
Some sites do not have a search function, we do our best to support those through direct matching.
Some sites do not have many high quality images that can be used as poster or background art. I have found the forums at [ViperGirls.to](https://linkthe.net/?https://www.vipergirls.to) to be a great resource for artwork in these situations.
Due to a bug in code, some sites are unavailable for matching on Linux installations of Plex. We're working on it.
Some sites with lots of content may return matching results, but still not include the specific scene you're trying to match. In some cases a means of direct match might work better, or choosing more unique search terms might help.

Change Log/Updates
------------------
- 2019-03-02 4:45PM CST - Bugfixes for SexBabesVR, added support for sister sites SinsVR and StasyQ VR
- 2019-03-02 11:00AM EST - Added Manyvids (by id)
- 2019-03-02 3:30PM AEST - Added Sis Loves Me (a TeemSkeet site) functional but can be refined.
- 2019-03-01 7:30AM CST - Bugfix for VRBangers
- 2019-02-28 4:30PM CST - Added BlackValleyGirls (a TeamSkeet site) and multiple bugfixes
- 2019-02-27 10:00AM CST - Added Amateur Allure and Swallow Salon
- 2019-02-25 3:45PM AEST - Pull summary and additional art from PornPros Fan Sites
- 2019-02-25 9:30PM CST - Nubiles now pulls site for tagline and collection from the scene details page
- 2019-02-24 8:45PM CST - Added new way to search for Nubiles Network sites: release date, and also manually added male actors to Nubiles scenes (via name match in the Summary)
- 2019-02-24 6:45PM CST - Nubiles.net workaround (match them to "NubilesNet") and actor image fix
- 2019-02-24 6:15PM CST - Updated SexyHub and FakeHub artwork potential
- 2019-02-24 5:00PM CST - Bugfixes for Devil's Film individual DVD scenes
- 2019-02-24 4:00PM CST - Added support for BellaPass network of sites (Bryci, KatieBanks, etc.)
- 2019-02-23 4:15PM CST - Bugfix for BadoinkVR network
- 2019-02-23 1:45AM CST - Additional artwork source for Nubiles
- 2019-02-23 12:30AM CST - DDF Prod and TrueAnal bugfixes
- 2019-02-22 8:15PM CST - Nubiles bugfixes
- 2019-02-22 9:45AM CST - Added a few more standalone sites from Studio Nubiles (Anilos, HotCrazyMess, NFBusty, and ThatSitcomShow)
- 2019-02-22 8:00AM CST - Couple of Nubiles updates and bugfixes
- 2019-02-21 1:00PM CST - Added Nubiles-Porn Network, Nubiles.net, Nubilefilms (Thanks b0nensfw!)
- 2019-02-21 9:00AM CST - Added FakeHub support (except Female Fake Taxi, the information just isn't there)
- 2019-02-17 1:45PM CST - Decompressed GammaEnt search strings in init to make searching faster, bugfixes for Mile High Media and Fame Digital
- 2019-02-13 10:00AM CST - Bugfixes for GammaEnt, specifically relating to 21Sextury channels
- 2019-02-12 11:00AM CST - Bugfixes to GammaEnt and beta.Blacked code. I think the beta.blacked redesign might be fully live now...
- 2019-02-11 11:00AM CST - Bugfix for Mile High Network
- 2019-02-11 10:00AM CST - Bugfix for SexyHub
- 2019-02-10 3:30PM CST - Added full movie (DVD) support for some Gamma Entertainment sites (specifically Evil Angel and SweetSinner, though others may work)
- 2019-02-09 9:30PM CST - More bugfixes and an overhaul of the art/poster assets for JulesJordan sites
- 2019-02-08 2:45PM CST - Bugfixes for newly added JulesJordan sites, added another method of pulling release date for Gamma Entertainment search results
- 2019-02-08 8:00AM CST - Added other JulesJordan sites
- 2019-02-07 10:45AM CST - Updates to Kink.com network to fix searching, clean up the Title and Summary, fix Actors, add Shoot ID search functionality
- 2019-02-06 11:00AM CST - Added Kink.com network of sites
- 2019-02-06 8:00AM CST - Bugfix for Joymii photo set results, added several aliases for Joymii to PAactors
- 2019-02-05 8:00AM CST - Added subsite to Bang Bros search results
- 2019-02-04 2:30PM CST - Joymii bugfixes to update() function after allowing photo sets in the search results
- 2019-02-04 11:30AM CST - Moved posterAlreadyExists() function into PAsearchSites, deleted all other copies of that function throughout the code and pointed all references to it to PAsearchSites.posterAlreadyExists()
- 2019-02-04 10:00AM CST - Added actor count Genres to all sites that have manual Genres
- 2019-02-04 8:00AM CST - Changed Joymii search to include photo results, as most (all?) photo sets on that site also have an accompanying video, and some releases were only listed in the search results as photo sets
- 2019-02-03 3:45PM CST - Merged Greg Lansky sites (Blacked/Tushy/Vixen/*Raw) into networkStrike3.py
- 2019-02-01 8:30AM CST - LegalPorno bugfix, they added forum links amid their Actor lists
- 2019-01-31 11:00AM CST - Joymii bugfixes, set delposibl's actorDBfinder() function to automatically search any actor passed into PAactors that doesn't have a photo, and to search AFTER being processed by PAactors name replacements
- 2019-01-30 11:00AM CST - Added Release Date scoring anywhere I could easily (I'll get the rest as I continue to convert all the search results to common format), removed the useless variable lowerResultTitle and searchAll across the board
- 2019-01-29 10:00AM CST - Uniformity of the releaseDate variable name across all files, removed individual PornPros files now that they're converged, cleanup of formatting on siteJoymii and networkPornPros, fix for RealityKings release date to pass it from the search function to the update function in the curID, standardized the use of siteNum instead of searchSiteID across all files that address multiple sites, adjusted a few search result formats for uniformity
- 2019-01-27 5:15PM CST - Merged delposibl's code for additional VR sites, Joymii, another addition to PAactors, consolidation of the PornPros sites, and a function to find actor photos when the site doesn't have them
- 2019-01-25 2:45PM CST - Spizoo bugfixes and Gamma Ent release date fix
- 2019-01-25 8:15AM CST - Twistys search result consistency, bugfixes, and additional posters
- 2019-01-24 1:15PM CST - Gamma Ent bugfix for sites that don't list DVDs (which is most of them)
- 2019-01-23 7:30AM CST - Merged delposibl's code for 2 new NaughtyAmerica sites, and several new VR sites, additional PAactors
- 2019-01-22 8:15AM CST - Consolidated PornFidelity sites to one file, updated search to return in standard format
- 2019-01-21 9:00AM CST - Cleaned up the search section of init, a few other bugfixes
- 2019-01-20 5:15PM CST - Merged blackibanez's code for JulesJordan, Dogfart Network, DDF Network, and the Perfect Gonzo network. Added 21Sextreme network to the existing GammaEnt file.
- 2019-01-15 7:45AM CST - Added 4 new NaughtyAmerica sites: LA Sluts, Slut Stepsister, Teens Love Cream, and Latina Stepmom
- 2019-01-14 7:15PM CST - Bugfix and a few enhancements for Evil Angel
- 2019-01-14 6:30PM CST - Fixed a bug in 2-digit year date matching that was truncating part of the search title, fixed a bug in NaughtyAmerica result URLs that prevented metadata, fixed a bug in Blacked's new beta.blacked.com DOM
- 2019-01-14 10:00AM CST - Consolidated/added all Gamma Enterprises sites into a single file: networkGammaEnt.py
- 2019-01-10 10:45AM CST - Consolidated TrueAnal/Swallowed/Nympho into a single file: networkSteppedUp.py
- 2019-01-09 11:45AM CST - Added Full Porn Network (Analized, James Deen, Twisted Visual, Only Prince, Bad Daddy POV, POV Perverts, Pervert Gallery, DTF Sluts)
- 2019-01-04 4:15PM CST - Bugfixes to SexyHub/Fitness Rooms
- 2019-01-04 11:00AM CST - Updated SexyHub code for Fitness Rooms acting as a separate entity, and bugfixed one of my previous bugfixes in NaughtyAmerica
- 2019-01-03 5:15PM CST - Another minor bugfix to NaughtyAmerica, this time to Actor metadata
- 2019-01-03 4:30PM CST - Another minor bugfix to NaughtyAmerica search
- 2019-01-03 2:30PM CST - Minor bugfixes to NaughtyAmerica search, several XEmpire sites posters
- 2019-01-02 4:00PM CST - Updated NaughtyAmerica metadata so the subsite is added as the tagline and a collection, and changed to the more interesting title instead of the one used in Search Results. In the process, I also put the Babes apostrophe-handling workaround in a more elegant place (in PAsearchSites.getSearchSettings instead of __init__)
- 2019-01-02 11:30AM CST - Added code to pull full name for GloryHoleSecrets where available, also changed the Studio to Aziani (as they have a few other sites as well)
- 2018-12-31 11:30AM CST - I started getting redirected to beta.blacked.com sometimes, started writing code to accommodate that new site layout
- 2018-12-29 9:00PM CST - Added NaughtyAmerica's new site 'Big Cock Bully', changed PassionHD and FantasyHD where they can hopefully be used now
- 2018-12-28 4:30PM CST - Updated Brazzers to add a Collection for the Series if a file is part of a series, along with some minor tweaks to Blacked and BlackedRaw Studio/Tagline
- 2018-12-28 11:15AM CST - Fixed Blacked and BlackedRaw search results
- 2018-12-27 2:00PM CST - Updated Brazzers and RealityKings search results to include subsite and release date, added support for SexyHub sites
- 2018-12-26 1:30PM CST - Added PAactors.py to help clean and match Actors
- 2018-12-22 8:45PM CST - Updated Girlsway to match the rest of the XEmpire code
- 2018-12-22 8:30PM CST - Added SweetSinner
- 2018-12-22 8:15PM CST - Added Nuru Massage
- 2018-12-22 7:45PM CST - Fixed images in XEmpire sites, fixed search results for PorndoePremium, added Throated.com, SweetheartVideo.com, fixed 21Naturals.com
- 2018-12-22 1:00PM CST - Added XXX as the Content Rating for all videos, added Blockbuster movie support for Digital Playground
- 2018-12-18 8:00AM CST - Been working on cleaning up the DigitalPlayground support. Also made some improvements to the PornFidelity network searches and some code cleanup here and there
- 2018-12-13 8:00AM CST - Fixed minor bugs in GloryholeSecrets; also discovered a bunch more sites that follow the XEmpire template, should be easy adds
- 2018-12-12 10:00AM CST - Applied recent PornFidelity fixes to TeenFidelity and Kelly Madison, added support for Digital Playground videos (full movies not yet supported)
- 2018-12-11 8:00AM CST - Fixed bugs in Private metadata and images
- 2018-12-08 3:00PM CST - Fixed bugs in PornFidelity search and metadata, and in Babes search results
- 2018-12-06 8:00AM CST - Worked on adding PornPros Network sites based on SwissPlexCode's Lubed code, but realized they don't have a search on their site :( Fixed a bug in the Twisty's code that was preventing the release date, also spruced up the poster code so it pulls 5 posters and 1 bg image to choose from
- 2018-12-05 8:00AM CST - Realized PureTaboo is made by same studio as XEmpire, so copied my recently updated code for Hardx into the PureTaboo file, then made the few changes needed...
- 2018-12-03 7:00PM CST - Lots of little bug fixes to XEmpire sites (though they still don't seem to pull poster/bg images) and GloryholeSecrets
- 2018-12-03 8:00AM CST - Updated code for Hardx to correct search results, fix metadata results, and add Posters and Background (though the images appear to work in logs, they didn't work in my testing... more to come on that)
- 2018-12-01 3:00PM CST - Forked the project and uploaded the changes I've been making over the last few weeks
    + Added support for Mofos (and subsites), Babes, EvilAngel, Hardx/Darkx/Lesbianx/Eroticax, GloryholeSecrets,NewSensations, PureTaboo, Swallowed/TrueAnal/Nympho
    + I also borrowed code from SwissAdult to add Twistys (and variants), Lubed, Spizoo, and Private (and subsites)
    + I also moved my TODO list into the GitHub Issues tab
- 2018-10-02 6:00PM CST - Date match on a 2 digit year added as failover. Fixed issue with ExposedCasting not matching. Fixed Brazzers error handling when background banner was missing
- 2018-09-26 3:00PM CST - Added Porndoe Premium Network, added LegalPorno
- 2018-09-25 3:15PM CST - Bug Fix for crashing on metadata load on some sites in the Reality Kings network
- 2018-09-23 1:45PM CST - Bug fixes, split code into multiple Python files by site for better organization and aid in allowing simpler code maintenance.
    + Files can be matched to sites with or without the spaces in the site name and if .com is left in the site name as well.
    + Bang Bros - Fixed incomplete metadata due to crashing when the agent reached the video date
    + Reality Kings - Fixed missing actors and occassional crashing on poster downloads preventing genres from being added.
    + TeamSkeet - Fixed incomplete metadata on videos in the month of August
    + X-Art - Fixed incomplete metadata on videos with special characters in the title
    + Girlsway - Fixed incomplete metadata on INTERVIEW and BTS videos
    + TeenFidelity/PornFidelity/Kelly Madison - Fixed lack of metadata due to an SSL issue


- 2018-09-13 2:30PM CST - Added TeamSkeet, added Genre/Tags cleanup v1
- 2018-09-12 12:00AM CST - Added 21Naturals, PornFidelity, TeenFidelity, Kelly Madison.
- 2018-09-11 1:00AM CST - Added Reality Kings Network and Tushy.
- 2018-09-10 2:30PM CST - Added Bang Bros Network and X-Art. Fixed some Brazzers bugs.
- 2018-09-09 6:00PM CST - Initial Upload

Supported Networks
------------------
#### - Bang Bros Network *Title Search *Date/Actor Search
#### - Blacked *Title Search *Date/Actor Search
#### - BlackedRaw *Title Search *Date/Actor Search
#### - Brazzers Network *Title Search
#### - Kelly Madison *Title Search *Date/Actor Search
#### - LegalPorno *Title Search
#### - Naughty America Network *Date/Actor Search
#### - LetsDoeIt / Porndoe Premium Network *Title Search *Date/Actor Search
#### - PornFidelity *Title Search *Date/Actor Search
#### - Reality Kings Network *Title Search
#### - TeamSkeet Network *Title Search *Date/Actor Search
#### - Black Valley Girls *Scene ID Search only
#### - Sis Loves Me *Scene ID Search only
#### - TeenFidelity *Title Search *Date/Actor Search
#### - Tushy *Title Search *Date/Actor Search
#### - Vixen *Title Search *Date/Actor Search
#### - X-Art *Title Search
#### - Mofos Network *Title Search *Actor Search (adding Date will help match either)
#### - Babes Network *Title Search *Actor Search (adding Date will help match either)
#### - Gloryhole Secrets *Title Search (Title includes actress first name)
#### - New Sensations
#### - Swallowed / TrueAnal / Nymphos *Title Search (Title includes actress first name)
#### - SexyHub *Title Search
#### - FakeHub *Title Search
#### - Full Porn Network *Title Search *Actor Search (adding Date will help match either)
#### - Xempire *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - Blowpass *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - FantasyMassage *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - MileHighNetwork *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - 21Sextury *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - 21Sextreme *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - 21Naturals *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - Girlsway *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - FameDigital *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - OpenlifeNetwork *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - PureTaboo *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - GirlfriendsFilms *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - BurningAngel *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - EvilAngel *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - PrettyDirty *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - JulesJordan network - *Title Search/Actress
#### - DDFNetwork - *Title Search/Actress
#### - Dogfart - *Title Search/Actress
#### - PerfectGonzo Network *Actor Search
#### - BaDoinkVR Network *Actor search*, *Title Search* (exact spelling)(e.g. Search for "BadoinkVR **actress name**" to choose from all scenes from actress OR .../**scene_title**-#####/ => Search for "BadoinkVR **Scene Title**" in the agent to match specific scene
#### - CzechVR *Actor Search* (exact spelling)
#### - VirtualRealPorn *Title Search* (exact spelling)
#### - VirtualTaboo *Title Search* (true search, partial name allowed)
#### - VRBangers *Title Search
#### - SexBabesVR *No Search available, exact URL match only* (e.g. [https://sexbabesvr.com/virtualreality/scene/id/**225-welcum_sexy_architect**/](https://linkthe.net/?https://sexbabesvr.com/virtualreality/scene/id/225-welcum_sexy_architect/) => Search for "SexBabesVR **225-welcum_sexy_architect**" in the agent to match)
#### - WankzVR Network *Title Search* *Actor search*
#### - Wankz Network *Title Search* *Actor search*
#### - Joymii *Title Search *Actor search
#### - PornPros Network *No Search available, exact URL match only
#### - Other PornPros sites *No Search available, exact URL match only
#### - Kink.com network *Title Search *Actor Search *Partial Title or Actor + Shoot ID
#### - Nubiles.net *Shoot ID (NubilesNet - id) *Date search
#### - Nubiles-porn.com Network *Shoot ID (Nubilesporn - id) *Date search
#### - Nubilesfilms *shoot ID (Nubilesfilms - id) *Date search
#### - Bratty Sis *shoot ID (BrattySis - id) *Date search
#### - Anilos *shoot ID (Anilos - id) *Date search
#### - Hot Crazy Mess *shoot ID (HotCrazyMess - id) *Date search
#### - NF Busty *shoot ID (NFBusty - id) *Date search
#### - That Sitcom Show *shoot ID (ThatSitcomShow - id) *Date search
#### - BellaPass *Title Search
#### - Amateur Allure *Title Search *Actor Search
#### - Swallow Salon *Title Search *Actor Search
#### - Manyvids (Manyvids - id)
#### - Spizoo *Title Search *Actor Search
#### - DigitalPlayground *Title Search *Actor Search
#### - NewSensations *Actress Search* *DVD search* (exact spellings)
#### - FinishesTheJob *Title Search* *Actor Search*
#### - SexArt *Title Search* *Actor Search*
#### - TeenMegaWorld Network *Title Search* *Actor Search*
#### - Karups Network *Actor Search*
#### - Tonight's Girlfriend *Actor Search*
#### - FamilyStrokes *url Match* *Unofficial Scene Title match*



To see the full list of all supported sites, [check out the wiki](https://github.com/PAhelper/PhoenixAdult.bundle/wiki/Full-site-support-list).
If your favorite site isn't supported, head over to [Issue #1](https://github.com/PAhelper/PhoenixAdult.bundle/issues/1) to add your request to the list, or vote on the current requests

If you like my work... I like beer :)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=K5NFB6DYPCZQA&item_name=Plex+Agent+code+development&currency_code=USD&source=url)
