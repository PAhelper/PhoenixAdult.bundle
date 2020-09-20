import gzip
import uuid

import googlesearch
import fake_useragent
import base58
import cloudscraper
import requests
from requests_toolbelt.utils import dump
from requests_response import FakeResponse

import PAsearchSites


def getUserAgent():
    ua = fake_useragent.UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

    return ua.random


def bypassCloudflare(url, method, **kwargs):
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
    proxies = kwargs.pop('proxies', {})
    params = kwargs.pop('params', {})

    scraper = cloudscraper.CloudScraper()
    if Prefs['captcha_enable']:
        scraper.captcha = {
            'provider': Prefs['captcha_type'],
            'api_key': Prefs['captcha_key']
        }
    scraper.headers.update(headers)
    scraper.cookies.update(cookies)

    req = scraper.request(method, url, data=params)

    return req


def reqBinRequest(url, method, **kwargs):
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
    proxies = kwargs.pop('proxies', {})
    params = kwargs.pop('params', {})

    if cookies and 'Cookie' not in headers:
        cookie = '; '.join(['%s=%s' % (key, cookies[key]) for key in cookies])
        headers['Cookie'] = cookie

    req_headers = '\n'.join(['%s: %s' % (key, headers[key]) for key in headers])

    for node in ['US', 'DE']:
        req_data = {
            'method': method,
            'url': url,
            'headers': req_headers,
            'apiNode': node,
            'idnUrl': url
        }

        if method == 'POST':
            if headers['Content-Type'] == 'application/json':
                req_data['contentType'] = 'JSON'
                req_data['content'] = params
            else:
                req_data['contentType'] = 'URLENCODED'
                req_data['content'] = '&'.join(['%s=%s' % (key, params[key]) for key in params])

        req_params = json.dumps({
            'id': 0,
            'json': json.dumps(req_data),
            'deviceId': '',
            'sessionId': ''
        })

        req = HTTPRequest('https://api.reqbin.com/api/v1/requests', headers={'Content-Type': 'application/json'}, params=req_params, proxies=proxies, bypass=False)
        if req.ok:
            data = req.json()
            return FakeResponse(req, url, int(data['StatusCode']), data['Content'])
    return None


def HTTPRequest(url, method='GET', **kwargs):
    url = getClearURL(url)
    method = method.upper()
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
    params = kwargs.pop('params', {})
    bypass = kwargs.pop('bypass', True)
    allow_redirects = kwargs.pop('allow_redirects', True)
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
    req = requests.request(method, url, proxies=proxies, headers=headers, cookies=cookies, data=params, verify=False, allow_redirects=allow_redirects)

    req_bypass = None
    if not req.ok and bypass:
        if req.status_code == 403 or req.status_code == 503:
            Log('%d: trying to bypass with CloudScraper' % req.status_code)
            try:
                req_bypass = bypassCloudflare(url, method, proxies=proxies, headers=headers, cookies=cookies, params=params)
                if not req_bypass.ok:
                    raise Exception(req.status_code)
            except Exception as e:
                Log('CloudScraper error: %s' % e)
                Log('Trying through ReqBIN')
                req_bypass = reqBinRequest(url, method, proxies=proxies, headers=headers, cookies=cookies, params=params)

    if req_bypass:
        req = req_bypass

    req.encoding = 'UTF-8'

    if Prefs['debug_enable']:
        saveRequest(url, req)

    return req


def getFromGoogleSearch(searchText, site='', **kwargs):
    stop = kwargs.pop('stop', 10)
    if isinstance(site, int):
        site = PAsearchSites.getSearchBaseURL(site).split('://')[1].lower()
        if site.startswith('www.'):
            site = site.replace('www.', '', 1)

    searchTerm = 'site:%s %s' % (site, searchText) if site else searchText

    Log('Using Google Search "%s"' % searchTerm)

    googleResults = []
    try:
        googleResults = list(googlesearch.search(searchTerm, stop=stop, user_agent=getUserAgent()))
    except:
        Log('Google Search Error')
        pass

    return googleResults


def Encode(text):
    text = text.encode('UTF-8')

    return base58.b58encode(text)


def Decode(text):
    if text.isalnum():
        text = text.encode('UTF-8')

        return base58.b58decode(text)
    else:
        # Old style decoding
        return text.replace('$', '/').replace('_', '/').replace('?', '!')


def getClearURL(url):
    url = urlparse.urlparse(url)
    path = url.path

    while '//' in path:
        path = path.replace('//', '/')

    newURL = '%s://%s%s' % (url.scheme, url.netloc, path)
    if url.query:
        newURL += '?%s' % url.query

    return newURL


def saveRequest(url, req):
    debug_dir = 'debug_data/%s/' % datetime.now().strftime('%d-%m-%Y')
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    raw_http = '< Target URL: "%s"\r\n\r\n' % url
    raw_http += dump.dump_all(req).decode('UTF-8')

    file_name = '%s.gz' % uuid.uuid4().hex
    with gzip.open(debug_dir + file_name, 'wb') as f:
        f.write(raw_http.encode('UTF-8'))

    Log('GZip request saved as "%s"' % file_name)

    return True
