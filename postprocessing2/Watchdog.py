## Dependencies
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
import os
import re
import time
import logging
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# import pymediainfo
# import ffmpeg
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
import searcher_networkbadoinkvr
## Functions
import LoggerFunction
import RenamerFunction

## The GUI + Watcher class code
class MyGui:
    def __init__(self):
        def get_pref_DIRECTORY_TO_WATCH():
            folder_selected = filedialog.askdirectory()
            DIR_W_Path.set(folder_selected)

        def get_pref_DIRECTORY_TO_MOVE():
            folder_selected = filedialog.askdirectory()
            DIR_M_Path.set(folder_selected)

        def get_pref_DIRECTORY_UNMATCHED():
            folder_selected = filedialog.askdirectory()
            DIR_U_Path.set(folder_selected)

        def pref_set():
            global DIRECTORY_UNMATCHED
            DIRECTORY_UNMATCHED = DIR_U_Path.get().replace("/","\\")
            global DIRECTORY_TO_MOVE
            DIRECTORY_TO_MOVE = DIR_M_Path.get().replace("/","\\")
            global DIRECTORY_TO_WATCH
            DIRECTORY_TO_WATCH = DIR_W_Path.get().replace("/","\\")
            global pref_ID
            pref_ID = UI_pref_ID.get()
            global pref_DryRun
            pref_DryRun = UI_pref_DryRun.get()
            global pref_StripSymbol
            pref_StripSymbol = UI_pref_StripSymbol.get()
            if ((DIRECTORY_TO_WATCH != "") and (DIRECTORY_TO_MOVE != "") and (DIRECTORY_UNMATCHED != "") and (os.path.exists(DIRECTORY_TO_WATCH)) and (os.path.exists(DIRECTORY_TO_MOVE)) and (os.path.exists(DIRECTORY_UNMATCHED))):
                self.but.config(state="normal",text="Start Watchdog")
            else:
                self.but.config(state="disabled",text="Set Preferences First") 

        root.title('Porndog - Adult Scene Renamer')
        root.iconbitmap('.\\icon.ico')
        root.geometry("500x500")

        Watchdog_Preferences_Label = Label(root ,text="Watchdog Preferences - Directories")
        Watchdog_Preferences_Label.place(x = 192,y = 5)

        DIR_W_Path = tk.StringVar()
        DIR_W_Label = Label(root ,text="Active Directory - ")
        DIR_W_Label.place(x = 80,y = 28)
        self.DIR_W_TextField = Entry(root,textvariable=DIR_W_Path,width=35)
        self.DIR_W_TextField.place(x = 180,y = 30)
        self.DIR_W_Button = ttk.Button(root, text="Browse Folder",command=get_pref_DIRECTORY_TO_WATCH)
        self.DIR_W_Button.place(x = 400,y = 28)

        DIR_M_Path = tk.StringVar()
        DIR_M_Label = Label(root ,text="Move Directory - ")
        DIR_M_Label.place(x = 82,y = 58)
        self.DIR_M_TextField = Entry(root,textvariable=DIR_M_Path,width=35)
        self.DIR_M_TextField.place(x = 180,y = 60)
        self.DIR_M_Button = ttk.Button(root, text="Browse Folder",command=get_pref_DIRECTORY_TO_MOVE)
        self.DIR_M_Button.place(x = 400,y = 58)

        DIR_U_Path = tk.StringVar()
        DIR_U_Label = Label(root ,text="Unmatched Directory - ")
        DIR_U_Label.place(x = 50,y = 88)
        self.DIR_U_TextField = Entry(root,textvariable=DIR_U_Path,width=35)
        self.DIR_U_TextField.place(x = 180,y = 90)
        self.DIR_U_Button = ttk.Button(root, text="Browse Folder",command=get_pref_DIRECTORY_UNMATCHED)
        self.DIR_U_Button.place(x = 400,y = 88)

        UI_FilenamePref_Label = Label(root ,text="Filename Preferences")
        UI_FilenamePref_Label.place(x = 225,y = 120)

        UI_pref_ID = BooleanVar()
        self.UI_Checkbutton_ID = Checkbutton(root, text="Prefer Scene ID over Scene Title", variable=UI_pref_ID)
        self.UI_Checkbutton_ID.place(x = 185,y = 150)

        UI_pref_StripSymbol = tk.StringVar()
        UI_pref_StripSymbol_Label = Label(root ,text="Strip Symbol - ")
        UI_pref_StripSymbol_Label.place(x = 95,y = 180)
        self.UI_pref_StripSymbol_TextField = Entry(root,textvariable=UI_pref_StripSymbol,width=35)
        self.UI_pref_StripSymbol_TextField.place(x = 180,y = 180)

        UI_OtherPref_Label = Label(root ,text="Other Preferences")
        UI_OtherPref_Label.place(x = 228,y = 210)

        UI_pref_DryRun = BooleanVar()
        self.UI_Checkbutton_DryRun = Checkbutton(root, text="Dry Run", variable=UI_pref_DryRun)
        self.UI_Checkbutton_DryRun.place(x = 240,y = 240)

        self.SET_BUTTON = tk.Button(root,text="Set Preferences",command=pref_set)
        self.SET_BUTTON.place(x = 230,y = 270)
        self.but = tk.Button(root,text="Start Watchdog",command=self.start_observer)
        self.but.place(x = 230,y = 300)  
        self.but.config(state="disabled",text="Set Preferences First") 

        self.but2 = tk.Button(root,text="Stop Watchdog",command=self.stop_observer)
        self.but2.place(x = 230,y = 330)  
        self.but2.config(state="disabled",text="Stop Watchdog")     

    def start_observer(self):
        loggerwatchdog.info("******************** Pre-initialization ********************")
        loggerwatchdog.info("Watchdog will be active to this directory: "+DIRECTORY_TO_WATCH)
        loggerwatchdog.info("Watchdog will move the files to this directory: " +DIRECTORY_TO_MOVE)
        loggerwatchdog.info("Watchdog will move unmatched files to this directory: " +DIRECTORY_UNMATCHED)
        loggerwatchdog.info("Preferred ID is set to: " +str(pref_ID))
        loggerwatchdog.info("Dry Run is set to: " +str(pref_DryRun))
        if (pref_StripSymbol != ""):
            loggerwatchdog.info("Your strip symbol is: " +(pref_StripSymbol))
        else:
            loggerwatchdog.info("You haven't set a Strip Symbol.")
        loggerwatchdog.info("******************** Pre-initialization ********************")
        self.DIR_W_TextField.config(state="disabled")
        self.DIR_W_Button.config(state="disabled")

        self.DIR_M_TextField.config(state="disabled")
        self.DIR_M_Button.config(state="disabled")

        self.DIR_U_TextField.config(state="disabled")
        self.DIR_U_Button.config(state="disabled")

        self.UI_Checkbutton_ID.config(state="disabled")
        self.UI_pref_StripSymbol_TextField.config(state="disabled")
        self.UI_Checkbutton_DryRun.config(state="disabled")
        
        self.SET_BUTTON.config(state="disabled")
        self.but.config(state="disabled",text="Watchdog Initiated")
        self.but2.config(state="normal",text="Stop Watchdog")

        self.observer = Observer()
        self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        loggerwatchdog.info("******************** Watchdog initiated ********************")

    def stop_observer(self):
        self.observer.stop()
        self.observer.join()
        self.observer = None
        self.DIR_W_TextField.config(state="normal")
        self.DIR_W_Button.config(state="normal")

        self.DIR_M_TextField.config(state="normal")
        self.DIR_M_Button.config(state="normal")

        self.DIR_U_TextField.config(state="normal")
        self.DIR_U_Button.config(state="normal")

        self.UI_Checkbutton_ID.config(state="normal")
        self.UI_pref_StripSymbol_TextField.config(state="normal")
        self.UI_Checkbutton_DryRun.config(state="normal")

        self.SET_BUTTON.config(state="normal")
        self.but.config(state="disabled",text="Set Preferences First")  
        self.but2.config(state="disabled",text="Stop Watchdog") 

