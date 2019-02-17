
# PhoenixAdult metadata agent

This metadata agent will receive data from multiple sites for scene video releases.

## Features

The agent searches in two ways, Scene title or scene date with at least one star name

Currently the features of this metadata agent are:
- Grabs Metadata
- Title
- Studio
- Release Data
- Genres
- Porn Stars stored in Actors with photo
- Movie Poster
- Video banner as video background

## File Naming

**Plex Video Files Scanner needs to be set as the library scanner for best results.

For best results, file names should follow the layout below

###### Title Search

- Site - Scene Title.[ext]

Examples:
- Blacked - Hot Vacation Adventures.mp4
- Blackedraw - Pass Me Around.mp4

###### Date/Actor Search

- Site - YYYY-MM-DD - Porn Star Names.[ext]
- Site - YYYY-MM-DD - Porn Star Name Porn Star Name.[ext]

Examples:
- Blacked - 2018-09-07 - Alecia Fox.mp4
- Blacked - 2018-09-07 - Alecia Fox Joss Lescaf.mp4
- Blacked - 2018-09-04 - Haley Reed.mp4
- Blacked - 2018-09-04 - Haley Reed Jason Luv.mp4

The site can be missing from the filename, but all sites will then be searched possibly causing a mismatch.

## Installation

Here is how to find the plug-in folder location:
https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-

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

## Usage Notes
If you are doing a manual search in Plex and you wish to only search a single site, prefix your title with "Sitename - " followed by the title of the scene you wish to search.

## Notice

No real error checking is implemented. It was quickly tested on 10+ titles per site before the initial posting.

** Plex Video Files Scanner needs to be set as the library scanner for best results. **

