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

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'


def getUserAgent(fixed=False):
    if fixed:
        result = UserAgent
    else:
        ua = fake_useragent.UserAgent(fallback=UserAgent)
        result = ua.random

    return result


def flareSolverrRequest(url, method, **kwargs):
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
    params = kwargs.pop('params', {})

    if method not in ['GET', 'POST']:
        return None

    req_params = {
        'cmd': 'request.%s' % method.lower(),
        'url': url,
        'userAgent': headers['User-Agent'] if 'User-Agent' in headers else getUserAgent(),
        'maxTimeout': 60000,
        'headers': json.dumps(headers),
    }

    if method == 'POST':
        req_params['postData'] = json.dumps(params)

    req = HTTPRequest('%s/v1' % Prefs['flaresolverr_endpoint'], headers={'Content-Type': 'application/json'}, params=json.dumps(req_params), timeout=60, bypass=False)
    if req.ok:
        data = req.json()['solution']
        headers = data['headers']
        headers['User-Agent'] = data['userAgent']
        cookies = {cookie['name']: cookie['value'] for cookie in data['cookies']}

        return FakeResponse(req, url, int(data['headers']['status']), data['response'], headers, cookies)

    return None


def cloudScraperRequest(url, method, **kwargs):
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
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


def HTTPBypass(url, method='GET', **kwargs):
    method = method.upper()
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
    params = kwargs.pop('params', {})
    proxies = kwargs.pop('proxies', {})

    req_bypass = None

    if not req_bypass or not req_bypass.ok:
        Log('FlareSolverr')
        try:
            req_bypass = flareSolverrRequest(url, method, proxies=proxies, headers=headers, cookies=cookies, params=params)
        except:
            pass

    if not req_bypass or not req_bypass.ok:
        Log('CloudScraper')
        try:
            req_bypass = cloudScraperRequest(url, method, proxies=proxies, headers=headers, cookies=cookies, params=params)
        except:
            pass

    if not req_bypass or not req_bypass.ok:
        Log('ReqBin')
        try:
            req_bypass = reqBinRequest(url, method, proxies=proxies, headers=headers, cookies=cookies, params=params)
        except:
            pass

    return req_bypass


def HTTPRequest(url, method='GET', **kwargs):
    url = getClearURL(url)
    method = method.upper()
    headers = kwargs.pop('headers', {})
    cookies = kwargs.pop('cookies', {})
    params = kwargs.pop('params', {})
    bypass = kwargs.pop('bypass', True)
    timeout = kwargs.pop('timeout', None)
    allow_redirects = kwargs.pop('allow_redirects', True)
    fixed_useragent = kwargs.pop('fixed_useragent', False)
    proxies = {}

    if Prefs['proxy_enable']:
        if Prefs['proxy_authentication_enable']:
            proxy = '%s://%s:%s@%s:%s' % (Prefs['proxy_type'], Prefs['proxy_user'], Prefs['proxy_password'], Prefs['proxy_ip'], Prefs['proxy_port'])
        else:
            proxy = '%s://%s:%s' % (Prefs['proxy_type'], Prefs['proxy_ip'], Prefs['proxy_port'])

        proxies = {
            'http': proxy,
            'https': proxy,
        }

    if 'User-Agent' not in headers:
        headers['User-Agent'] = getUserAgent(fixed_useragent)

    if params:
        method = 'POST'

    Log('Requesting %s "%s"' % (method, url))

    req = None
    try:
        req = requests.request(method, url, proxies=proxies, headers=headers, cookies=cookies, data=params, timeout=timeout, verify=False, allow_redirects=allow_redirects)
    except:
        req = FakeResponse(None, url, 418, None)

    req_bypass = None
    if not req.ok and bypass:
        if req.status_code == 403 or req.status_code == 503:
            req_bypass = HTTPBypass(url, method, proxies=proxies, headers=headers, cookies=cookies, params=params)

    if req_bypass:
        req = req_bypass

    req.encoding = 'UTF-8'

    if Prefs['debug_enable']:
        try:
            saveRequest(url, req)
        except:
            Log('saveRequest Error')
            pass

    return req


def getFromGoogleSearch(searchText, site='', **kwargs):
    stop = kwargs.pop('stop', 10)
    lang = kwargs.pop('lang', 'en')

    if isinstance(site, int):
        site = PAsearchSites.getSearchBaseURL(site).split('://')[1].lower()
        if site.startswith('www.'):
            site = site.replace('www.', '', 1)

    googleResults = []
    searchTerm = 'site:%s %s' % (site, searchText) if site else searchText

    if not searchText:
        return googleResults

    Log('Using Google Search "%s"' % searchTerm)

    try:
        googleResults = list(googlesearch.search(searchTerm, stop=stop, lang=lang, user_agent=getUserAgent()))
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
    newURL = url
    if url.startswith('http'):
        url = urlparse.urlparse(url)
        path = url.path

        while '//' in path:
            path = path.replace('//', '/')

        newURL = '%s://%s%s' % (url.scheme, url.netloc, path)
        if url.query:
            newURL += '?%s' % url.query

    return newURL


def saveRequest(url, req):
    debug_dir = os.path.join('debug_data', datetime.now().strftime('%d-%m-%Y'))
    debug_dir = os.path.realpath(debug_dir)
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    raw_http = '< Target URL: "%s"\r\n\r\n' % url
    raw_http += dump.dump_all(req).decode('UTF-8', errors='replace')

    file_name = '%s.gz' % uuid.uuid4().hex
    with gzip.open(os.path.join(debug_dir, file_name), 'wb') as f:
        f.write(raw_http.encode('UTF-8'))

    Log('GZip request saved as "%s"' % file_name)

    return True


