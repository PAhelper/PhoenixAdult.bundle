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
        URL = (siteBaseURL +'/vrpornvideo/'+ sceneID)
        logger.info ("******************** URL used section **********************")
        logger.info (URL)
        req = requests.get(URL)
        HTMLResponse = html.fromstring(req.content)
        searchResults = HTMLResponse.xpath('//h1[contains(@class, "video-title")]')
        ScenesQuantity = len(searchResults)
        logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
        curSubsite = ''
        curActorstring = ''
        curDate = ''
        curID = URL.split("/")[-1]
        curTitle = HTMLResponse.xpath('//h1[contains(@class, "video-title")]')[0].text_content().strip().replace(":"," ")
        curDate = datetime.datetime.strptime(str(HTMLResponse.xpath('//p[@itemprop="uploadDate"]')[0].text_content().strip().split("Uploaded: ")[1]),'%B %d, %Y').strftime('%Y-%m-%d')
        actorssize = len(HTMLResponse.xpath('//p[@class="video-actors"]/a'))
        for i in range(actorssize):
            actor = HTMLResponse.xpath('//p[@class="video-actors"]/a')[i].text_content().strip()
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
        req = requests.get(URL)
        HTMLResponse = html.fromstring(req.content)
        searchResults = HTMLResponse.xpath('//div[@class="tile-grid-item"]')
        ScenesQuantity = len(searchResults)
        logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
        for searchResult in searchResults:
            SceneURL = searchResult.xpath('./div/a/@href')[0]
            if not SceneURL.startswith('http'):
                SceneURL = (siteBaseURL + SceneURL)
                req = requests.get(SceneURL)
                HTMLResponse = html.fromstring(req.content)
            else:
                req = requests.get(SceneURL)
                HTMLResponse = html.fromstring(req.content)
            # logger.info ("******************** Scene URL section *********************")
            # logger.info (SceneURL)              
            curSubsite = ''
            curActorstring = ''
            curDate = ''
            curID = SceneURL.split("-")[-1].split("/")[0]
            curTitle = HTMLResponse.xpath('//h1[contains(@class, "video-title")]')[0].text_content().strip().replace(":"," ")
            curDate = datetime.datetime.strptime(str(HTMLResponse.xpath('//p[@itemprop="uploadDate"]')[0].text_content().strip().split("Uploaded: ")[1]),'%B %d, %Y').strftime('%Y-%m-%d')
            actorssize = len(HTMLResponse.xpath('//p[@class="video-actors"]/a'))
            for i in range(actorssize):
                actor = HTMLResponse.xpath('//p[@class="video-actors"]/a')[i].text_content().strip()
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