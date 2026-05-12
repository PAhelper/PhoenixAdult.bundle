import hashlib


class CaptchaHelper(object):

    def __init__(self, debug=False):
        self.debug = debug
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

    @staticmethod
    def solve_pow(challenge, difficulty):
        """
        Find a nonce such that SHA-256(challenge + ':' + nonce)
        has `difficulty` leading zero bits.
        """
        target = 1 << (256 - difficulty)
        nonce = 0

        while True:
            s = "%s:%d" % (challenge, nonce)
            h = hashlib.sha256(s.encode('utf-8')).digest()

            # Convert digest to integer (big‑endian)
            h_int = int(h.encode('hex'), 16)

            if h_int < target:
                return nonce

            nonce += 1

    def get_verified_cookies(self, base_url):
        """
        Solve the homegrown PoW captcha and return a dict of verified session cookies.

        Returns None on failure. Returns an empty dict if the site doesn't actually
        present the captcha (already accessible).
        """
        base = base_url.rstrip('/')
        gallery_url = base + '/video/gallery'

        session = requests.Session()
        session.headers.update({
            'User-Agent': self.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        })

        try:
            r = session.get(gallery_url, timeout=15)
        except requests.RequestException as e:
            Log.Warn("get_verified_cookies: GET %s failed: %s" % (gallery_url, e))
            return None

        if r.status_code == 429:
            Log.Warn("get_verified_cookies: rate-limited on %s" % gallery_url)
            return None

        m = re.search(r"var\s+turnstileConfig\s*=\s*(\{.*?\});", r.text)
        if not m:
            return dict(session.cookies)

        try:
            config = json.loads(m.group(1))
            nonce = self.solve_pow(config['challenge'], config['difficulty'])
        except Exception as e:
            Log.Warn("get_verified_cookies: PoW solve failed for %s: %s" % (base, e))
            return None

        verify_url = base + '/turnstile/verify'
        payload = {
            'nonce': str(nonce),
            'timestamp': config['timestamp'],
            'difficulty': config['difficulty'],
            'environmentChecks': {
                'screenWidth': 1920,
                'screenHeight': 1080,
                'hasCanvas': True,
                'hasWebGL': True,
                'colorDepth': 24,
                'timezoneOffset': 300,
                'languages': 'en-US,en',
                'platform': 'Win32',
                'cookieEnabled': True,
            },
            'returnTo': config['returnTo'],
        }

        try:
            vr = session.post(
                verify_url,
                data=json.dumps(payload),
                headers={
                    'Content-Type': 'application/json',
                    'Referer': gallery_url,
                    'Origin': base,
                },
                timeout=15,
            )
        except requests.RequestException as e:
            Log.Warn("get_verified_cookies: POST %s failed: %s" % (verify_url, e))
            return None

        if vr.status_code != 200:
            Log.Warn("get_verified_cookies: verify POST returned %d for %s" % (vr.status_code, base))
            return None

        try:
            result = vr.json()
        except ValueError:
            Log.Warn("get_verified_cookies: non-JSON verify response for %s" % base)
            return None

        if not result.get('success'):
            Log.Warn("get_verified_cookies: verify failed for %s: %s" % (base, result))
            return None

        if self.debug:
            Log.Debug("get_verified_cookies: solved PoW for %s (nonce=%d)" % (base, nonce))
        return dict(session.cookies)
