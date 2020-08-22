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

def search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate):
    ## Basic Log Configuration
    logger = LoggerFunction.setup_logger('Searcher', '.\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', '.\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    ResultsMatrix = [['0','0','0','0','0',0]]
    URL = (siteSearchURL + searchTitle.replace(" ","-"))
    logger.info ("******************** URL used section **********************")
    logger.info (URL)
    req = requests.get(URL)
    HTMLResponse = html.fromstring(req.content)
    searchResults = HTMLResponse.xpath('//h1[@class="t2019-stitle py-1 py-sm-2 pt-lg-0 mb-0 border-bottom"]')
    ScenesQuantity = len(searchResults)
    logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
    for searchResult in searchResults:
        curID = ''
        curDate = ''
        curActorstring = ''
        curSubsite = ''
        curTitle = searchResult.xpath('//h1[@class="t2019-stitle py-1 py-sm-2 pt-lg-0 mb-0 border-bottom"]')[0].text_content().strip()
        curDate = datetime.datetime.strptime(str(searchResult.xpath('//div[@class="d-inline d-lg-block mb-1"]/span')[0].text_content().strip()),'%B %d, %Y').strftime('%Y-%m-%d')
        actorssize = len(searchResult.xpath('//div[contains(@class, "pt-md")]//a[contains(@href, "/girls/")]'))
        for i in range(actorssize):
            actor = searchResult.xpath('//div[contains(@class, "pt-md")]//a[contains(@href, "/girls/")]')[i].text_content().strip()
            curActorstring += actor+' & '
        curActorstring = curActorstring[:-3]
        if (searchDate != None):
            curScore = 100 - enchant.utils.levenshtein(searchDate, curDate)
        else:
            curScore = 100 - enchant.utils.levenshtein(searchTitle.lower(), curTitle.lower())
        SceneNameLogger.debug ("************** Current Scene Matching section **************")
        SceneNameLogger.debug ("ID: Site doesn't provide sceneID information")
        SceneNameLogger.debug ("Title: " +curTitle)
        SceneNameLogger.debug ("Date: " +curDate)
        SceneNameLogger.debug ("Actors: " +curActorstring)
        SceneNameLogger.debug ("Subsite: Site doesn't provide Subsite information")
        SceneNameLogger.debug ("Score: " +str(curScore))
        ResultsMatrix.append([curID, curTitle, curDate, curActorstring, curSubsite, curScore])
    ResultsMatrix.sort(key=lambda x:x[5],reverse=True)
    logger.info ("*************** Moving to Renamer Function *****************")
    SceneNameLogger.handlers.pop()
    logger.handlers.pop()
    return ResultsMatrix