def parseTitle(s, siteNum):
    s = re.sub(r'w\/(?!\s)', 'w/ ', s, flags=re.IGNORECASE)
    s = re.sub(r'\,(?!\s)', ', ', s)
    s = s.replace('_', ' ')
    word_list = re.split(' ', s)

    firstword = parseWord(word_list[0], siteNum)
    if len(firstword) > 1:
        firstword = manualWordFix(firstword)
        firstword = firstword[0].capitalize() + firstword[1:]
    else:
        firstword = firstword.capitalize()

    final = [firstword]

    for word in word_list[1:]:
        final.append(parseWord(word, siteNum))

    output = ' '.join(final)
    output = re.sub(r'\b(?:\.)$', '', output)
    output = re.sub(r'(!|:|\?|\.|,)(?=\w)', lambda m: m.group(0) + ' ', output)
    output = re.sub(r'\s+(?=[.,!\":])', '', output)
    output = re.sub(r'(?<=!|:|\?|\.|-)(\s)(\S)', lambda m: m.group(1) + m.group(2).upper(), output)

    return output


def parseWord(word, siteNum):
    lower_exceptions = ['a', 'v', 'y', 'an', 'of', 'the', 'and', 'for', 'to', 'onto', 'but', 'or', 'nor', 'at', 'with', 'vs', 'in', 'on']
    upper_exceptions = ['bbc', 'xxx', 'bbw', 'bf', 'bff', 'bts', 'pov', 'dp', 'gf', 'bj', 'wtf', 'cfnm', 'bwc', 'fm', 'tv', 'ai', 'hd', 'milf']
    letter_exceptions = ['A', 'V', 'Y']
    sitename = PAsearchSites.getSearchSiteName(siteNum).replace(' ', '')

    pattern = re.compile(r'\W')
    cleanWord = re.sub(pattern, '', word)

    if '-' in word and '--' not in word:
        word_list = re.split('-', word)

        firstword = parseWord(word_list[0], siteNum)
        if len(firstword) > 1:
            firstword = firstword[0].capitalize() + firstword[1:]
        else:
            firstword = firstword.capitalize()
        nhword = firstword + '-'

        for hword in word_list[1:]:
            if len(hword) > 1:
                nhword += parseWord(hword, siteNum)
            else:
                nhword += hword.upper()

            if hword != word_list[-1]:
                nhword += '-'
        word = nhword
    elif '\'' in word:
        word_list = re.split('\'', word)

        firstword = parseWord(word_list[0], siteNum)
        if len(firstword) > 1:
            firstword = firstword[0].capitalize() + firstword[1:]
        else:
            firstword = firstword.upper()
        nhword = firstword + '\''

        for hword in word_list[1:]:
            if len(re.sub(pattern, '', hword)) > 2:
                nhword += parseWord(hword, siteNum)
            else:
                nhword += hword

            if hword != word_list[-1]:
                nhword += '\''
        word = nhword
    elif cleanWord.lower() in upper_exceptions:
        word = word.upper()
    elif cleanWord.isupper() and cleanWord not in letter_exceptions:
        word = word.upper()
    elif sitename.lower() == word.lower():
        word = sitename
    elif not (cleanWord.islower() or cleanWord.isupper() or cleanWord.lower() in lower_exceptions):
        pass
    else:
        word = word.lower() if cleanWord.lower() in lower_exceptions else word.capitalize()

    word = manualWordFix(word)

    return word


def manualWordFix(word):
    exceptions = ['im', 'theyll', 'cant', 'ive', 'shes', 'theyre', 'tshirt', 'dont', 'wasnt', 'youre', 'ill', 'whats', 'didnt', 'isnt', 'senor', 'senorita', 'thats', 'gstring', 'milfs', 'oreilly']
    corrections = ['I\'m', 'They\'ll', 'Can\'t', 'I\'ve', 'She\'s', 'They\'re', 'T-Shirt', 'Don\'t', 'Wasn\'t', 'You\'re', 'I\'ll', 'What\'s', 'Didn\'t', 'Isn\'t', 'Señor', 'Señorita', 'That\'s', 'G-String', 'MILFs', 'O\'Reilly']

    if word.lower() in exceptions:
        for correction in corrections:
            if word.lower() == correction.lower().replace('\'', '').replace('-', '').replace('ñ', 'n'):
                return correction

    return word


def cleanHTML(text):
    data = re.sub(r'<.*?>', '', text)
    data = data.strip()

    return data


def getCleanSearchTitle(title):
    trashTitle = (
        'RARBG', 'COM', r'\d{3,4}x\d{3,4}', 'HEVC', r'H\d{3}', 'AVC', r'\dK',
        r'\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4', 'KLEENEX', 'SD', 'HD',
        'KTR', 'IEVA', 'WRB', 'NBQ', 'ForeverAloneDude', r'X\d{3}', 'SoSuMi',
    )

    for trash in trashTitle:
        title = re.sub(r'\b%s\b' % trash, '', title, flags=re.IGNORECASE)

    title = ' '.join(title.split())

    return title


def getSearchTitleStrip(title):
    if Prefs['strip_enable']:
        if Prefs['strip_symbol'] and Prefs['strip_symbol'] in title:
            title = title.split(Prefs['strip_symbol'], 1)[0]

        if Prefs['strip_symbol_reverse'] and Prefs['strip_symbol_reverse'] in title:
            title = title.rsplit(Prefs['strip_symbol_reverse'], 1)[-1]

    return title.strip()
