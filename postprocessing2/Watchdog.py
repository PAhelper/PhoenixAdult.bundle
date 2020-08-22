## Dependencies
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import re
import time
import logging
## Phoenix adult agent files
import PAsearchSites
## Other .py files
## Searchers
import searcher_network1service
import searcher_sitebangbros
import searcher_networkpornpros
import searcher_networkmilfvr
import searcher_networkkink
import searcher_sitenaughtyamerica
## Functions
import LoggerFunction
import RenamerFunction

###################################################################### PREFERENCES ##################################################################################################
## Replace the following directories with yours. Use double \\
DIRECTORY_TO_WATCH = ""
DIRECTORY_TO_MOVE = ""
DIRECTORY_UNMATCHED = ""
## You prefer ID to your filename (True) or scene title (False).
pref_ID = False
## Change to (True) if you don't want the Watcher to actually move and rename the files (check matching result).
pref_DryRun = True
## Here you can set your strip symbol. After that symbol the rest part of the media title will be ignored by PhoenixAdult agent.
pref_StripSymbol = ""
## CAUTION! To be ignored you must have setup your Plex Library in the correct way. Below are some directions if you don't know how to set it up properly.
## You can set it during Plex library creation. Create Library, give a name, select your folder where your media is and at Advanced Tab, you need to choose the following settings.
## Choose PhoenixAdult as the agent.
## Choose Plex Video Files Scanner as the scanner.
## At the end you will find Enable Filename strip and Strip Symbol. Check the box and put your preffered symbol.
## If you have already created your library go to Your Library->Three Dots->Manage Library->Edit...->Advanced->Enable Filename strip checked, and put your preffered symbol.
## If you don't want to use a Strip Symbol just leave it empty like so "".
## Note: If you don't use a strip symbol the Watchdog will write 'minimal' information to your filename just to work with PhoenixAdult. Below are some examples.
## For example: If you have pref_ID = True and pref_StripSymbol = "" then the file will be siteName - sceneID - Date (if provided).
## For example: If you have pref_ID = True and pref_StripSymbol = "~" then the file will be siteName - sceneID - Date ~ Actors - Subsite (if provided).
## For example: If you have pref_ID = False and pref_StripSymbol = "" then the file will be siteName - Title - Date (if provided).
## For example: If you have pref_ID = False and pref_StripSymbol = "~" then the file will be siteName - Title - Date ~ Actors - Subsite (if provided).
###################################################################### PREFERENCES ##################################################################################################
## Basic Logger information
loggerwatchdog = LoggerFunction.setup_logger('Watchdog','.\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
################################################################## PRE-INITIALIZATION ###############################################################################################
## Start messages
loggerwatchdog.info("******************** Pre-initialization ********************")

## This checks if the directories you have entered are valid. If not it will create them
for directory in (DIRECTORY_TO_WATCH,DIRECTORY_TO_MOVE,DIRECTORY_UNMATCHED):
    if os.path.exists(directory):
        loggerwatchdog.info("Directory exists. Don't need to create: " +directory)
        pass
    else:
        loggerwatchdog.info("Directory doesn't exist. Will try to create: " +directory)
        try:
            os.mkdir(directory)
        except OSError:
            loggerwatchdog.info ("Error creating directory: " +directory) 
        else:
            loggerwatchdog.info ("Directory created successfully: " +directory)

loggerwatchdog.info("Watchdog will be active to this directory: "+DIRECTORY_TO_WATCH)
loggerwatchdog.info("Watchdog will move the files to this directory: " +DIRECTORY_TO_MOVE)
loggerwatchdog.info("Preferred ID is set to: " +str(pref_ID))
loggerwatchdog.info("Dry Run is set to: " +str(pref_DryRun))
if (pref_StripSymbol != ""):
    loggerwatchdog.info("Your strip symbol is: " +(pref_StripSymbol))
else:
    loggerwatchdog.info("You haven't set a Strip Symbol.")
loggerwatchdog.info("******************** Watchdog initiated ********************")
################################################################## PRE-INITIALIZATION ##############################################################################################

## The watcher class code
class Watcher:

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            loggerwatchdog.info ("Watchdog disabled")

        self.observer.join()

## The handler class code
class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            ## Take any action here when a file is first created.
            loggerwatchdog.info ("Received created event : %s" % event.src_path)

        ##elif ((event.event_type == 'created') or event.event_type == 'modified'):
        elif event.event_type == 'modified':
            ## Taken any action here when a file is modified.
            loggerwatchdog.info ("Received modified event: %s" % event.src_path)
            new_filename = None
            if os.path.exists(event.src_path):
                siteDirectory = os.path.dirname(event.src_path)
                siteFolder = os.path.basename(siteDirectory)
                complete_filename = os.path.basename(event.src_path)
                filename_title = os.path.splitext(complete_filename)[0]
                filename_type = os.path.splitext(complete_filename)[1]
                filename_size = os.stat(event.src_path).st_size
                if ((filename_type in ('.mp4','.mkv','.avi')) and (filename_size > 15000000)):
                    loggerwatchdog.info ("Processing filename %s which is a type of %s" % (filename_title, filename_type))
                    loggerwatchdog.info("The file was placed at folder: " +siteFolder)
                    trashTitle = ('RARBG', 'COM', '\d{3,4}x\d{3,4}', 'HEVC', 'H265', 'AVC', '\dK', '\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4', 'KLEENEX', 'SD', '1080p', '720p', '480p', '360p','mp4_1080','mp4_720','mp4_480','mp4_360','mp4_1080_18','mp4_720_18','mp4_480_18','mp4_360_18','180_180x180_3dh_LR')
                    filename_title = re.sub(r'\W', ' ', filename_title)
                    for trash in trashTitle:
                        filename_title = re.sub(r'\b%s\b' % trash, '', filename_title, flags=re.IGNORECASE)
                    filename_title = ' '.join(filename_title.split())
                    loggerwatchdog.info ("Filename after initial process: " +filename_title)
                    loggerwatchdog.info ("************ Process with PAsearchSites follows ************")
                    searchSettings = PAsearchSites.getSearchSettings(filename_title)
                    searchTitle = searchSettings[1]
                    searchDate = searchSettings[2]
                    loggerwatchdog.info ("searchTitle (after date processing): " +searchTitle)
                    if (searchDate != None):
                        loggerwatchdog.info ("searchDate Found: " +searchDate)
                    else:
                        loggerwatchdog.info ("File didn't contain Date information. If this is false check the RegEx at PASearchSites for Dates")
                    loggerwatchdog.info ("****************** PAsearchSites matching ******************")
                    loggerwatchdog.info("Use PAsearchSites to match %s folder with a supported PA Site ID" %siteFolder)
                    siteID = None
                    siteID = PAsearchSites.getSearchSiteIDByFilter(siteFolder)
                    if (siteID != None):
                        siteName = PAsearchSites.getSearchSiteName(siteID)
                        siteBaseURL = PAsearchSites.getSearchBaseURL(siteID)
                        siteSearchURL = PAsearchSites.getSearchSearchURL(siteID)
                        loggerwatchdog.info("PA Site ID: %d" %siteID)
                        loggerwatchdog.info("PA Site Name: %s" %siteName)
                        loggerwatchdog.info("PA Site Base URL: %s" %siteBaseURL)
                        loggerwatchdog.info("PA Site Search URL: %s" %siteSearchURL)
                        ######################################### All sites that are under the network1service - Start #########################################
                        ## Brazzers + Subsites
                        if ((siteID == 2) or (54 <= siteID <= 80) or (siteID == 582) or (siteID == 690)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## RealityKings + Subsites
                        elif ((137 <= siteID <= 182) or (822 <= siteID <= 828)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)   
                        ## Mofos + Subsites                    
                        elif ((261 <= siteID <= 270) or (siteID == 583) or (738 <= siteID <= 740)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol) 
                        ## Babes + Subsites                       
                        elif ((271 <= siteID <= 276)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Twistys + Subsites
                        elif ((288 <= siteID <= 291) or (siteID == 768)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## DigitalPlayground
                        elif ((siteID == 328)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## SexyHub + Subsites
                        elif ((333 <= siteID <= 339)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## FakeHub + Subsites
                        elif ((siteID == 340) or (397 <= siteID <= 407)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## MileHighMedia
                        elif ((361 <= siteID <= 364)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## PropertySex
                        elif ((siteID == 733)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## TransAngels
                        elif ((siteID == 737)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## FamilyHookUps
                        elif ((siteID == 759)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## LilHumpers
                        elif ((siteID == 798)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## BelessaFilms
                        elif ((siteID == 799) or (siteID == 876)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## FamilySinners
                        elif ((siteID == 802)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Transsensual
                        elif ((siteID == 806)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Erito
                        elif ((siteID == 808)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## TrueAmateurs
                        elif ((siteID == 809)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## LookAtHerNow
                        elif ((siteID == 841)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## BiEmpire
                        elif ((siteID == 852)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## DeviantHardcore
                        elif ((siteID == 859)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## SheWillCheat
                        elif ((siteID == 860)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## KinkySpa
                        elif ((siteID == 872)):
                            ResultsMatrix = searcher_network1service.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ########################################## All sites that are under the network1service - End #####################################
                        ########################################## All sites that are under the Bangbros - Start ##########################################
                        ## Bangbros + Subsites
                        elif ((83 <= siteID <= 135)):
                            ResultsMatrix = searcher_sitebangbros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ########################################## All sites that are under the Bangbros - End ############################################
                        ########################################## All sites that are under the Pornpros - Start ##########################################
                        ## PassionHD
                        elif ((siteID == 306)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## FantasyHD
                        elif ((siteID == 307)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Pornpros + Subsites
                        elif ((308 <= siteID <= 327)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## POVD
                        elif ((siteID == 479)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Cum4K
                        elif ((siteID == 480)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Exotic4K
                        elif ((siteID == 481)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Tiny4K
                        elif ((siteID == 482)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Lubed
                        elif ((siteID == 483)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## PureMature
                        elif ((siteID == 484)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## NannySpy
                        elif ((siteID == 485)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Holed
                        elif ((siteID == 486)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## CastingCouchX
                        elif ((siteID == 487)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## SpyFam
                        elif ((siteID == 488)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## MyVeryFirstTime
                        elif ((siteID == 489)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## Baeb
                        elif ((siteID == 624)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## GirlCum
                        elif ((siteID == 769)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## BBCPie
                        elif ((siteID == 844)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## WetVR
                        elif ((siteID == 890)):
                            ResultsMatrix = searcher_networkpornpros.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ########################################## All sites that are under the Pornpros - End ############################################
                        ########################################## All sites that are under the MilfVR - Start ############################################
                        ## WankzVR
                        elif ((siteID == 476)):
                            ResultsMatrix = searcher_networkmilfvr.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ## MilfVR
                        elif ((siteID == 477)):
                            ResultsMatrix = searcher_networkmilfvr.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ########################################## All sites that are under the MilfVR - End ##############################################
                        ########################################## All sites that are under the Kink - Start ##############################################
                        ## Kink + Subsites
                        elif ((490 <= siteID <= 521) or (siteID == 687) or (735 <= siteID <= 736) or (873 <= siteID <= 874) or (888 <= siteID <= 889)):
                            ResultsMatrix = searcher_networkkink.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ########################################## All sites that are under the Kink - End #################################################
                        ########################################## All sites that are under the NaughtyAmerica - Start #####################################
                        ## NaughtyAmerica + Subsites
                        elif ((5 <= siteID <= 51) or (siteID == 341) or (393 <= siteID <= 396) or (467 <= siteID <= 468) or (siteID == 581) or (siteID == 620) or (siteID == 625) or (siteID == 691) or (siteID == 749)):
                            ResultsMatrix = searcher_sitenaughtyamerica.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                            new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                        ########################################## All sites that are under the NaughtyAmerica - End #######################################
                        if (pref_DryRun == False):
                            if (new_filename != None):
                                if (os.path.exists(DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\')):
                                    loggerwatchdog.info("The site sub-folder was detected to %s location. Try to move %s there" % (DIRECTORY_TO_MOVE,new_filename))
                                    try:
                                        os.rename(event.src_path,r''+DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\'+new_filename)
                                    except OSError:
                                        loggerwatchdog.info ("There was an error moving %s file to %s location" % (new_filename,DIRECTORY_TO_MOVE))
                                    else:
                                        loggerwatchdog.info ("Successfully moved %s to %s location" % (new_filename,DIRECTORY_TO_MOVE))
                                else:
                                    loggerwatchdog.info("Couldn't detect site sub-folder to %s location. Try to create site's sub-folder and move the %s file there" % (DIRECTORY_TO_MOVE,new_filename))
                                    try:
                                        os.mkdir(DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\')
                                        os.rename(event.src_path,r''+DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\'+new_filename)
                                    except OSError:
                                        loggerwatchdog.info ("There was an error moving %s file to %s location" % (new_filename,DIRECTORY_TO_MOVE))
                                    else:
                                        loggerwatchdog.info ("Successfully created %s directory and move %s file there" % (DIRECTORY_TO_MOVE,new_filename))
                            else:
                                os.rename(event.src_path,r''+DIRECTORY_UNMATCHED+'\\'+complete_filename)
                                loggerwatchdog.info("Couldn't match scene. Moved to the Unmatched folder")
                        else:
                            loggerwatchdog.info("Dry run is enabled!!!")
                            if (new_filename != None):
                                loggerwatchdog.info("Your scene was matched and could be renamed to: " +new_filename)
                                loggerwatchdog.info("Disable dry run to do so")
                            else:
                                loggerwatchdog.info("Couldn't match scene. Scene should have moved to Unmatched folder")
                                loggerwatchdog.info("Disable Dry Run to do so") 
                    else:
                        loggerwatchdog.info("Couldn't found %s site to the PAsearchSites array" %siteFolder)
                        if (pref_DryRun == False):
                            os.rename(event.src_path,r''+DIRECTORY_UNMATCHED+'\\'+complete_filename)
                            loggerwatchdog.info("Scene was moved to the Unmatched folder")
                        else:
                            loggerwatchdog.info("Dry run is enabled!!!")
                            loggerwatchdog.info("Scene should have moved to Unmatched folder")
                            loggerwatchdog.info("Disable Dry Run to do so") 
                else:
                    pass
        elif event.event_type == 'deleted':
            ## Taken any action here when a file is deleted.
            loggerwatchdog.info ("Received deleted event: %s" % event.src_path)

if __name__ == '__main__':
    w = Watcher()
    w.run()