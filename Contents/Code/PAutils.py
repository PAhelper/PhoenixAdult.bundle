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
    stop = kwargs.pop('stop', 10)
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
    s = re.sub(r'\,(?![\s|\d])', ', ', s)
    s = s.replace('_', ' ')
    s = s.replace('’', '\'')
    s = s.replace('´', '\'')
    s = preParseTitle(s)
    word_list = re.split(' ', s)

    pattern = re.compile(r'\W')
    firstWord = parseWord(word_list[0], siteNum)
    cleanfirstWord = re.sub(pattern, '', firstWord)
    if len(cleanfirstWord) > 1:
        firstWord = firstWord[0].capitalize() + firstWord[1:]
    else:
        firstWord = firstWord.upper()

    final = [firstWord]

    for word in word_list[1:]:
        final.append(parseWord(word, siteNum))

    output = ' '.join(final)
    output = postParseTitle(output)

    return output


def parseWord(word, siteNum):
    lower_exceptions = ['a', 'y', 'n', 'an', 'of', 'the', 'and', 'for', 'to', 'onto', 'but', 'or', 'nor', 'at', 'with', 'vs', 'in', 'on', 'com', 'co', 'org']
    upper_exceptions = (
        'bbc', 'xxx', 'bbw', 'bf', 'bff', 'bts', 'pov', 'dp', 'gf', 'bj', 'wtf', 'cfnm', 'bwc', 'fm', 'tv', 'ai',
        'hd', 'milf', 'gilf', 'dilf', 'dtf', 'zz', 'xxxl', 'usa', 'nsa', 'hr', 'ii', 'iii', 'iv', 'bbq', 'avn', 'xtc', 'atv',
        'joi', 'rpg', 'wunf', 'uk', 'asap', 'sss', 'nf', 'pawg', 'ama'
    )
    symbolsClean = ['-', '/', '.', '+', '\'']
    symbolsEsc = ['-', '/', r'\.', r'\+', r'\'']

    pattern = re.compile(r'\W')
    cleanWord = re.sub(pattern, '', word)
    cleanSiteName = re.sub(pattern, '', PAsearchSites.getSearchSiteName(siteNum).replace(' ', ''))

    if cleanSiteName.lower() == cleanWord.lower():
        word = PAsearchSites.getSearchSiteName(siteNum)
    elif any(symbol in word for symbol in symbolsClean):
        for idx, symbol in enumerate(symbolsClean, 0):
            if symbol in word:
                word = parseTitleSymbol(word, siteNum, symbolsEsc[idx])
    elif cleanWord.lower() in upper_exceptions:
        word = word.upper()
    elif cleanWord.isupper() and cleanWord.lower() not in lower_exceptions:
        word = word.upper()
    elif not (cleanWord.islower() or cleanWord.isupper() or cleanWord.lower() in lower_exceptions):
        pass
    else:
        word = word.lower() if cleanWord.lower() in lower_exceptions else word.capitalize()

    word = manualWordFix(word)

    return word


def any(s):
    for v in s:
        if v:
            return True
    return False


def parseTitleSymbol(word, siteNum, symbol):
    lower_exceptions = ['vs']
    contraction_exceptions = ['re', 't', 's', 'd', 'll', 've', 'm', 'am', 'ed']
    word_list = re.split(symbol, word)
    symbols = ['-', '/', r'\.', r'\+']
    pattern = re.compile(r'\W')

    firstWord = parseWord(word_list[0], siteNum)
    if firstWord not in lower_exceptions:
        if re.search(r'^\W', firstWord):
            firstWord = firstWord[0:2].upper() + firstWord[2:]
        elif len(firstWord) > 1:
            firstWord = firstWord[0].capitalize() + firstWord[1:]
        else:
            firstWord = firstWord.upper()
    nhword = firstWord + symbol.replace('\\', '')

    for idx, hword in enumerate(word_list[1:], 1):
        cleanWord = re.sub(pattern, '', hword)
        if symbol in symbols:
            if idx == 1 and not firstWord:
                nhword += hword.capitalize()
            elif len(hword) > 1:
                nhword += parseWord(hword, siteNum)
            else:
                nhword += hword.capitalize()
        elif cleanWord.lower() in contraction_exceptions:
            nhword += hword.lower()
        else:
            nhword += parseWord(hword, siteNum)

        if idx != len(word_list) - 1:
            nhword += symbol.replace('\\', '')
    return nhword


