import os
import re
import random
import requests
import urllib
import urlparse
import json
from datetime import datetime
from PIL import Image
from cStringIO import StringIO
from dateutil.parser import parse
import time
import base64
import PAactors
import PAgenres
import PAsearchSites
import PAutils


def Start():
    HTTP.ClearCache()
    HTTP.CacheTime = CACHE_1MINUTE * 20
    HTTP.Headers['User-Agent'] = PAutils.getUserAgent()
    HTTP.Headers['Accept-Encoding'] = 'gzip'

    requests.packages.urllib3.disable_warnings()


class PhoenixAdultAgent(Agent.Movies):
    name = 'PhoenixAdult'
    languages = [Locale.Language.English]
    accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.lambda']
    primary_provider = True

    def search(self, results, media, lang):
        if Prefs['strip_enable']:
            title = media.name.split(Prefs['strip_symbol'], 1)[0]
        else:
            title = media.name

        if media.primary_metadata is not None:
            title = media.primary_metadata.studio + " " + media.primary_metadata.title

        trashTitle = (
            'RARBG', 'COM', r'\d{3,4}x\d{3,4}', 'HEVC', 'H265', 'AVC', r'\dK',
            r'\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4', 'KLEENEX', 'SD', 'HD',
            'ForeverAloneDude'
        )

        title = re.sub(r'\W', ' ', title)
        for trash in trashTitle:
            title = re.sub(r'\b%s\b' % trash, '', title, flags=re.IGNORECASE)
        title = ' '.join(title.split())

        Log('*******MEDIA TITLE****** ' + str(title))

        # Search for year
        year = media.year
        if media.primary_metadata is not None:
            year = media.primary_metadata.year

        Log("Getting Search Settings for: " + title)
        searchSettings = PAsearchSites.getSearchSettings(title)
        searchSiteID = searchSettings[0]
        searchTitle = searchSettings[1]
        searchDate = searchSettings[2]
        Log("Search Title: " + searchTitle)
        if searchDate:
            Log("Search Date: " + searchDate)

        encodedTitle = urllib.quote(searchTitle)
        Log(encodedTitle)

        if searchSiteID is not None:
            siteNum = searchSiteID

            # Blacked Raw
            if searchSiteID == 0:
                results = PAsearchSites.networkStrike3.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Blacked
            elif searchSiteID == 1:
                results = PAsearchSites.networkStrike3.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Brazzers
            elif searchSiteID == 2 or (54 <= searchSiteID <= 81) or searchSiteID == 582 or searchSiteID == 690:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Naughty America
            elif (5 <= searchSiteID <= 51) or searchSiteID == 341 or (393 <= searchSiteID <= 396) or (467 <= searchSiteID <= 468) or searchSiteID == 581 or searchSiteID == 620 or searchSiteID == 625 or searchSiteID == 691 or searchSiteID == 749:
                results = PAsearchSites.siteNaughtyAmerica.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Vixen
            elif searchSiteID == 52:
                results = PAsearchSites.networkStrike3.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # GirlsWay
            elif searchSiteID == 53 or (375 <= searchSiteID <= 379) or (795 <= searchSiteID <= 797):
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # 21Naturals
            elif searchSiteID == 183 or (373 <= searchSiteID <= 374):
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Evil Angel
            elif searchSiteID == 277 or searchSiteID == 975:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # XEmpire / Hardx
            elif searchSiteID == 278:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # XEmpire / Eroticax
            elif searchSiteID == 285:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # XEmpire / Darkx
            elif searchSiteID == 286:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # XEmpire / Lesbianx
            elif searchSiteID == 287:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Pure Taboo
            elif searchSiteID == 281:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Blowpass / Throated

            elif searchSiteID == 329:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Blowpass / Mommy Blows Best
            elif searchSiteID == 351:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Blowpass / Only Teen Blowjobs
            elif searchSiteID == 352:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Blowpass / 1000 Facials

            elif searchSiteID == 353:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Blowpass / Immoral Live
            elif searchSiteID == 354:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Blowpass / My XXX Pass
            elif searchSiteID == 861:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Mile High Media
            elif (361 <= searchSiteID <= 364) or searchSiteID == 852 or (914 <= searchSiteID <= 915):
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Fantasy Massage
            elif searchSiteID == 330 or (355 <= searchSiteID <= 360) or searchSiteID == 750:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # 21Sextury
            elif (365 <= searchSiteID <= 372) or searchSiteID == 466 or searchSiteID == 692:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Girlfriends Films
            elif searchSiteID == 380:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Burning Angel
            elif searchSiteID == 381:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Pretty Dirty
            elif searchSiteID == 382:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Devil's Film
            elif searchSiteID == 383:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Peter North
            elif searchSiteID == 384:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Rocco Siffredi
            elif searchSiteID == 385:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Tera Patrick
            elif searchSiteID == 386:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Sunny Leone
            elif searchSiteID == 387:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Lane Sisters
            elif searchSiteID == 388:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Dylan Ryder
            elif searchSiteID == 389:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Abbey Brooks
            elif searchSiteID == 390:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Devon Lee
            elif searchSiteID == 391:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Hanna Hilton
            elif searchSiteID == 392:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # 21Sextreme
            elif (460 <= searchSiteID <= 465):
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # X-Art
            elif searchSiteID == 82:
                results = PAsearchSites.siteXart.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Bang Bros
            elif (83 <= searchSiteID <= 135):
                results = PAsearchSites.siteBangBros.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Tushy
            elif searchSiteID == 136:
                results = PAsearchSites.networkStrike3.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Reality Kings
            elif (137 <= searchSiteID <= 182) or (822 <= searchSiteID <= 828):
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # PornFidelity
            elif searchSiteID == 184:
                results = PAsearchSites.networkPornFidelity.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # TeenFidelity
            elif searchSiteID == 185:
                results = PAsearchSites.networkPornFidelity.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Kelly Madison
            elif searchSiteID == 186:
                results = PAsearchSites.networkPornFidelity.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # TeamSkeet
            elif (187 <= searchSiteID <= 215) or (566 <= searchSiteID <= 567) or searchSiteID == 626 or searchSiteID == 686 or searchSiteID == 748 or searchSiteID == 807 or (845 <= searchSiteID <= 851) or searchSiteID == 875 or (997 <= searchSiteID <= 1011):
                results = PAsearchSites.networkTeamSkeet.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Porndoe Premium
            elif (216 <= searchSiteID <= 259):
                results = PAsearchSites.sitePorndoePremium.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Legal Porno
            elif searchSiteID == 260:
                results = PAsearchSites.siteLegalPorno.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Mofos
            elif (261 <= searchSiteID <= 270) or searchSiteID == 583 or (738 <= searchSiteID <= 740):
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Babes
            elif (271 <= searchSiteID <= 276):
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # GloryHoleSecrets
            elif searchSiteID == 279:
                results = PAsearchSites.siteGloryHoleSecrets.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # NewSensations
            elif searchSiteID == 280:
                results = PAsearchSites.siteNewSensations.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Swallowed
            elif searchSiteID == 282:
                results = PAsearchSites.networkSteppedUp.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # TrueAnal
            elif searchSiteID == 283:
                results = PAsearchSites.networkSteppedUp.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Nympho
            elif searchSiteID == 284:
                results = PAsearchSites.networkSteppedUp.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Twistys
            elif (288 <= searchSiteID <= 291) or searchSiteID == 768:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Spizoo
            elif searchSiteID == 293 or (571 <= searchSiteID <= 577):
                results = PAsearchSites.siteSpizoo.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Private
            elif (294 <= searchSiteID <= 305):
                results = PAsearchSites.sitePrivate.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # PornPros Network
            elif (306 <= searchSiteID <= 327) or (479 <= searchSiteID <= 489) or searchSiteID == 624 or searchSiteID == 769 or searchSiteID == 844 or searchSiteID == 890:
                results = PAsearchSites.networkPornPros.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # DigitalPlayground
            elif searchSiteID == 328:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # SexyHub
            elif (333 <= searchSiteID <= 339) or (406 <= searchSiteID <= 407):
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # FullPornNetwork
            elif (343 <= searchSiteID <= 350):
                results = PAsearchSites.networkFullPornNetwork.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # DogfartNetwork
            elif (408 <= searchSiteID <= 431):
                results = PAsearchSites.networkDogfart.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # FakeHub
            elif searchSiteID == 340 or (397 <= searchSiteID <= 407):
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # JulesJordan
            elif searchSiteID == 432:
                results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Manuel Ferrara
            elif searchSiteID == 522:
                results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # The Ass Factory
            elif searchSiteID == 523:
                results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Sperm Swallowers
            elif searchSiteID == 524:
                results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # GirlGirl
            elif searchSiteID == 782:
                results = PAsearchSites.siteJulesJordan.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # DDF Network
            elif (331 <= searchSiteID <= 332) or (433 <= searchSiteID <= 447):
                results = PAsearchSites.networkDDFNetwork.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # PerfectGonzo
            elif (448 <= searchSiteID <= 459) or (908 <= searchSiteID <= 911):
                results = PAsearchSites.networkPerfectGonzo.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # BadoinkVR Network
            elif (469 <= searchSiteID <= 473):
                results = PAsearchSites.networkBadoinkVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # VRBangers
            elif searchSiteID == 474:
                results = PAsearchSites.siteVRBangers.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # SexBabesVR
            elif searchSiteID == 475:
                results = PAsearchSites.networkHighTechVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # SinsVR
            elif searchSiteID == 569:
                results = PAsearchSites.networkHighTechVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # StasyQ VR
            elif searchSiteID == 570:
                results = PAsearchSites.networkHighTechVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # WankzVR
            elif searchSiteID == 476:
                results = PAsearchSites.siteMilfVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # MilfVR
            elif searchSiteID == 477:
                results = PAsearchSites.siteMilfVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Joymii
            elif searchSiteID == 478:
                results = PAsearchSites.siteJoymii.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Kink
            elif (490 <= searchSiteID <= 521) or searchSiteID == 687 or (735 <= searchSiteID <= 736) or (873 <= searchSiteID <= 874) or (888 <= searchSiteID <= 889):
                results = PAsearchSites.networkKink.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Nubiles
            elif (525 <= searchSiteID <= 545) or (755 <= searchSiteID <= 756) or searchSiteID == 766 or (995 <= searchSiteID <= 996):
                results = PAsearchSites.networkNubiles.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # BellaPass
            elif (548 <= searchSiteID <= 563):
                results = PAsearchSites.networkBellaPass.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # AllureMedia
            elif (564 <= searchSiteID <= 565):
                results = PAsearchSites.siteAllureMedia.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Manyvids
            elif searchSiteID == 568:
                results = PAsearchSites.siteManyvids.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # VirtualTaboo
            elif searchSiteID == 292:
                results = PAsearchSites.siteVirtualTaboo.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # VirtualRealPorn
            elif searchSiteID == 342:
                results = PAsearchSites.siteVirtualReal.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # CzechVR Network
            elif (578 <= searchSiteID <= 580):
                results = PAsearchSites.networkCzechVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # FinishesTheJob
            elif (584 <= searchSiteID <= 586):
                results = PAsearchSites.siteFinishesTheJob.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Wankz Network
            elif (587 <= searchSiteID <= 619):
                results = PAsearchSites.networkWankz.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # MetArt Network
            elif (621 <= searchSiteID <= 623) or (753 <= searchSiteID <= 754) or (816 <= searchSiteID <= 821):
                results = PAsearchSites.networkMetArt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Tonights Girlfriend
            elif searchSiteID == 627:
                results = PAsearchSites.siteTonightsGirlfriend.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Karups
            elif (628 <= searchSiteID <= 630):
                results = PAsearchSites.siteKarups.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # TeenMegaWorld
            elif (631 <= searchSiteID <= 666) or searchSiteID == 930:
                results = PAsearchSites.networkTeenMegaWorld.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Screwbox
            elif searchSiteID == 668:
                results = PAsearchSites.siteScrewbox.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # DorcelClub
            elif searchSiteID == 669:
                results = PAsearchSites.siteDorcelClub.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Tushy
            elif searchSiteID == 670:
                results = PAsearchSites.networkStrike3.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Deeper
            elif searchSiteID == 671:
                results = PAsearchSites.networkStrike3.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # MissaX / AllHerLuv
            elif searchSiteID == 672 or searchSiteID == 673:
                results = PAsearchSites.siteMissaX.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Mylf
            elif (674 <= searchSiteID <= 683) or searchSiteID == 757 or searchSiteID == 842 or (searchSiteID >= 853 and searchSiteID <= 858) or (881 <= searchSiteID <= 887):
                results = PAsearchSites.siteMylf.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Manually Add Actors
            elif searchSiteID == 684:
                results = PAsearchSites.addActors.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # First Anal Quest
            elif searchSiteID == 685:
                results = PAsearchSites.siteFirstAnalQuest.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Hegre
            elif searchSiteID == 688:
                results = PAsearchSites.siteHegre.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Femdom Empire
            elif searchSiteID == 689 or searchSiteID == 694:
                results = PAsearchSites.networkFemdomEmpire.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Dorcel Vision
            elif searchSiteID == 693:
                results = PAsearchSites.siteDorcelVision.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # XConfessions
            elif searchSiteID == 695:
                results = PAsearchSites.siteXConfessions.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # CzechAV
            elif (696 <= searchSiteID <= 728):
                results = PAsearchSites.networkCzechAV.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ArchAngel
            elif searchSiteID == 729:
                results = PAsearchSites.siteArchAngel.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # We Are Hairy
            elif searchSiteID == 730:
                results = PAsearchSites.siteWeAreHairy.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Love Her Feet
            elif searchSiteID == 731:
                results = PAsearchSites.siteLoveHerFeet.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # MomPOV
            elif searchSiteID == 732:
                results = PAsearchSites.siteMomPOV.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Property Sex
            elif searchSiteID == 733:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # FuelVirtual
            elif (546 <= searchSiteID <= 547):
                results = PAsearchSites.networkFuelVirtual.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # TransAngels
            elif searchSiteID == 737:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Straplezz
            elif searchSiteID == 741:
                results = PAsearchSites.siteStraplezz.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # LittleCaprice
            elif searchSiteID == 742:
                results = PAsearchSites.siteLittleCaprice.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # WowGirls
            elif searchSiteID == 743:
                results = PAsearchSites.siteWowGirls.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # VIPissy
            elif searchSiteID == 744:
                results = PAsearchSites.siteVIPissy.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # GirlsOutWest
            elif searchSiteID == 745:
                results = PAsearchSites.siteGirlsOutWest.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Girls Rimming
            elif searchSiteID == 746:
                results = PAsearchSites.siteGirlsRimming.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Gangbang Creampie
            elif searchSiteID == 747:
                results = PAsearchSites.siteGangbangCreampie.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # StepSecrets
            elif searchSiteID == 751:
                results = PAsearchSites.siteStepSecrets.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # VRHush
            elif searchSiteID == 752:
                results = PAsearchSites.siteVRHush.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Fitting-Room
            elif searchSiteID == 758:
                results = PAsearchSites.siteFittingRoom.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # FamilyHookups
            elif searchSiteID == 759:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Clips4Sale
            elif searchSiteID == 760:
                results = PAsearchSites.siteClips4Sale.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # VogoV
            elif searchSiteID == 761:
                results = PAsearchSites.siteVogoV.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Ultrafilms
            elif searchSiteID == 762:
                results = PAsearchSites.siteUltrafilms.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # fuckingawesome.com
            elif searchSiteID == 763:
                results = PAsearchSites.siteFuckingAwesome.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ToughLoveX
            elif searchSiteID == 764:
                results = PAsearchSites.siteToughLoveX.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # cumlouder.com
            elif searchSiteID == 765:
                results = PAsearchSites.siteCumLouder.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # AllAnal
            elif searchSiteID == 767:
                results = PAsearchSites.networkSteppedUp.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ZeroTolerance
            elif searchSiteID == 770:
                results = PAsearchSites.siteZTOD.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ClubFilly
            elif searchSiteID == 771:
                results = PAsearchSites.siteClubFilly.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Intersec
            elif (772 <= searchSiteID <= 781):
                results = PAsearchSites.networkIntersec.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Cherry Pimps
            elif (783 <= searchSiteID <= 792):
                results = PAsearchSites.networkCherryPimps.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Wicked
            elif searchSiteID == 793:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # 18OnlyGirls
            elif searchSiteID == 794:
                results = PAsearchSites.site18OnlyGirls.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # LilHumpers
            elif searchSiteID == 798:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Bellesa Films
            elif searchSiteID == 799 or searchSiteID == 876:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ClubSeventeen
            elif searchSiteID == 800:
                results = PAsearchSites.siteClubSeventeen.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Elegant Angel
            elif searchSiteID == 801:
                results = PAsearchSites.siteElegantAngel.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Family Sinners
            elif searchSiteID == 802:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ReidMyLips
            elif searchSiteID == 803:
                results = PAsearchSites.siteReidMyLips.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Playboy Plus
            elif searchSiteID == 804:
                results = PAsearchSites.sitePlayboyPlus.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Meana Wolf
            elif searchSiteID == 805:
                results = PAsearchSites.siteMeanaWolf.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Transsensual
            elif searchSiteID == 806:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Erito
            elif searchSiteID == 808:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # TrueAmateurs
            elif searchSiteID == 809:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Hustler
            elif searchSiteID == 810:
                results = PAsearchSites.siteHustler.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # AmourAngels
            elif searchSiteID == 811:
                results = PAsearchSites.siteAmourAngels.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # JAV
            elif searchSiteID == 812:
                results = PAsearchSites.networkR18.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Bang
            elif searchSiteID == 813:
                results = PAsearchSites.networkBang.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Vivid
            elif searchSiteID == 814:
                results = PAsearchSites.siteVivid.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # JAY's POV
            elif searchSiteID == 815:
                results = PAsearchSites.siteJaysPOV.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # PJGirls
            elif searchSiteID == 667:
                results = PAsearchSites.sitePJGirls.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # PureCFNM Network
            elif (829 <= searchSiteID <= 834):
                results = PAsearchSites.networkPureCFNM.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # BAMVisions
            elif searchSiteID == 835:
                results = PAsearchSites.siteBAMVisions.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ATKGirlfriends
            elif searchSiteID == 836:
                results = PAsearchSites.siteATKGirlfriends.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # TwoWebMedia
            elif (837 <= searchSiteID <= 839):
                results = PAsearchSites.networkTwoWebMedia.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Interracial Pass
            elif searchSiteID == 840:
                results = PAsearchSites.siteInterracialPass.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # LookAtHerNow
            elif searchSiteID == 841:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # XEmpire / AllBlackX
            elif searchSiteID == 843:
                results = PAsearchSites.networkGammaEnt.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Deviant Hardcore
            elif searchSiteID == 859:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # She Will Cheat
            elif searchSiteID == 860:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # SinsLife
            elif searchSiteID == 862:
                results = PAsearchSites.siteSinsLife.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Puffy Network
            elif searchSiteID == 863 or (867 <= searchSiteID <= 870):
                results = PAsearchSites.networkPuffy.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # SinX
            elif (864 <= searchSiteID <= 866) or searchSiteID == 871:
                results = PAsearchSites.networkSinX.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Kinky Spa
            elif searchSiteID == 872:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Reality Lovers
            elif searchSiteID == 877:
                results = PAsearchSites.siteRealityLovers.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Adult Time
            elif searchSiteID == 878:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # RealJamVR
            elif searchSiteID == 879:
                results = PAsearchSites.networkHighTechVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # BBC Paradise
            elif searchSiteID == 880:
                results = PAsearchSites.siteMylf.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # HoloGirlsVR
            elif searchSiteID == 891:
                results = PAsearchSites.siteHoloGirlsVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # LethalHardcoreVR
            elif searchSiteID == 892:
                results = PAsearchSites.siteLethalHardcoreVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Gender X
            elif searchSiteID == 893:
                results = PAsearchSites.networkGammaEntOther.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # WhoreCraftVR
            elif searchSiteID == 894:
                results = PAsearchSites.siteLethalHardcoreVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Defeated
            elif searchSiteID == 895 or searchSiteID == 896:
                results = PAsearchSites.siteDefeated.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # XVirtual
            elif searchSiteID == 897:
                results = PAsearchSites.siteXVirtual.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Lust Reality
            elif searchSiteID == 898:
                results = PAsearchSites.siteLustReality.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Sex Like Real
            elif searchSiteID == 899:
                results = PAsearchSites.siteSexLikeReal.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # DoeGirls
            elif searchSiteID == 900:
                results = PAsearchSites.sitePorndoePremium.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Xillimite
            elif searchSiteID == 901:
                results = PAsearchSites.siteXillimite.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # VRP Films
            elif searchSiteID == 902:
                results = PAsearchSites.siteVRPFilms.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # VR Latina
            elif searchSiteID == 903:
                results = PAsearchSites.siteVRLatina.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # VRConk
            elif searchSiteID == 904:
                results = PAsearchSites.siteVRConk.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # RealJamVR
            elif searchSiteID == 905:
                results = PAsearchSites.networkHighTechVR.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Evolved Fights Network
            elif searchSiteID == 906 or searchSiteID == 907:
                results = PAsearchSites.networkEvolvedFights.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # JavBus
            elif searchSiteID == 912:
                results = PAsearchSites.networkJavBus.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Hucows
            elif searchSiteID == 913:
                results = PAsearchSites.siteHucows.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Why Not Bi
            elif searchSiteID == 916:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # HentaiPros
            elif searchSiteID == 917:
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # PornPortal
            elif (918 <= searchSiteID <= 929):
                results = PAsearchSites.network1service.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # AllAnalAllTheTime
            elif searchSiteID == 931:
                results = PAsearchSites.siteAllAnalAllTheTime.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # QueenSnake
            elif searchSiteID == 932:
                results = PAsearchSites.siteQueenSnake.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # QueenSect
            elif searchSiteID == 933:
                results = PAsearchSites.siteQueenSnake.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Fetish Network
            elif (934 <= searchSiteID <= 937):
                results = PAsearchSites.networkKink.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ScrewMeToo
            elif searchSiteID == 938:
                results = PAsearchSites.siteScrewMeToo.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Box Truck Sex
            elif searchSiteID == 939:
                results = PAsearchSites.siteBoxTruckSex.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Aussie Ass
            elif searchSiteID == 940:
                results = PAsearchSites.siteAussieAss.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # 5Kporn
            elif (941 <= searchSiteID <= 942):
                results = PAsearchSites.network5Kporn.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Teen Core Club
            elif (943 <= searchSiteID <= 974):
                results = PAsearchSites.networkTeenCoreClub.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Exploited X
            elif (976 <= searchSiteID <= 978):
                results = PAsearchSites.networkExploitedX.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Desperate Amateurs
            elif (searchSiteID == 979):
                results = PAsearchSites.siteDesperateAmateurs.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Dirty Hard Drive
            elif (980 <= searchSiteID <= 987):
                results = PAsearchSites.networkDirtyHardDrive.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Melone Challenge
            elif (searchSiteID == 988):
                results = PAsearchSites.siteMeloneChallenge.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Holly Randall
            elif searchSiteID == 989:
                results = PAsearchSites.siteHollyRandall.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # In The Crack
            elif searchSiteID == 990:
                results = PAsearchSites.siteInTheCrack.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Angela White
            elif searchSiteID == 991:
                results = PAsearchSites.siteAngelaWhite.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Cumbizz
            elif searchSiteID == 992:
                results = PAsearchSites.siteCumbizz.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Pornstar Platinum
            elif searchSiteID == 993:
                results = PAsearchSites.sitePornstarPlatinum.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Woodman Casting X
            elif searchSiteID == 994:
                results = PAsearchSites.siteWoodmanCastingX.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ScoreGroup
            elif (1012 <= searchSiteID <= 1021):
                results = PAsearchSites.networkScoreGroup.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # TwoTGirls
            elif searchSiteID == 1022:
                results = PAsearchSites.siteTwoTGirls.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Sicflics
            elif searchSiteID == 1023:
                results = PAsearchSites.siteSicflics.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # ModelCentro network
            elif (1024 <= searchSiteID <= 1039) or searchSiteID == 1051:
                results = PAsearchSites.networkModelCentro.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

            # Culioneros
            elif (1040 <= searchSiteID <= 1050):
                results = PAsearchSites.siteCulioneros.search(results, encodedTitle, searchTitle, siteNum, lang, searchDate)

        results.Sort('score', descending=True)

    def update(self, metadata, media, lang):
        movieGenres = PAgenres.PhoenixGenres()
        movieActors = PAactors.PhoenixActors()

        HTTP.ClearCache()
        metadata.genres.clear()
        metadata.roles.clear()

        Log('******UPDATE CALLED*******')

        siteID = int(str(metadata.id).split('|')[1])
        Log(str(siteID))

        # Blacked
        if siteID == 1:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        # Blacked Raw
        elif siteID == 0:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        # Brazzers
        elif siteID == 2 or (siteID >= 54 and siteID <= 81) or siteID == 582 or siteID == 690:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # SexyHub
        elif (siteID >= 333 and siteID <= 339):
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # FakeHub
        elif siteID == 340 or (siteID >= 397 and siteID <= 407):
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # Naughty America
        elif (siteID >= 5 and siteID <= 51) or siteID == 341 or (siteID >= 393 and siteID <= 396) or siteID == 467 or siteID == 468 or siteID == 581 or siteID == 620 or siteID == 625 or siteID == 691 or siteID == 749:
            metadata = PAsearchSites.siteNaughtyAmerica.update(metadata, siteID, movieGenres, movieActors)

        # Vixen
        elif siteID == 52:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        # X-Art
        elif siteID == 82:
            metadata = PAsearchSites.siteXart.update(metadata, siteID, movieGenres, movieActors)

        # Bang Bros
        elif siteID >= 83 and siteID <= 135:
            metadata = PAsearchSites.siteBangBros.update(metadata, siteID, movieGenres, movieActors)

        # Tushy
        elif siteID == 136:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        # Reality Kings
        elif (siteID >= 137 and siteID <= 182) or (siteID >= 822 and siteID <= 828):
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # PornFidelity
        elif siteID >= 184 and siteID <= 186:
            metadata = PAsearchSites.networkPornFidelity.update(metadata, siteID, movieGenres, movieActors)

        # TeamSkeet
        elif (187 <= siteID <= 215) or (566 <= siteID <= 567) or siteID == 626 or siteID == 686 or siteID == 748 or siteID == 807 or (845 <= siteID <= 851) or siteID == 875 or (997 <= siteID <= 1011):
            metadata = PAsearchSites.networkTeamSkeet.update(metadata, siteID, movieGenres, movieActors)

        # Porndoe Premium
        elif siteID >= 216 and siteID <= 259:
            metadata = PAsearchSites.sitePorndoePremium.update(metadata, siteID, movieGenres, movieActors)

        # LegalPorno
        elif siteID == 260:
            metadata = PAsearchSites.siteLegalPorno.update(metadata, siteID, movieGenres, movieActors)

        # Mofos
        elif siteID >= 261 and siteID <= 270 or siteID == 583 or siteID >= 738 and siteID <= 740:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # Babes
        elif siteID >= 271 and siteID <= 276:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # GloryHoleSecrets
        elif siteID == 279:
            metadata = PAsearchSites.siteGloryHoleSecrets.update(metadata, siteID, movieGenres, movieActors)

        # NewSensations
        elif siteID == 280:
            metadata = PAsearchSites.siteNewSensations.update(metadata, siteID, movieGenres, movieActors)

        # Stepped Up Media
        elif siteID == 767 or (siteID >= 282 and siteID <= 284):
            metadata = PAsearchSites.networkSteppedUp.update(metadata, siteID, movieGenres, movieActors)

        # Twistys
        elif siteID >= 288 and siteID <= 291 or siteID == 768:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # Spizoo
        elif siteID == 293 or (siteID >= 571 and siteID <= 577):
            metadata = PAsearchSites.siteSpizoo.update(metadata, siteID, movieGenres, movieActors)

        # Private
        elif siteID >= 294 and siteID <= 305:
            metadata = PAsearchSites.sitePrivate.update(metadata, siteID, movieGenres, movieActors)

        # PornPros Network
        elif (siteID >= 306 and siteID <= 327) or (siteID >= 479 and siteID <= 489) or (siteID == 624) or (siteID == 769) or (siteID == 844) or (siteID == 890):
            metadata = PAsearchSites.networkPornPros.update(metadata, siteID, movieGenres, movieActors)

        # DigitalPlayground
        elif siteID == 328:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # FullPornNetwork
        elif siteID >= 343 and siteID <= 350:
            metadata = PAsearchSites.networkFullPornNetwork.update(metadata, siteID, movieGenres, movieActors)

        # Gamma Entertainment
        elif siteID == 278 or (siteID >= 285 and siteID <= 287) or (siteID >= 329 and siteID <= 330) or (siteID >= 351 and siteID <= 360) or siteID == 382 or siteID == 384 or (siteID >= 386 and siteID <= 392) or siteID == 750 or siteID == 843 or siteID == 861:
            metadata = PAsearchSites.networkGammaEnt.update(metadata, siteID, movieGenres, movieActors)

        # Gamma Entertainment Other
        elif siteID == 53 or siteID == 183 or siteID == 277 or siteID == 281 or (365 <= siteID <= 379) or siteID == 381 or siteID == 383 or siteID == 385 or (460 <= siteID <= 466) or siteID == 692 or siteID == 793 or (795 <= siteID <= 797) or siteID == 878 or siteID == 893 or siteID == 975:
            metadata = PAsearchSites.networkGammaEntOther.update(metadata, siteID, movieGenres, movieActors)

        # MileHighMedia
        elif siteID == 852 or (siteID >= 361 and siteID <= 364) or (914 <= siteID <= 915):
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # Dogfart Network
        elif siteID >= 408 and siteID <= 431:
            metadata = PAsearchSites.networkDogfart.update(metadata, siteID, movieGenres, movieActors)

        # Jules Jordan
        elif siteID == 432 or (siteID >= 522 and siteID <= 524) or siteID == 782:
            metadata = PAsearchSites.siteJulesJordan.update(metadata, siteID, movieGenres, movieActors)

        # DDF Network
        elif (siteID >= 331 and siteID <= 332) or (siteID >= 433 and siteID <= 447):
            metadata = PAsearchSites.networkDDFNetwork.update(metadata, siteID, movieGenres, movieActors)

        # Perfect Gonzo
        elif (448 <= siteID <= 459) or (908 <= siteID <= 911):
            metadata = PAsearchSites.networkPerfectGonzo.update(metadata, siteID, movieGenres, movieActors)

        # BadoinkVR Network
        elif siteID >= 469 and siteID <= 473:
            metadata = PAsearchSites.networkBadoinkVR.update(metadata, siteID, movieGenres, movieActors)

        # VRBangers
        elif siteID == 474:
            metadata = PAsearchSites.siteVRBangers.update(metadata, siteID, movieGenres, movieActors)

        # SexBabesVR
        elif siteID == 475:
            metadata = PAsearchSites.networkHighTechVR.update(metadata, siteID, movieGenres, movieActors)

        # SinsVR
        elif siteID == 569:
            metadata = PAsearchSites.networkHighTechVR.update(metadata, siteID, movieGenres, movieActors)

        # StasyQ VR
        elif siteID == 570:
            metadata = PAsearchSites.networkHighTechVR.update(metadata, siteID, movieGenres, movieActors)

        # WankzVR
        elif siteID == 476:
            metadata = PAsearchSites.siteMilfVR.update(metadata, siteID, movieGenres, movieActors)

        # MilfVR
        elif siteID == 477:
            metadata = PAsearchSites.siteMilfVR.update(metadata, siteID, movieGenres, movieActors)

        # Joymii
        elif siteID == 478:
            metadata = PAsearchSites.siteJoymii.update(metadata, siteID, movieGenres, movieActors)

        # Kink
        elif siteID >= 490 and siteID <= 521 or siteID == 687 or siteID == 735 or siteID == 736 or (873 <= siteID <= 875) or (888 <= siteID <= 889):
            metadata = PAsearchSites.networkKink.update(metadata, siteID, movieGenres, movieActors)

        # Nubiles
        elif (siteID >= 525 and siteID <= 545) or (755 <= siteID <= 756) or (siteID == 766) or (995 <= siteID <= 996):
            metadata = PAsearchSites.networkNubiles.update(metadata, siteID, movieGenres, movieActors)

        # BellaPass
        elif siteID >= 548 and siteID <= 563:
            metadata = PAsearchSites.networkBellaPass.update(metadata, siteID, movieGenres, movieActors)

        # AllureMedia
        elif siteID == 564 or siteID == 565:
            metadata = PAsearchSites.siteAllureMedia.update(metadata, siteID, movieGenres, movieActors)

        # Manyvids
        elif siteID == 568:
            metadata = PAsearchSites.siteManyvids.update(metadata, siteID, movieGenres, movieActors)

        # VirtualTaboo
        elif siteID == 292:
            metadata = PAsearchSites.siteVirtualTaboo.update(metadata, siteID, movieGenres, movieActors)

        # VirtualRealPorn
        elif siteID == 342:
            metadata = PAsearchSites.siteVirtualReal.update(metadata, siteID, movieGenres, movieActors)

        # CzechVR Network
        elif (siteID >= 578 and siteID <= 580):
            metadata = PAsearchSites.networkCzechVR.update(metadata, siteID, movieGenres, movieActors)

        # FinishesTheJob
        elif (siteID >= 584 and siteID <= 586):
            metadata = PAsearchSites.siteFinishesTheJob.update(metadata, siteID, movieGenres, movieActors)

        # Wankz Network
        elif (siteID >= 587 and siteID <= 619):
            metadata = PAsearchSites.networkWankz.update(metadata, siteID, movieGenres, movieActors)

        # Tonights Girlfriend
        elif siteID == 627:
            metadata = PAsearchSites.siteTonightsGirlfriend.update(metadata, siteID, movieGenres, movieActors)

        # Karups
        elif (siteID >= 628 and siteID <= 630):
            metadata = PAsearchSites.siteKarups.update(metadata, siteID, movieGenres, movieActors)

        # TeenMegaWorld
        elif (siteID >= 631 and siteID <= 666) or siteID == 930:
            metadata = PAsearchSites.networkTeenMegaWorld.update(metadata, siteID, movieGenres, movieActors)

        # ScrewBox
        elif siteID == 668:
            metadata = PAsearchSites.siteScrewbox.update(metadata, siteID, movieGenres, movieActors)

        # DorcelClub
        elif siteID == 669:
            metadata = PAsearchSites.siteDorcelClub.update(metadata, siteID, movieGenres, movieActors)

        # TushyRaw
        elif siteID == 670:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        # Deeper
        elif siteID == 671:
            metadata = PAsearchSites.networkStrike3.update(metadata, siteID, movieGenres, movieActors)

        # MissaX / AllHerLuv
        elif siteID == 672 or siteID == 673:
            metadata = PAsearchSites.siteMissaX.update(metadata, siteID, movieGenres, movieActors)

        # Mylf
        elif (siteID >= 674 and siteID <= 683) or siteID == 757 or siteID == 842 or (siteID >= 853 and siteID <= 858) or (881 <= siteID <= 887):
            metadata = PAsearchSites.siteMylf.update(metadata, siteID, movieGenres, movieActors)

        # Manually Add Actors
        elif siteID == 684:
            metadata = PAsearchSites.addActors.update(metadata, siteID, movieGenres, movieActors)

        # First Anal Quest
        elif siteID == 685:
            metadata = PAsearchSites.siteFirstAnalQuest.update(metadata, siteID, movieGenres, movieActors)

        # Hegre
        elif siteID == 688:
            metadata = PAsearchSites.siteHegre.update(metadata, siteID, movieGenres, movieActors)

        # FemdomEmpire
        elif siteID == 689 or siteID == 694:
            metadata = PAsearchSites.networkFemdomEmpire.update(metadata, siteID, movieGenres, movieActors)

        # DorcelVision
        elif siteID == 693:
            metadata = PAsearchSites.siteDorcelVision.update(metadata, siteID, movieGenres, movieActors)

        # XConfessions
        elif siteID == 695:
            metadata = PAsearchSites.siteXConfessions.update(metadata, siteID, movieGenres, movieActors)

        # Czech AV
        elif (siteID >= 696 and siteID <= 728):
            metadata = PAsearchSites.networkCzechAV.update(metadata, siteID, movieGenres, movieActors)

        # ArchAngel
        elif siteID == 729:
            metadata = PAsearchSites.siteArchAngel.update(metadata, siteID, movieGenres, movieActors)

        # We Are Hairy
        elif siteID == 730:
            metadata = PAsearchSites.siteWeAreHairy.update(metadata, siteID, movieGenres, movieActors)

        # Love Her Feet
        elif siteID == 731:
            metadata = PAsearchSites.siteLoveHerFeet.update(metadata, siteID, movieGenres, movieActors)

        # MomPOV
        elif siteID == 732:
            metadata = PAsearchSites.siteMomPOV.update(metadata, siteID, movieGenres, movieActors)

        # Property Sex
        elif siteID == 733:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # FuelVirtual
        elif (546 <= siteID <= 547):
            metadata = PAsearchSites.networkFuelVirtual.update(metadata, siteID, movieGenres, movieActors)

        # TransAngels
        elif siteID == 737:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # Straplezz
        elif siteID == 741:
            metadata = PAsearchSites.siteStraplezz.update(metadata, siteID, movieGenres, movieActors)

        # LittleCaprice
        elif siteID == 742:
            metadata = PAsearchSites.siteLittleCaprice.update(metadata, siteID, movieGenres, movieActors)

        # WowGirls
        elif siteID == 743:
            metadata = PAsearchSites.siteWowGirls.update(metadata, siteID, movieGenres, movieActors)

        # VIPissy
        elif siteID == 744:
            metadata = PAsearchSites.siteVIPissy.update(metadata, siteID, movieGenres, movieActors)

        # GirlsOutWest
        elif siteID == 745:
            metadata = PAsearchSites.siteGirlsOutWest.update(metadata, siteID, movieGenres, movieActors)

        # Girls Rimming
        elif siteID == 746:
            metadata = PAsearchSites.siteGirlsRimming.update(metadata, siteID, movieGenres, movieActors)

        # Gangbang Creampie
        elif siteID == 747:
            metadata = PAsearchSites.siteGangbangCreampie.update(metadata, siteID, movieGenres, movieActors)

        # StepSecrets
        elif siteID == 751:
            metadata = PAsearchSites.siteStepSecrets.update(metadata, siteID, movieGenres, movieActors)

        # VRHush
        elif siteID == 752:
            metadata = PAsearchSites.siteVRHush.update(metadata, siteID, movieGenres, movieActors)

        # MetArt Network
        elif (621 <= siteID <= 623) or (753 <= siteID <= 754) or (816 <= siteID <= 821):
            metadata = PAsearchSites.networkMetArt.update(metadata, siteID, movieGenres, movieActors)

        # Fitting-Room
        elif siteID == 758:
            metadata = PAsearchSites.siteFittingRoom.update(metadata, siteID, movieGenres, movieActors)

        # FamilyHookups
        elif siteID == 759:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # Clips4Sale
        elif siteID == 760:
            metadata = PAsearchSites.siteClips4Sale.update(metadata, siteID, movieGenres, movieActors)

        # VogoV
        elif siteID == 761:
            metadata = PAsearchSites.siteVogoV.update(metadata, siteID, movieGenres, movieActors)

        # Ultrafilms
        elif siteID == 762:
            metadata = PAsearchSites.siteUltrafilms.update(metadata, siteID, movieGenres, movieActors)

        # fuckingawesome.com
        elif siteID == 763:
            metadata = PAsearchSites.siteFuckingAwesome.update(metadata, siteID, movieGenres, movieActors)

        # ToughLoveX
        elif siteID == 764:
            metadata = PAsearchSites.siteToughLoveX.update(metadata, siteID, movieGenres, movieActors)

        # cumlouder.com
        elif siteID == 765:
            metadata = PAsearchSites.siteCumLouder.update(metadata, siteID, movieGenres, movieActors)

        # ztod.com
        elif siteID == 770:
            metadata = PAsearchSites.siteZTOD.update(metadata, siteID, movieGenres, movieActors)

        # ClubFilly
        elif siteID == 771:
            metadata = PAsearchSites.siteClubFilly.update(metadata, siteID, movieGenres, movieActors)

        # Intersec
        elif (siteID >= 772 and siteID <= 781):
            metadata = PAsearchSites.networkIntersec.update(metadata, siteID, movieGenres, movieActors)

        # Cherry Pimps
        elif (siteID >= 783 and siteID <= 792):
            metadata = PAsearchSites.networkCherryPimps.update(metadata, siteID, movieGenres, movieActors)

        # 18OnlyGirls
        elif siteID == 794:
            metadata = PAsearchSites.site18OnlyGirls.update(metadata, siteID, movieGenres, movieActors)

        # Lil Humpers
        elif siteID == 798:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # BellesaFilms
        elif siteID == 799 or siteID == 876:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # ClubSeventeen
        elif siteID == 800:
            metadata = PAsearchSites.siteClubSeventeen.update(metadata, siteID, movieGenres, movieActors)

        # Elegant Angel
        elif siteID == 801:
            metadata = PAsearchSites.siteElegantAngel.update(metadata, siteID, movieGenres, movieActors)

        # Family Sinners
        elif siteID == 802:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # ReidMyLips
        elif siteID == 803:
            metadata = PAsearchSites.siteReidMyLips.update(metadata, siteID, movieGenres, movieActors)

        # Playboy Plus
        elif siteID == 804:
            metadata = PAsearchSites.sitePlayboyPlus.update(metadata, siteID, movieGenres, movieActors)

        # Meana Wolf
        elif siteID == 805:
            metadata = PAsearchSites.siteMeanaWolf.update(metadata, siteID, movieGenres, movieActors)

        # Transsensual
        elif siteID == 806:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # Erito
        elif siteID == 808:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # TrueAmateurs
        elif siteID == 809:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # Hustler
        elif siteID == 810:
            metadata = PAsearchSites.siteHustler.update(metadata, siteID, movieGenres, movieActors)

        # AmourAngels
        elif siteID == 811:
            metadata = PAsearchSites.siteAmourAngels.update(metadata, siteID, movieGenres, movieActors)

        # JAV
        elif siteID == 812:
            metadata = PAsearchSites.networkR18.update(metadata, siteID, movieGenres, movieActors)

        # Bang
        elif siteID == 813:
            metadata = PAsearchSites.networkBang.update(metadata, siteID, movieGenres, movieActors)

        # Vivid
        elif siteID == 814:
            metadata = PAsearchSites.siteVivid.update(metadata, siteID, movieGenres, movieActors)

        # JAY's POV
        elif siteID == 815:
            metadata = PAsearchSites.siteJaysPOV.update(metadata, siteID, movieGenres, movieActors)

        # Girlfriends Films
        elif siteID == 380:
            metadata = PAsearchSites.networkGammaEntOther.update(metadata, siteID, movieGenres, movieActors)

        # PJGirls
        elif siteID == 667:
            metadata = PAsearchSites.sitePJGirls.update(metadata, siteID, movieGenres, movieActors)

        # PureCFNM Network
        elif siteID >= 829 and siteID <= 834:
            metadata = PAsearchSites.networkPureCFNM.update(metadata, siteID, movieGenres, movieActors)

        # BAMVisions
        elif siteID == 835:
            metadata = PAsearchSites.siteBAMVisions.update(metadata, siteID, movieGenres, movieActors)

        # ATK Girlfriends
        elif siteID == 836:
            metadata = PAsearchSites.siteATKGirlfriends.update(metadata, siteID, movieGenres, movieActors)

        # TwoWebMedia
        elif (837 <= siteID <= 839):
            metadata = PAsearchSites.networkTwoWebMedia.update(metadata, siteID, movieGenres, movieActors)

        # Interracial Pass
        elif siteID == 840:
            metadata = PAsearchSites.siteInterracialPass.update(metadata, siteID, movieGenres, movieActors)

        # LookAtHerNow
        elif siteID == 841:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # Deviant Hardcore
        elif siteID == 859:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # She Will Cheat
        elif siteID == 860:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # SinsLife
        elif siteID == 862:
            metadata = PAsearchSites.siteSinsLife.update(metadata, siteID, movieGenres, movieActors)

        # Puffy Network
        elif siteID == 863 or (siteID >= 867 and siteID <= 870):
            metadata = PAsearchSites.networkPuffy.update(metadata, siteID, movieGenres, movieActors)

        # SinX
        elif siteID == 871 or (siteID >= 864 and siteID <= 866):
            metadata = PAsearchSites.networkSinX.update(metadata, siteID, movieGenres, movieActors)

        # Kinky Spa
        elif siteID == 872:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # RealityLovers
        elif siteID == 877:
            metadata = PAsearchSites.siteRealityLovers.update(metadata, siteID, movieGenres, movieActors)

        # RealJamVR
        elif siteID == 879:
            metadata = PAsearchSites.networkHighTechVR.update(metadata, siteID, movieGenres, movieActors)

        # BBC Paradise
        elif siteID == 880:
            metadata = PAsearchSites.siteMylf.update(metadata, siteID, movieGenres, movieActors)

        # HoloGirlsVR
        elif siteID == 891:
            metadata = PAsearchSites.siteHoloGirlsVR.update(metadata, siteID, movieGenres, movieActors)

        # LethalHardcoreVR
        elif siteID == 892:
            metadata = PAsearchSites.siteLethalHardcoreVR.update(metadata, siteID, movieGenres, movieActors)

        # WhoreCraftVR
        elif siteID == 894:
            metadata = PAsearchSites.siteLethalHardcoreVR.update(metadata, siteID, movieGenres, movieActors)

        # Defeated
        elif siteID == 895 or siteID == 896:
            metadata = PAsearchSites.siteDefeated.update(metadata, siteID, movieGenres, movieActors)

        # XVirtual
        elif siteID == 897:
            metadata = PAsearchSites.siteXVirtual.update(metadata, siteID, movieGenres, movieActors)

        # Lust Reality
        elif siteID == 898:
            metadata = PAsearchSites.siteLustReality.update(metadata, siteID, movieGenres, movieActors)

        # Sex Like Real
        elif siteID == 899:
            metadata = PAsearchSites.siteSexLikeReal.update(metadata, siteID, movieGenres, movieActors)

        # DoeGirls
        elif siteID == 900:
            metadata = PAsearchSites.sitePorndoePremium.update(metadata, siteID, movieGenres, movieActors)

        # Xillimite
        elif siteID == 901:
            metadata = PAsearchSites.siteXillimite.update(metadata, siteID, movieGenres, movieActors)

        # VRPFilms
        elif siteID == 902:
            metadata = PAsearchSites.siteVRPFilms.update(metadata, siteID, movieGenres, movieActors)

        # VRLatina
        elif siteID == 903:
            metadata = PAsearchSites.siteVRLatina.update(metadata, siteID, movieGenres, movieActors)

        # VRConk
        elif siteID == 904:
            metadata = PAsearchSites.siteVRConk.update(metadata, siteID, movieGenres, movieActors)

        # RealJamVR
        elif siteID == 905:
            metadata = PAsearchSites.networkHighTechVR.update(metadata, siteID, movieGenres, movieActors)

        # Evolved Fights Network
        elif siteID == 906 or siteID == 907:
            metadata = PAsearchSites.networkEvolvedFights.update(metadata, siteID, movieGenres, movieActors)

        # JavBus
        elif siteID == 912:
            metadata = PAsearchSites.networkJavBus.update(metadata, siteID, movieGenres, movieActors)

        # Hucows
        elif siteID == 913:
            metadata = PAsearchSites.siteHucows.update(metadata, siteID, movieGenres, movieActors)

        # Why Not Bi
        elif siteID == 916:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # HentaiPros
        elif siteID == 917:
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # PornPortal
        elif (918 <= siteID <= 929):
            metadata = PAsearchSites.network1service.update(metadata, siteID, movieGenres, movieActors)

        # AllAnalAllTheTime
        elif siteID == 931:
            metadata = PAsearchSites.siteAllAnalAllTheTime.update(metadata, siteID, movieGenres, movieActors)

        # QueenSnake
        elif siteID == 932:
            metadata = PAsearchSites.siteQueenSnake.update(metadata, siteID, movieGenres, movieActors)

        # QueenSect
        elif siteID == 933:
            metadata = PAsearchSites.siteQueenSnake.update(metadata, siteID, movieGenres, movieActors)

        # Fetish Network
        elif (934 <= siteID <= 937):
            metadata = PAsearchSites.networkKink.update(metadata, siteID, movieGenres, movieActors)

        # ScrewMeToo
        elif siteID == 938:
            metadata = PAsearchSites.siteScrewMeToo.update(metadata, siteID, movieGenres, movieActors)

        # Box Truck Sex
        elif siteID == 939:
            metadata = PAsearchSites.siteBoxTruckSex.update(metadata, siteID, movieGenres, movieActors)

        # AussieAss
        elif siteID == 940:
            metadata = PAsearchSites.siteAussieAss.update(metadata, siteID, movieGenres, movieActors)

        # 5Kporn
        elif (941 <= siteID <= 942):
            metadata = PAsearchSites.network5Kporn.update(metadata, siteID, movieGenres, movieActors)

        # Teen Core Club
        elif (943 <= siteID <= 974):
            metadata = PAsearchSites.networkTeenCoreClub.update(metadata, siteID, movieGenres, movieActors)

        # Exploited X
        elif (976 <= siteID <= 978):
            results = PAsearchSites.networkExploitedX.update(metadata, siteID, movieGenres, movieActors)

        # Desperate Amateurs
        elif (siteID == 979):
            results = PAsearchSites.siteDesperateAmateurs.update(metadata, siteID, movieGenres, movieActors)

        # Dirty Hard Drive
        elif (980 <= siteID <= 987):
            results = PAsearchSites.networkDirtyHardDrive.update(metadata, siteID, movieGenres, movieActors)

        # Melone Challenge
        elif (siteID == 988):
            results = PAsearchSites.siteMeloneChallenge.update(metadata, siteID, movieGenres, movieActors)

        # Holly Randall
        elif siteID == 989:
            results = PAsearchSites.siteHollyRandall.update(metadata, siteID, movieGenres, movieActors)

        # In The Crack
        elif siteID == 990:
            results = PAsearchSites.siteInTheCrack.update(metadata, siteID, movieGenres, movieActors)

        # Angela White
        elif siteID == 991:
            results = PAsearchSites.siteAngelaWhite.update(metadata, siteID, movieGenres, movieActors)

        # Cumbizz
        elif siteID == 992:
            results = PAsearchSites.siteCumbizz.update(metadata, siteID, movieGenres, movieActors)

        # Pornstar Platinum
        elif siteID == 993:
            results = PAsearchSites.sitePornstarPlatinum.update(metadata, siteID, movieGenres, movieActors)

        # Woodman Casting X
        elif siteID == 994:
            results = PAsearchSites.siteWoodmanCastingX.update(metadata, siteID, movieGenres, movieActors)

        # ScoreGroup
        elif (1012 <= siteID <= 1021):
            results = PAsearchSites.networkScoreGroup.update(metadata, siteID, movieGenres, movieActors)

        # TwoTGirls
        elif siteID == 1022:
            results = PAsearchSites.siteTwoTGirls.update(metadata, siteID, movieGenres, movieActors)

        # Sicflics
        elif siteID == 1023:
            results = PAsearchSites.siteSicflics.update(metadata, siteID, movieGenres, movieActors)

        # ModelCentro network
        elif (1024 <= siteID <= 1039) or siteID == 1051:
            results = PAsearchSites.networkModelCentro.update(metadata, siteID, movieGenres, movieActors)

        # Culioneros
        elif (1040 <= siteID <= 1050):
            results = PAsearchSites.siteCulioneros.update(metadata, siteID, movieGenres, movieActors)

        # Cleanup Genres and Add
        Log("Genres")
        movieGenres.processGenres(metadata)
        metadata.genres = sorted(metadata.genres)

        # Cleanup Actors and Add
        Log("Actors")
        movieActors.processActors(metadata)

        # Add Content Rating
        metadata.content_rating = 'XXX'
