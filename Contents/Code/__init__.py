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
            title = media.primary_metadata.studio + " " + media.primary_metadata.title
        title = title.replace('"','').replace(":","").replace("!","").replace("[","").replace("]","").replace("(","").replace(")","").replace("&","").replace('RARBG.COM','').replace('RARBG','').replace('180 180x180','').replace('180x180','').replace('Hevc','').replace('H265','').replace('Avc','').replace('5k','').replace(' 4k','').replace('.4k','').replace('2300p60','').replace('2160p60','').replace('1920p60','').replace('1600p60','').replace('2300p','').replace('2160p','').replace('1900p','').replace('1600p','').replace('1080p','').replace('720p','').replace('480p','').replace('540p','').replace('3840x1920','').replace('5400x2700','').replace(' XXX',' ').replace('Ktr ','').replace('MP4-KTR','').replace('Oro ','').replace('Sexors','').replace('3dh','').replace('Oculus','').replace('Oculus5k','').replace('Lr','').replace('-180_','').replace('TOWN.AG_','').strip()

        Log('*******MEDIA TITLE****** ' + str(title))

        # Search for year
        year = media.year
        if media.primary_metadata is not None:
            year = media.primary_metadata.year

        Log("Getting Search Settings for: " + title)
        searchDate = None
        searchSiteID = None
        searchSettings = PAsearchSites.getSearchSettings(title)
        searchSiteID = searchSettings[0]
        if searchSiteID == 3:
            searchSiteID = 0
        if searchSiteID == 4:
            searchSiteID = 1
        searchTitle = searchSettings[2]
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

        #Dirty hack to prevent long all-site searches
        if searchSiteID == 9999:
            searchSiteID = 9998
        for searchSite in PAsearchSites.searchSites:
            ###############
            ## Blacked Raw
            ###############
            if siteNum == 0:
                if searchSiteID == 9999 or searchSiteID == 0:
                    results = PAsearchSites.networkStrike3.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Blacked
            ###############
            if siteNum == 1:
                if searchSiteID == 9999 or searchSiteID == 1:
                    results = PAsearchSites.networkStrike3.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Brazzers
            ###############
            if siteNum == 2:
                if searchSiteID == 9999 or searchSiteID == 2 or (54 <= searchSiteID <= 81) or searchSiteID == 582 or searchSiteID == 690:
                    results = PAsearchSites.siteBrazzers.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Naughty America
            ###############
            if siteNum == 5:
                if searchSiteID == 9999 or (5 <= searchSiteID <= 51) or searchSiteID == 341 or (393 <= searchSiteID <= 396) or (467 <= searchSiteID <= 468) or searchSiteID == 581 or searchSiteID == 620 or searchSiteID == 625 or searchSiteID == 691 or searchSiteID == 749:
                    results = PAsearchSites.siteNaughtyAmerica.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Vixen
            ###############
            if siteNum == 52:
                if searchSiteID == 9999 or searchSiteID == 52:
                    results = PAsearchSites.networkStrike3.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## GirlsWay
            ###############
            if siteNum == 53:
                if searchSiteID == 9999 or searchSiteID == 53 or (375 <= searchSiteID <= 379) or (795 <= searchSiteID <= 797):
                    results = PAsearchSites.siteGirlsWay.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## 21Naturals
            ###############
            if siteNum == 183:
                if searchSiteID == 9999 or searchSiteID == 183 or (373 <= searchSiteID <= 374):
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Evil Angel
            ###############
            if siteNum == 277:
                if searchSiteID == 9999 or searchSiteID == 277:
                    results = PAsearchSites.siteEvilAngel.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## XEmpire/Hardx
            ###############
            if siteNum == 278:
                if searchSiteID == 9999 or searchSiteID == 278:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## XEmpire/Eroticax
            ###############
            if siteNum == 285:
                if searchSiteID == 9999 or searchSiteID == 285:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## XEmpire/Darkx
            ###############
            if siteNum == 286:
                if searchSiteID == 9999 or searchSiteID == 286:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## XEmpire/Lesbianx
            ###############
            if siteNum == 287:
                if searchSiteID == 9999 or searchSiteID == 287:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Pure Taboo
            ###############
            if siteNum == 281:
                if searchSiteID == 9999 or searchSiteID == 281:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Blowpass/Throated
            ###############
            if siteNum == 329:
                if searchSiteID == 9999 or searchSiteID == 329:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Blowpass/Mommy Blows Best
            ###############
            if siteNum == 351:
                if searchSiteID == 9999 or searchSiteID == 351:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Blowpass/Only Teen Blowjobs
            ###############
            if siteNum == 352:
                if searchSiteID == 9999 or searchSiteID == 352:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Blowpass/1000 Facials
            ###############
            if siteNum == 353:
                if searchSiteID == 9999 or searchSiteID == 353:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Blowpass/Immoral Live
            ###############
            if siteNum == 354:
                if searchSiteID == 9999 or searchSiteID == 354:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Mile High Media
            ###############
            if siteNum == 361:
                if searchSiteID == 9999 or (361 <= searchSiteID <= 364):
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Fantasy Massage
            ###############
            if siteNum == 330:
                if searchSiteID == 9999 or searchSiteID == 330 or (355 <= searchSiteID <= 360) or searchSiteID == 750:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## 21Sextury
            ###############
            if siteNum == 365:
                if searchSiteID == 9999 or (365 <= searchSiteID <= 372) or searchSiteID == 466 or searchSiteID == 692:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Girlfriends Films
            ###############
            if siteNum == 380:
                if searchSiteID == 9999 or searchSiteID == 380:
                    results = PAsearchSites.siteGirlfriendsFilms.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Burning Angel
            ###############
            if siteNum == 381:
                if searchSiteID == 9999 or searchSiteID == 381:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Pretty Dirty
            ###############
            if siteNum == 382:
                if searchSiteID == 9999 or searchSiteID == 382:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Devil's Film
            ###############
            if siteNum == 383:
                if searchSiteID == 9999 or searchSiteID == 383:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Peter North
            ###############
            if siteNum == 384:
                if searchSiteID == 9999 or searchSiteID == 384:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Rocco Siffredi
            ###############
            if siteNum == 385:
                if searchSiteID == 9999 or searchSiteID == 385:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Tera Patrick
            ###############
            if siteNum == 386:
                if searchSiteID == 9999 or searchSiteID == 386:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Sunny Leone
            ###############
            if siteNum == 387:
                if searchSiteID == 9999 or searchSiteID == 387:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Lane Sisters
            ###############
            if siteNum == 388:
                if searchSiteID == 9999 or searchSiteID == 388:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Dylan Ryder
            ###############
            if siteNum == 389:
                if searchSiteID == 9999 or searchSiteID == 389:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Abbey Brooks
            ###############
            if siteNum == 390:
                if searchSiteID == 9999 or searchSiteID == 390:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Devon Lee
            ###############
            if siteNum == 391:
                if searchSiteID == 9999 or searchSiteID == 391:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Hanna Hilton
            ###############
            if siteNum == 392:
                if searchSiteID == 9999 or searchSiteID == 392:
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## 21Sextreme
            ###############
            if siteNum == 460:
                if searchSiteID == 9999 or (460 <= searchSiteID <= 465):
                    results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## X-Art
            ###############
            if siteNum == 82:
                if searchSiteID == 9999 or searchSiteID == 82:
                    results = PAsearchSites.siteXart.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Bang Bros
            ###############
            if siteNum == 83:
                if searchSiteID == 9999 or (83 <= searchSiteID <= 135):
                    results = PAsearchSites.siteBangBros.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Tushy
            ###############
            if siteNum == 136:
                if searchSiteID == 9999 or searchSiteID == 136:
                    results = PAsearchSites.networkStrike3.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Reality Kings
            ###############
            if siteNum == 137:
                if searchSiteID == 9999 or (137 <= searchSiteID <= 182) or (822 <= searchSiteID <= 828):
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## PornFidelity
            ###############
            if siteNum == 184:
                if searchSiteID == 9999 or searchSiteID == 184:
                    results = PAsearchSites.networkPornFidelity.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## TeenFidelity
            ###############
            if siteNum == 185:
                if searchSiteID == 9999 or searchSiteID == 185:
                    results = PAsearchSites.networkPornFidelity.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Kelly Madison
            ###############
            if siteNum == 186:
                if searchSiteID == 9999 or searchSiteID == 186:
                    results = PAsearchSites.networkPornFidelity.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Team Skeet
            ###############
            if siteNum == 187:
                if searchSiteID == 9999 or (187 <= searchSiteID <= 215):
                    results = PAsearchSites.siteTeamSkeet.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Porndoe Premium
            ###############
            if siteNum == 216:
                if searchSiteID == 9999 or (216 <= searchSiteID <= 259):
                    results = PAsearchSites.sitePorndoePremium.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Legal Porno
            ###############
            if siteNum == 260:
                if searchSiteID == 9999 or searchSiteID == 260:
                    results = PAsearchSites.siteLegalPorno.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Mofos
            ###############
            if siteNum == 261:
                if searchSiteID == 9999 or (261 <= searchSiteID <= 270) or searchSiteID == 583 or (738 <= searchSiteID <= 740):
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Babes
            ###############
            if siteNum == 271:
                if searchSiteID == 9999 or (271 <= searchSiteID <= 276):
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## GloryHoleSecrets
            ###############
            if siteNum == 279:
                if searchSiteID == 9999 or searchSiteID == 279:
                    results = PAsearchSites.siteGloryHoleSecrets.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## NewSensations
            ###############
            if siteNum == 280:
                if searchSiteID == 9999 or searchSiteID == 280:
                    results = PAsearchSites.siteNewSensations.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Swallowed
            ###############
            if siteNum == 282:
                if searchSiteID == 9999 or searchSiteID == 282:
                    results = PAsearchSites.networkSteppedUp.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## TrueAnal
            ###############
            if siteNum == 283:
                if searchSiteID == 9999 or searchSiteID == 283:
                    results = PAsearchSites.networkSteppedUp.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Nympho
            ###############
            if siteNum == 284:
                if searchSiteID == 9999 or searchSiteID == 284:
                    results = PAsearchSites.networkSteppedUp.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Twistys
            ###############
            if siteNum == 288:
                if searchSiteID == 9999 or (288 <= searchSiteID <= 291) or searchSiteID == 768:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Spizoo
            ###############
            if siteNum == 293:
                if searchSiteID == 9999 or searchSiteID == 293 or (571 <= searchSiteID <= 577):
                    results = PAsearchSites.siteSpizoo.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Private
            ###############
            if siteNum == 294:
                if searchSiteID == 9999 or (294 <= searchSiteID <= 305):
                    results = PAsearchSites.sitePrivate.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## PornPros Network
            ###############
            if (306 <= siteNum <= 308) or (479 <= siteNum <= 489) or siteNum == 624 or siteNum == 769:
                if searchSiteID == 9999 or (306 <= searchSiteID <= 327) or (479 <= searchSiteID <= 489) or searchSiteID == 624 or searchSiteID == 769:
                    results = PAsearchSites.networkPornPros.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## DigitalPlayground
            ###############
            if siteNum == 328:
                if searchSiteID == 9999 or searchSiteID == 328:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

             ###############
            ## SexyHub
            ###############
            if siteNum == 333 or siteNum == 335 or siteNum == 406 or siteNum == 407:
                if searchSiteID == 9999 or (333 <= searchSiteID <= 339):
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## FullPornNetwork
            ###############
            if (343 <= siteNum <= 350):
                if searchSiteID == 9999 or (343 <= searchSiteID <= 350):
                    results = PAsearchSites.networkFPN.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## DogfartNetwork
            ###############
            if siteNum == 408:
                if searchSiteID == 9999 or (408 <= searchSiteID <= 431):
                    results = PAsearchSites.networkDogfart.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## FakeHub
            ###############
            if siteNum == 340:
                if searchSiteID == 9999 or searchSiteID == 340 or (397 <= searchSiteID <= 407):
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## JulesJordan
            ###############
            if siteNum == 432:
                if searchSiteID == 9999 or searchSiteID == 432:
                    results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Manuel Ferrara
            ###############
            if siteNum == 522:
                if searchSiteID == 9999 or searchSiteID == 522:
                    results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## The Ass Factory
            ###############
            if siteNum == 523:
                if searchSiteID == 9999 or searchSiteID == 523:
                    results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Sperm Swallowers
            ###############
            if siteNum == 524:
                if searchSiteID == 9999 or searchSiteID == 524:
                    results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## GirlGirl
            ###############
            if siteNum == 782:
                if searchSiteID == 9999 or searchSiteID == 782:
                    results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## DDF Network
            ###############
            if siteNum == 433:
                if searchSiteID == 9999 or (331 <= searchSiteID <= 332) or (433 <= searchSiteID <= 447):
                    results = PAsearchSites.networkDDFNetwork.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## PerfectGonzo
            ###############
            if siteNum == 448:
                if searchSiteID == 9999 or (448 <= searchSiteID <= 459):
                    results = PAsearchSites.networkPerfectGonzo.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## BadoinkVR Network
            ###############
            if siteNum == 469:
                if searchSiteID == 9999 or (469 <= searchSiteID <= 473):
                    results = PAsearchSites.networkBadoinkVR.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## VRBangers
            ###############
            if siteNum == 474:
                if searchSiteID == 9999 or searchSiteID == 474:
                    results = PAsearchSites.siteVRBangers.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## SexBabesVR
            ###############
            if siteNum == 475:
                if searchSiteID == 9999 or searchSiteID == 475:
                    results = PAsearchSites.networkHighTechVR.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## SinsVR
            ###############
            if siteNum == 569:
                if searchSiteID == 9999 or searchSiteID == 569:
                    results = PAsearchSites.networkHighTechVR.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## StasyQ VR
            ###############
            if siteNum == 570:
                if searchSiteID == 9999 or searchSiteID == 570:
                    results = PAsearchSites.networkHighTechVR.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## WankzVR
            ###############
            if siteNum == 476:
                if searchSiteID == 9999 or searchSiteID == 476:
                    results = PAsearchSites.siteWankzVR.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## MilfVR
            ###############
            if siteNum == 477:
                if searchSiteID == 9999 or searchSiteID == 477:
                    results = PAsearchSites.siteMilfVR.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Joymii
            ###############
            if siteNum == 478:
                if searchSiteID == 9999 or searchSiteID == 478:
                    results = PAsearchSites.siteJoymii.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Kink
            ###############
            if siteNum == 490:
                if searchSiteID == 9999 or (490 <= searchSiteID <= 521) or searchSiteID == 687 or (735 <= searchSiteID <= 736):
                    results = PAsearchSites.networkKink.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Nubiles
            ###############
            if siteNum == 525:
                if searchSiteID == 9999 or (525 <= searchSiteID <= 545) or (755 <= searchSiteID <= 756) or searchSiteID == 766:
                    results = PAsearchSites.networkNubiles.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## BellaPass
            ###############
            if siteNum == 548:
                if searchSiteID == 9999 or (548 <= searchSiteID <= 563):
                    results = PAsearchSites.networkBellaPass.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## AllureMedia
            ###############
            if siteNum == 564 or siteNum == 565:
                if searchSiteID == 9999 or (564 <= searchSiteID <= 565):
                    results = PAsearchSites.siteAllureMedia.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## BlackValleyGirls
            ###############
            if siteNum == 566:
                if searchSiteID == 9999 or searchSiteID == 566:
                    results = PAsearchSites.siteBlackValleyGirls.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## SisLovesMe
            ###############
            if siteNum == 567:
                if searchSiteID == 9999 or searchSiteID == 567:
                    results = PAsearchSites.siteSisLovesMe.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Manyvids
            ###############
            if siteNum == 568:
                if searchSiteID == 9999 or searchSiteID == 568:
                    results = PAsearchSites.siteManyvids.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## VirtualTaboo
            ###############
            if siteNum == 292:
                if searchSiteID == 9999 or searchSiteID == 292:
                    results = PAsearchSites.siteVirtualTaboo.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## VirtualRealPorn
            ###############
            if siteNum == 342:
                if searchSiteID == 9999 or searchSiteID == 342:
                    results = PAsearchSites.siteVirtualReal.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## CzechVR Network
            ###############
            if siteNum == 578:
                if searchSiteID == 9999 or (578 <= searchSiteID <= 580):
                    results = PAsearchSites.networkCzechVR.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## FinishesTheJob
            ###############
            if siteNum == 584:
                if searchSiteID == 9999 or (584 <= searchSiteID <= 586):
                    results = PAsearchSites.siteFinishesTheJob.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Wankz Network
            ###############
            if siteNum == 587:
                if searchSiteID == 9999 or (587 <= searchSiteID <= 619):
                    results = PAsearchSites.networkWankz.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## MetArt Network
            ###############
            if siteNum == 621:
                if searchSiteID == 9999 or (621 <= searchSiteID <= 623) or (753 <= searchSiteID <= 754) or (816 <= searchSiteID <= 821):
                    results = PAsearchSites.networkMetArt.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Family Strokes
            ###############
            if siteNum == 626:
                if searchSiteID == 9999 or searchSiteID == 626:
                    results = PAsearchSites.siteFamilyStrokes.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Tonights Girlfriend
            ###############
            if siteNum == 627:
                if searchSiteID == 9999 or searchSiteID == 627:
                    results = PAsearchSites.siteTonightsGirlfriend.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Karups
            ###############
            if siteNum == 628:
                if searchSiteID == 9999 or (628 <= searchSiteID <= 630):
                    results = PAsearchSites.siteKarups.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## TeenMegaWorld
            ###############
            if siteNum == 631:
                if searchSiteID == 9999 or (631 <= searchSiteID <= 666):
                    results = PAsearchSites.networkTMW.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Screwbox
            ###############
            if siteNum == 668:
                if searchSiteID == 9999 or searchSiteID == 668:
                    results = PAsearchSites.siteScrewbox.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## DorcelClub
            ###############
            if siteNum == 669:
                if searchSiteID == 9999 or searchSiteID == 669:
                    results = PAsearchSites.siteDorcelClub.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Tushy
            ###############
            if siteNum == 670:
                if searchSiteID == 9999 or searchSiteID == 670:
                    results = PAsearchSites.networkStrike3.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Deeper
            ###############
            if siteNum == 671:
                if searchSiteID == 9999 or searchSiteID == 671:
                    results = PAsearchSites.networkStrike3.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## MissaX / AllHerLuv
            ###############
            if siteNum == 672:
                if searchSiteID == 9999 or searchSiteID == 672 or searchSiteID == 673:
                    results = PAsearchSites.siteMissaX.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Mylf
            ###############
            if siteNum == 674:
                if searchSiteID == 9999 or (674 <= searchSiteID <= 683) or searchSiteID == 757:
                    results = PAsearchSites.siteMylf.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Manually Add Actors
            ###############
            if siteNum == 684:
                if searchSiteID == 684:
                    results = PAsearchSites.addActors.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## First Anal Quest
            ###############
            if siteNum == 685:
                if searchSiteID == 9999 or searchSiteID == 685:
                    results = PAsearchSites.siteFirstAnalQuest.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## PervMom
            ###############
            if siteNum == 686:
                if searchSiteID == 9999 or searchSiteID == 686:
                    results = PAsearchSites.sitePervMom.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Hegre
            ###############
            if siteNum == 688:
                if searchSiteID == 9999 or searchSiteID == 688:
                    results = PAsearchSites.siteHegre.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Femdom Empire
            ###############
            if siteNum == 689:
                if searchSiteID == 9999 or searchSiteID == 689 or searchSiteID == 694:
                    results = PAsearchSites.networkFemdomEmpire.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Dorcel Vision
            ###############
            if siteNum == 693:
                if searchSiteID == 9999 or searchSiteID == 693:
                    results = PAsearchSites.siteDorcelVision.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## XConfessions
            ###############
            if siteNum == 695:
                if searchSiteID == 9999 or searchSiteID == 695:
                    results = PAsearchSites.siteXConfessions.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## CzechAV
            ###############
            if siteNum == 696:
                if searchSiteID == 9999 or (696 <= searchSiteID <= 728):
                    results = PAsearchSites.networkCzechAV.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## ArchAngel
            ###############
            if siteNum == 729:
                if searchSiteID == 9999 or searchSiteID == 729:
                    results = PAsearchSites.siteArchAngel.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## We Are Hairy
            ###############
            if siteNum == 730:
                if searchSiteID == 9999 or searchSiteID == 730:
                    results = PAsearchSites.siteWeAreHairy.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Love Her Feet
            ###############
            if siteNum == 731:
                if searchSiteID == 9999 or searchSiteID == 731:
                    results = PAsearchSites.siteLoveHerFeet.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## MomPOV
            ###############
            if siteNum == 732:
                if searchSiteID == 9999 or searchSiteID == 732:
                    results = PAsearchSites.siteMomPOV.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Property Sex
            ###############
            if siteNum == 733:
                if searchSiteID == 9999 or searchSiteID == 733:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## FuelVirtual
            ###############
            if siteNum == 546:
                if searchSiteID == 9999 or (546 <= searchSiteID <= 547):
                    results = PAsearchSites.networkFuelVirtual.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## TransAngels
            ###############
            if siteNum == 737:
                if searchSiteID == 9999 or searchSiteID == 737:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Straplezz
            ###############
            if siteNum == 741:
                if searchSiteID == 9999 or searchSiteID == 741:
                    results = PAsearchSites.siteStraplezz.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## LittleCaprice
            ###############
            if siteNum == 742:
                if searchSiteID == 9999 or searchSiteID == 742:
                    results = PAsearchSites.siteLittleCaprice.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## WowGirls
            ###############
            if siteNum == 743:
                if searchSiteID == 9999 or searchSiteID == 743:
                    results = PAsearchSites.siteWowGirls.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## VIPissy
            ###############
            if siteNum == 744:
                if searchSiteID == 9999 or searchSiteID == 744:
                    results = PAsearchSites.siteVIPissy.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## GirlsOutWest
            ###############
            if siteNum == 745:
                if searchSiteID == 9999 or searchSiteID == 745:
                    results = PAsearchSites.siteGirlsOutWest.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Girls Rimming
            ###############
            if siteNum == 746:
                if searchSiteID == 9999 or searchSiteID == 746:
                    results = PAsearchSites.siteGirlsRimming.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Gangbang Creampie
            ###############
            if siteNum == 747:
                if searchSiteID == 9999 or searchSiteID == 747:
                    results = PAsearchSites.siteGangbangCreampie.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## DadCrush
            ###############
            if siteNum == 748:
                if searchSiteID == 9999 or searchSiteID == 748:
                    results = PAsearchSites.siteDadCrush.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## StepSecrets
            ###############
            if siteNum == 751:
                if searchSiteID == 9999 or searchSiteID == 751:
                    results = PAsearchSites.siteStepSecrets.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## VRHush
            ###############
            if siteNum == 752:
                if searchSiteID == 9999 or searchSiteID == 752:
                    results = PAsearchSites.siteVRHush.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Fitting-Room
            ###############
            if siteNum == 758:
                if searchSiteID == 9999 or searchSiteID == 758:
                    results = PAsearchSites.siteFittingRoom.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## FamilyHookups
            ###############
            if siteNum == 759:
                if searchSiteID == 9999 or searchSiteID == 759:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Clips4Sale
            ###############
            if siteNum == 760:
                if searchSiteID == 9999 or searchSiteID == 760:
                    results = PAsearchSites.siteClips4Sale.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## VogoV
            ###############
            if siteNum == 761:
                if searchSiteID == 9999 or searchSiteID == 761:
                    results = PAsearchSites.siteVogoV.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Ultrafilms
            ###############
            if siteNum == 762:
                if searchSiteID == 9999 or searchSiteID == 762:
                    results = PAsearchSites.siteUltrafilms.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## fuckingawesome.com
            ###############
            if siteNum == 763:
                if searchSiteID == 9999 or searchSiteID == 763:
                    results = PAsearchSites.siteFuckingAwesome.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## ToughLoveX
            ###############
            if siteNum == 764:
                if searchSiteID == 9999 or searchSiteID == 764:
                    results = PAsearchSites.siteToughLoveX.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## cumlouder.com
            ###############
            if siteNum == 765:
                if searchSiteID == 9999 or searchSiteID == 765:
                    results = PAsearchSites.siteCumLouder.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## AllAnal
            ###############
            if siteNum == 767:
                if searchSiteID == 9999 or searchSiteID == 767:
                    results = PAsearchSites.networkSteppedUp.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## ZeroTolerance
            ###############
            if siteNum == 770:
                if searchSiteID == 9999 or searchSiteID == 770:
                    results = PAsearchSites.siteZTOD.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## ClubFilly
            ###############
            if siteNum == 771:
                if searchSiteID == 9999 or searchSiteID == 771:
                    results = PAsearchSites.siteClubFilly.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Intersec
            ###############
            if siteNum == 772:
                if searchSiteID == 9999 or (772 <= searchSiteID <= 781):
                    results = PAsearchSites.networkIntersec.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Cherry Pimps
            ###############
            if siteNum == 783:
                if searchSiteID == 9999 or (783 <= searchSiteID <= 792):
                    results = PAsearchSites.networkCherryPimps.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Wicked
            ###############
            if siteNum == 793:
                if searchSiteID == 9999 or searchSiteID == 793:
                    results = PAsearchSites.siteWicked.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## 18OnlyGirls
            ###############
            if siteNum == 794:
                if searchSiteID == 9999 or searchSiteID == 794:
                    results = PAsearchSites.site18OnlyGirls.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## LilHumpers
            ###############
            if siteNum == 798:
                if searchSiteID == 9999 or searchSiteID == 798:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Bellesa Films
            ###############
            if siteNum == 799:
                if searchSiteID == 9999 or searchSiteID == 799:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## ClubSeventeen
            ###############
            if siteNum == 800:
                if searchSiteID == 9999 or searchSiteID == 800:
                    results = PAsearchSites.siteClubSeventeen.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Elegant Angel
            ###############
            if siteNum == 801:
                if searchSiteID == 9999 or searchSiteID == 801:
                    results = PAsearchSites.siteElegantAngel.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Family Sinners
            ###############
            if siteNum == 802:
                if searchSiteID == 9999 or searchSiteID == 802:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## ReidMyLips
            ###############
            if siteNum == 803:
                if searchSiteID == 9999 or searchSiteID == 803:
                    results = PAsearchSites.siteReidMyLips.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Playboy Plus
            ###############
            if siteNum == 804:
                if searchSiteID == 9999 or searchSiteID == 804:
                    results = PAsearchSites.sitePlayboyPlus.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Meana Wolf
            ###############
            if siteNum == 805:
                if searchSiteID == 9999 or searchSiteID == 805:
                    results = PAsearchSites.siteMeanaWolf.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Transsensual
            ###############
            if siteNum == 806:
                if searchSiteID == 9999 or searchSiteID == 806:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## DaughterSwap
            ###############
            if siteNum == 807:
                if searchSiteID == 9999 or searchSiteID == 807:
                    results = PAsearchSites.siteDaughterSwap.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)
 
            ###############
            ## Erito
            ###############
            if siteNum == 808:
                if searchSiteID == 9999 or searchSiteID == 808:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## TrueAmateurs
            ###############
            if siteNum == 809:
                if searchSiteID == 9999 or searchSiteID == 809:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Hustler
            ###############
            if siteNum == 810:
                if searchSiteID == 9999 or searchSiteID == 810:
                    results = PAsearchSites.siteHustler.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## AmourAngels
            ###############
            if siteNum == 811:
                if searchSiteID == 9999 or searchSiteID == 811:
                    results = PAsearchSites.siteAmourAngels.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## JAV
            ###############
            if siteNum == 812:
                if searchSiteID == 9999 or searchSiteID == 812:
                    results = PAsearchSites.networkR18.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Bang
            ###############
            if siteNum == 813:
                if searchSiteID == 9999 or searchSiteID == 813:
                    results = PAsearchSites.networkBang.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## Vivid
            ###############
            if siteNum == 814:
                if searchSiteID == 9999 or searchSiteID == 814:
                    results = PAsearchSites.siteVivid.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## JAY's POV
            ###############
            if siteNum == 815:
                if searchSiteID == 9999 or searchSiteID == 815:
                    results = PAsearchSites.siteJaysPOV.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## PJGirls
            ###############
            if siteNum == 667:
                if searchSiteID == 9999 or searchSiteID == 667:
                    results = PAsearchSites.sitePJGirls.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)
                    
            ###############
            ## PureCFNM Network
            ###############
            if siteNum == 829:
                if searchSiteID == 9999 or (829 <= searchSiteID <= 834):
                    results = PAsearchSites.networkPureCFNM.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)
                    
            ###############
            ## BAMVisions
            ###############
            if siteNum == 835:
                if searchSiteID == 9999 or searchSiteID == 835:
                    results = PAsearchSites.siteBAMVisions.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)
                    
            ###############
            ## ATKGirlfriends
            ###############
            if siteNum == 836:
                if searchSiteID == 9999 or searchSiteID == 836:
                    results = PAsearchSites.siteATKGirlfriends.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

            ###############
            ## LookAtHerNow
            ###############
            if siteNum == 837:
                if searchSiteID == 9999 or searchSiteID == 837:
                    results = PAsearchSites.network1service.search(results, encodedTitle, title, searchTitle, siteNum, lang, searchByDateActor, searchDate, searchSiteID)

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
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Blacked Raw                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 0:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Brazzers                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 2 or (siteID >= 54 and siteID <= 81) or siteID == 582 or siteID == 690:
            metadata = PAsearchSites.siteBrazzers.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   SexyHub                                                ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 333 and siteID <= 339):
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   FakeHub                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 340 or (siteID >= 397 and siteID <= 407):
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Naughty America                                        ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 5 and siteID <= 51) or siteID == 341 or (siteID >= 393 and siteID <= 396) or siteID == 467 or siteID == 468 or siteID == 581 or siteID == 620 or siteID == 625 or siteID == 691 or siteID == 749:
            metadata = PAsearchSites.siteNaughtyAmerica.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Vixen                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 52:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   X-Art                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 82:
            metadata = PAsearchSites.siteXart.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Bang Bros                                              ##
        ##                                                          ##
        ##############################################################
        if siteID >= 83 and siteID <= 135:
            metadata = PAsearchSites.siteBangBros.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Tushy                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 136:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Reality Kings                                          ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 137 and siteID <= 182) or (siteID >= 822 and siteID <= 828):
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   PornFidelity                                           ##
        ##                                                          ##
        ##############################################################
        if siteID >= 184 and siteID <= 186:
            metadata = PAsearchSites.networkPornFidelity.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   TeamSkeet                                              ##
        ##                                                          ##
        ##############################################################
        if siteID >= 187 and siteID <= 215:
            metadata = PAsearchSites.siteTeamSkeet.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Porndoe Premium                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 216 and siteID <= 259:
            metadata = PAsearchSites.sitePorndoePremium.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   LegalPorno                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 260:
            metadata = PAsearchSites.siteLegalPorno.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Mofos                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID >= 261 and siteID <= 270 or siteID == 583 or siteID >= 738 and siteID <= 740:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Babes                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID >= 271 and siteID <= 276:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   GloryHoleSecrets                                       ##
        ##                                                          ##
        ##############################################################
        if siteID == 279:
            metadata = PAsearchSites.siteGloryHoleSecrets.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   NewSensations                                          ##
        ##                                                          ##
        ##############################################################
        if siteID == 280:
            metadata = PAsearchSites.siteNewSensations.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Stepped Up Media                                       ##
        ##                                                          ##
        ##############################################################
        if siteID == 767 or (siteID >= 282 and siteID <= 284):
            metadata = PAsearchSites.networkSteppedUp.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Twistys		                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 288 and siteID <= 291 or siteID == 768:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Spizoo                                                 ##
        ##                                                          ##
        ##############################################################
        if siteID == 293 or (siteID >= 571 and siteID <= 577):
            metadata = PAsearchSites.siteSpizoo.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Private		                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 294 and siteID <= 305:
            metadata = PAsearchSites.sitePrivate.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   PornPros Network                                       ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 306 and siteID <= 327) or (siteID >= 479 and siteID <= 489) or (siteID == 624) or (siteID == 769):
            metadata = PAsearchSites.networkPornPros.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   DigitalPlayground                                      ##
        ##                                                          ##
        ##############################################################
        if siteID == 328:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   FullPornNetwork                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 343 and siteID <= 350:
            metadata = PAsearchSites.networkFPN.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Gamma Entertainment                                    ##
        ##                                                          ##
        ##############################################################
        if siteID == 183 or siteID == 278 or siteID == 281 or (siteID >= 285 and siteID <= 287) or (siteID >= 329 and siteID <= 330) or (siteID >= 351 and siteID <= 360) or (siteID >= 365 and siteID <= 374) or (siteID >= 381 and siteID <= 392) or (siteID >= 460 and siteID <= 466) or siteID == 750:
            metadata = PAsearchSites.networkGammaEnt.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  MileHighMedia                                           ##
        ##                                                          ##
        ##############################################################
        if siteID >= 361 and siteID <= 364:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Dogfart Network                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >= 408 and siteID <= 431:
            metadata = PAsearchSites.networkDogfart.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Jules Jordan                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 432 or (siteID >= 522 and siteID <= 524) or siteID == 782:
            metadata = PAsearchSites.siteJulesJordan.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   DDF Network                                            ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 331 and siteID <= 332) or (siteID >= 433 and siteID <= 447):
            metadata = PAsearchSites.networkDDFNetwork.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Perfect Gonzo                                          ##
        ##                                                          ##
        ##############################################################
        if siteID >= 448 and siteID <= 459:
            metadata = PAsearchSites.networkPerfectGonzo.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  BadoinkVR Network                                       ##
        ##                                                          ##
        ##############################################################
        if siteID >= 469 and siteID <= 473:
            metadata = PAsearchSites.networkBadoinkVR.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  VRBangers                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 474:
            metadata = PAsearchSites.siteVRBangers.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  SexBabesVR                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 475:
            metadata = PAsearchSites.networkHighTechVR.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  SinsVR                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 569:
            metadata = PAsearchSites.networkHighTechVR.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  StasyQ VR                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 570:
            metadata = PAsearchSites.networkHighTechVR.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  WankzVR                                                 ##
        ##                                                          ##
        ##############################################################
        if siteID == 476:
            metadata = PAsearchSites.siteWankzVR.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  MilfVR                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 477:
            metadata = PAsearchSites.siteMilfVR.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Joymii                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 478:
            metadata = PAsearchSites.siteJoymii.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Kink                                                    ##
        ##                                                          ##
        ##############################################################
        if siteID >= 490 and siteID <= 521 or siteID == 687 or siteID == 735 or siteID == 736:
            metadata = PAsearchSites.networkKink.update(metadata, siteID, movieGenres, movieActors)
            
        ##############################################################
        ##                                                          ##
        ##  Nubiles                                                  ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 525 and siteID <= 545) or (siteID >= 755 and siteID <= 756) or (siteID == 766):
            metadata = PAsearchSites.networkNubiles.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  BellaPass                                               ##
        ##                                                          ##
        ##############################################################
        if siteID >= 548 and siteID <= 563:
            metadata = PAsearchSites.networkBellaPass.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  AllureMedia                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 564 or siteID == 565:
            metadata = PAsearchSites.siteAllureMedia.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  BlackValleyGirls                                        ##
        ##                                                          ##
        ##############################################################
        if siteID == 566:
            metadata = PAsearchSites.siteBlackValleyGirls.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  SisLovesMe                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 567:
            metadata = PAsearchSites.siteSisLovesMe.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Manyvids                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 568:
            metadata = PAsearchSites.siteManyvids.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  VirtualTaboo                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 292:
            metadata = PAsearchSites.siteVirtualTaboo.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  VirtualRealPorn                                         ##
        ##                                                          ##
        ##############################################################
        if siteID == 342:
            metadata = PAsearchSites.siteVirtualReal.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  CzechVR Network                                         ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 578 and siteID <= 580):
            metadata = PAsearchSites.networkCzechVR.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  FinishesTheJob                                          ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 584 and siteID <= 586):
            metadata = PAsearchSites.siteFinishesTheJob.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Wankz Network                                          ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 587 and siteID <= 619):
            metadata = PAsearchSites.networkWankz.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Family Strokes                                          ##
        ##                                                          ##
        ##############################################################
        if siteID == 626:
            metadata = PAsearchSites.siteFamilyStrokes.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Tonights Girlfriend                                     ##
        ##                                                          ##
        ##############################################################
        if siteID == 627:
            metadata = PAsearchSites.siteTonightsGirlfriend.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Karups                                                  ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 628 and siteID <= 630):
            metadata = PAsearchSites.siteKarups.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  TeenMegaWorld                                           ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 631 and siteID <= 666):
            metadata = PAsearchSites.networkTMW.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  ScrewBox                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 668:
            metadata = PAsearchSites.siteScrewbox.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  DorcelClub                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 669:
            metadata = PAsearchSites.siteDorcelClub.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   TushyRaw                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 670:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   Deeper                                                 ##
        ##                                                          ##
        ##############################################################
        if siteID == 671:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  MissaX / AllHerLuv                                      ##
        ##                                                          ##
        ##############################################################
        if siteID == 672 or siteID == 673:
            metadata = PAsearchSites.siteMissaX.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Mylf                                                    ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 674 and siteID <= 683) or siteID == 757:
            metadata = PAsearchSites.siteMylf.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Manually Add Actors                                     ##
        ##                                                          ##
        ##############################################################
        if siteID == 684:
            metadata = PAsearchSites.addActors.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##   First Anal Quest                                       ##
        ##                                                          ##
        ##############################################################
        if siteID == 685:
            metadata = PAsearchSites.siteFirstAnalQuest.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  PervMom                                                 ##
        ##                                                          ##
        ##############################################################
        if siteID == 686:
            metadata = PAsearchSites.sitePervMom.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Hegre                                                   ##
        ##                                                          ##
        ##############################################################
        if siteID == 688:
            metadata = PAsearchSites.siteHegre.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  FemdomEmpire                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 689 or siteID == 694:
            metadata = PAsearchSites.networkFemdomEmpire.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  DorcelVision                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 693:
            metadata = PAsearchSites.siteDorcelVision.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  XConfessions                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 695:
            metadata = PAsearchSites.siteXConfessions.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Czech AV                                                ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 696 and siteID <= 728):
            metadata = PAsearchSites.networkCzechAV.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  ArchAngel                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 729:
            metadata = PAsearchSites.siteArchAngel.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  We Are Hairy                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 730:
            metadata = PAsearchSites.siteWeAreHairy.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Love Her Feet                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 731:
            metadata = PAsearchSites.siteLoveHerFeet.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  MomPOV                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 732:
            metadata = PAsearchSites.siteMomPOV.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Property Sex                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 733:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  FuelVirtual                                             ##
        ##                                                          ##
        ##############################################################
        if 546 <= siteID <= 547:
            metadata = PAsearchSites.networkFuelVirtual.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  TransAngels                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 737:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Straplezz                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 741:
            metadata = PAsearchSites.siteStraplezz.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  LittleCaprice                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 742:
            metadata = PAsearchSites.siteLittleCaprice.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  WowGirls                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 743:
            metadata = PAsearchSites.siteWowGirls.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  VIPissy                                                 ##
        ##                                                          ##
        ##############################################################
        if siteID == 744:
            metadata = PAsearchSites.siteVIPissy.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  GirlsOutWest                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 745:
            metadata = PAsearchSites.siteGirlsOutWest.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Girls Rimming                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 746:
            metadata = PAsearchSites.siteGirlsRimming.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Gangbang Creampie                                       ##
        ##                                                          ##
        ##############################################################
        if siteID == 747:
            metadata = PAsearchSites.siteGangbangCreampie.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  DadCrush                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 748:
            metadata = PAsearchSites.siteDadCrush.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  StepSecrets                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 751:
            metadata = PAsearchSites.siteStepSecrets.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  VRHush                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 752:
            metadata = PAsearchSites.siteVRHush.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  MetArt Network                                          ##
        ##                                                          ##
        ##############################################################
        if (621 <= siteID <= 623) or (753 <= siteID <= 754) or (816 <= siteID <= 821):
            metadata = PAsearchSites.networkMetArt.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Fitting-Room                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 758:
            metadata = PAsearchSites.siteFittingRoom.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  FamilyHookups                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 759:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Clips4Sale                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 760:
            metadata = PAsearchSites.siteClips4Sale.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  VogoV                                                   ##
        ##                                                          ##
        ##############################################################
        if siteID == 761:
            metadata = PAsearchSites.siteVogoV.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Ultrafilms                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 762:
            metadata = PAsearchSites.siteUltrafilms.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  fuckingawesome.com                                      ##
        ##                                                          ##
        ##############################################################
        if siteID == 763:
            metadata = PAsearchSites.siteFuckingAwesome.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  ToughLoveX                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 764:
            metadata = PAsearchSites.siteToughLoveX.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  cumlouder.com                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 765:
            metadata = PAsearchSites.siteCumLouder.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  ztod.com                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 770:
            metadata = PAsearchSites.siteZTOD.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  ClubFilly                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 771:
            metadata = PAsearchSites.siteClubFilly.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Intersec                                                ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 772 and siteID <= 781):
            metadata = PAsearchSites.networkIntersec.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Cherry Pimps                                            ##
        ##                                                          ##
        ##############################################################
        if (siteID >= 783 and siteID <= 792):
            metadata = PAsearchSites.networkCherryPimps.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Wicked                                                  ##
        ##                                                          ##
        ##############################################################
        if siteID == 793:
            metadata = PAsearchSites.siteWicked.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  18OnlyGirls                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 794:
            metadata = PAsearchSites.site18OnlyGirls.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  GirlsWay                                                ##
        ##                                                          ##
        ##############################################################
        if siteID == 53 or (siteID >=  375 and siteID <= 379) or (siteID >=  795 and siteID <= 797):
            metadata = PAsearchSites.siteGirlsWay.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Evil Angel                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 277:
            metadata = PAsearchSites.siteEvilAngel.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Lil Humpers                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 798:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  BellesaFilms                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 799:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  ClubSeventeen                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 800:
            metadata = PAsearchSites.siteClubSeventeen.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Elegant Angel                                           ##
        ##                                                          ##
        ##############################################################
        if siteID == 801:
            metadata = PAsearchSites.siteElegantAngel.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Family Sinners                                          ##
        ##                                                          ##
        ##############################################################
        if siteID == 802:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  ReidMyLips                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 803:
            metadata = PAsearchSites.siteReidMyLips.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Playboy Plus                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 804:
            metadata = PAsearchSites.sitePlayboyPlus.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Meana Wolf                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 805:
            metadata = PAsearchSites.siteMeanaWolf.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Transsensual                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 806:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  DaughterSwap                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 807:
            metadata = PAsearchSites.siteDaughterSwap.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Erito                                                   ##
        ##                                                          ##
        ##############################################################
        if siteID == 808:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  TrueAmateurs                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 809:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Hustler                                                 ##
        ##                                                          ##
        ##############################################################
        if siteID == 810:
            metadata = PAsearchSites.siteHustler.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  AmourAngels                                             ##
        ##                                                          ##
        ##############################################################
        if siteID == 811:
            metadata = PAsearchSites.siteAmourAngels.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  JAV                                                     ##
        ##                                                          ##
        ##############################################################
        if siteID == 812:
            metadata = PAsearchSites.networkR18.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Bang                                                    ##
        ##                                                          ##
        ##############################################################
        if siteID == 813:
            metadata = PAsearchSites.networkBang.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Vivid                                                   ##
        ##                                                          ##
        ##############################################################
        if siteID == 814:
            metadata = PAsearchSites.siteVivid.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  JAY's POV                                               ##
        ##                                                          ##
        ##############################################################
        if siteID == 815:
            metadata = PAsearchSites.siteJaysPOV.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  Girlfriends Films                                       ##
        ##                                                          ##
        ##############################################################
        if siteID == 380:
            metadata = PAsearchSites.siteGirlfriendsFilms.update(metadata, siteID, movieGenres, movieActors)
         
        ##############################################################
        ##                                                          ##
        ##  PJGirls                                                 ##
        ##                                                          ##
        ##############################################################
        if siteID == 667:
            metadata = PAsearchSites.sitePJGirls.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  PureCFNM Network                                        ##
        ##                                                          ##
        ##############################################################
        if siteID >=  829 and siteID <= 834:
            metadata = PAsearchSites.networkPureCFNM.update(metadata, siteID, movieGenres, movieActors)
        
        ##############################################################
        ##                                                          ##
        ##  BAMVisions                                              ##
        ##                                                          ##
        ##############################################################
        if siteID == 835:
            metadata = PAsearchSites.siteBAMVisions.update(metadata, siteID, movieGenres, movieActors)
            
        ##############################################################
        ##                                                          ##
        ##  ATK Girlfriends                                         ##
        ##                                                          ##
        ##############################################################
        if siteID == 836:
            metadata = PAsearchSites.siteATKGirlfriends.update(metadata, siteID, movieGenres, movieActors)

        ##############################################################
        ##                                                          ##
        ##  LookAtHerNow                                            ##
        ##                                                          ##
        ##############################################################
        if siteID == 837:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)
            
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
