class PhoenixActors:
    actorsTable = None
    photosTable = None
    actorsNum = 0
    def __init__(self):
        self.actorsTable = [None] * 100
        self.photosTable = [None] * 100
        self.actorsNum = 0
    def addActor(self,newActor,newPhoto):
        self.actorsTable[self.actorsNum] = newActor
        self.photosTable[self.actorsNum] = newPhoto
        self.actorsNum = self.actorsNum + 1
    def clearActors(self):
        self.actorsNum = 0
    def processActors(self,metadata):
        actorsProcessed = 0
        while actorsProcessed < self.actorsNum:
            skip = False
            # Save the potentional new Actor or Actress to a new variable, replace &nbsp; with a true space, and strip off any surrounding whitespace
            newActor = self.actorsTable[actorsProcessed].replace("\xc2\xa0", " ").replace(',','').strip().title()
            newPhoto = self.photosTable[actorsProcessed].strip()

            ##### Skip an actor completely; this could be used to filter out male actors if desired
            if "Bad Name" == newActor:
                skip = True

            ##### Replace by actor name; for actors that have different aliases in the industry
            if "Josephine" == newActor or "Conny" == newActor or "Conny Carter" == newActor or "Connie" == newActor:
                newActor = "Connie Carter"
            if "Doris Ivy" == newActor:
                newActor = "Gina Gerson"
            if "Anjelica" == newActor or "Ebbi" == newActor or "Abby H" == newActor or "Katherine A" == newActor:
                newActor = "Krystal Boyd"
            if "Nathaly" == newActor or "Nathalie Cherie" == newActor:
                newActor = "Nathaly Cherie"
            if newActor == "Alex D":
                newActor = "Alex D."
            if "Crissy Kay" == newActor or "Emma Hicks" == newActor or "Emma Hixx" == newActor:
                newActor = "Emma Hix"

            ##### Replace by site + actor; use when an actor just has an alias or abbreviated name on one site
            if metadata.studio == "21Sextury" and "Abbie" == newActor:
                newActor = "Krystal Boyd"
            if metadata.studio == "Babes" and "Angelica" == newActor:
                newActor = "Krystal Boyd"
            if metadata.studio == "LegalPorno" and "Abby" == newActor:
                newActor = "Krystal Boyd"
            if metadata.studio == "Joymii":
                if "Valentina" in newActor:
                    newActor == "Valentina Nappi"
                if newActor == "Gina G.":
                    newActor = "Gina Gerson"
                if newActor == "Tasha R.":
                    newActor = "Tasha Reign"
                if newActor == "Piper P.":
                    newActor = "Piper Perri"
                if newActor == "Lara":
                    newActor = "Dido Angel"
                if newActor == "Cindy L.":
                    newActor = "Cindy Carson"
                if newActor == "Denisa":
                    newActor == "Denisa Heaven"
                if newActor == "Abigail":
                    newActor = "Abigaile Johnson"
			if metadata.studio == "Nubiles":
                if "Lilian" in newActor:
                    newActor == "Lillian Lee"
                if "Kimmie" in newActor:
                    newActor == "Kimmie Cream"
                if "Kimberly" in newActor:
                    newActor == "Kimberly Allure"
                if "Eriko" in newActor:
                    newActor == "Nikko Jordan"
                if "Sandra" in newActor:
                    newActor == "Sandra Shine"
                if "Sarah" in newActor:
                    newActor == "Sarah Blake"
                if "Ginnah" in newActor:
                    newActor == "Lucie"
                if "Tereza" in newActor:
                    newActor == "Tereza Ilova"
                if "Janelle" in newActor:
                    newActor == "Karlie Montana"
                if "Christine" in newActor:
                    newActor == "Christie Lee"
                if "Diana" in newActor:
                    newActor == "Belicia"
                if "Layna" in newActor:
                    newActor == "Brigitte Hunter"
                if "Nicole" in newActor:
                    newActor == "Nikita G."
                if "Andrea" in newActor:
                    newActor == "Jenny Sanders"
                if "Britney" in newActor:
                    newActor == "Liz Honey"
                if "Jenny" in newActor:
                    newActor == "Jenni Lee"
                if "Zeina" in newActor:
                    newActor == "Zeina Heart"
                if "Leah" in newActor:
                    newActor == "Leah Luv"
                if "Courtney" in newActor:
                    newActor == "Courtney Cummz"
                if "Celeste" in newActor:
                    newActor == "Celeste Star"
                if "Valerie" in newActor:
                    newActor == "Valerie Herrera"
                if "Smokie" in newActor:
                    newActor == "Smokie Flame"
                if "Charlie" in newActor:
                    newActor == "Charlie Laine"
                if "Dana" in newActor:
                    newActor == "Monica Sweet"
                if "Rachel" in newActor:
                    newActor == "Yasmine Gold"
                if "Jane" in newActor:
                    newActor == "Mellie Williams"
                if "Sheridan" in newActor:
                    newActor == "Jana Sheridan"
                if "Ariel" in newActor:
                    newActor == "Ariel Rebel"
                if "Judith" in newActor:
                    newActor == "Judith Fox"
                if "Amy" in newActor:
                    newActor == "Amy Reid"
                if "Amber" in newActor:
                    newActor == "Roxy Carter"
                if "Crystal" in newActor:
                    newActor == "Nesty"
                if "Dina" in newActor:
                    newActor == "Dana Sinnz"
                if "Eve" in newActor:
                    newActor == "Eve Angel"
                if "Carrie" in newActor:
                    newActor == "Sandra Kalermen"
                if "Kelly" in newActor:
                    newActor == "Adrienn Levai"

            if not skip:
                if newPhoto == '':
                    newPhoto = actorDBfinder(newActor)
                Log("Actor: "+newActor+" "+newPhoto)

                role = metadata.roles.new()
                role.name = newActor
                role.photo = newPhoto
            actorsProcessed = actorsProcessed + 1

