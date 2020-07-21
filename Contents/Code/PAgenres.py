class PhoenixGenres:
    genresTable = None
    genresNum = 0

    def __init__(self):
        self.genresTable = [None] * 150
        self.genresNum = 0

    def addGenre(self, newGenre):
        self.genresTable[self.genresNum] = newGenre
        self.genresNum = self.genresNum + 1

    def clearGenres(self):
        self.genresNum = 0

    def processGenres(self, metadata):
        genresProcessed = 0
        while genresProcessed < self.genresNum:
            skip = False
            newGenre = self.genresTable[genresProcessed].replace('"', '').strip()

            # Skips
            # Match and Skip
            if 'photos' == newGenre.lower():
                skip = True
            elif '4k' == newGenre.lower():
                skip = True
            elif '18+teens' == newGenre.lower():
                skip = True
            elif '18+ teens' == newGenre.lower():
                skip = True
            elif 'babes' == newGenre.lower():
                skip = True
            elif 'bonus' == newGenre.lower():
                skip = True
            elif 'gonzo' == newGenre.lower():
                skip = True
            elif 'hd videos' == newGenre.lower():
                skip = True
            elif 'show less' == newGenre.lower():
                skip = True
            elif 'show more' == newGenre.lower():
                skip = True
            elif 'episode' in newGenre.lower():
                skip = True
            elif '60p' == newGenre.lower():
                skip = True
            elif 'acworthy' == newGenre.lower():
                skip = True
            elif 'april' == newGenre.lower():
                skip = True
            elif 'april showers' == newGenre.lower():
                skip = True
            elif 'beaverday' == newGenre.lower():
                skip = True
            elif 'van styles' == newGenre.lower():
                skip = True
            elif 'yes, mistress' == newGenre.lower():
                skip = True
            elif 'tj cummings' == newGenre.lower():
                skip = True
            elif 'tony' == newGenre.lower():
                skip = True
            elif 'the pope' == newGenre.lower():
                skip = True
            elif 'mr. cummings' == newGenre.lower():
                skip = True
            elif 'keiran' == newGenre.lower():
                skip = True
            elif 'exclusive' == newGenre.lower():
                skip = True
            elif 'babe' == newGenre.lower():
                skip = True
            elif 'smart' == newGenre.lower():
                skip = True
            elif 'ryan mclane' == newGenre.lower():
                skip = True
            elif 'destruction' == newGenre.lower():
                skip = True
            elif 'site member' == newGenre.lower():
                skip = True
            elif 'st patrick\'s day' == newGenre.lower():
                skip = True
            elif 'workitout' == newGenre.lower():
                skip = True
            elif 'little runaway' == newGenre.lower():
                skip = True
            elif 'feel me' == newGenre.lower():
                skip = True
            elif 'get sprung' == newGenre.lower():
                skip = True
            elif 'daylight savings' == newGenre.lower():
                skip = True
            elif 'heavymetal' == newGenre.lower():
                skip = True
            elif 'public disgrace\'s best' == newGenre.lower():
                skip = True
            elif 'faces of pain' == newGenre.lower():
                skip = True
            elif 'tyler steele' == newGenre.lower():
                skip = True
            elif 'wow girls special' == newGenre.lower():
                skip = True
            elif 'spring cleaning' == newGenre.lower():
                skip = True
            elif 'irreconcilable slut' == newGenre.lower():
                skip = True
            elif 'desert apocalypse' == newGenre.lower():
                skip = True
            elif 'grey' == newGenre.lower():
                skip = True
            elif 'twistys hard' == newGenre.lower():
                skip = True
            elif 'extra update' == newGenre.lower():
                skip = True

            # Search and Skip
            if '5k' in newGenre.lower():
                skip = True
            elif '60fps' in newGenre.lower():
                skip = True
            elif 'hd' in newGenre.lower():
                skip = True
            elif '1080p' in newGenre.lower():
                skip = True
            elif 'aprilfools' in newGenre.lower():
                skip = True
            elif 'chibbles' in newGenre.lower():
                skip = True
            elif 'folsom' in newGenre.lower():
                skip = True

            # Replace
            if 'atm' == newGenre.lower():
                newGenre = 'Ass to Mouth'
            elif 'big ass' == newGenre.lower() or 'big booty' == newGenre.lower() or 'bib booty' == newGenre.lower() or 'girl big ass' == newGenre.lower() or 'big butts' == newGenre.lower() or 'fat ass' == newGenre.lower():
                newGenre = 'Big Butt'
            elif '3some' == newGenre.lower() or '3 way' == newGenre.lower() or '2-on-1' == newGenre.lower() or '2on1' == newGenre.lower() or '2 on 1' == newGenre.lower() or 'threesomes' == newGenre.lower():
                newGenre = 'threesome'
            elif 'ball licking' == newGenre.lower() or 'ball sucking' == newGenre.lower() or 'ball lick' == newGenre.lower():
                newGenre = 'ball licking'
            elif 'big cock' == newGenre.lower() or 'big cocks' == newGenre.lower() or 'big dicks' == newGenre.lower() or '2 big cocks' == newGenre.lower():
                newGenre = 'big dick'
            elif 'bikin' == newGenre.lower():
                newGenre = 'bikini'
            elif 'big boobs' == newGenre.lower() or 'bit tits' == newGenre.lower() or 'girl big tits' == newGenre.lower() or 'large tits' == newGenre.lower():
                newGenre = 'big tits'
            elif 'black' == newGenre.lower() or 'black girl' == newGenre.lower() or 'dark skin' == newGenre.lower() or 'african american' == newGenre.lower():
                newGenre = 'ebony'
            elif 'shaved pussy' == newGenre.lower() or 'bald pussy' == newGenre.lower() or 'shaved' == newGenre.lower():
                newGenre = 'shaven pussy'
            elif 'blowjob' == newGenre.lower() or 'blowjob (pov)' == newGenre.lower() or 'blowjob (double)' == newGenre.lower() or 'bj' == newGenre.lower() or 'amateur blowjobs' == newGenre.lower() or 'blowjobs' == newGenre.lower() or 'blowjob - pov' == newGenre.lower() or 'blow jobs' == newGenre.lower() or 'blowjob - double' == newGenre.lower():
                newGenre = 'blow job'
            elif 'handjob' == newGenre.lower() or 'handjob (pov)' == newGenre.lower() or 'handjobs' == newGenre.lower() or 'handjob - pov' == newGenre.lower():
                newGenre = 'hand job'
            elif 'tittyfuck (pov)' == newGenre.lower() or 'tittyfuck' == newGenre.lower() or 'tit fuck' == newGenre.lower() or 'titty fucking' == newGenre.lower() or 'tittyfuck - pov' == newGenre.lower() or 'tit fucking' == newGenre.lower():
                newGenre = 'titty fuck'
            elif 'deepthroat' == newGenre.lower() or 'deepthroating' == newGenre.lower():
                newGenre = 'deep throat'
            elif 'dp' == newGenre.lower() or 'double penetration' == newGenre.lower() or 'double penetraton (dp)' == newGenre.lower():
                newGenre = 'Double Penetration (DP)'
            elif 'face fuck' == newGenre.lower() or 'facefucking' == newGenre.lower():
                newGenre = 'face fucking'
            elif 'facesitting' == newGenre.lower() or 'queening' == newGenre.lower():
                newGenre = 'face sitting'
            elif 'facial (multiple)' == newGenre.lower() or 'facial (pov)' == newGenre.lower() or 'cumshot facial' == newGenre.lower() or 'open mouth facial' == newGenre.lower() or 'facials' == newGenre.lower() or 'facial - pov' == newGenre.lower():
                newGenre = 'Facial'
            elif 'cum-in-mouth' == newGenre.lower():
                newGenre = 'Cum In Mouth'
            elif 'cumshot' == newGenre.lower():
                newGenre = 'cum shot'
            elif 'hairy' == newGenre.lower() or 'hairy bush' == newGenre.lower() or 'bush' == newGenre.lower():
                newGenre = 'hairy pussy'
            elif 'hardcore sex' == newGenre.lower():
                newGenre = 'hardcore'
            elif 'outdoor' == newGenre.lower():
                newGenre = 'outdoors'
            elif 'indoor' == newGenre.lower():
                newGenre = 'indoors'
            elif 'stepdaughter' == newGenre.lower():
                newGenre = 'step daughter'
            elif 'stepmom' == newGenre.lower():
                newGenre = 'step mom'
            elif 'stepsister' == newGenre.lower() or 'stepsis' == newGenre.lower() or 'step sis' == newGenre.lower() or 'ste sister' == newGenre.lower() or 'step siter' == newGenre.lower() or 'step-sister' == newGenre.lower():
                newGenre = 'step sister'
            elif 'tattoos' == newGenre.lower() or 'tattoo girl' == newGenre.lower() or 'tattooed' == newGenre.lower():
                newGenre = 'tattoo'
            elif 'white' == newGenre.lower() or 'white girl' == newGenre.lower() or 'while' == newGenre.lower():
                newGenre = 'Caucasian'
            elif 'amatuer' == newGenre.lower() or 'amateur pre auditions' == newGenre.lower():
                newGenre = 'amateur'
            elif 'cumswap' == newGenre.lower() or 'cum swapping' == newGenre.lower():
                newGenre = 'cum swap'
            elif 'euro' == newGenre.lower() or 'europe' == newGenre.lower():
                newGenre = 'european'
            elif 'enhanced' == newGenre.lower() or 'enhanced tits' == newGenre.lower() or 'silicone tits' == newGenre.lower() or 'fake boobs' == newGenre.lower():
                newGenre = 'fake tits'
            elif 'trimmed' == newGenre.lower() or 'trimmed bush' == newGenre.lower():
                newGenre = 'trimmed pussy'
            elif 'pse' == newGenre.lower():
                newGenre = 'Pornstar Experience'
            elif 'gfe' == newGenre.lower():
                newGenre = 'Girlfriend Experience'
            elif 'blond' == newGenre.lower() or 'blonde hair' == newGenre.lower() or 'blondes' == newGenre.lower() or 'blond hair' == newGenre.lower():
                newGenre = 'Blonde'
            elif 'blowbang' == newGenre.lower():
                newGenre = 'Blow Bang'
            elif 'big beauteliful women' == newGenre.lower():
                newGenre = 'BBW'
            elif 'big areolas' == newGenre.lower():
                newGenre = 'Big Nipples'
            elif 'buttplug' == newGenre.lower() or 'anal plug' == newGenre.lower():
                newGenre = 'Butt Plug'
            elif 'ts' == newGenre.lower() or 'transexual' == newGenre.lower() or 'trans' == newGenre.lower():
                newGenre = 'Transsexual'
            elif 'squirt' == newGenre.lower() or 'top squirting videos' == newGenre.lower():
                newGenre = 'Squirting'
            elif 'big naturals' == newGenre.lower():
                newGenre = 'Big Natural Tits'
            elif 'medium boobs' == newGenre.lower():
                newGenre = 'Medium Tits'
            elif 'no condom' == newGenre.lower():
                newGenre = 'bareback'
            elif 'piercings' == newGenre.lower():
                newGenre = 'piercing'
            elif 'pussy lick' == newGenre.lower() or 'pussy licking' == newGenre.lower() or 'cunilingus' == newGenre.lower():
                newGenre = 'Pussy Eating'
            elif 'completely naked' == newGenre.lower() or 'naked' == newGenre.lower():
                newGenre = 'Nude'
            elif 'boot' == newGenre.lower():
                newGenre = 'Boots'
            elif 'older / younger' == newGenre.lower():
                newGenre = 'older/younger'
            elif 'milfs' == newGenre.lower():
                newGenre = 'milf'
            elif 'mature & milf' == newGenre.lower():
                newGenre = 'Milf & Mature'
            elif 'sex toys' == newGenre.lower() or 'toy insertions' == newGenre.lower():
                newGenre = 'toys'
            elif 'interviews' == newGenre.lower():
                newGenre = 'interview'
            elif 'skirts' == newGenre.lower():
                newGenre = 'skirt'
            elif 'brown hair' == newGenre.lower() or 'brunettes' == newGenre.lower() or 'brunet' == newGenre.lower():
                newGenre = 'Brunette'
            elif 'brutal cuckolding' == newGenre.lower() or 'cuckolding' == newGenre.lower():
                newGenre = 'Cuckold'
            elif 'small boobs' == newGenre.lower():
                newGenre = 'Small Tits'
            elif 'nurse' == newGenre.lower() or 'doctor' == newGenre.lower() or 'nurse play' == newGenre.lower() or 'doctor/nurse' == newGenre.lower():
                newGenre = 'Medical Fetish'
            elif 'electrical play' == newGenre.lower() or 'electrode punishments' == newGenre.lower():
                newGenre = 'Electro Play'
            elif 'chastity' == newGenre.lower():
                newGenre = 'Chastity Play'
            elif 'cum swallow' == newGenre.lower() or 'swallow cum' == newGenre.lower() or 'swallowing cum' == newGenre.lower() or 'cum swallowers' == newGenre.lower():
                newGenre = 'Cum Swallowing'
            elif 'rimming' == newGenre.lower() or 'rimjob' == newGenre.lower():
                newGenre = 'Rim Job'
            elif 'uneliforms' == newGenre.lower():
                newGenre = 'uneliform'
            elif 'latex darlings' == newGenre.lower():
                newGenre = 'latex'
            elif 'red head' == newGenre.lower() or 'red heads' == newGenre.lower():
                newGenre = 'Redhead'
            elif 'school girl' == newGenre.lower() or 'schoolgirl' == newGenre.lower():
                newGenre = 'Schoolgirl Outfit'
            elif 'teens' == newGenre.lower() or 'teen role' == newGenre.lower() or 'bad teens punished' == newGenre.lower() or 'teen porn' == newGenre.lower() or '18+ teen' == newGenre.lower():
                newGenre = 'teen'
            elif 'bgg' == newGenre.lower() or 'threesome bgg' == newGenre.lower() or 'girl-girl-boy' == newGenre.lower() or 'ffm' == newGenre.lower() or '2 girl bj' == newGenre.lower():
                newGenre = 'Boy-Girl-Girl'
            elif 'girl-on-girl' == newGenre.lower() or 'girl on girl' == newGenre.lower() or 'girl girl' == newGenre.lower():
                newGenre = 'Girl-Girl'
            elif 'girl-boy' == newGenre.lower() or 'girl/boy' == newGenre.lower() or 'boy girl' == newGenre.lower():
                newGenre = 'Boy-Girl'
            elif 'threesome bbg' == newGenre.lower() or 'mmf' == newGenre.lower() or 'bbg' == newGenre.lower():
                newGenre = 'Boy-Boy-Girl'
            elif 'mmff' == newGenre.lower():
                newGenre = 'Boy-Boy-Girl-Girl'
            elif 'mmmf' == newGenre.lower():
                newGenre = 'Boy-Boy-Boy-Girl'
            elif 'fffmm' == newGenre.lower():
                newGenre = 'Boy-Boy-Girl-Girl-Girl'
            elif 'swallow' == newGenre.lower() or 'amateur swallow' == newGenre.lower():
                newGenre = 'swallowing'
            elif 'housewives' == newGenre.lower():
                newGenre = 'Housewelife'
            elif 'oral' == newGenre.lower():
                newGenre = 'Oral Sex'
            elif 'athletic' == newGenre.lower() or 'athlete' == newGenre.lower():
                newGenre = 'athletic body'
            elif 'office' == newGenre.lower():
                newGenre = 'Office Setting'
            elif 'muscle' == newGenre.lower():
                newGenre = 'Muscular'
            elif 'pale' == newGenre.lower() or 'pale skin' == newGenre.lower() or 'whiteskin' == newGenre.lower():
                newGenre = 'Fair Skin'
            elif 'hotel' == newGenre.lower():
                newGenre = 'Hotel Room'
            elif 'landing strip pussy' == newGenre.lower():
                newGenre = 'Landing Strip'
            elif 'fishnet' == newGenre.lower() or 'fishnet stockings' == newGenre.lower():
                newGenre = 'Fishnets'
            elif 'death defying cbt' == newGenre.lower():
                newGenre = 'cbt'
            elif 'police' == newGenre.lower():
                newGenre = 'cop'
            elif 'first time porn' == newGenre.lower() or 'first porn shoot' == newGenre.lower() or 'debut' == newGenre.lower() or 'model debut' == newGenre.lower():
                newGenre = 'First Appearance'
            elif 'foot' == newGenre.lower() or 'barefeet' == newGenre.lower():
                newGenre = 'Feet'
            elif 'strap on' == newGenre.lower() or 'pov strapon' == newGenre.lower():
                newGenre = 'Strap-On'
            elif 'lesbians' == newGenre.lower():
                newGenre = 'Lesbian'
            elif 'straight' == newGenre.lower() or 'straight porn' == newGenre.lower():
                newGenre = 'Heterosexual'
            elif 'asian amateur' == newGenre.lower():
                newGenre = 'Asian'
            elif 'curly' == newGenre.lower():
                newGenre = 'curly hair'
            elif 'thongs' == newGenre.lower():
                newGenre = 'thong'
            elif 'college' == newGenre.lower() or 'university' == newGenre.lower() or 'coed' == newGenre.lower():
                newGenre = 'coeds'
            elif 'oiled' == newGenre.lower() or 'babyoil' == newGenre.lower():
                newGenre = 'oil'
            elif 'thick' == newGenre.lower() or 'voluptuous' == newGenre.lower() or 'curvy woman' == newGenre.lower():
                newGenre = 'curvy'
            elif 'reality' == newGenre.lower():
                newGenre = 'reality porn'
            elif 'group' == newGenre.lower():
                newGenre = 'group sex'
            elif 'hooded' == newGenre.lower():
                newGenre = 'hood'
            elif 'p.o.v.' == newGenre.lower() or 'femdom pov' == newGenre.lower():
                newGenre = 'pov'
            elif 'body massage' == newGenre.lower():
                newGenre = 'massage'
            elif 'gape' == newGenre.lower() or 'gaping playlist' == newGenre.lower() or 'gaping' == newGenre.lower() or 'gaped ass' == newGenre.lower():
                newGenre = 'Gaping'
            elif 'tanlines' == newGenre.lower():
                newGenre = 'Tan Lines'
            elif 'heels' == newGenre.lower():
                newGenre = 'High Heels'
            elif 'footjobs' == newGenre.lower() or 'footjob' == newGenre.lower():
                newGenre = 'Foot Job'
            elif 'behind the scene' == newGenre.lower():
                newGenre = 'Behind The Scenes'
            elif 'best bound breasts' == newGenre.lower():
                newGenre = 'Breast Bondage'
            elif 'dildo play' == newGenre.lower():
                newGenre = 'Dildo'
            elif 'eighteen and...' == newGenre.lower() or '18' == newGenre.lower() or '18 year' == newGenre.lower():
                newGenre = '18-Year-Old'
            elif 'solo masturbation' == newGenre.lower() or 'solo sex' == newGenre.lower() or 'solo action' == newGenre.lower():
                newGenre = 'Solo'
            elif 'pee' == newGenre.lower() or 'pissing' == newGenre.lower():
                newGenre = 'Piss Play'
            elif 'fisting\'s finest' == newGenre.lower():
                newGenre = 'Fisting'
            elif 'ass fingering' == newGenre.lower():
                newGenre = 'Anal Fingering'
            elif 'big toy' == newGenre.lower():
                newGenre = 'big toys'
            elif 'butt' == newGenre.lower() or 'booty' == newGenre.lower():
                newGenre = 'ass'
            elif 'couples' == newGenre.lower():
                newGenre = 'couple'
            elif 'first time anal' == newGenre.lower():
                newGenre = 'first anal'
            elif 'sci fi' == newGenre.lower():
                newGenre = 'sci-fi and fantasy'
            elif 'scissoring' == newGenre.lower():
                newGenre = 'tribbing'
            elif 'tease & denial' == newGenre.lower():
                newGenre = 'Tease And Denial'
            elif 'four or more' == newGenre.lower():
                newGenre = 'orgy'
            elif 'nude stockings' == newGenre.lower() or 'stockings' == newGenre.lower() or 'nylons stockings' == newGenre.lower() or 'pantyhose' == newGenre.lower() or 'pantyhose footjobs' == newGenre.lower() or 'black stockings' == newGenre.lower() or 'pantyhose / stockings' == newGenre.lower() or 'stocking' == newGenre.lower():
                newGenre = 'pantyhose & stockings'
            elif 'ballgagged' == newGenre.lower():
                newGenre = 'Ball Gag'
            elif 'camel toe pussy' == newGenre.lower():
                newGenre = 'Camel Toe'
            elif 'dirty talking' == newGenre.lower():
                newGenre = 'Dirty Talk'
            elif 'finger fucking' == newGenre.lower():
                newGenre = 'fingering'
            elif 'gangbangs' == newGenre.lower():
                newGenre = 'Gangbang'
            elif 'glamour' == newGenre.lower():
                newGenre = 'Glamorous'
            elif 'jerk off instruction' == newGenre.lower() or 'joi' == newGenre.lower() or 'joi games' == newGenre.lower():
                newGenre = 'Jerk Off Instructions (JOI)'
            elif 'maid fetish' == newGenre.lower():
                newGenre = 'maid'
            elif 'miniskirts' == newGenre.lower():
                newGenre = 'Mini Skirt'
            elif 'hair color' == newGenre.lower() or 'other hair color' == newGenre.lower():
                newGenre = 'Colored Hair'
            elif 'outdoors' == newGenre.lower():
                newGenre = 'Outdoor Sex'
            elif 'small booty' == newGenre.lower() or 'small butt' == newGenre.lower():
                newGenre = 'Small Ass'
            elif 'sneaker fetish' == newGenre.lower() or 'shoeplay' == newGenre.lower():
                newGenre = 'Shoe Fetish'
            elif 'uncut dicks' == newGenre.lower():
                newGenre = 'uncircumcised'
            elif 'natural boobs' == newGenre.lower() or 'real tits' == newGenre.lower():
                newGenre = 'Natural Tits'
            elif 'natural' == newGenre.lower():
                newGenre = 'All Natural'
            elif 'barely-legal' == newGenre.lower():
                newGenre = 'Barely Legal'
            elif 'in the gym' == newGenre.lower() or 'gym selfie porn' == newGenre.lower():
                newGenre = 'Gym'
            elif 'orgasm' == newGenre.lower() or 'amazing orgasms' == newGenre.lower():
                newGenre = 'orgasms'
            elif 'sissy training course' == newGenre.lower():
                newGenre = 'sisselification'
            elif 'strip tease' == newGenre.lower():
                newGenre = 'striptease'
            elif 'ass licking' == newGenre.lower():
                newGenre = 'ass eating'
            elif 'poolparty' == newGenre.lower():
                newGenre = 'pool'
            elif 'holidayparty' == newGenre.lower():
                newGenre = 'holidays'
            elif 'sexo' == newGenre.lower():
                newGenre = 'sex'
            elif 'modelo' == newGenre.lower():
                newGenre = 'model'
            elif 'braguitas' == newGenre.lower():
                newGenre = 'panties'
            elif 'lenceria' == newGenre.lower():
                newGenre = 'lingerie'
            elif 'masturbacion' == newGenre.lower():
                newGenre = 'masturbation'
            elif 'whip' == newGenre.lower():
                newGenre = 'whipping'
            elif 'valentines day' == newGenre.lower():
                newGenre = 'Valentine\'s Day'
            elif 'bukakke' == newGenre.lower():
                newGenre = 'Bukkake'
            elif 'cream pie' == newGenre.lower() or 'creampie compilation' == newGenre.lower():
                newGenre = 'Creampie'
            elif 'first time ir' == newGenre.lower():
                newGenre = 'First Interracial'
            elif 'latinas' == newGenre.lower():
                newGenre = 'Latina'
            elif 'lesbian pissing' == newGenre.lower() or 'girl girl pissing' == newGenre.lower():
                newGenre = 'Girl-Girl Pissing'
            elif 'lesbian domination' == newGenre.lower():
                newGenre = 'Lezdom'
            elif 'masks' == newGenre.lower():
                newGenre = 'mask'
            elif 'nerdy' == newGenre.lower():
                newGenre = 'nerd'
            elif '1 on 1' == newGenre.lower():
                newGenre = 'One-On-One'
            elif 'paddling' == newGenre.lower():
                newGenre = 'Paddle'
            elif 'teacher' == newGenre.lower():
                newGenre = 'Teacher Fetish'
            elif 'tanned skin' == newGenre.lower():
                newGenre = 'Tan'
            elif 'pile driving' == newGenre.lower():
                newGenre = 'pile driver'
            elif 'pornstars' == newGenre.lower():
                newGenre = 'pornstar'

            # Position
            if 'doggystyle' in newGenre.lower() or 'doggy style' in newGenre.lower():
                newGenre = 'doggystyle (Position)'
            elif 'cow girl' == newGenre.lower() or 'cowgirl' == newGenre.lower() or 'cowgirl (pov)' == newGenre.lower():
                newGenre = 'cowgirl (Position)'
            elif 'reverse cow girl' == newGenre.lower() or 'reverse cowgirl' == newGenre.lower() or 'reverse cowgirl (pov)' == newGenre.lower() or 'cowgirl - pov' == newGenre.lower():
                newGenre = 'reverse cowgirl (Position)'
            elif 'missionary' == newGenre.lower() or 'missionary (pov)' == newGenre.lower() or 'missionary - pov' == newGenre.lower():
                newGenre = 'missionary (Position)'
            elif 'sixty-nine' == newGenre.lower() or '69' == newGenre.lower() or '69 position' == newGenre.lower():
                newGenre = '69 (Position)'

            if len(newGenre) > 25:
                skip = True
                # Log('skip7')
            if ':' in metadata.title:
                if newGenre.lower() in metadata.title.split(':')[0].lower():
                    skip = True
                    # Log('skip8')
            if '-' in metadata.title:
                if newGenre.lower() in metadata.title.split('-')[0].lower():
                    skip = True
                    # Log('skip9')
            if ' ' in newGenre:
                if 3 < len(newGenre.split(' ')):
                    skip = True

            if not skip:
                metadata.genres.add(newGenre.title())
            genresProcessed = genresProcessed + 1
