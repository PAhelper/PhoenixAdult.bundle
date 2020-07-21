import PAsearchSites

import googlesearch
import fake_useragent
import base58
import cloudscraper
import requests


def getUserAgent():
    ua = fake_useragent.UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

    return ua.random


def bypassCloudflare(url, method, **kwargs):
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
    proxies = kwargs.pop('proxies', {})
    params = kwargs.pop('params', {})

    scraper = cloudscraper.CloudScraper()
    scraper.headers.update(headers)
    scraper.cookies.update(cookies)

    req = scraper.request(method, url, proxies=proxies, data=params)

    return req


def HTTPRequest(url, method='GET', **kwargs):
    method = method.upper()
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
    params = kwargs.pop('params', {})
    bypass = kwargs.pop('bypass', True)
    proxies = {}

    if Prefs['proxy_enable']:
        proxy = '%s://%s:%s' % (Prefs['proxy_type'], Prefs['proxy_ip'], Prefs['proxy_port'])
        proxies = {
            'http': proxy,
            'https': proxy,
        }

    if 'User-Agent' not in headers:
        headers['User-Agent'] = getUserAgent()

    if params:
        method = 'POST'

    Log('Requesting %s "%s"' % (method, url))
    req = requests.request(method, url, proxies=proxies, headers=headers, cookies=cookies, data=params)

    req_bypass = None
    if not req.ok and bypass:
        if req.status_code == 403 or req.status_code == 503:
            Log('%d: trying to bypass with CloudScraper' % req.status_code)
            try:
                req_bypass = bypassCloudflare(url, method, proxies=proxies, headers=headers, cookies=cookies, params=params)
            except Exception as e:
                Log('CloudScraper error: %s' % e)

    if req_bypass:
        req = req_bypass

    req.encoding = 'UTF-8'

    return req


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
