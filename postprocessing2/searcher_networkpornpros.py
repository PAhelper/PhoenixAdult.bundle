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
import GoogleSearchFunction

def search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,WorkingDir):
    ## Basic Log Configuration
    logger = LoggerFunction.setup_logger('Searcher', WorkingDir+'\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', WorkingDir+'\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    ResultsMatrix = [['0','0','0','0','0',0]]
    DirectURL = (siteSearchURL + searchTitle.replace(" ","-"))
    ScenesURL = [DirectURL]
    googleResults = GoogleSearchFunction.getFromGoogleSearch(searchTitle, siteBaseURL, WorkingDir)
    for searchURL in googleResults:
        if ('/video/' in searchURL and searchURL not in ScenesURL):
            ScenesURL.append(searchURL)
    logger.info("Possible matching scenes found in results: " +str(len(ScenesURL)))
    for SceneURL in ScenesURL:
        try:
            logger.info ("******************** URL used section **********************")
            logger.info (SceneURL)
            req = requests.get(SceneURL)
            HTMLResponse = html.fromstring(req.content)
            curID = ''
            curDate = ''
            curActorstring = ''
            curSubsite = ''
            curTitle = HTMLResponse.xpath('//h1[@class="t2019-stitle py-1 py-sm-2 pt-lg-0 mb-0 border-bottom"]')[0].text_content().strip()
            try:
                curDate = datetime.datetime.strptime(str(HTMLResponse.xpath('//div[@class="d-inline d-lg-block mb-1"]/span')[0].text_content().strip()),'%B %d, %Y').strftime('%Y-%m-%d')
            except:
                pass
            actorssize = len(HTMLResponse.xpath('//div[contains(@class, "pt-md")]//a[contains(@href, "/girls/")]'))
            for i in range(actorssize):
                actor = HTMLResponse.xpath('//div[contains(@class, "pt-md")]//a[contains(@href, "/girls/")]')[i].text_content().strip()
                curActorstring += actor+' & '
            curActorstring = curActorstring[:-3]
            if ((searchDate != None) and (curDate != '')):
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
        except:
            pass
    ResultsMatrix.sort(key=lambda x:x[5],reverse=True)
    logger.info ("*************** Moving to Renamer Function *****************")
    SceneNameLogger.handlers.pop()
    logger.handlers.pop()
    return ResultsMatrix