## The handler class code
class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if not event.is_directory:
            file_path = None

            if ((event.event_type == 'created') or (event.event_type == 'modified')):
                file_path = event.src_path
            elif (event.event_type == 'moved'):
                file_path = event.dest_path
            elif (event.event_type == 'deleted'):
                loggerwatchdog.info ("Received deleted event: %s" % event.src_path)
            if (file_path != None):
                new_filename = None
                if os.path.exists(file_path):
                    siteDirectory = os.path.dirname(file_path)
                    siteFolder = os.path.basename(siteDirectory)
                    complete_filename = os.path.basename(file_path)
                    filename_title = os.path.splitext(complete_filename)[0]
                    filename_type = os.path.splitext(complete_filename)[1]
                    filename_size = os.stat(file_path).st_size
                    if ((filename_type in ('.mp4','.mkv','.avi','.wmv')) and (filename_size > 15000000)):
                        loggerwatchdog.info ("Processing filename %s which is a type of %s" % (filename_title, filename_type))
                        loggerwatchdog.info("The file was placed at folder: " +siteFolder)
                        trashTitle = ('RARBG', 'COM', '\d{3,4}x\d{3,4}', 'HEVC', 'H265', 'AVC', '\dK', '\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4', 'KLEENEX', 'SD','mp4_1080','mp4_720','mp4_480','mp4_360','mp4_1080_18','mp4_720_18','mp4_480_18','mp4_360_18','180_180x180_3dh_LR')
                        filename_title = re.sub(r'\W', ' ', filename_title)
                        for trash in trashTitle:
                            filename_title = re.sub(r'\b%s\b' % trash, '', filename_title, flags=re.IGNORECASE)
                        filename_title = ' '.join(filename_title.split())
                        loggerwatchdog.info ("Filename after initial process: " +filename_title)
                        loggerwatchdog.info ("************ Process with PAsearchSites follows ************")
                        searchSettings = PAsearchSites.getSearchSettings(filename_title)
                        searchTitle = searchSettings[1]
                        searchDate = searchSettings[2]
                        loggerwatchdog.info ("Filename (after date processing): " +searchTitle)
                        if (searchDate != None):
                            loggerwatchdog.info ("Date Found embedded at the filename: " +searchDate)
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
                            ########################################## All sites that are under the BaDoinkVR - Start ##########################################
                            ## BaDoinkVR
                            elif ((siteID == 469)):
                                ResultsMatrix = searcher_networkbadoinkvr.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                                new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                            ## BabeVR
                            elif ((siteID == 470)):
                                ResultsMatrix = searcher_networkbadoinkvr.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                                new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                            ## 18VR
                            elif ((siteID == 471)):
                                ResultsMatrix = searcher_networkbadoinkvr.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                                new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                            ## KinkVR
                            elif ((siteID == 472)):
                                ResultsMatrix = searcher_networkbadoinkvr.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                                new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                            ## VRCosplayX
                            elif ((siteID == 473)):
                                ResultsMatrix = searcher_networkbadoinkvr.search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate)
                                new_filename = RenamerFunction.renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol)
                            ########################################## All sites that are under the BaDoinkVR - End #############################################
                            if (pref_DryRun == False):
                                if (new_filename != None):
                                    if (os.path.exists(DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\')):
                                        loggerwatchdog.info("The site sub-folder was detected to %s location. Try to move %s there" % (DIRECTORY_TO_MOVE,new_filename))
                                        try:
                                            os.rename(file_path,r''+DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\'+new_filename)
                                        except OSError:
                                            loggerwatchdog.info ("There was an error moving %s file to %s location" % (new_filename,DIRECTORY_TO_MOVE))
                                        else:
                                            loggerwatchdog.info ("Successfully moved %s to %s location" % (new_filename,DIRECTORY_TO_MOVE))
                                    else:
                                        loggerwatchdog.info("Couldn't detect site sub-folder to %s location. Try to create site's sub-folder and move the %s file there" % (DIRECTORY_TO_MOVE,new_filename))
                                        try:
                                            os.mkdir(DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\')
                                            os.rename(file_path,r''+DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\'+new_filename)
                                        except OSError:
                                            loggerwatchdog.info ("There was an error moving %s file to %s location" % (new_filename,DIRECTORY_TO_MOVE))
                                        else:
                                            loggerwatchdog.info ("Successfully created %s directory and move %s file there" % (DIRECTORY_TO_MOVE,new_filename))
                                else:
                                    os.rename(file_path,r''+DIRECTORY_UNMATCHED+'\\'+complete_filename)
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
                                os.rename(file_path,r''+DIRECTORY_UNMATCHED+'\\'+complete_filename)
                                loggerwatchdog.info("Scene was moved to the Unmatched folder")
                            else:
                                loggerwatchdog.info("Dry run is enabled!!!")
                                loggerwatchdog.info("Scene should have moved to Unmatched folder")
                                loggerwatchdog.info("Disable Dry Run to do so") 
                    else:
                        pass
        else:
            pass

if __name__ == '__main__':
    ## Basic Logger information
    # WorkingDir = os.path.dirname(os.path.abspath(__file__))
    loggerwatchdog = LoggerFunction.setup_logger('Watchdog','.\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    root = tk.Tk()
    event_handler = Handler()
    gui = MyGui()
    root.mainloop()