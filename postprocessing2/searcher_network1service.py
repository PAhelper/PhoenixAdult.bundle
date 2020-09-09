## Dependencies
import time
import requests
import json
import logging
import enchant
## Other .py files
import LoggerFunction

## Get cookies function
def get_Cookies(url):
    time.sleep(2)
    req = requests.get(url)

    return req.cookies

def search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,WorkingDir):
    ## Basic Log Configuration
    logger = LoggerFunction.setup_logger('Searches', WorkingDir+'\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', WorkingDir+'\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    ResultsMatrix = [['0','0','0','0','0',0]]
    cookies = get_Cookies(siteBaseURL)
    searchTitle = searchTitle.split("_")[0]
    splited = searchTitle.split(' ')[0]
    sceneID = None
    if (splited.isdigit()):
        sceneID = splited
        searchTitle = searchTitle.replace(splited, '', 1).strip()
        URL = siteSearchURL+'/v2/releases?type=scene&id='+sceneID
    else:
        URL = siteSearchURL+'/v2/releases?type=scene&search='+searchTitle
    ## Scene matching section
    logger.info ("******************** URL used section **********************")
    logger.info (URL)
    page = requests.get(URL,headers={'Instance': cookies['instance_token']})
    searchResults = page.json()['result']
    ## The below line logger.debugs the json. You can comment it out to see the retrieved information and for debugging
    ##logger.debug (searchResults)
    ScenesQuantity = len(searchResults)
    logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
    for searchResult in searchResults:
        curActorstring = ''
        curDate = ''
        curID = str(searchResult['id'])
        curTitle = searchResult['title']
        curDate = searchResult['dateReleased'].split("T")[0]
        actorssize = len(searchResult['actors'])
        for i in range(actorssize):
            actor = searchResult['actors'][i]['name']
            curActorstring += actor+' & '
        curActorstring = curActorstring[:-3]
        curSubsite = ''
        if 'collections' in searchResult and searchResult['collections']:
            curSubsite = searchResult['collections'][0]['name']
        if (sceneID != None):
            curScore = 100 - enchant.utils.levenshtein(sceneID, curID)
        elif ((searchDate != None) and (curDate != '')):
            curScore = 100 - enchant.utils.levenshtein(searchDate, curDate)
        else:
            curScore = 100 - enchant.utils.levenshtein(searchTitle.lower(), curTitle.lower())
        SceneNameLogger.debug ("************** Current Scene Matching section **************")
        SceneNameLogger.debug ("ID: " +curID)
        SceneNameLogger.debug ("Title: " +curTitle)
        SceneNameLogger.debug ("Date: " +curDate)
        SceneNameLogger.debug ("Actors: " +curActorstring)
        SceneNameLogger.debug ("Subsite: " +curSubsite)
        SceneNameLogger.debug ("Score: " +str(curScore))
        ResultsMatrix.append([curID, curTitle, curDate, curActorstring, curSubsite, curScore])
    ResultsMatrix.sort(key=lambda x:x[5],reverse=True)
    logger.info ("*************** Moving to Renamer Function *****************")
    SceneNameLogger.handlers.pop()
    logger.handlers.pop()
    return ResultsMatrix
