import PAsearchSites


class Token(object):
    def __init__(self, text, kind):
        self.text = text
        self.kind = kind
        self.normalized = None


class TitleCaseEngine(object):

    # -----------------------------
    # CONSTANTS
    # -----------------------------

    WORD_RE = re.compile(r'\w+', re.UNICODE)
    SPACE_RE = re.compile(r'\s+', re.UNICODE)

    LOWER_EXCEPTIONS = set([
        'a', 'y', 'n', 'an', 'of', 'the', 'and', 'for', 'to', 'onto',
        'but', 'or', 'nor', 'at', 'with', 'vs', 'com', 'co', 'org',
    ])

    UPPER_EXCEPTIONS = set([
        'bbc', 'xxx', 'bbw', 'bf', 'bff', 'bts', 'pov', 'dp', 'gf', 'bj', 'wtf', 'cfnm', 'bwc', 'fm', 'tv',
        'hd', 'milf', 'gilf', 'dilf', 'dtf', 'zz', 'xxxl', 'usa', 'nsa', 'hr', 'ii', 'iii', 'iv', 'bbq',
        'avn', 'xtc', 'atv', 'joi', 'rpg', 'wunf', 'uk', 'asap', 'sss', 'nf', 'pawg', 'ama',
    ])

    ACRONYMS = set([
        'ai', 'vr', 'hd', 'uhd', 'sd', 'hdr', '4k', '3d', '2d',
    ])

    SIZE_CODES = set([
        'xs', 's', 'm', 'l', 'xl', 'xxl', 'xxxl', 'xxxxl'
    ])

    NAME_EXCEPTIONS = set([
        'ai'
    ])

    NAME_EXCEPTION_SITES = set([
        '912', '13671' '1411', '1600', '1685'
    ])

    CONTRACTION_EXCEPTIONS = set([
        're', 't', 's', 'd', 'll', 've', 'm', 'am', 'ed'
    ])

    SYMBOLS = set(['-', '/', '.', '+', '\''])

    SYMBOL_RULES = {
        '-': {'join': True, 'treat_as': 'compound'},
        '/': {'join': True, 'treat_as': 'compound'},
        '.': {'join': True, 'treat_as': 'initials_or_acronym'},
        '+': {'join': True, 'treat_as': 'compound'},
        '\'': {'join': True, 'treat_as': 'contraction'},
    }

    MANUAL_CORRECTIONS = {
        'im': 'I\'m', 'theyll': 'They\'ll', 'cant': 'Can\'t', 'ive': 'I\'ve', 'shes': 'She\'s', 'theyre': 'They\'re', 'tshirt': 'T-Shirt', 'dont': 'Don\'t',
        'wasnt': 'Wasn\'t', 'youre': 'You\'re', 'ill': 'I\'ll', 'whats': 'What\'s', 'didnt': 'Didn\'t', 'isnt': 'Isn\'t', 'senor': 'Señor', 'senorita': 'Señorita',
        'thats': 'That\'s', 'gstring': 'G-String', 'milfs': 'MILFs', 'oreilly': 'O\'Reilly', 'bangbros': 'BangBros', 'bday': 'B-Day', 'dms': 'DMs', 'bffs': 'BFFs',
        'ohmy': 'OhMy', 'wont': 'Won\'t', 'whos': 'Who\'s', 'shouldnt': 'Shouldn\'t', 'lasirena': 'LaSirena', 'espanol': 'español', 'jmac': 'J-Mac', 'youd': 'You\'d',
        'redwolf': 'RedWolf', 'mccray': 'McCray', 'mccullough': 'McCullough', 'mccall': 'McCall', 'mccarthy': 'McCarthy',
    }

    POST_PROCESS_RULES = [
        # Normalize curly quotes
        (r'“', '"', 0),
        (r'”', '"', 0),
        (r'’', '\'', 0),
        # Rotate trailing ", the/a/an" to front
        (r'^(.*?)(,\s*(the|a|an))$', lambda m: m.group(3).capitalize() + ' ' + m.group(1), re.IGNORECASE),
        # Add missing space after ! : ? (but not before domains)
        (r'(?<=[!:\?])(?=\w)(?!(co\b|net\b|com\b|org\b|porn\b|E\d|xxx\b))', ' ', re.IGNORECASE),
        # Add missing space after period when followed by a letter (not domains)
        (r'(?<=\.)(?=[A-Za-z])(?!co\b|net\b|com\b|org\b|porn\b|E\d|xxx\b)', ' ', re.IGNORECASE),
        # Remove stray period at end of title (but not ".." etc.)
        (r'(?<!\.)\.$', '', 0),
        # Remove space before punctuation
        (r'\s+(?=[.,!\'\)]|(:(?!\))))', '', 0),
        # Add space before opening double quote
        (r'(?<=\S)(["]\S+)', lambda m: ' ' + m.group(1), 0),
        # Add space before opening single quote, capitalizing if not a contraction
        (r'(?<=\S)(\'(?!re\b|t\b|s\b|d\b|ll\b|ve\b|m\b|am\b|ed\b)\S+)(?=.*\')', lambda m: ' ' + m.group(1)[0] + m.group(1)[1:].capitalize(), 0),
        # Remove space after certain opening punctuation
        (r'(?<=[#\("\[])\s+', '', 0),
        # Add space after closing double quote (only when balanced)
        (r'"(?!\s)(?=(?:(?:[^"]*"){2})*[^"]*$)', '" ', 0),
        # Capitalize word after punctuation
        (ur'(?<!vs\.)(?<=!|:|\?|\.|-|\u2013)(\s)(\S)', lambda m: m.group(1) + m.group(2).upper(), 0),
        # Capitalize word after certain opening punctuation
        (r'(?<=[\(|\&|\"|\[|\*|\~])(\w)', lambda m: m.group(0).upper(), 0),
        # Capitalize last word in a section
        (r'\S+[\]\)\"\~\:]', lambda m: m.group(0)[0].capitalize() + m.group(0)[1:], 0),
        # Capitalize final word
        (r'\S+$', lambda m: m.group(0)[0].capitalize() + m.group(0)[1:], 0),
        # Add period for initials like "A. B"
        (r'^\w\.\s\w(?=$)', lambda m: m.group(0) + '.', 0),
        # Remove space between initials "A. B." → "A.B."
        (r'^(\w\.)\s(\w\.)', lambda m: m.group(1) + m.group(2), 0),
    ]

    # -----------------------------
    # INIT
    # -----------------------------

    def __init__(self, title_type, debug=False):
        self.debug = debug
        self.title_type = title_type
        self.nonword_re = re.compile(r'\W', re.UNICODE)
        self.manual_fix_cache = {}

    def trace(self, *args):
        if self.debug:
            msg = ' '.join((a if isinstance(a, basestring) else str(a)).encode('utf-8') for a in args)
            Log.Debug('%s: %s - %s', 'PAparseTitle', self.title_type, msg)

    # -----------------------------
    # PUBLIC API
    # -----------------------------

    def parse_title(self, s, siteNum):
        s = self.pre_process(s)
        tokens = self.tokenize(s)
        tokens = self.apply_word_rules(tokens, siteNum)
        output = self.reconstruct(tokens)
        output = self.post_process(output)
        return output

    # -----------------------------
    # PRE-PROCESS
    # -----------------------------

    def pre_process(self, s):
        s = s.replace('_', ' ')
        s = s.replace('’', '\'').replace('´', '\'')
        s = re.sub(r'w\/(?!\s)', 'w/ ', s, flags=re.IGNORECASE)
        s = re.sub(r'\,(?![\s|\d])', ', ', s)
        s = s.replace('\xc2\xa0', ' ')
        return s

    # -----------------------------
    # TOKENIZER
    # -----------------------------

    def tokenize(self, s):
        tokens = []
        i = 0
        length = len(s)

        while i < length:
            ch = s[i]

            # SPACE
            if ch.isspace():
                j = i + 1
                while j < length and s[j].isspace():
                    j += 1
                tok = Token(s[i:j], 'space')
                tokens.append(tok)
                self.trace('TOKEN(space):', tok.text)
                i = j
                continue

            # WORD (letters, digits, apostrophes inside words)
            if ch.isalnum():
                j = i + 1
                while j < length and (s[j].isalnum() or s[j] == '\''):
                    j += 1
                tok = Token(s[i:j], 'word')
                tokens.append(tok)
                self.trace('TOKEN(word):', tok.text)
                i = j
                continue

            # APOSTROPHE
            if ch == '\'':
                # If between alnum characters, merge into previous word
                if i > 0 and i + 1 < length and s[i - 1].isalnum() and s[i + 1].isalnum():
                    prev = tokens[-1]
                    prev.text = prev.text + '\''
                    i += 1
                    continue

                # Standalone apostrophe
                tok = Token('\'', 'symbol')
                tokens.append(tok)
                self.trace('TOKEN(symbol):', tok.text)
                i += 1
                continue

            # EVERYTHING ELSE = punctuation
            tok = Token(ch, 'punct')
            tokens.append(tok)
            self.trace('TOKEN(punct):', tok.text)
            i += 1

        return tokens

    # -----------------------------
    # MISSING BUILT-INS
    # -----------------------------

    def next(self, iterable, default=None):
        for item in iterable:
            return item
        return default

    def any(self, iterable):
        for item in iterable:
            if item:
                return True
        return False

    # -----------------------------
    # WORD RULE ENGINE
    # -----------------------------

    def apply_word_rules(self, tokens, siteNum):
        site_name = PAsearchSites.getSearchSiteName(siteNum)
        clean_site = self.nonword_re.sub('', site_name.replace(' ', '')).lower()

        for idx, token in enumerate(tokens):
            if token.kind != 'word':
                continue
            token.normalized = self.normalize_word(token.text, idx, tokens, site_name, siteNum, clean_site)

        self.capitalize_first_word(tokens)
        return tokens

    def is_acronym_or_size(self, clean_lower, clean_word, siteNum):
        if clean_lower in self.NAME_EXCEPTIONS and siteNum in self.NAME_EXCEPTION_SITES:
            return False, None

        if clean_lower in self.LOWER_EXCEPTIONS:
            return False, None

        if self.title_type == 'name':
            return False, None

        if clean_lower in self.SIZE_CODES:
            return True, clean_word.upper()

        if clean_lower in self.ACRONYMS:
            return True, clean_word.upper()

        if 2 <= len(clean_word) <= 4 and clean_word.upper() == clean_word:
            return True, clean_word.upper()

        return False, None

    def normalize_word(self, word, idx, tokens, site_name, siteNum, clean_site):

        clean_word = self.nonword_re.sub('', word)
        clean_lower = clean_word.lower()

        self.trace('FSM(word):', word)

        # Site name match
        if clean_site and clean_lower == clean_site:
            self.trace(' -> RULE: site match')
            return self.manual_word_fix(site_name)

        # Symbol-containing word
        symbol = self.next((s for s in self.SYMBOLS if s in word), None)
        if symbol:
            self.trace(' -> RULE: symbol word')
            return self.manual_word_fix(self.handle_symbol_word(word, site_name, siteNum))

        # Contraction handling
        if '\'' in word:
            base, _, suffix = word.partition('\'')
            clean_suffix = self.nonword_re.sub('', suffix).lower()
            if clean_suffix in self.CONTRACTION_EXCEPTIONS:
                self.trace(' -> RULE: contraction')
                base_norm = self.normalize_word(base, idx, tokens, site_name, siteNum, clean_site)
                return base_norm + '\'' + clean_suffix

        # Acronym / size code
        is_special, special_val = self.is_acronym_or_size(clean_lower, clean_word, siteNum)
        if is_special:
            self.trace(' -> RULE: acronym/size')
            return self.manual_word_fix(special_val)

        # Explicit upper exceptions
        if clean_lower in self.UPPER_EXCEPTIONS:
            self.trace(' -> RULE: upper exception')
            return self.manual_word_fix(word.upper())

        # Force upper if all caps and not a lower exception
        if clean_word and clean_word.isupper() and clean_lower not in self.LOWER_EXCEPTIONS:
            self.trace(' -> RULE: force upper')
            return self.manual_word_fix(word.upper())

        # Explicit lower exceptions
        if clean_lower in self.LOWER_EXCEPTIONS:
            self.trace(' -> RULE: lower exception')
            return self.manual_word_fix(word.lower())

        # Brand/stylized casing: mixed case, leave as-is (then manual fix)
        if self.any(c.islower() for c in list(word)) and self.any(c.isupper() for c in list(word)):
            self.trace(' -> RULE: mixed-case brand')
            return self.manual_word_fix(word)

        # Default: capitalize
        self.trace(' -> RULE: default capitalize')
        return self.manual_word_fix(word.capitalize())

    # -----------------------------
    # SYMBOL HANDLER
    # -----------------------------

    def handle_symbol_word(self, word, site_name, siteNum):
        self.trace('SYMBOL-HANDLER:', word)

        symbol = None
        for s in self.SYMBOLS:
            if s in word:
                symbol = s
                break

        if not symbol:
            self.trace(' -> No symbol found')
            return word

        rule = self.SYMBOL_RULES.get(symbol, {'join': True, 'treat_as': 'compound'})
        self.trace(' -> Symbol:', symbol, 'Rule:', rule)

        parts = word.split(symbol)
        sep = symbol if rule['join'] else ''

        result_parts = []

        for idx, part in enumerate(parts):
            clean = self.nonword_re.sub('', part)
            lower_clean = clean.lower()

            self.trace('   PART:', part)

            if not part:
                result_parts.append(part)
                continue

            if rule['treat_as'] == 'contraction' and lower_clean in self.CONTRACTION_EXCEPTIONS:
                self.trace('    -> contraction part')
                norm = part.lower()

            elif rule['treat_as'] == 'initials_or_acronym' and len(clean) == 1:
                self.trace('    -> initial')
                norm = clean.upper()

            else:
                self.trace('    -> apply normalize_word')
                norm = self.normalize_word(part, idx, None, site_name, siteNum, None)

            norm = self.manual_word_fix(norm)
            result_parts.append(norm)

        final = sep.join(result_parts)
        self.trace('SYMBOL-HANDLER RESULT:', final)
        return final

    # -----------------------------
    # FIRST WORD CAPITALIZATION
    # -----------------------------

    def capitalize_first_word(self, tokens):
        for token in tokens:
            if token.kind == 'word':
                text = token.normalized or token.text
                clean = self.nonword_re.sub('', text)
                if not clean:
                    return
                if len(clean) > 1:
                    token.normalized = text[0].upper() + text[1:]
                else:
                    token.normalized = text.upper()
                return

    # -----------------------------
    # MANUAL WORD FIX
    # -----------------------------

    def manual_word_fix(self, word):
        cached = self.manual_fix_cache.get(word)
        if cached is not None:
            return cached

        clean = self.nonword_re.sub('', word).lower()

        if clean in self.MANUAL_CORRECTIONS:
            corrected = self.MANUAL_CORRECTIONS[clean]
            self.trace('MANUAL-FIX:', word, '->', corrected)
            fixed = re.sub(re.escape(clean), corrected, word, flags=re.IGNORECASE)
            self.manual_fix_cache[word] = fixed
            return fixed

        self.manual_fix_cache[word] = word
        return word

    # -----------------------------
    # RECONSTRUCT
    # -----------------------------

    def reconstruct(self, tokens):
        parts = []
        for t in tokens:
            parts.append(t.normalized if t.normalized is not None else t.text)
        return ''.join(parts)

    # -----------------------------
    # POST-PROCESS
    # -----------------------------

    def post_process(self, output):
        self.trace('POST-PROCESS START:', output)

        for pattern, repl, flags in self.POST_PROCESS_RULES:
            new_output = re.sub(pattern, repl, output, flags=flags)
            if new_output != output:
                self.trace('RULE HIT:', pattern, '->', new_output)
            output = new_output

        self.trace('POST-PROCESS END:', output)
        return output
