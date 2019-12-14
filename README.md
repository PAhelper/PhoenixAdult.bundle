
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
  - Originating Site / Subsite / Site Collection (saved as the Tagline, and also a Collection for easy searching)
  - Release Date
  - Genres / Categories / Tags
  - Porn Stars (stored as Actors, with photo)
  - Scene Director(s)
  - Movie Poster(s) / Background Art

- Function to strip common "scene" tags to assist with matching
- Function to replace abbreviated site names with full site names to assist with matching
- Function to clean up / merge genres
- Function to clean up / merge actresses with aliases (e.g. Doris Ivy is Gina Gerson)
- Function to locate an image for actors where the original site doesn't provide one
- Function to manually add actors for sites the agent doesn't support
- Function to automatically rename files (WIP)

File Naming
-----------
The agent will try to match your file automatically, usually based on the filename. You can assist it by renaming your video appropriately.
If the video is not successfully matched, you can try to manually match it using the [Match...] function in Plex. See the [manual searching document](./docs/manualsearch.md) for more information.
Best practice for each site is listed in the [sitelist document](./docs/sitelist.md).
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

Some sites do not have a search function available. This is where SceneID and Direct URL come in to play.
These usually don't make the most intuitive filenames, so it is often better to use the [Match...] function in Plex. See the [manual searching document](./docs/manualsearch.md) for more information.

#### If you would prefer to integrate SceneIDs into your filenames, instead of manually matching in Plex, here are some naming structures we recommend:

- `SiteName` - `YYYY-MM-DD` - `SceneID` `.[ext]`
- `SiteName` - `SceneID` `.[ext]`
- `SiteName` - `SceneID` - `Scene Name` `.[ext]`

Real world examples:
- `EvilAngel - 2016-10-02 - 119883` (taken from the URL [https://www.evilangel.com/en/video/Allie--Lilys-Slobbery-Anal-Threesome/**119883**](https://www.evilangel.com/en/video/Allie--Lilys-Slobbery-Anal-Threesome/119883))
- `MomsTeachSex - 314082` (taken from the URL [https://momsteachsex.com/tube/watch/**314082**](https://momsteachsex.com/tube/watch/314082))
- `Babes - 3075191 - Give In to Desire` (taken from the URL [https://www.babes.com/scene/**3075191**/1](https://www.babes.com/scene/3075191/1))

Installation
------------
How to find the plug-in folder location:
[https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-](https://linkthe.net/?https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-)

- Get the PAhelper source zip in GitHub release at https://github.com/PAhelper/PhoenixAdult.bundle > "Clone or download > Download Zip
- Open PhoenixAdult.bundle-master.zip and copy the folder inside (PhoenixAdult.bundle-master) to the plug-ins folders
- Rename folder to "PhoenixAdult.bundle" (remove "-master")

Reporting a bug
------
We try to maintain bug-free code, but bugs do happen. If you are having difficulty matching a scene, please refer to [Known Issues](https://github.com/PAhelper/PhoenixAdult.bundle/issues/218) before submitting an Issue.

Known Limitations
-----------------
Some sites do not have many high quality images that can be used as poster or background art. I have found the forums at [ViperGirls.to](https://linkthe.net/?https://www.vipergirls.to) to be a great resource for artwork in these situations.

Change Log/Updates
------------------
To view the most detailed changes to code, check the [commit log](https://github.com/PAhelper/PhoenixAdult.bundle/commits/master). Additional information can be obtained from the list of [merged pull requests](https://github.com/PAhelper/PhoenixAdult.bundle/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Amerged).

Supported Networks
------------------

To view the full list of supported sites, [check out the sitelist doc](./docs/sitelist.md).
If your favorite site isn't supported, head over to [Issue #1](https://github.com/PAhelper/PhoenixAdult.bundle/issues/1) to add your request to the list, or vote on the current requests.
