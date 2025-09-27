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
from datetime import datetime, timedelta
from dateutil.parser import parse
from PIL import Image
from slugify import slugify
from traceback import format_exc
import PAactors
import PAgenres
import PAcollections
import PAsearchSites
import PAsiteList
import PAutils
import PAsearchData


def Start():
    HTTP.ClearCache()
    HTTP.CacheTime = CACHE_1MINUTE * 20
    HTTP.Headers['User-Agent'] = PAutils.getUserAgent(True)
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
    languages = [Locale.Language.NoLanguage, Locale.Language.English, Locale.Language.German, Locale.Language.French, Locale.Language.Spanish, Locale.Language.Italian, Locale.Language.Dutch]
    accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.lambda']
    contributes_to = ['com.plexapp.agents.none', 'com.plexapp.agents.stashplexagent', 'com.plexapp.agents.themoviedb', 'com.plexapp.agents.imdb']
    primary_provider = True

    def search(self, results, media, lang, manual):
        if not manual and Prefs['manual_override']:
            Log('Skipping Search for Manual Override')
            return

        filepath = None
        filename = None
        if media.filename:
            filepath = urllib.unquote(media.filename)
            filename = str(os.path.splitext(os.path.basename(filepath))[0])
            filename = PAutils.getSearchTitleStrip(filename)

        if not media.name and media.primary_metadata.title:
            media.name = media.primary_metadata.title

        title = PAutils.getSearchTitleStrip(media.name)

        if filename and '5.1080p' in filename.lower():
            title = title.replace(' 080p', ' 5 1080p').strip()

        title = PAutils.getCleanSearchTitle(title)

        Log('***MEDIA TITLE [from media.name]*** %s' % title)
        searchSettings = PAsearchSites.getSearchSettings(title, filename)
        Log(searchSettings)

        if searchSettings['siteNum'] is None and filepath:
            directory = str(os.path.split(os.path.dirname(filepath))[1])
            directory = PAutils.getSearchTitleStrip(directory)

            newTitle = PAutils.getCleanSearchTitle(directory)
            Log('***MEDIA TITLE [from directory]*** %s' % newTitle)
            searchSettings = PAsearchSites.getSearchSettings(newTitle, filename)

            if searchSettings['siteNum'] is None:
                if title == newTitle and title != filename:
                    title = filename

                newTitle = '%s %s' % (newTitle, title)
                Log('***MEDIA TITLE [from directory + media.name]*** %s' % newTitle)
                searchSettings = PAsearchSites.getSearchSettings(newTitle, filename)

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
        movieCollections = PAcollections.PhoenixCollections()
        movieGenres = PAgenres.PhoenixGenres()
        movieActors = PAactors.PhoenixActors()
        valid_images = list()

        HTTP.ClearCache()
        metadata.collections.clear()
        movieCollections.clearCollections()

        metadata.genres.clear()
        movieGenres.clearGenres()

        metadata.roles.clear()
        movieActors.clearActors()

        metadata.directors.clear()
        movieActors.clearDirectors()

        metadata.producers.clear()
        movieActors.clearProducers()

        Log('******UPDATE CALLED*******')

        metadata_id = str(metadata.id).split('|')
        siteNum = int(metadata_id[1])
        Log('SiteNum: %d' % siteNum)

        if Prefs['remove_images']:
            metadata.posters.validate_keys(valid_images)
            metadata.art.validate_keys(valid_images)

        provider = PAsiteList.getProviderFromSiteNum(siteNum)
        if provider is not None:
            providerName = getattr(provider, '__name__')
            Log('Provider: %s' % providerName)
            provider.update(metadata, lang, siteNum, movieGenres, movieActors, movieCollections, valid_images)

        # Cleanup Collections and Add
        Log('Collections')
        movieCollections.processCollections(metadata, siteNum)

        # Cleanup Genres and Add
        Log('Genres')
        movieGenres.processGenres(metadata, siteNum)
        metadata.genres = sorted(metadata.genres)

        # Cleanup Actors and Add
        Log('Actors')
        movieActors.processActors(metadata, siteNum)

        # Cleanup Directors and Add
        Log('Directors')
        movieActors.processDirectors(metadata, siteNum)

        # Cleanup Producers and Add
        Log('Producers')
        movieActors.processProducers(metadata, siteNum)

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

        if Prefs['validate_image_keys']:
            metadata.posters.validate_keys(valid_images)
            metadata.art.validate_keys(valid_images)