## Known Limitations
- Teen Fidelity, Porn Fidelity, Kelly Madison, and X-Art will sometimes not pull metadata when many files from that site are being added at once. This is a limitation on the number of requests to their website. Just go back to that video and hit Refresh Metadata (or Match if it didn't make it that far) and everything should then be added.

- LegalPorno does not have high quality pictures to be used for metadata.

- GloryholeSecrets only searches by their video title, and their title is very structured and limited. Best to just search for girl's first name only e.g. "GloryholeSecrets - Rachele"

## Change Log/Updates
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

## Supported Networks/Site

#### - Bang Bros Network *Title Search *Date/Actor Search
-   Ass Parade
-   AvaSpice
-   Back Room Facials
-   Backroom MILF
-   Ball Honeys
-   Bang Bus
-   Bang Casting
-   Bang POV
-   Bang Tryouts
-   BangBros 18
-   BangBros Angels
-   Bangbros Clips
-   BangBros Remastered
-   Big Mouthfuls
-   Big Tit Cream Pie
-   Big Tits Round Asses
-   BlowJob Fridays
-   Blowjob Ninjas
-   Boob Squad
-   Brown Bunnies
-   Can He Score
-   Casting
-   Chongas
-   Colombia Fuck Fest
-   Dirty World Tour
-   Dorm Invasion
-   Facial Fest
-   Fuck Team Five
-   Glory Hole Loads
-   Latina Rampage
-   Living With Anna
-   Magical Feet
-   MILF Lessons
-   Milf Soup
-   MomIsHorny
-   Monsters of Cock
-   Mr CamelToe
-   Mr Anal
-   My Dirty Maid
-   My Life In Brazil
-   Newbie Black
-   Party of 3
-   Pawg
-   Penny Show
-   Porn Star Spa
-   Power Munch
-   Public Bang
-   Slutty White Girls
-   Stepmom Videos
-   Street Ranger
-   Tugjobs
-   Working Latinas
#### - Blacked *Title Search *Date/Actor Search
#### - BlackedRaw *Title Search *Date/Actor Search
#### - Brazzers Network *Title Search
-   Moms in Control
-   Pornstars Like It Big
-   Big Tits at Work
-   Big Tits at School
-   Baby Got Boobs
-   Real Wife Stories
-   Teens Like It Big
-   ZZ Series
-   Mommy Got Boobs
-   Milfs Like It Big
-   Big Tits in Uniform
-   Doctor Adventures
-   Exxtra
-   Big Tits in Sports
-   Big Butts like it big
-   Big Wet Butts
-   Dirty Masseur
-   Hot and Mean
-   Shes Gonna Squirt
-   Asses In Public
-   Busty Z
-   Busty and Real
-   Hot Chicks Big Asses
-   CFNM Clothed Female Male Nude
-   Teens Like It Black
-   Racks and Blacks
-   Butts and Blacks
#### - Kelly Madison *Title Search *Date/Actor Search
#### - LegalPorno *Title Search
#### - Naughty America Network *Date/Actor Search
-   Anal College
-   Watch Your Wife
-   My Friends Hot Mom
-   LA Sluts
-   Big Cock Bully
-   Slut Stepsister
-   Teens Love Cream
-   Latina Stepmom
-   My First Sex Teacher
-   Seduced By A Cougar
-   My Daughters Hot Friend
-   My Wife is My Pornstar
-   Tonights Girlfriend Class
-   Wives on Vacation
-   My Sisters Hot Friend
-   Naughty Weddings
-   Dirty Wives Club
-   My Dads Hot Girlfriend
-   My Girl Loves Anal
-   Lesbian Girl on Girl
-   Naughty Office
-   I have a Wife
-   Naughty Bookworms
-   Housewife 1 on 1
-   My Wifes Hot Friend
-   Latin Adultery
-   Ass Masterpiece
-   2 Chicks Same Time
-   My Friends Hot Girl
-   Neighbor Affair
-   My Girlfriends Busty Friend
-   Naughty Athletics
-   My Naughty Massage
-   Fast Times
-   The Passenger
-   Milf Sugar Babes Classic
-   Perfect Fucking Strangers Classic
-   Asian 1 on 1
-   American Daydreams
-   SoCal Coeds
-   Naughty Country Girls
-   Diary of a Milf
-   Naughty Rich Girls
-   My Naughty Latin Maid
-   Naughty America
-   Diary of a Nanny
-   Naughty Flipside
-   Live Party Girl
-   Live Naughty Student
-   Live Naughty Secretary
-   Live Gym Cam
-   Live Naughty Teacher
-   Live Naughty Milf
-   Live Naughty Nurse
#### - Porndoe Premium Network *Title Search *Date/Actor Search
-   Porndoe Premium
-   The White Boxxx
-   Scam Angels
-   Chicas Loca
-   Her Limit
-   A Girl Knows
-   Porno Academie
-   Xchimera
-   Carne Del Mercado
-   XXXShades
-   BumsBus
-   Bitches Abroad
-   La Cochonne
-   Crowd Bondage
-   Relaxxxed
-   My Naughty Album
-   Tu Venganza
-   Bums Buero
-   Los Consoladores
-   Quest for Orgasm
-   Transbella
-   Her Big Ass
-   Narcos X
-   Fucked In Traffic
-   Las Folladoras
-   Badtime Stories
-   Exposed Casting
-   Kinky Inlaws
-   Doe Projects
-   Porndoepedia
-   Casting Francais
-   Bums Besuch
-   Special Feet Force
-   Trans Taboo
-   Operacion Limpieza
-   La Novice
-   Casting Alla Italiana
-   PinUp Sex
-   Hausfrau Ficken
-   Deutchland Report
-   Reife Swinger
-   Scambisti Maturi
-   STG
-   XXX Omas
#### - PornFidelity *Title Search *Date/Actor Search
#### - Reality Kings Network *Title Search
-   40 Inch Plus
-   8th Street Latinas
-   Bad Tow Truck
-   Big Naturals
-   Big Tits Boss
-   Bikini Crashers
-   Captain Stabbin
-   CFNM Secret
-   Cum Fiesta
-   Cum Girls
-   Dangerous Dongs
-   Euro Sex Parties
-   Extreme Asses
-   Extreme Naturals
-   First Time Auditions
-   Flower Tucci
-   Girls of Naked
-   Happy Tugs
-   HD Love
-   Hot Bush
-   In the VIP
-   Mike in Brazil
-   Mike's Apartment
-   Milf Hunter
-   Milf Next Door
-   Moms Bang Teens
-   Moms Lick Teens
-   Money Talks
-   Monster Curves
-   No Faces
-   Pure 18
-   Real Orgasms
-   RK Prime
-   Round and Brown
-   Saturday Night Latinas
-   See My Wife
-   Sneaky Sex
-   Street BlowJobs
-   Team Squirt
-   Teens Love Huge Cocks
-   Top Shelf Pussy
-   Tranny Surprise
-   VIP Crew
-   We Live Together
-   Wives in Pantyhose
#### - TeamSkeet Network *Title Search *Date/Actor Search
-   Exxxtra small
-   Teen Pies
-   Innocent High
-   Teen Curves
-   CFNM Teens
-   Teens Love Anal
-   My Babysitters Club
-   She's New
-   Teens Do Porn
-   POV Life
-   The Real Workout
-   This Girl Sucks
-   Teens Love Money
-   Oye Loca
-   Titty Attack
-   Teeny Black
-   Lust HD
-   Rub A Teen
-   Her Freshman Year
-   Self Desire
-   Solo Interviews
-   Team Skeet Extras
-   Dyked
-   Badmilfs
-   Gingerpatch
-   BraceFaced
-   TeenJoi
-   StepSiblings
#### - TeenFidelity *Title Search *Date/Actor Search
#### - Tushy *Title Search *Date/Actor Search
#### - Vixen *Title Search *Date/Actor Search
#### - X-Art *Title Search
#### - Mofos Network
 -  Mofos
 -  Share My BF
 -  Don't Break Me
 -  I Know That Girl
 -  Let's Try Anal
 -  Pervs On Patrol
 -  Stranded Teens
 -  Mofos B Sides
 -  She's A Freak
 -  Public Pickups
#### - Babes Network
 -  Babes
 -  Babes Unleashed
 -  Black is Better
 -  Elegant Anal
 -  Office Obsession
 -  Stepmom Lessons
#### - Gloryhole Secrets *Title Search (Title includes actress first name)
#### - New Sensations
#### - Swallowed / TrueAnal / Nymphos *Title Search (Title includes actress first name)
#### - SexyHub *Title Search
 -  Dane Jones
 -  Fitness Rooms
 -  Girlfriends
 -  Lesbea
 -  Massage Rooms
 -  MomXXX
#### - Full Porn Network
 -  Analized
 -  James Deen
 -  Twisted Visual
 -  Only Prince
 -  Bad Daddy POV
 -  POV Perverts
 -  Pervert Gallery
 -  DTF Sluts
#### - Xempire *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  Hardx
 -  Darkx
 -  Lesbianx
 -  Eroticax
#### - Blowpass *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  Throated
 -  MommyBlowsBest
 -  OnlyTeenBlowjobs
 -  1000 Facials
 -  ImmoralLive
#### - FantasyMassage *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  FantasyMassage
 -  AllGirlMassage
 -  NuruMassage
 -  SoapyMassage
 -  MilkingTable
 -  MassageParlor
 -  TrickySpa
#### - MileHighNetwork *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  CherryPop
 -  SweetSinner
 -  RealityJunkies
 -  SweetheartVideo
 -  LesbianOlderYounger
 -  DoghouseDigital
#### - 21Sextury *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  AnalTeenAngels
 -  DeepthroatFrenzy
 -  DPFanatics
 -  FootsieBabes
 -  Gapeland
 -  LezCuties
 -  PixandVideo
#### - 21Sextreme *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  LustyGrandmas
 -  GrandpasFuckTeens
 -  TeachMeFisting
 -  Zoliboy
 -  DominatedGirls
#### - 21Naturals *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  21Naturals
 -  21FootArt
 -  21EroticAnal
#### - Girlsway *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  MommysGirl
 -  WebYoung
 -  GirlsTryAnal
 -  SextapeLesbians
 -  GirlswayOriginals
#### - FameDigital *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  DevilsFilm
 -  PeterNorth
 -  RoccoSiffredi
 -  TeraPatrick
#### - OpenlifeNetwork *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
 -  SunnyLeone
 -  LaneSisters
 -  DylanRyder
 -  AbbeyBrooks
 -  AshleyFires
 -  DevonLee
 -  HannaHilton
#### - PureTaboo *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - GirlfriendsFilms *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - BurningAngel *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - EvilAngel *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - PrettyDirty *Title Search *Date/Actor Search *SceneID Search (found at the end of the URL)
#### - JulesJordan network - *Title Search/Actress
 -  JulesJordan
 -  ManuelFerarra
 -  TheAssFactory
 -  SpermSwallowers
#### - DDFNetwork - *Title Search/Actress
 -  HandsOnHardcore
 -  DDFBusty
 -  HouseOfTaboo
 -  EuroGirlsOnGirls
 -  1By-Day
 -  ddfnetworkvr
 -  EuroTeenErotica
 -  HotLegsandFeet
 -  OnlyBlowJob
 -  SandysFantasys
 -  CherryJul
 -  EveAngelOfficial
 -  SexVideoCasting
 -  HairyTwatter
#### - Dogfart - *Title Search/Actress
 -  BlacksOnBlondes
 -  InterracialBlowbang
 -  CuckoldSessions
 -  GloryHole
 -  InterracialBlowbang
 -  InterracialPickups
 -  BlacksOnCougars
 -  WeFuckBlackGirls
 -  WatchingMyMomGoBlack
 -  CumBang
 -  WatchingMyDaughterGoBlack
 -  ZebraGirls
 -  Gloryhole-Initiations
 -  DogfarBehindTheScenes
 -  BlackMeatWhiteFeet
 -  SpringThomas
 -  KatieThomas
 -  RuthBlackwell
 -  CandyMonroe
 -  WifeWriting
 -  BarbCummings
 -  TheMinion
 -  BlacksOnBoys
 -  GloryholesAndHandjobs
#### - PerfectGonzo Network
 -  PerfectGonzo
 -  AllInternal
 -  AssTraffic
 -  CumForCover
 -  PrimeCups
 -  PurePOV
 -  SpermSwap
 -  TamedTeens
#### - BaDoinkVR Network *No Search available, exact URL match only
 -  BaDoinkVR
 -  18VR
 -  BabeVR
 -  KinkVR
 -  VRCosplayX
#### - VRBangers *Title Search
#### - SexBabesVR *Title (+SceneNumber) Search
#### - WankzVR Network *Title Search *Actor search
  - WankzVR
  - MilfVR
#### - Joymii *Title Search *Actor search
#### - PornPros Network *No Search available, exact URL match only
  - RealExGirlfriends
  - 18YearsOld
  - MassageCreep
  - DeepThroatLove
  - PornPros
  - TeenBFF
  - ShadyPi
  - CrueltyParty
  - Disgraced18
  - MilfHumiliation
  - CumshotSurprise
  - 40ozBounce
  - JurassicCock
  - FreaksOfCock
  - EuroHumpers
  - FreaksOfBoobs
  - CumDisgrace
  - CockCompetition
  - PimpParade
  - SquirtDisgrace
#### - Other PornPros sites *No Search available, exact URL match only
  - POVD
  - Tiny4k
  - Cum4K
  - Exotic4k
  - PureMature
  - MyVeryFirstTime
  - Holed
  - Lubed
  - Passion-HD
  - FantasyHD
  - NannySpy
  - CastingCouch-X
  - SpyFam
#### - Kink.com network *Title Search *Actor Search *Partial Title or Actor + Shoot ID
  - BoundGangBangs
  - BrutalSessions
  - DeviceBondage
  - FamiliesTied
  - HardcoreGangbang
  - Hogtied
  - KinkFeatures
  - KinkUniversity
  - PublicDisgrace
  - SadisticRope
  - SexAndSubmission
  - TheTrainingOfO
  - TheUpperFloor
  - WaterBondage
  - EverythingButt
  - FootWorship
  - FuckingMachines
  - TSPussyHunters
  - TSSeduction
  - UltimateSurrender
  - 30MinutesofTorment
  - BoundGods
  - BoundinPublic
  - ButtMachineBoys
  - MenOnEdge
  - NakedKombat
  - DivineBitches
  - Electrosluts
  - MenInPain
  - WhippedAss
  - WiredPussy
