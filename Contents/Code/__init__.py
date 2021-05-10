import base64
import codecs
import json
import mimetypes
import os
import random
import re
import requests
import shutil
import time
import urllib
import urlparse
from cStringIO import StringIO
from datetime import datetime
from dateutil.parser import parse
from PIL import Image
from traceback import format_exc
import PAactors
import PAgenres
import PAsearchSites
import PAsiteList
import PAutils
import PAsearchData


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


def ValidatePrefs():
    Log('ValidatePrefs function call')


class PhoenixAdultAgent(Agent.Movies):
    name = 'PhoenixAdult'
    languages = [Locale.Language.English, Locale.Language.German, Locale.Language.French, Locale.Language.Spanish, Locale.Language.Italian, Locale.Language.Dutch]
    accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.lambda']
    primary_provider = True

    def search(self, results, media, lang):
        if Prefs['strip_enable']:
            title = media.name.split(Prefs['strip_symbol'], 1)[0]
        else:
            title = media.name

        title = getSearchTitle(title)

        #Use AdultEmpire to check dvd split scenes automatically
        scene_title = re.search(r'.*(?=.Scene\s\d)', title)
        if scene_title is not None:
            searchSettings = {
                'siteNum': 1334,
                'siteName': "Adult Empire",
                'searchTitle': title,
                'searchDate': None,
            }


        Log('***MEDIA TITLE [from media.name]*** %s' % title)
        if searchSettings is None:
            searchSettings = PAsearchSites.getSearchSettings(title)
            Log(searchSettings)

        filepath = None
        filename = None
        if media.filename:
            filepath = urllib.unquote(media.filename)
            filename = str(os.path.splitext(os.path.basename(filepath))[0])
        
        if searchSettings['siteNum'] is None and filepath:
            directory = str(os.path.split(os.path.dirname(filepath))[1])

            newTitle = getSearchTitle(directory)
            Log('***MEDIA TITLE [from directory]*** %s' % newTitle)
            searchSettings = PAsearchSites.getSearchSettings(newTitle)

            if searchSettings['siteNum'] is None:
                if title == newTitle and title != filename:
                    title = filename

                newTitle = '%s %s' % (newTitle, title)
                Log('***MEDIA TITLE [from directory + media.name]*** %s' % newTitle)
                searchSettings = PAsearchSites.getSearchSettings(newTitle)

        providerName = None
        siteNum = searchSettings['siteNum']
        searchTitle = searchSettings['searchTitle']
        if not searchTitle:
            searchTitle = title
        searchDate = searchSettings['searchDate']
        search = PAsearchData.SearchData(media, searchTitle, searchDate, filepath)

        if siteNum is not None:
            provider = PAsiteList.getProviderFromSiteNum(siteNum)
            if provider is not None:
                providerName = getattr(provider, '__name__')
                Log('Provider: %s' % providerName)
                try:
                    provider.search(results, lang, siteNum, search)
                except Exception as e:
                    Log.Error(format_exc())

        if Prefs['metadataapi_enable'] and providerName != 'networkMetadataAPI' and (siteNum is None or not results or 100 != max([result.score for result in results])):
            siteNum = PAsearchSites.getSiteNumByFilter('MetadataAPI')
            if siteNum is not None:
                provider = PAsiteList.getProviderFromSiteNum(siteNum)
                if provider is not None:
                    providerName = getattr(provider, '__name__')
                    Log('Provider: %s' % providerName)
                    try:
                        provider.search(results, lang, siteNum, search)
                    except Exception as e:
                        Log.Error(format_exc())

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
        Log('SiteNum: %d' % siteNum)

        provider = PAsiteList.getProviderFromSiteNum(siteNum)
        if provider is not None:
            providerName = getattr(provider, '__name__')
            Log('Provider: %s' % providerName)
            provider.update(metadata, lang, siteNum, movieGenres, movieActors)

        # Cleanup Genres and Add
        Log('Genres')
        movieGenres.processGenres(metadata)
        metadata.genres = sorted(metadata.genres)

        # Cleanup Actors and Add
        Log('Actors')
        movieActors.processActors(metadata)

        # Add Content Rating
        metadata.content_rating = 'XXX'

        if Prefs['custom_title_enable']:
            data = {
                'title': metadata.title,
                'actors': ', '.join([actor.name.encode('ascii', 'ignore') for actor in metadata.roles]),
                'studio': metadata.studio,
                'series': ', '.join(set([collection.encode('ascii', 'ignore') for collection in metadata.collections if collection not in metadata.studio])),
            }
            metadata.title = Prefs['custom_title'].format(**data)


def getSearchTitle(title):
    trashTitle = (
        'RARBG', 'COM', r'\d{3,4}x\d{3,4}', 'HEVC', r'H\d{3}', 'AVC', r'\dK',
        r'\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4', 'KLEENEX', 'SD', 'HD',
        'KTR', 'IEVA', 'WRB', 'NBQ', 'ForeverAloneDude', r'X\d{3}', 'SoSuMi',
    )

    for trash in trashTitle:
        title = re.sub(r'\b%s\b' % trash, '', title, flags=re.IGNORECASE)

    title = ' '.join(title.split())

    return title
