import PAsearchSites
import PAgenres
from dateutil.parser import parse

# This function will pull Search Results from the appropriate site
def search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate,searchSiteID):
    if searchSiteID != 9999:
        siteNum = searchSiteID
    searchResults = HTML.ElementFromURL(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    for searchResult in searchResults.xpath('//article[@class="release-card scene"]'): # some xpath that represents the top HTML element of each new result match scene
        titleNoFormatting = searchResult.xpath('./div[@class="card-title/a"]')[0].text_content().strip() # starting the xpath with ./ means it will search from within the current block of scene code
        curID = searchResult.xpath('./div[@class="card-title/a"]')[0].get('href').replace('/','_').replace('?','!') # find the URL, then replace all / with _ and all ? with !. We'll put the URL back together in the update function below
        subSite = searchResult.xpath('./div[@class="site-domain"]')[0].text_content().strip()
        releaseDate = parse(searchResult.xpath('./div[@class="release-date"]')[0].text_content().strip()).strftime('%Y-%m-%d') # this finds the release date, turns it into a date_time object, then converts it back out as a string in standardized format
        score = 100 - Util.LevenshteinDistance(title.lower(), titleNoFormatting.lower()) # compare the title actually searched in Plex vs the title we found in this result and give score out of 100

        results.Append(MetadataSearchResult(id = curID + "|" + str(siteNum), name = titleNoFormatting + " [SexyHub/"+subSite+"] " + releaseDate, score = score, lang = lang)) # add this as a possible match

    return results # return all our matches


# This function will pull the metadata for a specific result once it has been matched in a search
def update(metadata,siteID,movieGenres,movieActors):





    return metadata
