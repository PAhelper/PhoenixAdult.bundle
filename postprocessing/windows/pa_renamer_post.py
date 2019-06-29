#!/usr/local/sabnzbd/env/bin/python
# !/usr/bin/env python

import sys
import os, glob
import logging
import argparse
from patools import pa_parse_dir

def main():
    dryrun=False
    batch=False
    if "SAB_VERSION" in os.environ:
        (scriptname,dir,orgnzbname,jobname,reportnumber,category,group,postprocstatus,url) = sys.argv
    else:
        parser = argparse.ArgumentParser(description='Rename adult media downloads for import into Plex with the PhoenixAdult metadat agent')
        parser.add_argument("directory")
        parser.add_argument("-d", "--dryrun", help="don't do work, just show what will happen", action="store_true")
        parser.add_argument("-b", "--batch", help="Do not try to log as batch job will fail", action ="store_true")
        args = parser.parse_args()
        if args.dryrun:
            print "Dry-run mode enabled."
            dryrun=True
        if args.batch:
            print "Batch mode enabled. Logging disabled!"
            batch=True
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
        filename_new = shoot['studio'] + ' - ' + shoot['filename_title'] + ' (' + shoot['date'] + ').mp4'
        logger.debug("New file name: %s" % filename_new)

        for item in os.listdir(dir):
            if item.endswith(".avi"):
                filename_new = filename_new.replace(".mp4", ".avi")
            if item.endswith(".mp4") or item.endswith(".avi"):
                item = os.path.join(dir, item)
                newname = os.path.join(dir, filename_new)
                if dryrun:
                    logger.info("[DRYRUN] Renaming: %s -> %s" % (item, newname))
                else:
                    logger.info("Renaming: %s -> %s" % (item, newname))
                    os.rename(item, newname)
                    os.chmod(newname, 0775)
                exit(0)
    else:
        logger.critical("No match found for dir: %s" % dir)

if __name__ == '__main__':
    main()
