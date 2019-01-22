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
from dateutil.parser import parse
import PAactors
import PAgenres
import PAsearchSites

VERSION_NO = '2.2018.12.08.1'

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
        title = title.replace('"','').replace(":","").replace("!","").replace("[","").replace("]","").replace("(","").replace(")","").replace("&","").replace('RARBG','').replace('1080p','').replace('720p','')
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
        Log("Site ID: " + str(searchSiteID))
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
            ## Blacked Raw
            ###############
            if siteNum == 0:
                if searchAll or searchSiteID == 0:
                    results = PAsearchSites.siteBlacked.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Blacked
            ###############
            if siteNum == 1:
                if searchAll or searchSiteID == 1:
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
                if searchAll or (searchSiteID >= 5 and searchSiteID <= 51) or searchSiteID == 341 or (searchSiteID >= 393 and searchSiteID <= 396):
                    results = PAsearchSites.siteNaughtyAmerica.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Vixen
            ###############
            if siteNum == 52:
                if searchAll or searchSiteID == 52:
                    results = PAsearchSites.siteVixen.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## GammaEnt
            ###############
            if siteNum == 53 or siteNum == 183 or siteNum == 277 or siteNum == 278 or siteNum == 281 or (siteNum >=285 and siteNum <= 287) or siteNum == 329 or siteNum == 330 or (siteNum >= 351 and siteNum <= 355) or siteNum == 365 or (siteNum >= 380 and siteNum <= 392) or siteNum == 460:
                if searchAll or searchSiteID == 53 or searchSiteID == 183 or (searchSiteID >= 277 and searchSiteID <= 278) or searchSiteID == 281 or (searchSiteID >= 285 and searchSiteID <= 287) or (searchSiteID >= 329 and searchSiteID <= 332) or (searchSiteID >= 351 and searchSiteID <= 383) or (searchSiteID >= 460 and searchSiteID <= 466):
                    results = PAsearchSites.networkGammaEnt.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

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
            ## PornFidelity
            ###############
            if siteNum == 184:
                if searchAll or searchSiteID == 184:
                    results = PAsearchSites.networkPornFidelity.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## TeenFidelity
            ###############
            if siteNum == 185:
                if searchAll or searchSiteID == 185:
                    results = PAsearchSites.networkPornFidelity.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Kelly Madison
            ###############
            if siteNum == 186:
                if searchAll or searchSiteID == 186:
                    results = PAsearchSites.networkPornFidelity.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

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

            ###############
            ## Mofos
            ###############
            if siteNum == 261:
                if searchAll or (searchSiteID >= 261 and searchSiteID <= 270):
                    results = PAsearchSites.siteMofos.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Babes
            ###############
            if siteNum == 271:
                if searchAll or (searchSiteID >= 271 and searchSiteID <= 276):
                    results = PAsearchSites.siteBabes.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## GloryHoleSecrets
            ###############
            if siteNum == 279:
                if searchAll or searchSiteID == 279:
                    results = PAsearchSites.siteGloryHoleSecrets.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## NewSensations
            ###############
            if siteNum == 280:
                if searchAll or searchSiteID == 280:
                    results = PAsearchSites.siteNewSensations.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Swallowed
            ###############
            if siteNum == 282:
                if searchAll or searchSiteID == 282:
                    results = PAsearchSites.networkSteppedUp.searchSwallowed(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## TrueAnal
            ###############
            if siteNum == 283:
                if searchAll or searchSiteID == 283:
                    results = PAsearchSites.networkSteppedUp.searchTrueAnal(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Nympho
            ###############
            if siteNum == 284:
                if searchAll or searchSiteID == 284:
                    results = PAsearchSites.networkSteppedUp.searchNympho(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Twistys
            ###############
            if siteNum == 288:
                if searchAll or (searchSiteID >= 288 and searchSiteID <= 291):
                    results = PAsearchSites.siteTwistys.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Lubed
            ###############
            if siteNum == 292:
                if searchAll or searchSiteID == 292:
                    results = PAsearchSites.siteLubed.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Spizoo
            ###############
            if siteNum == 293:
                if searchAll or searchSiteID == 293:
                    results = PAsearchSites.siteSpizoo.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Private
            ###############
            if siteNum == 294:
                if searchAll or (searchSiteID >= 294 and searchSiteID <= 305):
                    results = PAsearchSites.sitePrivate.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Passion-HD
            ###############
            if siteNum == 306:
                if searchAll or searchSiteID == 306:
                    results = PAsearchSites.sitePassionHD.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Fantasy-HD
            ###############
            if siteNum == 307:
                if searchAll or searchSiteID == 307:
                    results = PAsearchSites.siteFantasyHD.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## PornPros
            ###############
            if siteNum == 308:
                if searchAll or (searchSiteID >= 308 and searchSiteID <= 327):
                    results = PAsearchSites.sitePornPros.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## DigitalPlayground
            ###############
            if siteNum == 328:
                if searchAll or searchSiteID == 328:
                    results = PAsearchSites.siteDigitalPlayground.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## SexyHub
            ###############
            if siteNum == 333 or siteNum == 335 or siteNum == 406 or siteNum == 407:
                if searchAll or (searchSiteID >= 333 and searchSiteID <= 339) or (searchSiteID >= 406 and searchSiteID <= 407):
                    results = PAsearchSites.networkSexyHub.searchSexy(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## GloryHoleSwallow
            ###############
            if siteNum == 342:
                if searchAll or searchSiteID == 342:
                    results = PAsearchSites.siteGloryHoleSwallow.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## FullPornNetwork
            ###############
            if siteNum >= 343 and siteNum <=350:
                if searchAll or (searchSiteID >= 343 and searchSiteID <= 350):
                    results = PAsearchSites.networkFPN.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## DogfartNetwork
            ###############
            if siteNum == 408:
                if searchAll or (searchSiteID >= 408 and searchSiteID <= 431):
                    results = PAsearchSites.networkDogfart.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## FakeHub
            ###############
            if siteNum == 340 or siteNum == 405:
                if searchAll or (searchSiteID >= 397 and searchSiteID <= 405):
                    results = PAsearchSites.networkSexyHub.searchFake(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## JulesJordan
            ###############
            if siteNum == 432:
                if searchAll or searchSiteID == 432:
                    results = PAsearchSites.siteJulesJordan.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## DDFNetwork
            ###############
            if siteNum == 433:
                if searchAll or (searchSiteID >= 433 and searchSiteID <= 447):
                    results = PAsearchSites.networkDDFNetwork.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## PerfectGonzo
            ###############
            if siteNum == 448:
                if searchAll or (searchSiteID >= 448 and searchSiteID <= 459):
                    results = PAsearchSites.networkPerfectGonzo.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            siteNum += 1

        results.Sort('score', descending=True)

    def update(self, metadata, media, lang):
        movieGenres = PAgenres.PhoenixGenres()
        movieActors = PAactors.PhoenixActors()

        HTTP.ClearCache()
        metadata.genres.clear()
        metadata.roles.clear()

        Log('******UPDATE CALLED*******')

        siteID = int(str(metadata.id).split("|")[1])
        Log(str(siteID))
        ##############################################################
        ##                                                          ##
        ##   Blacked                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 1:
            metadata = PAsearchSites.siteBlacked.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Blacked Raw                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 0:
            metadata = PAsearchSites.siteBlacked.updateRaw(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Brazzers                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 2 or (siteID >= 54 and siteID <= 81):
            metadata = PAsearchSites.siteBrazzers.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   SexyHub/FakeHub                                        ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 333 and siteID <= 338) or (siteID >= 397 and siteID <= 407):
            metadata = PAsearchSites.networkSexyHub.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Naughty America                                        ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 5 and siteID <= 51) or siteID == 341 or (siteID >= 393 and siteID <= 396):
            metadata = PAsearchSites.siteNaughtyAmerica.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Vixen                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 52:
            metadata = PAsearchSites.siteVixen.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   X-Art                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 82:
            metadata = PAsearchSites.siteXart.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Bang Bros                                              ##
        ##                                                          ##
        ##############################################################
        if siteID >= 83 and siteID <= 135:
            metadata = PAsearchSites.siteBangBros.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Tushy                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 136:
            metadata = PAsearchSites.siteTushy.update(metadata,siteID,movieGenres,movieActors)


        ##############################################################
        ##                                                          ##
        ##   Reality Kings                                          ##
        ##                                                          ##
        ##############################################################
        if siteID >= 137 and siteID <= 182:
            metadata = PAsearchSites.siteRealityKings.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   PornFidelity                                           ##
        ##                                                          ##
        ##############################################################
        if siteID >= 184 and siteID <= 186:
            metadata = PAsearchSites.networkPornFidelity.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   TeamSkeet                                              ##
        ##                                                          ##
        ##############################################################
        if siteID >= 187 and siteID <= 215:
            metadata = PAsearchSites.siteTeamSkeet.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Porndoe Premium                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 216 and siteID <= 259:
            metadata = PAsearchSites.sitePorndoePremium.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   LegalPorno                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 260:
            metadata = PAsearchSites.siteLegalPorno.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Mofos                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID >= 261 and siteID <= 270:
            metadata = PAsearchSites.siteMofos.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Babes                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID >= 271 and siteID <= 276:
            metadata = PAsearchSites.siteBabes.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   GloryHoleSecrets                                       ##
        ##                                                          ##
        ##############################################################
        if siteID == 279:
            metadata = PAsearchSites.siteGloryHoleSecrets.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   NewSensations                                          ##
        ##                                                          ##
        ##############################################################
        if siteID == 280:
            metadata = PAsearchSites.siteNewSensations.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Stepped Up Media                                       ##
        ##                                                          ##
        ##############################################################
        if siteID >= 282 and siteID <= 284:
            metadata = PAsearchSites.networkSteppedUp.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Twistys		                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 288 and siteID <= 291:
            metadata = PAsearchSites.siteTwistys.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Lubed                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 292:
            metadata = PAsearchSites.siteLubed.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Spizoo                                                 ##
        ##                                                          ##
        ##############################################################
        if siteID == 293:
            metadata = PAsearchSites.siteSpizoo.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Private		                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 294 and siteID <= 305:
            metadata = PAsearchSites.sitePrivate.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Passion-HD                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 306:
            metadata = PAsearchSites.sitePassionHD.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Fantasy-HD                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 307:
            metadata = PAsearchSites.siteFantasyHD.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   PornPros                                               ##
        ##                                                          ##
        ##############################################################
        if siteID >= 308 and siteID <= 327:
            metadata = PAsearchSites.sitePornPros.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   DigitalPlayground                                      ##
        ##                                                          ##
        ##############################################################
        if siteID == 328:
            metadata = PAsearchSites.siteDigitalPlayground.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   GloryHoleSwallow                                       ##
        ##                                                          ##
        ##############################################################
        if siteID == 342:
            metadata = PAsearchSites.siteGloryHoleSwallow.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   FullPornNetwork                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 343 and siteID <= 350:
            metadata = PAsearchSites.networkFPN.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Gamma Entertainment                                    ##
        ##                                                          ##
        ##############################################################
        if siteID == 53 or siteID == 183 or (siteID >= 277 and siteID <= 278) or siteID == 281 or (siteID >= 285 and siteID <= 287) or (siteID >= 329 and siteID <= 332) or (siteID >= 351 and siteID <= 383) or (siteID >= 460 and siteID <= 466):
            metadata = PAsearchSites.networkGammaEnt.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Dogfart Network                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 408 and siteID <= 431:
            metadata = PAsearchSites.networkDogfart.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Jules Jordan                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 432:
            metadata = PAsearchSites.siteJulesJordan.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   DDF Network                                            ##
        ##                                                          ##
        ##############################################################
        if siteID >= 433 and siteID <= 447:
            metadata = PAsearchSites.networkDDFNetwork.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Perfect Gonzo                                          ##
        ##                                                          ##
        ##############################################################
        if siteID >= 448 and siteID <= 459:
            metadata = PAsearchSites.networkPerfectGonzo.update(metadata,siteID,movieGenres,movieActors)


        ##############################################################
        ## Cleanup Genres and Add
        Log("Genres")
        movieGenres.processGenres(metadata)

        ##############################################################
        ## Cleanup Actors and Add
        Log("Actors")
        movieActors.processActors(metadata)

        ##############################################################
        ## Add Content Rating
        metadata.content_rating = 'XXX'
