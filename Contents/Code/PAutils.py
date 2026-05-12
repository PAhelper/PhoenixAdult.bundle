import gzip
import uuid

import googlesearch
import ddgsearch
import fake_useragent
import base58
import cloudscraper
import requests
from requests_toolbelt.utils import dump
from requests_response import FakeResponse
from HTMLParser import HTMLParser

import PAsearchSites
from PAparseTitle import TitleCaseEngine
from PAcaptchaHelper import CaptchaHelper

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
        headers = {'User-Agent': data['userAgent']}
        cookies = {cookie['name']: cookie['value'] for cookie in data['cookies']}

        return FakeResponse(req, url, data['status'], data['response'], headers, cookies)

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


def getFromSearchEngine(searchText, site='', **kwargs):
    lang = kwargs.pop('lang', 'en')

    if isinstance(site, int):
        site = PAsearchSites.getSearchBaseURL(site).split('://')[1].lower()
        if site.startswith('www.'):
            site = site.replace('www.', '', 1)

    results = []
    searchTerm = 'site:%s %s' % (site, searchText) if site else searchText

    if not searchText:
        return results

    Log('Using Google Search "%s"' % searchText)
    try:
        results = list(googlesearch.search(searchText, site, lang=lang, sleep_interval=1))
        if not results:
            raise ValueError("No Results")
    except:
        Log('Google Search Error')
        Log('Using Duck Duck Go Search "%s"' % searchTerm)
        try:
            results = list(ddgsearch.search(searchTerm, site, lang=lang, sleep_interval=1))
            if not results:
                raise ValueError("No Results")
        except:
            Log('DDGS Search Error')

    return results


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
    if not url.startswith('http'):
        return url

    parsed = urlparse.urlparse(url)
    path = parsed.path.replace('//', '/')

    # Rebuild URL
    new_url = '%s://%s%s' % (parsed.scheme, parsed.netloc, path)

    if parsed.query:
        new_url += '?' + parsed.query

    return new_url


def saveRequest(url, req):
    # Build dated debug directory
    debug_dir = os.path.join('debug_data', datetime.now().strftime('%d-%m-%Y'))

    if not os.path.exists(debug_dir):
        try:
            os.makedirs(debug_dir)
        except OSError:
            pass

    # Build raw HTTP dump
    raw_http = '\r\n'.join(['< Target URL: "%s"' % url, '', dump.dump_all(req).decode('UTF-8', 'replace')])

    # Create gzip file
    file_name = uuid.uuid4().hex + '.gz'
    file_path = os.path.join(debug_dir, file_name)

    with gzip.open(file_path, 'wb') as f:
        f.write(raw_http.encode('UTF-8'))

    Log('GZip request saved as "%s"' % file_name)

    return True


def parseTitle(s, siteNum, title_type='title'):
    engine = TitleCaseEngine(title_type, debug=Prefs['debug_enable'])
    return engine.parse_title(s, siteNum)


def nCookies(siteNum):
    helper = CaptchaHelper(debug=Prefs['debug_enable'])
    return helper.get_verified_cookies(PAsearchSites.getSearchBaseURL(siteNum))


def any(s):
    for v in s:
        if v:
            return True
    return False


def cleanSummary(summary):
    replace = [(r'“', '\"'), (r'”', '\"'), (r'’', '\''), (r'W/', 'w/'), (r'A\.\sJ\.', 'A.J.'), (r'T\.\sJ\.', 'T.J.'), (r'(?<!\S)AJ(?!\S)', 'A.J.'), ('\xc2\xa0', ' ')]

    # Initialize to first word only being capitalized
    summary = summary.lower().capitalize()
    # Replace common issues
    for value in replace:
        summary = re.sub(value[0], value[1], summary, flags=re.IGNORECASE)
    # Add space after a punctuation if missing
    summary = re.sub(r'(?=[\!|\:|\?|\.](?=(\w{1,}))\b)\S(?!(co\b|net\b|com\b|org\b|porn\b|E\d|xxx\b))', lambda m: m.group(0) + ' ', summary, flags=re.IGNORECASE)
    # Remove space between word and punctuation
    summary = re.sub(r'\s+(?=[.,!:\'\)])', '', summary)
    # Remove space between punctuation and word
    summary = re.sub(r'(?<=[#\(])\s+', '', summary)
    # Override lowercase if word follows a punctuation
    summary = re.sub(ur'(?<!vs\.)(?<=!|:|\?|\.)(\s)(\S)', lambda m: m.group(1) + m.group(2).upper(), summary)
    # Add period to end of summary if no other punctuation present
    if re.search(r'.$(?<=(!|\.|\?))', summary) is None:
        summary = summary + '.'

    return summary


