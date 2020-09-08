## Dependencies
import time
import requests
import json
import logging
import enchant
from datetime import datetime
## Other .py files
import LoggerFunction

def search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,WorkingDir):
    ## Basic Log Configuration
    logger = LoggerFunction.setup_logger('Searches', WorkingDir+'\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', WorkingDir+'\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    SearchURLFixed = siteSearchURL.replace('/queries','') + '?x-algolia-application-id=I6P9Q9R18E&x-algolia-api-key=08396b1791d619478a55687b4deb48b4'
    ResultsMatrix = [['0','0','0','0','0',0]]
    searchTitle = searchTitle.split("_")[0]
    splited = searchTitle.split(' ')[0]
    sceneID = None
    if (splited.isdigit()):
        sceneID = splited
        searchTitle = searchTitle.replace(splited, '', 1).strip()
        URL = (SearchURLFixed.replace('*','nacms_scenes_production')+'&filters=id='+sceneID+'&hitsPerPage=100')
    else:
        URL = (SearchURLFixed.replace('*','nacms_scenes_production')+'&query='+searchTitle+'&hitsPerPage=100')
    ## Scene matching section
    logger.info ("******************** URL used section **********************")
    logger.info (URL)
    page = requests.get(URL)
    searchResults = page.json()['hits']
    ## The below line logger.debugs the json. You can comment it out to see the retrieved information and for debugging
    ## print (searchResults)
    ScenesQuantity = len(searchResults)
    logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
    for searchResult in searchResults:
        curActorstring = ''
        curDate = ''
        curID = str(searchResult['id'])
        curTitle = searchResult['title']
        curDate = datetime.fromtimestamp(searchResult['published_at']).strftime('%Y-%m-%d')
        actorssize = len(searchResult['performers'])
        for i in range(actorssize):
            actor = searchResult['performers'][i]
            curActorstring += actor+' & '
        curActorstring = curActorstring[:-3]
        curSubsite = ''
        curSubsite = searchResult['site']
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
