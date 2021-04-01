import base64
import codecs
import json
import mimetypes
import os
import random
import re
import requests
import socks
import socket
import shutil
import time
import urllib
import urlparse
from cStringIO import StringIO
from datetime import datetime
from dateutil.parser import parse
from PIL import Image
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
    languages = [Locale.Language.English, Locale.Language.German, Locale.Language.French, Locale.Language.Spanish, Locale.Language.Italian]
    accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.lambda']
    primary_provider = True

    def search(self, results, media, lang):
        # Set default socket if using socket with authentication
        previousSocket = socket.socket
        if Prefs['proxy_enable'] and Prefs['proxy_authentication_enable']:
            if Prefs['proxy_type'].upper() not in socks.PROXY_TYPES:
                Log('Error, proxy type (' + Prefs['proxy_type'] + ') must be one of the following: ' + str(socks.PROXY_TYPES.keys()))
                raise ValueError("Invalid Proxy type: " + Prefs['proxy_type'])
            else:
                socks.set_default_proxy(socks.SOCKS5, Prefs['proxy_ip'], int(Prefs['proxy_port']), True, Prefs['proxy_user'],Prefs['proxy_password'])
                socket.socket = socks.socksocket
        if Prefs['ip_test']:
            Log("Detecting ip: " + requests.get('http://ifconfig.me/ip').text)
        
        if Prefs['strip_enable']:
            title = media.name.split(Prefs['strip_symbol'], 1)[0]
        else:
            title = media.name

        title = getSearchTitle(title)

        Log('***MEDIA TITLE [from media.name]*** %s' % title)
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

            if searchSettings['siteNum'] is not None and searchSettings['searchTitle'].lower() == PAsearchSites.getSearchSiteName(searchSettings['siteNum']).lower():
                newTitle = '%s %s' % (newTitle, title)
                Log('***MEDIA TITLE [from directory + media.name]*** %s' % newTitle)
                searchSettings = PAsearchSites.getSearchSettings(newTitle)

        siteNum = searchSettings['siteNum']

        if siteNum is not None:
            search = PAsearchData.SearchData(media, searchSettings['searchTitle'], searchSettings['searchDate'], filepath, filename)

            provider = PAsiteList.getProviderFromSiteNum(siteNum)
            if provider is not None:
                providerName = getattr(provider, '__name__')
                Log('Provider: %s' % providerName)
                provider.search(results, lang, siteNum, search)

                if Prefs['metadataapi_enable']:
                    if providerName != 'networkMetadataAPI' and (not results or 100 != max([result.score for result in results])):
                        siteNum = PAsearchSites.getSiteNumByFilter('MetadataAPI')
                        if siteNum is not None:
                            provider = PAsiteList.getProviderFromSiteNum(siteNum)
                            if provider is not None:
                                providerName = getattr(provider, '__name__')
                                Log('Provider: %s' % providerName)
                                try:
                                    provider.search(results, lang, siteNum, search)
                                except Exception as e:
                                    Log(e)

        results.Sort('score', descending=True)
        # Revert to default socket
        if (Prefs['proxy_authentication_enable']):
            socket.socket = previousSocket

    def update(self, metadata, media, lang):
        # Set default socket if using socket with authentication
        previousSocket = socket.socket
        if Prefs['proxy_enable'] and Prefs['proxy_authentication_enable']:
            if Prefs['proxy_type'].upper() not in socks.PROXY_TYPES:
                Log('Error, proxy type (' + Prefs['proxy_type'] + ') must be one of the following: ' + str(socks.PROXY_TYPES.keys()))
                raise ValueError("Invalid Proxy type: " + Prefs['proxy_type'])
            else:
                socks.set_default_proxy(socks.SOCKS5, Prefs['proxy_ip'], int(Prefs['proxy_port']), True, Prefs['proxy_user'],Prefs['proxy_password'])
                socket.socket = socks.socksocket
        if Prefs['ip_test']:
            Log("Detecting ip: " + requests.get('http://ifconfig.me/ip').text)
        
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

        # Revert to default socket
        if (Prefs['proxy_authentication_enable']):
            socket.socket = previousSocket


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
