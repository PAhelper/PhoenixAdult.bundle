#!/usr/local/sabnzbd/env/bin/python
# !/usr/bin/env python

# point sabnzbd to this file for automated postprocessing
# configure and customise siteOverrides.py
# install lxml if required -> pip install lxml

#Media Info is a beta option and will require you to install two things.
# install pymedia info -> pip install pymediainfo
# https://mediaarea.net/en/MediaInfo the MediaInfo.DLL file for your system (NOTE: I did find this must have already been installed on my system and was not nedded)

import sys
import os, glob, shutil
import logging
import argparse
import string
from patools import pa_parse_dir
import siteOverrides

def main():
    dryrun=False
    batch=False
    cleanup=False
    mediainfo=False
    mediainfo2=False
    if "SAB_VERSION" in os.environ:
        (scriptname,dir,orgnzbname,jobname,reportnumber,category,group,postprocstatus,url) = sys.argv
        # set to True/False to enable/Disable when using sabnzbd
        cleanup=False
        mediainfo=False
        mediainfo2=False
    else:
        parser = argparse.ArgumentParser(description='Rename adult media downloads for import into Plex with the PhoenixAdult metadat agent')
        parser.add_argument("directory")
        parser.add_argument("-d", "--dryrun", help="don't do work, just show what will happen", action="store_true")
        parser.add_argument("-b", "--batch", help="Do not try to log as batch job will fail", action="store_true")
        parser.add_argument("-c", "--cleanup", help="Delete leftover files and cleanup folders after rename", action="store_true")
        parser.add_argument("-m", "--mediainfo", help="Add media info to the folder. Resolution and framerate", action="store_true")
        parser.add_argument("-m2", "--mediainfo2", help="Add media info to the filename. Resolution and framerate", action="store_true")
        args = parser.parse_args()
        if args.dryrun:
            print "Dry-run mode enabled."
            dryrun=True
        if args.batch:
            print "Batch mode enabled. Logging partially disabled!"
            batch=True
        if args.cleanup:
            print "Cleanup Enabled!"
            cleanup=True
        if args.mediainfo:
            print "Folder MediaInfo enabled."
            mediainfo=True
        if args.mediainfo2:
            print "File MediaInfo enabled."
            mediainfo2=True
        dir = args.directory

    debug=False

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger('pa_renamer')
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    if not dryrun and not batch:
        hdlr = logging.FileHandler('C:\Program Files\SABnzbd\scripts\pa_post.log')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

    logger.info("Starting to process: %s" % dir)

    shoot = pa_parse_dir(dir)
    logger.debug("Full shoot dict:")
    logger.debug(shoot)
    # shoot = {
    #     'studio': "DigitalPlayground",
    #     'date': "2018-12-12",
    #     'filename_title': 'Elsa.Jean.And.Romi.Rain.The.Secret.Life.Of.A.Housewife'
    # }

    if shoot is not None:
        # filename should be: "Studio - Model Names.mp4" or "Studio - Title Words.mp4"
        # TODO: figure out if we should use titles or models
        
        # Capitalise the title (first letter of every word). Keep original studio in case we swap it out later.
        filename_new = shoot['studio'] + ' - ' + string.capwords(shoot['filename_title'] + ' (' + shoot['date'] + ').mp4')
        logger.debug(" Before overrides the name is : %s" % filename_new)
        
        #check if any overrides are set in siteOverrides.py
        overrideSettings = siteOverrides.getSiteMatch(shoot['studio'], dir)
        correctName = siteOverrides.getRename(shoot['studio'], "filleractor", shoot['filename_title'], shoot['date'])

        for item in os.listdir(dir):
            fullfilepath = os.path.join(dir, item)
            filetype = item.split('.')[-1]
            logger.debug(" The filetype is: %s" % filetype)
            #if the file is over 50MB rename it
            if os.path.getsize(fullfilepath) > 50000000:
                if overrideSettings != 9999:
                    filename_new = filename_new.replace(shoot['studio'], overrideSettings[0])
                    dir_new = dir.split(overrideSettings[1])[0] + overrideSettings[2]
                else:
                    dir_new = dir
                if correctName != 9999:
                    filename_new = filename_new.replace(string.capwords(shoot['filename_title']), string.capwords(correctName))
                    
                #Add Media Info
                if mediainfo or mediainfo2:
                    logger.debug(" Atempting to gather Media Info")
                    media_Info = siteOverrides.getMediaInfo(fullfilepath)
                    if media_Info != 9999:
                        if mediainfo:
                            dir_new = dir_new + " " + media_Info
                        if mediainfo2:
                            filename_new = filename_new.replace(" (", " (" + media_Info + ") (")
                logger.debug(" After:")
                logger.debug("    New directory: %s" % dir_new)
                logger.debug("    New file name: %s" % filename_new)
                if filetype in ["mp4", "avi", "mkv"]:
                    newpath = os.path.join(dir_new, filename_new.replace(".mp4", '.' + filetype))
                    if dryrun:
                        logger.info("[DRYRUN] Renaming: %s -> %s" % (fullfilepath, newpath))
                    else:
                        try:
                            os.makedirs(dir_new)
                        except:
                            pass
                        logger.info(" Renaming/Moving from: %s --> %s" % (fullfilepath, newpath))
                        os.rename(fullfilepath, newpath)
                        os.chmod(newpath, 0775)
            if cleanup and not dryrun:
                if filetype in ["txt", "jpg", "jpeg", "nfo", "sfv", "srr"]:
                    os.remove(fullfilepath)
                    logger.info(" Removed: %s" % item)
                try:
                    os.rmdir(dir)
                    logger.info(" Empty Directory Deleted")
                except:
                    pass
        logger.info(" Successful")
                
    else:
        logger.critical("No match found for dir: %s" % dir)

if __name__ == '__main__':
    main()
