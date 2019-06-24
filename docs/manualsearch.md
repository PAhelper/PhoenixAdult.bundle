# Manual Search Usage

Each search query will be comprised of *up to* 5 parts, depending on the supported *level*:
- `Site` - Either the shorthand abbreviation, or full site name.
- `Date` (more on this below)
- `Actor(s)`
- `Scene Name` - The title/name of the scene.
- `Scene ID` (more on this below)

Depending on the capability of any one network/site, you can try a few combiations of the above.

Here are some examples, within each level:
+ **Level 1** examples:
  - A full search, with all available details:
    - `SiteName` `19 06 15` `Jane Doe` `An Interesting Plot`
  - A minimal search, with fewer details:
    - `SiteName` `Jane Doe`
  - Another minimal search, using the site shorthand:
    - `SN` `An Interesting Plot`
  
+ **Level 2** examples:
  - A search using site name and the scene date:
    - `SiteName` `19 06 15`
  - A search using site shorthand with date + scene ID:
    - `SN` `19 06 15` `Scene ID`
  - A **Level 2/3** search using site name and just an ID:
    - `SiteName` `Scene ID`
    
+ **Level 3** examples:
  - An exact search using site name and ID:
    - `SiteName` `Scene ID`
  - An exact search using site shorthand and ID:
    - `SN` `Scene ID`

# Search Levels and their capabilities
There are 3 available levels, as listed below:
+ **Level 1:** `SceneID Match`, `Date Match` and `Date Add`
+ **Level 2:** `SceneID Search` and `Date Search`
+ **Level 3:** `SceneID Only`

## Level 1
#### Multi-search available. This includes, searching by actor, by scene name, or by date (or all of the above).
+ **SceneID Match:** SceneID can be entered as a search term alongside other search terms (Title, Actor) to increase the possibility for a match, but cannot be entered as a standalone search term.
  - Example: Though Kink has a full-fledged title/actor search function, you cannot enter just a SceneID and find results. However, if a SceneID is entered alongside a title/actor, it will increase the possibility of locating the correct scene
+ **Date Match:** Date can be entered alongside other search terms to improve search results
+ **Date Add:** If Date is entered as a search term and the site doesn't provide a publish date, the agent will strip the search date and attach it to the scene

## Level 2
#### Limited-search available. This is broken down into 2 sub-levels, which commonly cannot be used together:
+ **SceneID Search:** Scene ID can be entered as the *ONLY* search term and the agent will locate results
  - Example: Though EvilAngel has a full-fledged title/actor search function, you can also just search by Scene ID and find results
+ **Date Search:** Date can be entered as the only search term and results will be found (not sure if this is implemented anywhere)

## Level 3
#### Exact matching only.
+ **SceneID Only:** Search relies solely on SceneID. You may add additional terms to your search (Title, Actor, Date), but if a SceneID is not entered you will not receive any results
  - Example: Babes/PropertySex/etc. The agent strips the SceneID from your search term and plugs it into a URL. I've implemented some code so that adding a title to your search term increases the "score" you see, without a SceneID your search will return no results
