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
        URL = (siteBaseURL +'/'+ sceneID)
        logger.info ("******************** URL used section **********************")
        logger.info (URL)
        req = requests.get(URL, cookies={'sst': 'ulang-en'})
        HTMLResponse = html.fromstring(req.content)
        searchResults = HTMLResponse.xpath('//div[@class="detail__header detail__header-lg"]/h1[@class="detail__title"]')
        ScenesQuantity = len(searchResults)
        logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
        curSubsite = ''
        curActorstring = ''
        curDate = ''
        curID = URL.split("/")[-1]
        curTitle = HTMLResponse.xpath('//div[@class="detail__header detail__header-lg"]/h1[@class="detail__title"]')[0].text_content().strip().replace(":"," ")
        curDate = datetime.datetime.strptime(str(HTMLResponse.xpath('//span[@class="detail__date"]')[0].text_content().strip()),'%d %B, %Y').strftime('%Y-%m-%d')
        actorssize = len(HTMLResponse.xpath('//div[@class="detail__inf detail__inf-align_right"]/div[@class="detail__models"]/a'))
        for i in range(actorssize):
            actor = HTMLResponse.xpath('//div[@class="detail__inf detail__inf-align_right"]/div[@class="detail__models"]/a')[i].text_content().strip()
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
        req = requests.get(URL, cookies={'sst': 'ulang-en'})
        HTMLResponse = html.fromstring(req.content)
        searchResults = HTMLResponse.xpath('//ul[@class="cards-list"]//li')
        ScenesQuantity = len(searchResults)
        logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
        for searchResult in searchResults:
            curSubsite = ''
            curActorstring = ''
            curDate = ''
            curID = searchResult.xpath('.//div[contains(@class, "card__body")]/a/@href')[0].split("-")[-1]
            curTitle = searchResult.xpath('.//div[@class="card__footer"]//div[@class="card__h"]/text()')[0].replace(":"," ")
            curDate = datetime.datetime.strptime(str(searchResult.xpath('.//div[@class="card__date"]')[0].text_content().strip()),'%d %B, %Y').strftime('%Y-%m-%d')
            actorssize = len(searchResult.xpath('.//div[@class="card__links"]/a'))
            for i in range(actorssize):
                actor = searchResult.xpath('.//div[@class="card__links"]/a')[i].text_content().strip()
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