
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
If the video is not successfully matched, you can manually try to match it using the [Match...] function in Plex, and entering as much information as you have, see the [manual searching document](./docs/manualsearch.md) for more information.
Which type of search each site accepts is listed in the [sitelist document](./docs/sitelist.md).
**Plex Video Files Scanner needs to be set as the library scanner for best results.**

#### Here are some naming structures we recommend:
- `SiteName` - `YYYY-MM-DD` - `Scene Name` `.[ext]`
- `SiteName` - `Scene Name` `.[ext]`
- `SiteName` - `YYYY-MM-DD` - `Actor(s)` `.[ext]`
- `SiteName` - `Actor(s)` `.[ext]`

Real world examples:
- `Blacked - 2018-12-11 - The Real Thing.mp4`
- `Blacked - Hot Vacation Adventures.mp4`
- `Blacked - 2018-09-07 - Alecia Fox.mp4`
- `Blacked - Alecia Fox Joss Lescaf.mp4`

Some sites do not have a search function available, but are still supported through direct matching. This is where SceneID Search/Match and Direct URL Match come in to play.
These usually don't make the most intuitive filenames, so it is often better to use the [Match...] function in Plex. This is further covered in the [manual searching document](./docs/manualsearch.md).

#### If you would like to name your files with SceneIDs instead of just matching in Plex, here are some examples:

- `SiteName` - `YYYY-MM-DD` - `SceneID` `.[ext]`
- `SiteName` - `SceneID` `.[ext]`
- `SiteName` - `SceneID` - `Scene Name` `.[ext]`

Real world examples:
- `EvilAngel - 2016-10-02 - 119883` (taken from the URL [https://www.evilangel.com/en/video/Allie--Lilys-Slobbery-Anal-Threesome/**119883**](https://www.evilangel.com/en/video/Allie--Lilys-Slobbery-Anal-Threesome/119883))
- `MomsTeachSex - 314082` (taken from the URL [https://momsteachsex.com/tube/watch/**314082**](https://momsteachsex.com/tube/watch/314082))
- `Babes - 3075191 - Give In to Desire` (taken from the URL [https://www.babes.com/scene/**3075191**/1](https://www.babes.com/scene/3075191/1))

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

Supported Networks
------------------

To see the full list of all supported sites, [check out the sitelist doc](./docs/sitelist.md).
If your favorite site isn't supported, head over to [Issue #1](https://github.com/PAhelper/PhoenixAdult.bundle/issues/1) to add your request to the list, or vote on the current requests

If you like my work... I like beer :)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=K5NFB6DYPCZQA&item_name=Plex+Agent+code+development&currency_code=USD&source=url)
