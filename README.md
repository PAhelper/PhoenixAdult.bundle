
PhoenixAdult metadata agent
===========================
This metadata agent helps fill Plex with information for your adult videos by pulling from the original site.

Features
--------
Currently the features of this metadata agent are:
- Scrapes any available Metadata, including:
  - Scene Title
  - Scene Summary
  - Studio
  - Originating Site (saved as the Tagline, and also a Collection for easy searching)
  - Release Date
  - Genres / Categories / Tags
  - Porn Stars (stored as Actors, with photo)
  - Scene Director
  - Movie Poster(s) / Background Art

- Function to strip common "scene" tags from filenames to assist with matching
- Function to help replace abbreviations in filenames with the full names to assist with matching
- Function to help clean up extraneous Genres
- Function to map actresses with aliases on different sites together (e.g. Doris Ivy is Gina Gerson)
- Function to locate an image for actresses where the original site doesn't provide one
- Workaround to manually set actors for unsupported sites

File Naming
-----------
The agent will try to match your file automatically, usually based on the filename. You can help it match by renaming your video appropriately (see below).
If the video is not successfully matched, you can manually try to match it using the [Match...] function in Plex, and entering as much information as you have in the format examples below.
Which type of search each site accepts is listed at the bottom of this README.
**Plex Video Files Scanner needs to be set as the library scanner for best results.

The release date can optionally be added to the filename or search terms for more accurate matching (referred to below as "Date Match" or "Date Search"). 
In select instances where a site does not make release dates available, the agent can manually add a release date if it is included in the filename or search term.  
Dates can use a 2-digit year or 4-digit year, and should always be listed directly after the Site Name.

###### Title Search

- Site - YYYY-MM-DD - Scene Title.[ext]
- Site - Scene Title.[ext]

Examples:
- Blacked - 2018-12-11 - The Real Thing.mp4
- Blacked - Hot Vacation Adventures.mp4

###### Actor Search

- Site - YYYY-MM-DD - Porn Star Name(s).[ext]
- Site - Porn Star Name(s).[ext]

Examples:
- Blacked - 2018-09-07 - Alecia Fox.mp4
- Blacked - Alecia Fox Joss Lescaf.mp4

Some sites do not have a search function available, but are still supported through direct matching. This is where SceneID Search/Match and Direct URL Match come in to play.
These usually don't make the most intuitive filenames, so it is often better to use the [Match...] function in Plex.

###### SceneID Search/Match
A numeric value found in the URL of a scene. 
Some sites rely entirely on SceneID for matching, while others only utilize it for more accurate matching. 

- Site - YYYY-MM-DD - SceneID.[ext]
- Site - SceneID.[ext]
- Site - SceneID - Scene Title.[ext]

Examples:
- EvilAngel - 2016-10-02 - 119883 (taken from the URL [https://www.evilangel.com/en/video/Allie--Lilys-Slobbery-Anal-Threesome/**119883**](https://www.evilangel.com/en/video/Allie--Lilys-Slobbery-Anal-Threesome/119883))
- MomsTeachSex - 314082 (taken from the URL [https://momsteachsex.com/tube/watch/**314082**](https://momsteachsex.com/tube/watch/314082))
- Babes - 3075191 - Give In to Desire (taken from the URL [https://www.babes.com/scene/**3075191**/1](https://www.babes.com/scene/3075191/1))

###### Direct URL Match
A string of characters at the end of a URL. Typically includes some combination of a SceneID, Scene Title, or Scene Actor.

- Site - YYYY-MM-DD - URL.[ext]
- Site - URL.[ext]

Examples:
- Mylf - 2019.01.01 - 1809 manicured-milf-masturbation (taken from the URL [https://www.mylf.com/movies/**1809/manicured-milf-masturbation**](https://www.mylf.com/movies/1809/manicured-milf-masturbation))
- PornPros - eager-hands (taken from the URL [https://pornpros.com/video/**eager-hands**](https://pornpros.com/video/eager-hands))


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

Get the PAhelper source zip in GitHub release at https://github.com/PAhelper/PhoenixAdult.bundle > "Clone or download > Download Zip
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
- 2019-06-02 2:15PM CST - Bugfix for FamilyStrokes
- 2019-05-29 3:30PM CST - Bugfixes for VirtualTaboo
- 2019-05-22:
    - Add Butt Plays (21Sextury subsite)
    - Add DorcelVision
    - Add Day With A Porn Star (Brazzers subsite)
    - Add Watch Your Mom (Naughty America subsite)
    - Fix Title DevilsFilm
    - Fix That Sitcom Show
    - Fix Search Page for DDF Network
    - Fix Search Page for Allure Media
    - Fix Search Page for network Gamma Entertainment
        - Get all pages for scenes
        - Get actress in search
    - Amateur Allure improvements:
        - More Actress Additions
    - SisLovesMe improvements:
        - Add alternate scene match method
        - Add genre "Step Sister" to all scenes
        - Poster bugfix
    - Merged multiple genres
    - Actress Aliases
    - Other fixes:
        - Term "180" was being stripped from scene titles. Was causing issues with multiple sites (ie. Kink, Evil Angel) where a numeric Scene ID is necessary/beneficial for scene matching
        - Term "4k" was being stripped from search. Causing issues with Cum4k, other sites with "4k" in title. Client now strips " 4k" or ".4k", instead
- 2019-04-23 9:45AM CST - Added Hegre.com support
- 2019-04-15 9:00AM CST - Cleaned up Perfect Gonzo code, other minor bugfixes and additions
- 2019-04-13 4:30PM CST - Added support for PervMom (direct match only)
- 2019-04-13 3:15PM CST - Added support for First Anal Quest
- 2019-04-08 6:30PM CST - Blindly added support for new Greg Lansky site Deeper, will test / confirm once I have some content downloaded
- 2019-04-07 4:15PM CST - PornPros (and related sites) now work on Linux
- 2019-04-07 2:00PM CST - Cleaned out old code from Blacked/Tushy/Vixen, improved search results (now pulls release date), improved artwork support
- 2019-04-07 11:15AM CST - Added temporary TushyRaw support through direct match (until they have enough scenes to add a search function to the site). Direct Match URL usually is the video title...
- 2019-04-06 8:30PM CST - Added DorcelClub support
- 2019-04-05 8:00AM CST - Bugfix for BadoinkVR scene match
- 2019-03-28 8:15AM CST - Cleaning up Genres all over the place, and made TeenMegaWorld Linux compatible :)
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

Supported Networks
------------------

To see the full list of all supported sites, [check out the sitelist doc](./docs/sitelist.md).
If your favorite site isn't supported, head over to [Issue #1](https://github.com/PAhelper/PhoenixAdult.bundle/issues/1) to add your request to the list, or vote on the current requests

If you like my work... I like beer :)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=K5NFB6DYPCZQA&item_name=Plex+Agent+code+development&currency_code=USD&source=url)
