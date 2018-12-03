
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

## Change Log/Updates
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

#### - 21Naturals *Title Search *Date/Actor Search
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
#### - Girlsway *Title Search
#### - Kelly Madison *Title Search *Date/Actor Search
#### - LegalPorno *Title Search
#### - Naughty America Network *Date/Actor Search
-   My Friends Hot Mom
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
#### - Evil Angel
#### - XEmpire
 -  Hardx
 -  Darkx
 -  Lesbianx
 -  Eroticax
#### - Gloryhole Secrets
#### - New Sensations
#### - Pure Taboo
#### - Swallowed / TrueAnal / Nymphos



