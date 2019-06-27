# Manual Search Usage

Each search query will be comprised of *up to* 5 parts, depending on the supported *search type*:
- `Site` - Either the shorthand abbreviation, or full site name.
- `Date` - in the format of either `YYYY-MM-DD` or `YY-MM-DD` ([more on how this can be used](./manualsearch.md#search-levels-and-their-capabilities))
- `Actor(s)`
- `Scene Name` - The title/name of the scene.
- `Scene ID` - A numeric value found in the URL of a scene. ([more on how this can be used](./manualsearch.md#search-levels-and-their-capabilities))
- `URL Suffix` - A string of characters at the end of a URL

Depending on the capability of any one network/site, you can try a few combiations of the above.

Here are some examples, within each level:
+ **Enhanced Search** examples:
  - A full search, with all available details:
    - `SiteName` `19 06 15` `Jane Doe` `An Interesting Plot`
  - A minimal search, with fewer details:
    - `SiteName` `Jane Doe`
  - Another minimal search, using the site shorthand:
    - `SN` `An Interesting Plot`
  
+ **Limited Search** examples:
  - A search using site name and the scene date:
    - `SiteName` `19 06 15`
  - A search using site shorthand with date + scene ID:
    - `SN` `19 06 15` `Scene ID`
  - A **Level 2/3** search using site name and just an ID:
    - `SiteName` `Scene ID`
    
+ **Exact Match** examples:
  - An exact search using site name and ID:
    - `SiteName` `Scene ID`
  - An exact search using site shorthand and ID:
    - `SN` `Scene ID`
  - A direct url match, using only a suffix:
    - `SiteName` `URL Suffix`
      - `PornPros eager-hands` (taken from the URL [https://pornpros.com/video/**eager-hands**](https://pornpros.com/video/eager-hands))
    - `SiteName` `Date` `URL Suffix`
      - `Mylf 2019.01.01 1809 manicured-milf-masturbation` (taken from the URL [https://www.mylf.com/movies/**1809/manicured-milf-masturbation**](https://www.mylf.com/movies/1809/manicured-milf-masturbation))

# Search types and their capabilities
There are 3 available search/matching methods, as listed below:
+ **Enhanced Search:** `Title` `Actor` `Date` `SceneID` (SceneID is only used to potentially enhance the search)
+ **Limited Search:** `Title` `Actor`
+ **Exact Match:** `SceneID` `Direct URL`

## Enhanced Search
#### Multi-search available.
+ Available search methods
  - **Title**
  - **Actor**
  - **Date**
  - **SceneID** (where available)

+ **SceneID Match:** SceneID can be entered as a search term alongside other search terms (Title, Actor) to increase the possibility for a match, but cannot be entered as a standalone search term.
  - Example: Though Kink has a full-fledged title/actor search function, you cannot enter just a SceneID and find results. However, if a SceneID is entered alongside a title/actor, it will increase the possibility of locating the correct scene
+ **Date Match:** Date can be entered alongside other search terms to improve search results

## Limited Search
#### Limited-search available.
+ Available search methods:
  - **Title**
  - **Actor**

## Exact Match
#### No search available.
+ **SceneID Only:** Matching relies solely on SceneID. You may add additional terms to your search (Title, Actor, Date), but if a SceneID is not entered you will not receive any results
  - Title/Actor may be added after the SceneID, however this will only serve to improve the score of releavnt results.
  - Example: Babes/PropertySex/etc. The agent strips the SceneID from your search term and plugs it into a URL. I've implemented some code so that adding a title to your search term increases the "score" you see, without a SceneID your search will return no results
+ **Direct URL Match:** A string of characters at the end of a URL. Typically includes some combination of a SceneID, Scene Title, or Scene Actor.
  - Note: Nothing can be added after the URL as it will cause issues
