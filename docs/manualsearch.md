# Manual Search Usage

Each search query will be comprised of *up to* 5 parts, depending on the supported [*search type*](./manualsearch.md#search-types-and-their-capabilities):
- `Site` - Either the shorthand abbreviation, or full site name.
- `Date` - Follows immediately after site name, in the format of either `YYYY-MM-DD` or `YY-MM-DD` ([more on how this can be used](./manualsearch.md#search-types-and-their-capabilities))
- `Actor(s)`
- `Title` - The title/name of the scene.
- `SceneID` - A numeric value found in the URL of a scene. ([more on how this can be used](./manualsearch.md#search-types-and-their-capabilities))
- `Direct URL` - A string of characters at the end of a URL

# Search types and their capabilities
There are 3 available search/matching methods, as listed below:
+ **Enhanced Search:** `Title` `Actor` `Date` `SceneID`
+ **Limited Search:** `Title` `Actor`
+ **Exact Match:** `SceneID` `Direct URL`

## Enhanced Search
#### Multi-search available.
+ Available search methods
  - **Title**
  - **Actor**
  - **Date**
  - **SceneID** (where available, and is only used to potentially enhance the search)

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

# Search Examples
Depending on the capability of any one network/site, you can try a few combiations of the above.

Here are some examples for each type of search:
+ **Enhanced Search** examples:
  - A full search, with all available details:
    - `SiteName` `YY-MM-DD` `Jane Doe` `An Interesting Plot`
  - A minimal search, with fewer details, but includes SceneID:
    - `SiteName` `Jane Doe` `SceneID`
  - A basic search with the most common details:
    - `SiteName` `Jane Doe` `An Interesting Plot`
  - Another minimal search, using the site shorthand:
    - `SN` `An Interesting Plot`
  
+ **Limited Search** examples:
  - A search using both actor and scene title:
    - `SiteName` `Jane Doe` `An Interesting Plot`
  - A search using site name and an actor from the scene:
    - `SiteName` `Jane Doe`
  - A search using site shorthand with the scene title:
    - `SN` `An Interesting Plot`
    
+ **Exact Match** examples:
  - An exact search using site name and ID:
    - `SiteName` `SceneID`
  - An exact search using site shorthand and ID:
    - `SN` `SceneID`
  - A direct url match, using only a suffix:
    - `SiteName` `Direct URL`
      - `PornPros` `eager-hands` (taken from the URL [https://pornpros.com/video/**eager-hands**](https://pornpros.com/video/eager-hands))
    - `SiteName` `YY-MM-DD` `Direct URL`
      - `Mylf 2019.01.01 1809` `manicured-milf-masturbation` (taken from the URL [https://www.mylf.com/movies/**1809/manicured-milf-masturbation**](https://www.mylf.com/movies/1809/manicured-milf-masturbation))
