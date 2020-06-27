import PAsearchSites

import googlesearch
import fake_useragent


def getUserAgent():
    ua = fake_useragent.UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

    return ua.random


def bypassCloudflare(url, **kwargs):
    headers = kwargs['headers'] if 'headers' in kwargs else {}
    req_headers = '\n'.join(['%s: %s' % (key, headers[key]) for key in headers])

    for node in ['US', 'DE']:
        params = json.dumps({'id': 0, 'json': json.dumps({'method': 'GET', 'url': url, 'headers': req_headers, 'apiNode': node, 'idnUrl': url}), 'deviceId': '', 'sessionId': ''})
        req = urllib.Request('https://api.reqbin.com/api/v1/requests', params, headers={
            'Content-Type': 'application/json',
            'User-Agent': getUserAgent()
        })
        data = urllib.urlopen(req).read()
        data = json.loads(data)
        if data['Success']:
            return data['Content']

    Log('Bypass error: %s' % data['Content'])
    return None


def HTTPRequest(url, **kwargs):
    headers = kwargs['headers'] if 'headers' in kwargs else {}
    cookies = kwargs['cookies'] if 'cookies' in kwargs else {}
    data = None

    if 'User-Agent' not in headers:
        headers['User-Agent'] = getUserAgent()
    if cookies and 'Cookie' not in headers:
        cookie = '; '.join(['%s=%s' % (key, cookies[key]) for key in cookies])
        headers['Cookie'] = cookie

    try:
        Log('Requesting "%s"' % url)
        req = urllib.Request(url, headers=headers)
        data = urllib.urlopen(req).read()
    except Exception as e:
        Log('%s: trying to bypass' % e)
        data = bypassCloudflare(url, headers=headers)
        pass

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
