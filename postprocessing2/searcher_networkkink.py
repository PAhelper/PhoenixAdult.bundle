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
        URL = (siteBaseURL +'/shoot/'+ sceneID)
        logger.info ("******************** URL used section **********************")
        logger.info (URL)
        req = requests.get(URL, headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
        HTMLResponse = html.fromstring(req.content)
        searchResults = HTMLResponse.xpath('//h1[@class="shoot-title"]')
        ScenesQuantity = len(searchResults)
        logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
        curSubsite = ''
        curActorstring = ''
        curDate = ''
        curID = URL.split("/")[-1]
        curTitle = HTMLResponse.xpath('//h1[@class="shoot-title"]')[0].text_content().strip()[:-1].replace(":"," ")
        curDate = datetime.datetime.strptime(str(HTMLResponse.xpath('//span[@class="shoot-date"]')[0].text_content().strip()),'%B %d, %Y').strftime('%Y-%m-%d')
        actorssize = len(HTMLResponse.xpath('//p[@class="starring"]//a'))
        for i in range(actorssize):
            actor = HTMLResponse.xpath('//p[@class="starring"]//a')[i].text_content().strip()
            curActorstring += actor+' & '
        curActorstring = curActorstring[:-3]
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
        SceneNameLogger.debug ("Subsite: Site doesn't provide Subsite information")
        SceneNameLogger.debug ("Score: " +str(curScore))
        ResultsMatrix.append([curID, curTitle, curDate, curActorstring, curSubsite, curScore])
    else:
        URL = (siteSearchURL + searchTitle)
        logger.info ("******************** URL used section **********************")
        logger.info (URL)
        req = requests.get(URL, headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
        HTMLResponse = html.fromstring(req.content)
        searchResults = HTMLResponse.xpath('//div[@class="shoot-card scene"]')
        ScenesQuantity = len(searchResults)
        logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
        for searchResult in searchResults:
            curSubsite = ''
            curActorstring = ''
            curDate = ''
            curID = searchResult.xpath('./div/a')[0].split("/")[-1]
            curTitle = searchResult.xpath('.//img/@alt')[0].strip.replace(":"," ")
            curDate = datetime.datetime.strptime(str(searchResult.xpath('.//div[@class="date"]')[0].text_content().strip()),'%b %d, %Y').strftime('%Y-%m-%d')
            actorssize = len(searchResult.xpath('.//div[@class="shoot-thumb-models"]/a'))
            for i in range(actorssize):
                actor = searchResult.xpath('.//div[@class="shoot-thumb-models"]/a')[i].text_content().strip()
                curActorstring += actor+' & '
            curActorstring = curActorstring[:-3]
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
            SceneNameLogger.debug ("Subsite: Site doesn't provide Subsite information")
            SceneNameLogger.debug ("Score: " +str(curScore))
            ResultsMatrix.append([curID, curTitle, curDate, curActorstring, curSubsite, curScore])
    ResultsMatrix.sort(key=lambda x:x[5],reverse=True)
    logger.info ("*************** Moving to Renamer Function *****************")
    SceneNameLogger.handlers.pop()
    logger.handlers.pop()
    return ResultsMatrix