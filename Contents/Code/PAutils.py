import PAsearchSites

import googlesearch
import fake_useragent
import base58
import cloudscraper
import requests


def getUserAgent():
    ua = fake_useragent.UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

    return ua.random


def bypassCloudflare(url, **kwargs):
    headers = kwargs.pop('headers', {})
    proxies = kwargs.pop('proxies', {})
    scraper = cloudscraper.CloudScraper()

    for head in ['Authorization', 'Cookie']:
        if head in headers:
            scraper.headers[head] = headers[head]

    data = scraper.get(url, proxies=proxies).text
    if data:
       return data

    Log('Bypass error')
    return None


def HTTPRequest(url, **kwargs):
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
    proxies = {}

    if Prefs['proxy_enable']:
        proxy = '%s://%s:%s' % (Prefs['proxy_type'], Prefs['proxy_ip'], Prefs['proxy_port'])
        proxies = {
            'http': proxy,
            'https': proxy,
        }

    if 'User-Agent' not in headers:
        headers['User-Agent'] = getUserAgent()
    if cookies and 'Cookie' not in headers:
        cookie = '; '.join(['%s=%s' % (key, cookies[key]) for key in cookies])
        headers['Cookie'] = cookie

    Log('Requesting "%s"' % url)
    req = requests.get(url, proxies=proxies, headers=headers)
    if 200 <= req.status_code <= 299:
        data = req.text
    else:
        Log('%d: trying to bypass' % req.status_code)
        data = bypassCloudflare(url, proxies=proxies, headers=headers)

    return data


def getFromGoogleSearch(searchText, site='', **kwargs):
    stop = kwargs['stop'] if 'stop' in kwargs else 10
    if isinstance(site, int):
        site = PAsearchSites.getSearchBaseURL(site).split('://')[1]

    searchTerm = 'site:%s %s' % (site, searchText) if site else searchText

    Log('Using Google Search "%s"' % searchTerm)

    googleResults = []
    try:
        googleResults = list(googlesearch.search(searchTerm, stop=stop))
    except:
        Log('Google Search Error')
        pass

    return googleResults


def Encode(text):
    text = text.encode('UTF-8')

    return base58.b58encode(text)


def Decode(text):
    text = text.encode('UTF-8')

    return base58.b58decode(text)
