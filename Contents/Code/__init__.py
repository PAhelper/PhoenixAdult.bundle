import os
import re
import random
import requests
import urllib
import urlparse
import json
import shutil
from datetime import datetime
from PIL import Image
from cStringIO import StringIO
from dateutil.parser import parse
import time
import base64
import PAactors
import PAgenres
import PAsearchSites
import PAsiteList
import PAutils


def Start():
    HTTP.ClearCache()
    HTTP.CacheTime = CACHE_1MINUTE * 20
    HTTP.Headers['User-Agent'] = PAutils.getUserAgent()
    HTTP.Headers['Accept-Encoding'] = 'gzip'

    requests.packages.urllib3.disable_warnings()

    dateNowObj = datetime.now()
    debug_dir = os.path.realpath('debug_data')
    if os.path.exists(debug_dir):
        for directoryName in os.listdir(debug_dir):
            debugDateObj = parse(directoryName)
            if abs((dateNowObj - debugDateObj).days) > 3:
                debugLogs = os.path.join(debug_dir, directoryName)
                shutil.rmtree(debugLogs)
                Log('Deleted debug data: %s' % directoryName)


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

        title = getSearchTitle(title)

        Log('*** MEDIA TITLE [from media.name] *** %s' % title)
        searchSettings = PAsearchSites.getSearchSettings(title)

        filepath = None
        filename = None
        if media.filename:
            filepath = urllib.unquote(media.filename)
            filename = str(os.path.splitext(os.path.basename(filepath))[0])

        if searchSettings['siteNum'] is None and filepath:
            directory = str(os.path.split(os.path.dirname(filepath))[1])

            newTitle = getSearchTitle(directory)
            Log('*** MEDIA TITLE [from directory] *** %s' % newTitle)
            searchSettings = PAsearchSites.getSearchSettings(newTitle)

            if searchSettings['siteNum'] is not None and searchSettings['searchTitle'].lower() == PAsearchSites.getSearchSiteName(searchSettings['siteNum']).lower():
                newTitle = '%s %s' % (siteName, title)
                Log('*** MEDIA TITLE [from directory + media.name] *** %s' % newTitle)
                searchSettings = PAsearchSites.getSearchSettings(newTitle)

        siteNum = searchSettings['siteNum']

        if siteNum is not None:
            search = SearchData(media, searchSettings['searchTitle'], searchSettings['searchDate'], filepath, filename)

            provider = PAsiteList.getProviderFromSiteNum(siteNum)
            if provider is not None:
                provider.search(results, lang, siteNum, search)

        results.Sort('score', descending=True)

    def update(self, metadata, media, lang):
        movieGenres = PAgenres.PhoenixGenres()
        movieActors = PAactors.PhoenixActors()

        HTTP.ClearCache()
        metadata.genres.clear()
        metadata.roles.clear()

        Log('******UPDATE CALLED*******')

        metadata_id = str(metadata.id).split('|')
        siteNum = int(metadata_id[1])
        Log(str(siteNum))

        provider = PAsiteList.getProviderFromSiteNum(siteNum)
        if provider is not None:
            provider.update(metadata, siteNum, movieGenres, movieActors)

        # Cleanup Genres and Add
        Log('Genres')
        movieGenres.processGenres(metadata)
        metadata.genres = sorted(metadata.genres)

        # Cleanup Actors and Add
        Log('Actors')
        movieActors.processActors(metadata)

        # Add Content Rating
        metadata.content_rating = 'XXX'


def getSearchTitle(title):
    trashTitle = (
        'RARBG', 'COM', r'\d{3,4}x\d{3,4}', 'HEVC', 'H265', 'AVC', r'\dK',
        r'\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4', 'KLEENEX', 'SD', 'HD',
        'KTR', 'IEVA', 'WRB', 'NBQ', 'ForeverAloneDude',
    )

    for trash in trashTitle:
        title = re.sub(r'\b%s\b' % trash, '', title, flags=re.IGNORECASE)

    title = ' '.join(title.split())

    return title

class SearchData:
    title = ''
    encoded = ''
    date = ''
    filepath = ''
    filename = ''
    duration = ''

    def __init__(self, media, searchTitle, searchDate, filepath, filename):
        self.title = searchTitle
        self.encoded = urllib.quote(searchTitle)
        self.date = searchDate
        self.filepath = filepath
        self.filename = filename
        self.duration = media.duration

        Log('SearchData.title: %s' % self.title)

        if self.date:
            Log('SearchData.date: %s' % self.date)

        if self.filename:
            Log('SearchData.filename: %s' % self.filename)

    def dateFormat(self, format = '%Y-%m-%d'):
        if self.date:
            return parse(self.date).strftime(format)
        else:
            return ''

    def durationFormat(self, hoursFormat = '%02d:%02d:%02d', minutesFormat = '%d:%02d'):
        durationString = ''

        if self.duration:
            import math
            seconds = round(float(self.duration) / 1000)
            hours = math.floor(seconds / 3600)
            seconds = seconds - hours * 3600
            minutes = math.floor(seconds / 60)
            seconds = seconds - minutes * 60

            if hours:
                durationString = hoursFormat % (hours, minutes, seconds)
            else:
                durationString = minutesFormat % (minutes, seconds)

        return durationString