def postParseTitle(output):
    replace = [(r'“', '\"'), (r'”', '\"'), (r'’', '\''), (r'W/', 'w/'), (r'A\.\sJ\.', 'A.J.'), (r'T\.\sJ\.', 'T.J.'), (r'(?<!\S)AJ(?!\S)', 'A.J.')]
    lower_exceptions = ['a', 'y', 'n', 'an', 'of', 'the', 'and', 'for', 'to', 'onto', 'but', 'or', 'nor', 'at', 'with', 'vs', 'com', 'co', 'org']

    # Add space after a punctuation if missing
    output = re.sub(r'(?=[\!|\:|\?|\.](?=(\w{2,}))\b)\S(?!(co\b|net\b|com\b|org\b|porn\b|E\d|xxx\b))', lambda m: m.group(0) + ' ', output, flags=re.IGNORECASE)
    # Remove single period at end of title
    output = re.sub(r'(?<=[^\.].)(?<=\w)(?:\.)$', '', output)
    # Remove space between word and certain punctuation
    output = re.sub(r'\s+(?=[.,!\'\)]|(:(?!\))))', '', output)
    # Add space between word and opening quote
    output = re.sub(r'(?<=\S)([\"]\S+)', lambda m: ' ' + m.group(1), output)
    # Remove space between punctuation and word
    output = re.sub(r'(?<=[#\(\"])\s+', '', output)
    # Add space after closing double quote
    output = re.sub(r'"(?!\s)(?=(?:(?:[^"]*"){2})*[^"]*$)', '" ', output)
    # Override lowercase if word follows a punctuation
    output = re.sub(ur'(?<!vs\.)(?<=!|:|\?|\.|-|\u2013)(\s)(\S)', lambda m: m.group(1) + m.group(2).upper(), output)
    # Override lowercase if word follows certain punctuation
    output = re.sub(r'(?<=[\(|\&|\"|\[|\*|\~])(\w)', lambda m: m.group(0).upper() + m.group(1)[1:] if m.group(1).lower() not in lower_exceptions else m.group(1), output)
    # Override lowercase if last word in section
    output = re.sub(r'\S+[\]\)\"\~\:]', lambda m: m.group(0)[0].capitalize() + m.group(0)[1:], output)
    # Override lowercase if last word
    output = re.sub(r'\S+$', lambda m: m.group(0)[0].capitalize() + m.group(0)[1:], output)
    # Add period at end of string for Initials
    output = re.sub(r'^\w\.\s\w(?<=$)', lambda m: m.group(0) + '.', output)
    # Remove space between initials
    output = re.sub(r'^(\w\.)\s(\w\.)', lambda m: m.group(1) + m.group(2), output)

    if re.search(r'(,\sthe)(?=:|\s\()', output, re.IGNORECASE):
        output = re.sub(r'(,\sthe)(?=:|\s\()', '', output, flags=re.IGNORECASE)
        output = 'The ' + output
    elif re.search(r'(,\sthe)$', output, re.IGNORECASE):
        output = re.sub(r'(,\sthe)$', '', output, flags=re.IGNORECASE)
        output = 'The ' + output
    elif re.search(r'(,\sA)$', output, re.IGNORECASE):
        output = re.sub(r'(,\sA)$', '', output, flags=re.IGNORECASE)
        output = 'A ' + output

    for value in replace:
        output = output.replace(value[0], value[1])

    return output


def preParseTitle(input):
    exceptions_corrections = {
        (r'(?<!\S)t\sshirt', 'tshirt'), (r'j\smac|jmac', 'jmac'), (r'\bmr(?=\s)', 'mr.'), (r'\bmrs(?=\s)', 'mrs.'),
        (r'\bms(?=\s)', 'ms.'), (r'\bdr(?=\s)', 'dr.'), (r'\bvs(?=\s)', 'vs.'), (r'\bst(?=\s)', 'st.'), (r'\s\s+', ' '),
        (r'\bvol(?=\s)', 'vol.')
    }

    output = input.replace('\xc2\xa0', ' ')

    for value in exceptions_corrections:
        output = re.sub(value[0], value[1], output, flags=re.IGNORECASE)

    return output


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
    exceptions = (
        'im', 'theyll', 'cant', 'ive', 'shes', 'theyre', 'tshirt', 'dont', 'wasnt', 'youre', 'ill', 'whats', 'didnt',
        'isnt', 'senor', 'senorita', 'thats', 'gstring', 'milfs', 'oreilly', 'bangbros', 'bday', 'dms', 'bffs',
        'ohmy', 'wont', 'whos', 'shouldnt', 'lasirena', 'espanol', 'youd'
    )
    corrections = (
        'I\'m', 'They\'ll', 'Can\'t', 'I\'ve', 'She\'s', 'They\'re', 'T-Shirt', 'Don\'t', 'Wasn\'t', 'You\'re', 'I\'ll', 'What\'s', 'Didn\'t',
        'Isn\'t', 'Señor', 'Señorita', 'That\'s', 'G-String', 'MILFs', 'O\'Reilly', 'BangBros', 'B-Day', 'DMs', 'BFFs',
        'OhMy', 'Won\'t', 'Who\'s', 'Shouldn\'t', 'LaSirena', 'español', 'You\'d'
    )
    pattern = re.compile(r'\d|\W')
    cleanWord = re.sub(pattern, '', word)

    if cleanWord.lower() in exceptions:
        for correction in corrections:
            if cleanWord.lower() == re.sub(pattern, '', correction.replace('ñ', 'n')).lower():
                return re.sub(re.escape(cleanWord), correction, word)

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
    for key, values in dictDB.items():
        keys = list(key) if type(key) == tuple else [key]
        for key in keys:
            if str(key).lower() == str(identifier).lower():
                return values

    return []


def getDictKeyFromValues(dictDB, identifier):
    keys = []
    for key, values in dictDB.items():
        for item in values:
            if str(item).lower() == str(identifier).lower():
                keys.append(key)
                break

    return keys


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def functionTimer(fun, msg, *args):
    start_time = time.time()
    fun(*args)
    end_time = time.time()
    Log('%s: %s' % (msg, str(timedelta(seconds=(end_time - start_time)))))


def rreplace(s, r, n, o):
    li = s.rsplit(r, o)
    return n.join(li)
