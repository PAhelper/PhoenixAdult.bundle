
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

+ **Most common locations:**
  - **Linux**: `/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/`
  - **Mac**: `~/Library/Application Support/Plex Media Server/`
  - **Windows**: `%LOCALAPPDATA%\Plex Media Server/`
  - More paths listed in the [Plex documentation](https://support.plex.tv/articles/202915258-where-is-the-plex-media-server-data-directory-located/)

Get the PAhelper source zip in GitHub release at https://github.com/PAhelper/PhoenixAdult.bundle > "Clone or download > Download Zip
- Open PhoenixAdult.bundle-master.zip and copy the folder inside (PhoenixAdult.bundle-master) to the plug-ins folders
- Rename folder to "PhoenixAdult.bundle" (remove -master)

Notice
------
I try to maintain bug-free code, but sometimes bugs happen. If you are having difficulty matching a scene, [create an issue on Github](https://github.com/PAhelper/PhoenixAdult.bundle/issues) and I will do my best to address it.

**Plex Video Files Scanner needs to be set as the library scanner for best results.**

Known Limitations
-----------------
Some sites do not have a search function, we do our best to support those through direct matching.
Some sites do not have many high quality images that can be used as poster or background art. I have found the forums at [ViperGirls.to](https://linkthe.net/?https://www.vipergirls.to) to be a great resource for artwork in these situations.
Due to a bug in code, some sites are unavailable for matching on Linux installations of Plex. We're working on it.
Some sites with lots of content may return matching results, but still not include the specific scene you're trying to match. In some cases a means of direct match might work better, or choosing more unique search terms might help.

Change Log/Updates
------------------
Aside from viewing normal commit logs to see changes, an official record of changes can be found in the [CHANGELOG.md](./CHANGELOG.md) file.

Supported Networks
------------------

To see the full list of all supported sites, [check out the sitelist doc](./docs/sitelist.md).
If your favorite site isn't supported, head over to [Issue #1](https://github.com/PAhelper/PhoenixAdult.bundle/issues/1) to add your request to the list, or vote on the current requests

If you like my work... I like beer :)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=K5NFB6DYPCZQA&item_name=Plex+Agent+code+development&currency_code=USD&source=url)
