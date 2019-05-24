class PhoenixGenres:
    genresTable = None
    genresNum = 0
    def __init__(self):
        self.genresTable = [None] * 100
        self.genresNum = 0
    def addGenre(self,newGenre):
        self.genresTable[self.genresNum] = newGenre
        self.genresNum = self.genresNum + 1
    def clearGenres(self):
        self.genresNum = 0
    def processGenres(self,metadata):
        genresProcessed = 0
        while genresProcessed < self.genresNum:
            skip = False
            newGenre = self.genresTable[genresProcessed].replace('"','').strip()

            ##### Skips
            #Match and Skip
            if "4k" == newGenre.lower():
                skip = True
            if "18+teens" == newGenre.lower():
                skip = True
            if "18+ teens" == newGenre.lower():
                skip = True
            if "babes" == newGenre.lower():
                skip = True
            if "bonus" == newGenre.lower():
                skip = True
            if "gonzo" == newGenre.lower():
                skip = True
            if "18" == newGenre.lower():
                skip = True
            if "18 year" == newGenre.lower():
                skip = True
            if "hd videos" == newGenre.lower():
                skip = True
            if "show less" == newGenre.lower():
                skip = True
            if "show more" == newGenre.lower():
                skip = True
            if "episode" in newGenre.lower():
                skip = True
            if "60p" == newGenre.lower():
                skip = True
            if "acworthy" == newGenre.lower():
                skip = True
            if "april" == newGenre.lower():
                skip = True
            if "april showers" == newGenre.lower():
                skip = True
            if "beaverday" == newGenre.lower():
                skip = True
            if "van styles" == newGenre.lower():
                skip = True
            if "yes, mistress" == newGenre.lower():
                skip = True
            if "tj cummings" == newGenre.lower():
                skip = True
            if "tony" == newGenre.lower():
                skip = True
            if "the pope" == newGenre.lower():
                skip = True
            if "mr. cummings" == newGenre.lower():
                skip = True
            if "keiran" == newGenre.lower():
                skip = True
            if "exclusive" == newGenre.lower():
                skip = True
            if "babe" == newGenre.lower():
                skip = True
            if "18-23" == newGenre.lower():
                skip = True
            if "smart" == newGenre.lower():
                skip = True
            if "ryan mclane" == newGenre.lower():
                skip = True
            if "destruction" == newGenre.lower():
                skip = True
            if "site member" == newGenre.lower():
                skip = True
            if "st patrick's day" == newGenre.lower():
                skip = True
            if "workitout" == newGenre.lower():
                skip = True
            if "little runaway" == newGenre.lower():
                skip = True
            if "feel me" == newGenre.lower():
                skip = True
            if "get sprung" == newGenre.lower():
                skip = True

            #Search and Skip
            if "5k" in newGenre.lower():
                skip = True
            if "60fps" in newGenre.lower():
                skip = True
            if "hd" in newGenre.lower():
                skip = True
            if "1080p" in newGenre.lower():
                skip = True
            if "aprilfools" in newGenre.lower():
                skip = True
            if "chibbles" in newGenre.lower():
                skip = True

            ##### Replace
            if "atm" == newGenre.lower():
                newGenre = "Ass to Mouth"
            if "big ass" == newGenre.lower() or "big booty" == newGenre.lower() or "bib booty" == newGenre.lower() or "girl big ass" == newGenre.lower() or "big butts" == newGenre.lower() or "fat ass" == newGenre.lower():
                newGenre = "Big Butt"
            if "3some" == newGenre.lower() or "3 way" == newGenre.lower() or "2-on-1" == newGenre.lower() or "2on1" == newGenre.lower():
                newGenre = "threesome"
            if "ball licking" == newGenre.lower() or "ball sucking" == newGenre.lower() or "ball lick" == newGenre.lower():
                newGenre = "ball licking"
            if "big cock" == newGenre.lower() or "big cocks" == newGenre.lower() or "big dicks" == newGenre.lower() or "2 big cocks" == newGenre.lower():
                newGenre = "big dick"
            if "bikin" == newGenre.lower():
                newGenre = "bikini"
            if "big boobs" == newGenre.lower() or "bit tits" == newGenre.lower() or "girl big tits" == newGenre.lower():
                newGenre = "big tits"
            if "black" == newGenre.lower() or "black girl" == newGenre.lower() or "dark skin" == newGenre.lower() or "african american" == newGenre.lower():
                newGenre = "ebony"
            if "shaved pussy" == newGenre.lower() or "bald pussy" == newGenre.lower() or "shaved" == newGenre.lower():
                newGenre = "shaven pussy"
            if "blowjob" == newGenre.lower() or "blowjob (pov)" == newGenre.lower() or "blowjob (double)" == newGenre.lower() or "bj" == newGenre.lower() or "amateur blowjobs" == newGenre.lower() or "blowjobs" == newGenre.lower():
                newGenre = "blow job"
            if "handjob" == newGenre.lower() or "handjob (pov)" == newGenre.lower() or "handjobs" == newGenre.lower():
                newGenre = "hand job"
            if "tittyfuck (pov)" == newGenre.lower() or "tittyfuck" == newGenre.lower() or "tit fuck" == newGenre.lower() or "titty fucking" == newGenre.lower():
                newGenre = "titty fuck"
            if "deepthroat" == newGenre.lower() or "deepthroating" == newGenre.lower():
                newGenre = "deep throat"
            if "dp" == newGenre.lower() or "double penetration" == newGenre.lower() or "double penetraton (dp)" == newGenre.lower():
                newGenre = "Double Penetration (DP)"
            if "face fuck" == newGenre.lower() or "facefucking" == newGenre.lower():
                newGenre = "face fucking"
            if "facesitting" == newGenre.lower():
                newGenre = "face sitting"
            if "facial (multiple)" == newGenre.lower() or "facial (pov)" == newGenre.lower() or "cumshot facial" == newGenre.lower() or "open mouth facial" == newGenre.lower():
                newGenre = "Facial"
            if "cum-in-mouth" == newGenre.lower():
                newGenre = "Cum In Mouth"
            if "cumshot" == newGenre.lower():
                newGenre = "cum shot"
            if "hairy" == newGenre.lower() or "hairy bush" == newGenre.lower() or "bush" == newGenre.lower():
                newGenre = "hairy pussy"
            if "hardcore sex" == newGenre.lower():
                newGenre = "hardcore"
            if "outdoor" == newGenre.lower():
                newGenre = "outdoors"
            if "indoor" == newGenre.lower():
                newGenre = "indoors"
            if "stepdaughter" == newGenre.lower():
                newGenre = "step daughter"
            if "stepmom" == newGenre.lower():
                newGenre = "step mom"
            if "stepsister" == newGenre.lower() or "stepsis" == newGenre.lower() or "step sis" == newGenre.lower() or "ste sister" == newGenre.lower() or "step siter" == newGenre.lower() or "step-sister" == newGenre.lower():
                newGenre = "step sister" 
            if "tattoos" == newGenre.lower() or "tattoo girl" == newGenre.lower() or "tattooed" == newGenre.lower():
                newGenre = "tattoo"
            if "white" == newGenre.lower() or "white girl" == newGenre.lower() or "while" == newGenre.lower():
                newGenre = "Caucasian"
            if "amatuer" == newGenre.lower() or "amateur pre auditions" == newGenre.lower():
                newGenre = "amateur"
            if "cumswap" == newGenre.lower() or "cum swapping" == newGenre.lower():
                newGenre = "cum swap"
            if "euro" == newGenre.lower() or "europe" == newGenre.lower():
                newGenre = "european"
            if "enhanced" == newGenre.lower() or "enhanced tits" == newGenre.lower() or "silicone tits" == newGenre.lower():
                newGenre = "fake tits"
            if "trimmed" == newGenre.lower() or "trimmed bush" == newGenre.lower():
                newGenre = "trimmed pussy"
            if "pse" == newGenre.lower():
                newGenre = "Pornstar Experience"
            if "gfe" == newGenre.lower():
                newGenre = "Girlfriend Experience"
            if "blond" == newGenre.lower() or "blonde hair" == newGenre.lower() or "blondes" == newGenre.lower():
                newGenre = "Blonde"
            if "blowbang" == newGenre.lower():
                newGenre = "Blow Bang"
            if "big beautiful women" == newGenre.lower():
                newGenre = "BBW"
            if "big areolas" == newGenre.lower():
                newGenre = "Big Nipples"
            if "buttplug" == newGenre.lower():
                newGenre = "Butt Plug"
            if "ts" == newGenre.lower():
                newGenre = "Transexual"
            if "squirt" == newGenre.lower() or "top squirting videos" == newGenre.lower():
                newGenre = "Squirting"
            if "big naturals" == newGenre.lower():
                newGenre = "Big Natural Tits"
            if "medium boobs" == newGenre.lower():
                newGenre = "Medium Tits"
            if "no condom" == newGenre.lower():
                newGenre = "bareback"
            if "piercings" == newGenre.lower():
                newGenre = "piercing"
            if "pussy lick" == newGenre.lower() or "pussy licking" == newGenre.lower() or "cunilingus" == newGenre.lower():
                newGenre = "Pussy Eating"
            if "completely naked" == newGenre.lower():
                newGenre = "Nude"
            if "boot" == newGenre.lower():
                newGenre = "Boots"
            if "older / younger" == newGenre.lower():
                newGenre = "older/younger"
            if "milfs" == newGenre.lower():
                newGenre = "milf"
            if "mature & milf" == newGenre.lower():
                newGenre = "Milf & Mature"
            if "sex toys" == newGenre.lower():
                newGenre = "toys"
            if "interviews" == newGenre.lower():
                newGenre = "interview"
            if "skirts" == newGenre.lower():
                newGenre = "skirt"
            if "brown hair" == newGenre.lower() or "brunettes" == newGenre.lower():
                newGenre = "Brunette"
            if "brutal cuckolding" == newGenre.lower() or "cuckolding" == newGenre.lower():
                newGenre = "Cuckold"
            if "small boobs" == newGenre.lower():
                newGenre = "Small Tits"
            if "nurse" == newGenre.lower():
                newGenre = "Nurse Play"
            if "electrical play" == newGenre.lower():
                newGenre = "Electro Play"
            if "chastity" == newGenre.lower():
                newGenre = "Chastity Play"
            if "cum swallow" == newGenre.lower() or "swallow cum" == newGenre.lower():
                newGenre = "Cum Swallowing"
            if "rimming" == newGenre.lower():
                newGenre = "Rim Job"
            if "uniforms" == newGenre.lower():
                newGenre = "uniform"
            if "latex darlings" == newGenre.lower():
                newGenre = "latex"
            if "red head" == newGenre.lower():
                newGenre = "Redhead"
            if "school girl" == newGenre.lower() or "schoolgirl" == newGenre.lower():
                newGenre = "Schoolgirl Outfit"
            if "teens" == newGenre.lower() or "teen role" == newGenre.lower() or "bad teens punished" == newGenre.lower():
                newGenre = "teen"
            if "bgg" == newGenre.lower() or "threesome bgg" == newGenre.lower() or "girl-girl-boy" == newGenre.lower() or "ffm" == newGenre.lower() or "2 girl bj" == newGenre.lower():
                newGenre = "Boy-Girl-Girl"
            if "girl-on-girl" == newGenre.lower() or "girl on girl" == newGenre.lower():
                newGenre = "Girl-Girl"
            if "girl-boy" == newGenre.lower():
                newGenre = "Boy-Girl"
            if "threesome bbg" == newGenre.lower() or "mmf" == newGenre.lower():
                newGenre = "Boy-Boy-Girl"
            if "mmff" == newGenre.lower():
                newGenre = "Boy-Boy-Girl-Girl"
            if "mmmf" == newGenre.lower():
                newGenre = "Boy-Boy-Boy-Girl"
            if "fffmm" == newGenre.lower():
                newGenre = "Boy-Boy-Girl-Girl-Girl"
            if "swallow" == newGenre.lower() or "amateur swallow" == newGenre.lower():
                newGenre = "swallowing"
            if "housewives" == newGenre.lower():
                newGenre = "Housewife"
            if "oral" == newGenre.lower():
                newGenre = "Oral Sex"
            if "athletic" == newGenre.lower():
                newGenre = "athletic body"
            if "office" == newGenre.lower():
                newGenre = "Office Setting"
            if "muscle" == newGenre.lower():
                newGenre = "Muscular"
            if "pale" == newGenre.lower():
                newGenre = "Fair Skin"
            if "hotel" == newGenre.lower():
                newGenre = "Hotel Room"
            if "landing strip pussy" == newGenre.lower():
                newGenre = "Landing Strip"
            if "fishnet" == newGenre.lower() or "fishnet stockings" == newGenre.lower():
                newGenre = "Fishnets"
            if "death defying cbt" == newGenre.lower():
                newGenre = "cbt"
            if "police" == newGenre.lower():
                newGenre = "cop"
            if "first time porn" == newGenre.lower() or "first porn shoot" == newGenre.lower() or "debut" == newGenre.lower() or "model debut" == newGenre.lower():
                newGenre = "First Appearance"
            if "foot" == newGenre.lower() or "barefeet" == newGenre.lower():
                newGenre = "Feet"
            if "strap on" == newGenre.lower():
                newGenre = "Strap-On"
            if "lesbians" == newGenre.lower():
                newGenre = "Lesbian"
            if "straight" == newGenre.lower() or "straight porn" == newGenre.lower():
                newGenre = "Heterosexual"
            if "asian amateur" == newGenre.lower():
                newGenre = "Asian"
            if "curly" == newGenre.lower():
                newGenre = "curly hair"
            if "thongs" == newGenre.lower():
                newGenre = "thong"
            if "college" == newGenre.lower() or "university" == newGenre.lower() or "coed" == newGenre.lower():
                newGenre = "coeds"
            if "oiled" == newGenre.lower() or "babyoil" == newGenre.lower():
                newGenre = "oil"
            if "thick" == newGenre.lower():
                newGenre = "curvy"
            if "reality" == newGenre.lower():
                newGenre = "reality porn"
            if "group" == newGenre.lower():
                newGenre = "group sex"
            if "hooded" == newGenre.lower():
                newGenre = "hood"
            if "p.o.v." == newGenre.lower() or "femdom pov" == newGenre.lower():
                newGenre = "pov"
            if "body massage" == newGenre.lower():
                newGenre = "massage"
            if "gape" == newGenre.lower() or "gaping playlist" == newGenre.lower():
                newGenre = "Gaping"
            if "tanlines" == newGenre.lower():
                newGenre = "Tan Lines"
            if "heels" == newGenre.lower():
                newGenre = "High Heels"
            if "footjobs" == newGenre.lower() or "footjob" == newGenre.lower():
                newGenre = "Foot Job"
            if "behind the scene" == newGenre.lower():
                newGenre = "Behind The Scenes"
            if "best bound breasts" == newGenre.lower():
                newGenre = "Breast Bondage"
            if "dildo play" == newGenre.lower():
                newGenre = "Dildo"
            if "eighteen and..." == newGenre.lower():
                newGenre = "18-Year-Old"
            if "solo masturbation" == newGenre.lower():
                newGenre = "Solo"
            if "pee" == newGenre.lower():
                newGenre = "Piss Play"
            if "fisting's finest" == newGenre.lower():
                newGenre = "Fisting"

            ##### Position
            if "doggystyle" == newGenre.lower() or "doggystyle (standing)" == newGenre.lower() or "doggystyle (pov)" == newGenre.lower() or "doggystye" == newGenre.lower() or "doggy style" == newGenre.lower() or "doggiestyle" == newGenre.lower():
                newGenre = "doggystyle (Position)"
            if "cow girl" == newGenre.lower() or "cowgirl" == newGenre.lower() or "cowgirl (pov)" == newGenre.lower():
                newGenre = "cowgirl (Position)"
            if "reverse cow girl" == newGenre.lower() or "reverse cowgirl" == newGenre.lower() or "reverse cowgirl (pov)" == newGenre.lower():
                newGenre = "reverse cowgirl (Position)"
            if "missionary" == newGenre.lower() or "missionary (pov)" == newGenre.lower():
                newGenre = "missionary (Position)"
            if "sixty-nine" == newGenre.lower() or "69" == newGenre.lower() or "69 position" == newGenre.lower():
                newGenre = "69 (Position)"

            if len(newGenre) > 25:
                skip = True
                #Log("skip7")
            if ":" in metadata.title:
                if newGenre.lower() in metadata.title.split(":")[0].lower():
                    skip = True
                    #Log("skip8")
            if "-" in metadata.title:
                if newGenre.lower() in metadata.title.split("-")[0].lower():
                    skip = True
                    #Log("skip9")
            if " " in newGenre:
                if 3 < len(newGenre.split(" ")):
                    skip = True
                    
            if not skip:
                metadata.genres.add(newGenre.title())
            genresProcessed = genresProcessed + 1