def manualWordFix(word):
    corrections_map = {
        'im': 'I\'m', 'theyll': 'They\'ll', 'cant': 'Can\'t', 'ive': 'I\'ve', 'shes': 'She\'s', 'theyre': 'They\'re', 'tshirt': 'T-Shirt', 'dont': 'Don\'t',
        'wasnt': 'Wasn\'t', 'youre': 'You\'re', 'ill': 'I\'ll', 'whats': 'What\'s', 'didnt': 'Didn\'t', 'isnt': 'Isn\'t', 'senor': 'Señor', 'senorita': 'Señorita',
        'thats': 'That\'s', 'gstring': 'G-String', 'milfs': 'MILFs', 'oreilly': 'O\'Reilly', 'bangbros': 'BangBros', 'bday': 'B-Day', 'dms': 'DMs', 'bffs': 'BFFs',
        'ohmy': 'OhMy', 'wont': 'Won\'t', 'whos': 'Who\'s', 'shouldnt': 'Shouldn\'t', 'lasirena': 'LaSirena', 'espanol': 'español', 'jmac': 'J-Mac', 'youd': 'You\'d',
        'redwolf': 'RedWolf'
    }

    pattern = re.compile(r'\d|\W')
    cleanWord = re.sub(pattern, '', word)
    cleanWordLower = cleanWord.lower()

    if cleanWordLower in corrections_map:
        correction = corrections_map[cleanWordLower]
        return re.sub(re.escape(cleanWord), correction, word, flags=re.IGNORECASE)

    return word


def cleanHTML(text):
    data = re.sub(r'<.*?>', '', text)
    data = HTMLParser().unescape(data)
    data = data.strip()

    return data


def getCleanSearchTitle(title):
    trashTitle = (
        'RARBG', 'COM', r'\d{3,4}x\d{3,4}', 'HEVC', r'H\d{3}', 'AVC', r'\dK',
        r'\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4', 'KLEENEX', 'SD', 'HD',
        'KTR', 'IEVA', 'WRB', 'NBQ', 'ForeverAloneDude', r'X\d{3}', 'SoSuMi',
        'sexors', 'gush', '3dh', 'lr', 'int'
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


def getDictValuesFromKey(dictDB, identifier):
    ident = str(identifier).lower()

    for key, values in dictDB.items():
        key_items = key if isinstance(key, tuple) else (key,)

        for item in key_items:
            if str(item).lower() == ident:
                return values

    return []


def getDictKeyFromValues(dictDB, identifier):
    ident = str(identifier).lower()
    result = []

    for key, values in dictDB.items():
        lower_values = [str(v).lower() for v in values]

        if ident in lower_values:
            result.append(key)

    return result


class MLStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = StringIO()
        self.skip_flag = False  # skip script/style content

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip_flag = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip_flag = False

    def handle_data(self, data):
        if not self.skip_flag:
            self.text.write(data)

    def handle_entityref(self, name):
        try:
            from htmlentitydefs import name2codepoint
        except ImportError:
            from html.entities import name2codepoint
        cp = name2codepoint.get(name)
        if cp:
            self.text.write(unichr(cp))

    def handle_charref(self, name):
        try:
            if name.startswith('x'):
                cp = int(name[1:], 16)
            else:
                cp = int(name)
            self.text.write(unichr(cp))
        except:
            pass

    def get_data(self):
        return self.text.getvalue()

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def functionTimer(fun, msg, *args):
    start_time = time.time()
    output = fun(*args)
    end_time = time.time()
    Log('%s: %s' % (msg, str(timedelta(seconds=(end_time - start_time)))))
    return output


def rreplace(s, r, n, o):
    li = s.rsplit(r, o)
    return n.join(li)
