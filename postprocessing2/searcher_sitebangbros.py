## Dependencies
import time
import requests
import json
import logging
import enchant
from lxml import html
import datetime
## Other .py files
import LoggerFunction

def search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,WorkingDir):
    ## Basic Log Configuration
    logger = LoggerFunction.setup_logger('Searcher', WorkingDir+'\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', WorkingDir+'\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    ResultsMatrix = [['0','0','0','0','0',0]]
    splited = searchTitle.split(' ')[0]
    if (splited.isdigit()):
        sceneID = splited
    else:
        sceneID = None
    if (sceneID != None):
        URL = (siteSearchURL + sceneID + "/1")
    else:
        URL = (siteSearchURL + searchTitle.replace(" ","-") + "/1")
    logger.info ("******************** URL used section **********************")
    logger.info (URL)
    req = requests.get(URL)
    HTMLResponse = html.fromstring(req.content)
    searchResults = HTMLResponse.xpath('//div[@class="thumbsHolder elipsTxt"]/div[1]/div[@class="echThumb"]')
    ScenesQuantity = len(searchResults)
    logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
    for searchResult in searchResults:
        if searchResult.xpath('.//a[contains(@href, "/video")]'):
            curID = ''
            curDate = ''
            curSubsite = ''
            curActorstring = ''
            curID = searchResult.xpath('.//a[contains(@href, "/video")]//@href')[0].replace("/video","").split("/")[0]
            curTitle = searchResult.xpath('.//a[contains(@href, "/video")]/@title')[0].replace(":"," ")
            curDate = datetime.datetime.strptime(str(searchResult.xpath('.//span[@class="faTxt"]')[1].text_content().strip()),'%b %d, %Y').strftime('%Y-%m-%d')
            curSubsite = searchResult.xpath('.//span[@class="faTxt"]')[0].text_content().strip()
            actorssize = len(searchResult.xpath('.//div[contains(@class, "cast-wrapper")]/a'))
            for i in range(actorssize):
                actor = searchResult.xpath('.//div[contains(@class, "cast-wrapper")]/a')[i].text_content().strip()
                curActorstring += actor+' & '
            curActorstring = curActorstring[:-3]
            if (sceneID != None):
                curScore = 100 - enchant.utils.levenshtein(sceneID, curID)
            elif (searchDate != None):
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