# https://www.indexxx.com/models/59558/anjelica-1/

# For sites without a proper actor profile picture, this method looks in external databases based on actorName            
def actorDBfinder(actorName):
    try:
        databaseName = "AdultDVDEmpire"
        actorsearch = HTML.ElementFromURL("https://www.adultdvdempire.com/performer/search?q=" + actorName.replace(' ','%20'))
        actorPageURL = actorsearch.xpath('//div[@class="col-xs-6 col-sm-3 grid-item grid-item-performer grid-item-performer-145"]/a')[0].get("href")
        actorPageURL = "https://www.adultdvdempire.com" + actorPageURL
        actorPage = HTML.ElementFromURL(actorPageURL)
        actorPhotoURL = actorPage.xpath('//a[@class="fancy headshot"]')[0].get("href")
        Log(actorName + " found in " + databaseName)
        Log("PhotoURL: " + actorPhotoURL)
    except:
        try:
            databaseName = "Boobpedia"
        # Code Removed - website has standardized actor page
            # searchURL = "http://www.boobpedia.com/wiki/index.php?title=Special%3ASearch&profile=default&search=" + actorName.replace(' ', '+') + "&fulltext=Search"
            # Log(databaseName + "-searchURL: " + searchURL)
            # actorSearch = HTML.ElementFromURL(searchURL)
            # actorPageURL = actorSearch.xpath('//div[@class="mw-search-result-heading"]/a')[0].get("href")
            # actorPageURL = "http://www.boobpedia.com" + actorPageURL
            actorPageURL = "http://www.boobpedia.com/boobs/" + actorName.lower().replace(" ", "_")
            # Log(databaseName + "-PageURL: " + actorPageURL)
            actorPage = HTML.ElementFromURL(actorPageURL)
            actorPhotoURL = actorPage.xpath('//table[@class="infobox"]//a[@class="image"]//img')[0].get("src")
            actorPhotoURL = "http://www.boobpedia.com" + actorPhotoURL
            Log(actorName + " found in " + databaseName)
            Log("PhotoURL: " + actorPhotoURL)
        except:
            try:
                databaseName = "Babes and Stars"
                # searchURL = "http://www.babesandstars.com/search/?t=models&q=" + actorName.replace(' ','+')
                # Log(databaseName + "-searchURL: " + searchURL)
                # actorSearch = HTML.ElementFromURL(searchURL)
                # actorPageURL = actorSearch.xpath('//div[contains(@class,"thumb")]//a')[0].get("href")
                actorPageURL = "http://www.babesandstars.com/" + actorName[0:1] + "/" + actorName.lower().replace(" ","-") +"/"
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//div[@class="profile"]//div[@class="thumb"]/img')[0].get("src")
                Log(actorName + " found in " + databaseName)
                Log("PhotoURL: " + actorPhotoURL)
            except:
                try:
                    databaseName = "IAFD"
                    searchURL = "http://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=" + actorName.replace(' ', '+')
                    actorSearch = HTML.ElementFromURL(searchURL)
                    actorPageURL = actorSearch.xpath('//table[@id="tblFem"]//tbody//a')[0].get("href")
                    actorPageURL = "http://www.iafd.com" + actorPageURL
                    actorPage = HTML.ElementFromURL(actorPageURL)
                    actorPhotoURL = actorPage.xpath('//div[@id="headshot"]//img')[0].get("src")
                    Log(actorName + " found in " + databaseName)
                    Log("PhotoURL: " + actorPhotoURL)
                except:
                    try:
                        databaseName = "Babepedia"
                        # searchURL = "https://www.babepedia.com/search/" + actorName.replace(' ', '%20')
                        # Log(databaseName + "-searchURL: " + searchURL)
                        # actorSearch = HTML.ElementFromURL(searchURL)
                        # actorPageURL = actorSearch.xpath('//div[contains(@class,"thumbshot")]//a')[0].get("href")
                        # actorPageURL = "http://www.babepedia.com" + actorPageURL
                        # actorPageURL = "http://www.babepedia.com/babe/" + actorName.lower().replace(" ", "_")
                        # actorPage = HTML.ElementFromURL(actorPageURL)
                        # actorPhotoURL = actorPage.xpath('//div[@id="profimg"]//a')[0].get("href")
                        # actorPhotoURL = "http://www.babepedia.com" + actorPhotoURL
                        actorPhotoURL = "http://www.babepedia.com/pics/" + actorName.title().replace(" ", "%20") + ".jpg"
                        Log(actorName + " found in " + databaseName)
                        Log("PhotoURL: " + actorPhotoURL)
                    except:
                        Log(actorName + "not found.")
                        actorPhotoURL = ""
    return actorPhotoURL
