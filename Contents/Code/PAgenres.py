class PhoenixGenres:
    genresTable = None
    genresNum = 0
    def __init__(self):
        self.genresTable = [None] * 60
        self.genresNum = 0
    def addGenre(self,newGenre):
        #Log("GenresNum: " + str(self.genresNum))
        #Log("SizeOf: " + str(len(self.genresTable)))
        self.genresTable[self.genresNum] = newGenre
        self.genresNum = self.genresNum + 1
    def clearGenres(self):
        self.genresNum = 0
    def processGenres(self,metadata):
        genresProcessed = 0
        while genresProcessed < self.genresNum:
            skip = False
            #Log(str(skip))
            newGenre = self.genresTable[genresProcessed]
            ##### Skips
            if "4k" == newGenre.lower():
                skip = True
                #Log("skip1")
            if "18+teens" == newGenre.lower():
                skip = True
                #Log("skip2")
            if "18+ teens" == newGenre.lower():
                skip = True
                #Log("skip3")
            if "babes" == newGenre.lower():
                skip = True
                #Log("skip4")
            if "bonus" == newGenre.lower():
                skip = True
                #Log("skip5")
            if "gonzo" == newGenre.lower():
                skip = True
                #Log("skip6")
            if "18" == newGenre.lower():
                skip = True
            if "18 year" == newGenre.lower():
                skip = True
            if "hd videos" == newGenre.lower():
                skip = True

            ##### Replace
            if "big ass" == newGenre.lower() or "big booty" == newGenre.lower() or "bib booty" == newGenre.lower() or "girl big ass" == newGenre.lower():
                newGenre = "Big Butt"
            if "3some" == newGenre.lower():
                newGenre = "threesome"
            if "ball licking" == newGenre.lower() or "ball sucking" == newGenre.lower():
                newGenre = "ball play"
            if "big cock" == newGenre.lower():
                newGenre = "big dick"
            if "bikin" == newGenre.lower():
                newGenre = "bikini"
            if "big boobs" == newGenre.lower() or "bit tits" == newGenre.lower() or "girl big tits" == newGenre.lower():
                newGenre = "big tits"
            if "black" == newGenre.lower() or "black girl" == newGenre.lower():
                newGenre = "ebony"
            if "shaved pussy" == newGenre.lower() or "bald pussy" == newGenre.lower():
                newGenre = "shaven pussy"
            if "blowjob" == newGenre.lower():
                newGenre = "blow job"
            if "blowjob (pov)" == newGenre.lower() or "blowjob (double)" == newGenre.lower() or "bj" == newGenre.lower():
                newGenre = "blow job"
            if "handjob" == newGenre.lower() or "handjob (pov)" == newGenre.lower():
                newGenre = "hand job"
            if "tittyfuck (pov)" == newGenre.lower() or "tittyfuck" == newGenre.lower() or "tit fuck" == newGenre.lower():
                newGenre = "titty fuck"
            if "deepthroat" == newGenre.lower() or "deepthroating" == newGenre.lower():
                newGenre = "deep throat"
            if "dp" == newGenre.lower() or "double penetration" == newGenre.lower() or "double penetraton (dp)" == newGenre.lower():
                newGenre = "Double Penetration (DP)"
            if "face fucking" == newGenre.lower():
                newGenre = "face fuck"
            if "facesitting" == newGenre.lower():
                newGenre = "face sitting"
            if "facial (multiple)" == newGenre.lower() or "facial (pov)" == newGenre.lower() or "cumshot facial" == newGenre.lower():
                newGenre = "Facial"
            if "fat ass" == newGenre.lower():
                newGenre = "big butt"
            if "fishnet stockings" == newGenre.lower():
                newGenre = "Fishnet"
            if "shaved" == newGenre.lower():
                newGenre = "shaven pussy"
            if "cum-in-mouth" == newGenre.lower():
                newGenre = "Cum In Mouth"
            if "cumshot" == newGenre.lower():
                newGenre = "cum shot"
            if "hairy" == newGenre.lower() or "hairy bush" == newGenre.lower():
                newGenre = "hairy pussy"
            if "hardcore sex" == newGenre.lower():
                newGenre = "hardcore"
            if "outdoor" == newGenre.lower():
                newGenre = "outdoors"
            if "stepdaughter" == newGenre.lower():
                newGenre = "step daughter"
            if "stepmom" == newGenre.lower():
                newGenre = "step mom"
            if "stepsister" == newGenre.lower() or "stepsis" == newGenre.lower() or "step sis" == newGenre.lower() or "ste sister" == newGenre.lower() or "step siter" == newGenre.lower() or "step-sister" == newGenre.lower():
                newGenre = "step sister" 
            if "tattoos" == newGenre.lower() or "tattoo girl" == newGenre.lower():
                newGenre = "tattoo"
            if "white" == newGenre.lower() or "white girl" == newGenre.lower() or "while" == newGenre.lower():
                newGenre = "Caucasian"
            if "amatuer" == newGenre.lower():
                newGenre = "amateur"
            if "cumswap" == newGenre.lower() or "cum swapping" == newGenre.lower():
                newGenre = "cum swap"
            if "euro" == newGenre.lower() or "europe" == newGenre.lower():
                newGenre = "european"
            if "enhanced" == newGenre.lower() or "enhanced tits" == newGenre.lower() or "silicone tits" == newGenre.lower():
                newGenre = "fake tits"
            if "trimmed" == newGenre.lower():
                newGenre = "trimmed pussy"

            
            
            

            ##### Position
            if "doggystyle" == newGenre.lower() or "doggystyle (standing)" == newGenre.lower() or "doggystyle (pov)" == newGenre.lower() or "doggystye" == newGenre.lower() or "doggy style" == newGenre.lower():
                newGenre = "doggystyle (Position)"
            if "cow girl" == newGenre.lower() or "cowgirl" == newGenre.lower() or "cowgirl (pov)" == newGenre.lower():
                newGenre = "cowgirl (Position)"
            if "reverse cow girl" == newGenre.lower() or "reverse cowgirl" == newGenre.lower() or "reverse cowgirl (pov)" == newGenre.lower():
                newGenre = "reverse cowgirl (Position)"
            if "missionary" == newGenre.lower() or "missionary (pov)" == newGenre.lower():
                newGenre = "missionary (Position)"



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
                    
            #if skip:
                #Log("Skip genre")
            

            #Log("Genre: " + newGenre)
            if not skip:
                metadata.genres.add(newGenre.title())
            genresProcessed = genresProcessed + 1
