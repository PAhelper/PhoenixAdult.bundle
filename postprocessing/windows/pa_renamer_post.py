#!/usr/local/sabnzbd/env/bin/python
# !/usr/bin/env python

import sys
import os, glob
import logging
import argparse
import string
import re
from patools import pa_parse_dir
import collections

def main():
    dryrun=False
    batch=False
    cleanup=False
    if "SAB_VERSION" in os.environ:
        (scriptname,dir,orgnzbname,jobname,reportnumber,category,group,postprocstatus,url) = sys.argv
    else:
        parser = argparse.ArgumentParser(description='Rename adult media downloads for import into Plex with the PhoenixAdult metadat agent')
        parser.add_argument("directory")
        parser.add_argument("-d", "--dryrun", help="don't do work, just show what will happen", action="store_true")
        parser.add_argument("-b", "--batch", help="Do not try to log as batch job will fail", action="store_true")
        parser.add_argument("-c", "--cleanup", help="Delete oleftover files and cleanup folders after rename", action="store_true")
        args = parser.parse_args()
        if args.dryrun:
            print "Dry-run mode enabled."
            dryrun=True
        if args.batch:
            print "Batch mode enabled. Logging disabled!"
            batch=True
        if args.cleanup:
            print "Cleanup Enabled!"
            cleanup=True
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
        filename_new = string.capwords(shoot['studio'] + ' - ' + shoot['filename_title'] + ' (' + shoot['date'] + ').mp4')
        logger.debug("New file name: %s" % filename_new)
        
        overrideSettings = collections.getSiteMatch(shoot['studio'], dir)

        for item in os.listdir(dir):
            fullfilepath = os.path.join(dir, item)
            filetype = item.split('.')[-1]
            logger.info("The filetype is: %s" % filetype)
            if os.path.getsize(fullfilepath) > 50000000:
                if overrideSettings != 9999:
                    filename_new = re.sub(shoot['studio'], overrideSettings[0], filename_new, flags=re.IGNORECASE)
                    dir_new = dir.split(overrideSettings[1])[0] + overrideSettings[2]
                else:
                    dir_new = dir
                filename_new = filename_new.replace(".mp4", '.' + filetype)
                if filetype in ["mp4", "avi", "mkv"]:
                    item = os.path.join(dir, item)
                    newname = os.path.join(dir_new, filename_new)
                    if dryrun:
                        logger.info("[DRYRUN] Renaming: %s -> %s" % (item, newname))
                    else:
                        try:
                            os.makedirs(dir_new)
                        except:
                            pass
                        logger.info("Renaming/Moving from: %s --> %s" % (item, newname))
                        os.rename(item, newname)
                        os.chmod(newname, 0775)
            if cleanup:
                if filetype in ["txt", "jpg", "jpeg"]:
                    os.remove(fullfilepath)
                    logger.info("Removed: %s" % item)
                try:
                    os.rmdir(dir)
                    logger.info("Empy Directory Deleted")
                except:
                    pass
                
                
#        for item in os.listdir(dir):
#            if item.endswith(".avi"):
#                filename_new = filename_new.replace(".mp4", ".avi")
#            elif item.endswith(".mkv"):
#                filename_new = filename_new.replace(".mp4", ".mkv")
#            if item.endswith(".mp4") or item.endswith(".avi") or item.endswith(".mkv"):
#                item = os.path.join(dir, item)
#                newname = os.path.join(dir, filename_new)
#                if dryrun:
#                    logger.info("[DRYRUN] Renaming: %s -> %s" % (item, newname))
#                else:
#                    logger.info("Renaming: %s -> %s" % (item, newname))
#                    os.rename(item, newname)
#                    os.chmod(newname, 0775)
#                exit(0)
    else:
        logger.critical("No match found for dir: %s" % dir)

if __name__ == '__main__':
    main()
