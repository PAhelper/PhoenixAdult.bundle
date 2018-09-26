import re
import random
import urllib
import urllib2 as urllib
import urlparse
import json
from datetime import datetime
from PIL import Image
from cStringIO import StringIO
from SSLEXTRA import sslOptions
import PAgenres
import PAsearchSites

VERSION_NO = '2.2018.09.22.1'

def any(s):
    for v in s:
        if v:
            return True
    return False

def Start():
    HTTP.ClearCache()
    HTTP.CacheTime = CACHE_1MINUTE*20
    HTTP.Headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    HTTP.Headers['Accept-Encoding'] = 'gzip'

def capitalize(line):
    return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])


class PhoenixAdultAgent(Agent.Movies):
    name = 'PhoenixAdult'
    languages = [Locale.Language.English]
    accepts_from = ['com.plexapp.agents.localmedia']
    primary_provider = True

    def search(self, results, media, lang):
        title = media.name
        if media.primary_metadata is not None:
            title = media.primary_metadata.title
        title = title.replace('"','').replace("'","").replace(":","").replace("!","").replace("(","").replace(")","").replace("&","")
        Log('*******MEDIA TITLE****** ' + str(title))

        # Search for year
        year = media.year
        if media.primary_metadata is not None:
            year = media.primary_metadata.year

        Log("Getting Search Settings for: " + title)
        searchDate = None
        searchSiteID = None
        searchSettings = PAsearchSites.getSearchSettings(title)
        if searchSettings[0] == 9999:
            searchAll = True
        else:
            searchAll = False
            searchSiteID = searchSettings[0]
            if searchSiteID == 3:
                searchSiteID = 0
            if searchSiteID == 4:
                searchSiteID = 1
        searchTitle = searchSettings[2]
        Log("Site ID: " + str(searchSettings[0]))
        Log("Search Title: " + searchSettings[2])
        if searchSettings[1]:
            searchByDateActor = True
            searchDate = searchSettings[3]
            Log("Search Date: " + searchSettings[3])
        else:
            searchByDateActor = False

        encodedTitle = urllib.quote(searchTitle)
        Log(encodedTitle)
        siteNum = 0
        for searchSite in PAsearchSites.searchSites:
            ###############
            ## Blacked and Blacked Raw Search
            ###############
            if siteNum == 0 or siteNum == 1:
                if searchAll or searchSiteID == 0 or searchSiteID == 1:
                    results = PAsearchSites.siteBlacked.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Brazzers
            ###############
            if siteNum == 2:
                if searchAll or searchSiteID == 2 or (searchSiteID >= 54 and searchSiteID <= 81):
                    results = PAsearchSites.siteBrazzers.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)
            ###############
            ## Naughty America
            ###############
            if siteNum == 5:
                if searchAll or (searchSiteID >= 5 and searchSiteID <= 51): 
                    results = PAsearchSites.siteNaughtyAmerica.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Vixen
            ###############
            if siteNum == 52:
                if searchAll or searchSiteID == 52:
                    results = PAsearchSites.siteVixen.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)
                
            ###############
            ## Girlsway
            ###############
            if siteNum == 53:
                if searchAll or searchSiteID == 53:
                    results = PAsearchSites.siteGirlsway.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

                
            ###############
            ## X-Art
            ###############
            if siteNum == 82:
                if searchAll or searchSiteID == 82:
                    results = PAsearchSites.siteXart.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)
            
            ###############
            ## Bang Bros
            ###############
            if siteNum == 83:
                if searchAll or (searchSiteID >= 83 and searchSiteID <= 135):
                    results = PAsearchSites.siteBangBros.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)
                    
            ###############
            ## Tushy
            ###############
            if siteNum == 136:
                if searchAll or searchSiteID == 136:
                    results = PAsearchSites.siteTushy.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)


            ###############
            ## Reality Kings
            ###############
            if siteNum == 137:
                if searchAll or (searchSiteID >= 137 and searchSiteID <= 182):
                    results = PAsearchSites.siteRealityKings.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)
                            
            
            ###############
            ## 21Naturals
            ###############
            if siteNum == 183:
                if searchAll or searchSiteID == 183:
                    results = PAsearchSites.site21Naturals.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)
                            

            ###############
            ## PornFidelity
            ###############
            if siteNum == 184:
                
                if searchAll or searchSiteID == 184:
                    results = PAsearchSites.sitePornFidelity.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)
            
            ###############
            ## TeenFidelity
            ###############
            if siteNum == 185:
                
                if searchAll or searchSiteID == 185:
                    results = PAsearchSites.siteTeenFidelity.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Kelly Madison
            ###############
            if siteNum == 186:
                if searchAll or searchSiteID == 186:
                    results = PAsearchSites.siteKellyMadison.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

        
            ###############
            ## Team Skeet
            ###############
            if siteNum == 187:
                if searchAll or (searchSiteID >= 187 and searchSiteID <= 215):
                    results = PAsearchSites.siteTeamSkeet.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Porndoe Premium
            ###############
            if siteNum == 216:
                if searchAll or (searchSiteID >= 216 and searchSiteID <= 259):
                    results = PAsearchSites.sitePorndoePremium.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Legal Porno
            ###############
            if siteNum == 260:
                if searchAll or searchSiteID == 260:
                    results = PAsearchSites.siteLegalPorno.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            siteNum += 1 
        
        results.Sort('score', descending=True)

    def update(self, metadata, media, lang):
        movieGenres = PAgenres.PhoenixGenres()
        
        HTTP.ClearCache()

        Log('******UPDATE CALLED*******')
        
        siteID = int(str(metadata.id).split("|")[1])
        Log(str(siteID))
        ##############################################################
        ##                                                          ##
        ##   Blacked                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 1:
            metadata = PAsearchSites.siteBlacked.update(metadata,siteID,movieGenres)
            
        ##############################################################
        ##                                                          ##
        ##   Blacked Raw                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 0:
            metadata = PAsearchSites.siteBlacked.updateRaw(metadata,siteID,movieGenres)
        
        ##############################################################
        ##                                                          ##
        ##   Brazzers                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 2 or (siteID >= 54 and siteID <= 81):
            metadata = PAsearchSites.siteBrazzers.update(metadata,siteID,movieGenres)
                
        ##############################################################
        ##                                                          ##
        ##   Naughty America                                        ##
        ##                                                          ##
        ##############################################################        
        if siteID >= 5 and siteID <= 51:
            metadata = PAsearchSites.siteNaughtyAmerica.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   Vixen                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 52:
            metadata = PAsearchSites.siteVixen.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   Girlsway                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 53:
            metadata = PAsearchSites.siteGirlsway.update(metadata,siteID,movieGenres)


        ##############################################################
        ##                                                          ##
        ##   X-Art                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 82:
            metadata = PAsearchSites.siteXart.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   Bang Bros                                              ##
        ##                                                          ##
        ##############################################################
        if siteID >= 83 and siteID <= 135:
            metadata = PAsearchSites.siteBangBros.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   Tushy                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 136:
            metadata = PAsearchSites.siteTushy.update(metadata,siteID,movieGenres)


        ##############################################################
        ##                                                          ##
        ##   Reality Kings                                          ##
        ##                                                          ##
        ##############################################################
        if siteID >= 137 and siteID <= 182:
            metadata = PAsearchSites.siteRealityKings.update(metadata,siteID,movieGenres)


        ##############################################################
        ##                                                          ##
        ##   21Naturals                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 183:
            metadata = PAsearchSites.site21Naturals.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   PornFidelity                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 184:
            metadata = PAsearchSites.sitePornFidelity.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   TeenFidelity                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 185:
            metadata = PAsearchSites.siteTeenFidelity.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   Kelly Madison                                          ##
        ##                                                          ##
        ##############################################################
        if siteID == 186:
            metadata = PAsearchSites.siteKellyMadison.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   TeamSkeet                                              ##
        ##                                                          ##
        ##############################################################
        if siteID >= 187 and siteID <= 215:
            metadata = PAsearchSites.siteTeamSkeet.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   Porndoe Premium                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 216 and siteID <= 259:
            metadata = PAsearchSites.sitePorndoePremium.update(metadata,siteID,movieGenres)

        ##############################################################
        ##                                                          ##
        ##   LegalPorno                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 260:
            metadata = PAsearchSites.siteLegalPorno.update(metadata,siteID,movieGenres)





















        ##############################################################
        ## Cleanup Genres and Add
        metadata.genres.clear()
        Log("Genres")
        movieGenres.processGenres(metadata)
       