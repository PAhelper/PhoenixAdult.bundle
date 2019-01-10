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
            ## SexyHub
            ###############
            if siteNum == 333:
                if searchAll or searchSiteID == 333 or (searchSiteID >= 333 and searchSiteID <= 339):
                    results = PAsearchSites.networkSexyHub.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Naughty America
            ###############
            if siteNum == 5:
                if searchAll or (searchSiteID >= 5 and searchSiteID <= 51) or searchSiteID == 341:
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
            ## Evil Angel
            ###############
            if siteNum == 277:
                if searchAll or searchSiteID == 277:
                    results = PAsearchSites.siteEvilAngel.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## HardX
            ###############
            if siteNum == 278:
                if searchAll or searchSiteID == 278:
                    results = PAsearchSites.siteHardX.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

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
            ## PureTaboo
            ###############
            if siteNum == 281:
                if searchAll or searchSiteID == 281:
                    results = PAsearchSites.sitePureTaboo.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

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
            ## EroticaX
            ###############
            if siteNum == 285:
                if searchAll or searchSiteID == 285:
                    results = PAsearchSites.siteEroticaX.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## DarkX
            ###############
            if siteNum == 286:
                if searchAll or searchSiteID == 286:
                    results = PAsearchSites.siteDarkX.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## LesbianX
            ###############
            if siteNum == 287:
                if searchAll or searchSiteID == 287:
                    results = PAsearchSites.siteLesbianX.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

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
            ## Throated
            ###############
            if siteNum == 329:
                if searchAll or searchSiteID == 329:
                    results = PAsearchSites.siteThroated.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Sweetheart Video
            ###############
            if siteNum == 330:
                if searchAll or searchSiteID == 330:
                    results = PAsearchSites.siteSweetheartVideo.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## Nuru Massage
            ###############
            if siteNum == 331:
                if searchAll or searchSiteID == 331:
                    results = PAsearchSites.siteNuruMassage.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## SweetSinner
            ###############
            if siteNum == 332:
                if searchAll or searchSiteID == 332:
                    results = PAsearchSites.siteSweetSinner.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## GloryHoleSwallow
            ###############
            if siteNum == 342:
                if searchAll or searchSiteID == 342:
                    results = PAsearchSites.siteGloryHoleSwallow.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

            ###############
            ## FullPornNetwork
            ###############
            if siteNum == 343:
                if searchAll or (searchSiteID >= 343 and searchSiteID <= 350):
                    results = PAsearchSites.networkFPN.search(results,encodedTitle,title,searchTitle,siteNum,lang,searchByDateActor,searchDate, searchAll, searchSiteID)

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
        ##   SexyHub                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 333 or (siteID >= 333 and siteID <= 338):
            metadata = PAsearchSites.networkSexyHub.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Naughty America                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 5 and siteID <= 51 or siteID == 341:
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
        ##   Girlsway                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 53:
            metadata = PAsearchSites.siteGirlsway.update(metadata,siteID,movieGenres,movieActors)

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
        ##   21Naturals                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 183:
            metadata = PAsearchSites.site21Naturals.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   PornFidelity                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 184:
            metadata = PAsearchSites.sitePornFidelity.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   TeenFidelity                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 185:
            metadata = PAsearchSites.siteTeenFidelity.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Kelly Madison                                          ##
        ##                                                          ##
        ##############################################################
        if siteID == 186:
            metadata = PAsearchSites.siteKellyMadison.update(metadata,siteID,movieGenres,movieActors)

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
        ##   Evil Angel                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 277:
            metadata = PAsearchSites.siteEvilAngel.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   HardX                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 278:
            metadata = PAsearchSites.siteHardX.update(metadata,siteID,movieGenres,movieActors)

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
        ##   PureTaboo                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 281:
            metadata = PAsearchSites.sitePureTaboo.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Stepped Up Media                                       ##
        ##                                                          ##
        ##############################################################
        if siteID >= 282 and siteID <= 284:
            metadata = PAsearchSites.networkSteppedUp.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   EroticaX                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 285:
            metadata = PAsearchSites.siteEroticaX.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   DarkX                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 286:
            metadata = PAsearchSites.siteDarkX.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   LesbianX                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 287:
            metadata = PAsearchSites.siteLesbianX.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Twistys		                                    ##
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
        ##   Private		                                    ##
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
        ##   Throated                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 329:
            metadata = PAsearchSites.siteThroated.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   SweetheartVideo                                        ##
        ##                                                          ##
        ##############################################################
        if siteID == 330:
            metadata = PAsearchSites.siteSweetheartVideo.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   Nuru Massage                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 331:
            metadata = PAsearchSites.siteNuruMassage.update(metadata,siteID,movieGenres,movieActors)

        ##############################################################
        ##                                                          ##
        ##   SweetSinner                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 332:
            metadata = PAsearchSites.siteSweetSinner.update(metadata,siteID,movieGenres,movieActors)

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
