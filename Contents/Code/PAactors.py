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
            if "Katarina" == newActor:
                newActor = "Katerina Hartlova"
            if newActor == "Alex D":
                newActor = "Alex D."
            if "Crissy Kay" == newActor or "Emma Hicks" == newActor or "Emma Hixx" == newActor:
                newActor = "Emma Hix"
            if newActor == "Elsa Dream":
                newActor = "Elsa Jean"
            if newActor == "Hailey Reed":
                newActor = "Haley Reed"
            if "Lilly LaBeau" == newActor or "Lilly Labuea" == newActor or "Lily La Beau" == newActor or "Lily Lebeau" == newActor or "Lily Luvs" == newActor:
                newActor = "Lily Labeau"
            if "Noe Milk" == newActor or "Noemiek" == newActor:
                newActor = "Noemilk"
            if "Riley Jenson" == newActor or "Riley Anne" == newActor or "Rilee Jensen" == newActor:
                newActor = "Riley Jensen"
            if "Stella Bankxxx" == newActor or "Stella Ferrari" == newActor:
                newActor = "Stella Banxxx"
            if newActor == "Lara Craft":
                newActor = "Lora Craft"
            if newActor == "Amia Moretti":
                newActor = "Amia Miley"
            if newActor == "Abby Rains":
                newActor = "Abbey Rain"
            if newActor == "Charlotte Lee":
                newActor = "Jaye Summers"
            if newActor == "Grace Hartley":
                newActor = "Pinky June"
            if newActor == "Jenny Ferri":
                newActor = "Jenny Fer"
            if newActor == "Sara Luv":
                newActor = "Sara Luvv"
            if newActor == "Kari Sweets":
                newActor = "Kari Sweet"
            if newActor == "Criss Strokes":
                newActor = "Chris Strokes"
            if "Jassie Gold" == newActor or "Jaggie Gold" == newActor:
                newActor = "Jessi Gold"
            if "Maria Rya" == newActor or "Melena Maria" == newActor:
                newActor = "Melena Maria Rya"
            if newActor == "Nika Noir":
                newActor = "Nika Noire"
            if "Jessica Blue" == newActor or "Jessica Cute" == newActor:
                newActor = "Jessica Foxx"
            if "Nadya Nabakova" == newActor or "Nadya Nabokova" == newActor:
                newActor = "Bunny Colby"
            if "April ONeil" == newActor or "April Oneil" == newActor or "April O'neil" == newActor:
                newActor == "April O'Neil"
            if "Tiny Teen" == newActor or "Tieny Mieny" == newActor or "Lady Jay" == newActor:
                newActor == "Eva Elfie"

            ##### Replace by site + actor; use when an actor just has an alias or abbreviated name on one site
            if metadata.studio == "21Sextury" and "Abbie" == newActor:
                newActor = "Krystal Boyd"
            if metadata.studio == "Babes" and "Angelica" == newActor:
                newActor = "Krystal Boyd"
            if metadata.studio == "LegalPorno" and "Abby" == newActor:
                newActor = "Krystal Boyd"
            if metadata.studio == "Joymii":
                if newActor == "Abigail":
                    newActor = "Abigaile Johnson"
                if newActor == "Aleska D.":
                    newActor = "Aleska Diamond"
                if newActor == "Alessandra J.":
                    newActor = "Alessandra Jane"
                if newActor == "Alexa":
                    newActor = "Alexa Tomas"
                if newActor == "Alexis":
                    newActor = "Alexis Crystal"
                if newActor == "Alexis B.":
                    newActor = "Alexis Brill"
                if newActor == "Alexis T.":
                    newActor = "Alexis Texas"
                if newActor == "Alexis V.":
                    newActor = "Alexis Venton"
                if newActor == "Alice B.":
                    newActor = "Mira Sunset"
                if newActor == "Allie J.":
                    newActor = "Allie Jordan"
                if newActor == "Alysa":
                    newActor = "Alyssa Branch"
                if newActor == "Amirah A.":
                    newActor = "Amirah Adara"
                if newActor == "Andie":
                    newActor = "Andie Darling"
                if newActor == "Angel B.":
                    newActor = "Angel Blade"
                if newActor == "Anita B.":
                    newActor = "Anita Bellini"
                if newActor == "Anna P.":
                    newActor = "Cayenne Klein"
                if newActor == "Anneli":
                    newActor = "Pinky June"
                if newActor == "Apolonia":
                    newActor = "Apolonia Lapiedra"
                if newActor == "Ariel":
                    newActor = "Ariel Piper Fawn"
                if newActor == "Athina":
                    newActor = "Tyra Moon"
                if newActor == "Aubrey J.":
                    newActor = "Aubrey James"
                if newActor == "Avril H.":
                    newActor = "Avril Hall"
                if newActor == "Bailey D.":
                    newActor = "Lovenia Lux"
                if newActor == "Bailey R.":
                    newActor = "Bailey Ryder"
                if newActor == "Belinda":
                    newActor = "Rose Delight"
                if newActor == "Billie":
                    newActor = "Billie Star"
                if newActor == "Blanche B.":
                    newActor = "Blanche Bradburry"
                if newActor == "Brittany":
                    newActor = "Brittney Banxxx"
                if newActor == "Candice":
                    newActor = "Candice Luca"
                if newActor == "Candy B.":
                    newActor = "Candy Blond"
                if newActor == "Caprice":
                    newActor = "Little Caprice"
                if newActor == "Carmen C.":
                    newActor = "Carmen McCarthy"
                if newActor == "Carolina":
                    newActor = "Carolina Abril"
                if newActor == "Cayla L.":
                    newActor = "Cayla Lyons"
                if newActor == "Celeste":
                    newActor = "Celeste Star"
                if newActor == "Chastity L.":
                    newActor = "Chastity Lynn"
                if newActor == "Cherry K.":
                    newActor = "Cherry Kiss"
                if newActor == "Christen":
                    newActor = "Christen Courtney"
                if newActor == "Cindy D.":
                    newActor = "Cindy Dollar"
                if newActor == "Cindy L.":
                    newActor = "Cindy Carson"
                if newActor == "Clea G":
                    newActor = "Clea Gaultier"
                if newActor == "Clover":
                    newActor = "Katya Clover"
                if newActor == "Coco":
                    newActor = "Coco de Mal"
                if newActor == "Dani D.":
                    newActor = "Dani Daniels"
                if newActor == "Davina E.":
                    newActor = "Sybil"
                if newActor == "Dee":
                    newActor = "Lady Dee"
                if newActor == "Defrancesca":
                    newActor = "Defrancesca Gallardo"
                if newActor == "Delphine":
                    newActor = "Izzy Delphine"
                if newActor == "Denisa":
                    newActor = "Denisa Heaven"
                if newActor == "Eliana R.":
                    newActor = "Elaina Raye"
                if newActor == "Ella M.":
                    newActor = "Ella Milano"
                if newActor == "Erika K.":
                    newActor = "Erika Kortni"
                if newActor == "Eufrat":
                    newActor = "Eufrat Mai"
                if newActor == "Eveline D.":
                    newActor = "Eveline Dellai"
                if newActor == "Evi F.":
                    newActor = "Evi Fox"
                if newActor == "Evilyn F.":
                    newActor = "Evilyn Fierce"
                if newActor == "Faye R.":
                    newActor = "Faye Reagan"
                if newActor == "Ferrera":
                    newActor = "Ferrera Gomez"
                if newActor == "Frida S.":
                    newActor = "Frida Sante"
                if newActor == "Gina G.":
                    newActor = "Gina Gerson"
                if newActor == "Gina V.":
                    newActor = "Gina Devine"
                if newActor == "Ginebra B.":
                    newActor = "Ginebra Bellucci"
                if newActor == "Ginger":
                    newActor = "Ginger Fox"
                if newActor == "Giselle L.":
                    newActor = "Giselle Leon"
                if newActor == "Hayden W.":
                    newActor = "Hayden Winters"
                if newActor == "Heather S.":
                    newActor = "Heather Starlet"
                if newActor == "Holly":
                    newActor = "Holly Anderson"
                if newActor == "Holly M.":
                    newActor = "Holly Michaels"
                if newActor == "Ivy":
                    newActor = "Iwia"
                if newActor == "Jana J.":
                    newActor = "Jana Jordan"
                if newActor == "Jana Q.":
                    newActor = "Emma Brown"
                if newActor == "Jane F.":
                    newActor = "Nancy Ace"
                if newActor == "Jayden C.":
                    newActor = "Jayden Cole"
                if newActor == "Jennifer W.":
                    newActor = "Jennifer White"
                if newActor == "Jessica":
                    newActor = "Leony April"
                if newActor == "Jessica B.":
                    newActor = "Jessica Bee"
                if newActor == "Jessie":
                    newActor = "Jessie Jazz"
                if newActor == "Josephine":
                    newActor = "Connie Carter"
                if newActor == "Julia R.":
                    newActor = "Julia Roca"
                if newActor == "Kaci S.":
                    newActor = "Kaci Starr"
                if newActor == "Kari":
                    newActor = "Kari Sweet"
                if newActor == "Karlie":
                    newActor = "Karlie Montana"
                if newActor == "Karol T.":
                    newActor = "Karol Lilien"
                if newActor == "Katie G.":
                    newActor = "Kattie Gold"
                if newActor == "Katie J.":
                    newActor = "Katie Jordin"
                if newActor == "Katy R.":
                    newActor = "Katy Rose"
                if newActor == "Kelly W":
                    newActor = "Kelly White"
                if newActor == "Kiara D.":
                    newActor = "Kiara Diane"
                if newActor == "Kiara L.":
                    newActor = "Kiara Lord"
                if newActor == "Kira T.":
                    newActor = "Kira Thorn"
                if newActor == "Kitty J.":
                    newActor = "Kitty Jane"
                if newActor == "Lara":
                    newActor = "Dido Angel"
                if newActor == "Lena N.":
                    newActor = "Lena Nicole"
                if newActor == "Lexi D.":
                    newActor = "Lexi Dona"
                if newActor == "Lexi S.":
                    newActor = "Lexi Swallow"
                if newActor == "Lilly K.":
                    newActor = "Zena Little"
                if newActor == "Lilu":
                    newActor = "Lilu Moon"
                if newActor == "Lily B.":
                    newActor = "Lily Carter"
                if newActor == "Lily L.":
                    newActor = "Lily Labeau"
                if newActor == "Lucy H.":
                    newActor = "Lucy Heart"
                if newActor == "Lucy L.":
                    newActor = "Lucy Li"
                if newActor == "Luna C.":
                    newActor = "Luna Corazon"
                if newActor == "Maria C.":
                    newActor = "Marie McCray"
                if newActor == "Medina U.":
                    newActor = "Foxy Di"
                if newActor == "Mia D.":
                    newActor = "Mia Manarote"
                if newActor == "Miela":
                    newActor = "Marry Queen"
                if newActor == "Mila K.":
                    newActor = "Michaela Isizzu"
                if newActor == "Milana R.":
                    newActor = "Milana Blanc"
                if newActor == "Milena D.":
                    newActor = "Milena Devi"
                if newActor == "Misty S.":
                    newActor = "Misty Stone"
                if newActor == "Mona L.":
                    newActor = "Mona Lee"
                if newActor == "Natalie N.":
                    newActor = "Natalie Nice"
                if newActor == "Natalli":
                    newActor = "Nathaly Cherie"
                if newActor == "Nataly G.":
                    newActor = "Nataly Gold"
                if newActor == "Nikki":
                    newActor = "Nikki Daniels"
                if newActor == "Niky S.":
                    newActor = "Niki Sweet"
                if newActor == "Patricya L.":
                    newActor = "Merry Pie"
                if newActor == "Paula S.":
                    newActor = "Paula Shy"
                if newActor == "Paulina S":
                    newActor = "Paulina Soul"
                if newActor == "Piper P.":
                    newActor = "Piper Perri"
                if newActor == "Presley H.":
                    newActor = "Presley Hart"
                if newActor == "Pristine E.":
                    newActor = "Pristine Edge"
                if newActor == "Reena":
                    newActor = "Reena Sky"
                if newActor == "Rena":
                    newActor = "Cara Mell"
                if newActor == "Renee P.":
                    newActor = "Renee Perez"
                if newActor == "Ria R.":
                    newActor = "Ria Rodrigez"
                if newActor == "Rihanna":
                    newActor = "Rihanna Samuel"
                if newActor == "Riley":
                    newActor = "Riley Jensen"
                if newActor == "Rina":
                    newActor = "Rina Ellis"
                if newActor == "Sage E.":
                    newActor = "Sage Evans"
                if newActor == "Sally C.":
                    newActor = "Sally Charles"
                if newActor == "Sandy A.":
                    newActor = "Sandy Ambrosia"
                if newActor == "Sara":
                    newActor = "Sara Jaymes"
                if newActor == "Sara L.":
                    newActor = "Sara Luvv"
                if newActor == "Scarlet B.":
                    newActor = "Scarlet Banks"
                if newActor == "Shyla":
                    newActor = "Shyla Jennings"
                if newActor == "Shyla G.":
                    newActor = "Shyla Jennings"
                if newActor == "Simona":
                    newActor = "Silvie Deluxe"
                if newActor == "Sophia J.":
                    newActor = "Sophia Jade"
                if newActor == "Stacey":
                    newActor = "Monika Benz"
                if newActor == "Stella C":
                    newActor = "Stella Cox"
                if newActor == "Sunny G.":
                    newActor = "Adele Sunshine"
                if newActor == "Suzie":
                    newActor = "Suzie Carina"
                if newActor == "Tarra W.":
                    newActor = "Tarra White"
                if newActor == "Tasha R.":
                    newActor = "Tasha Reign"
                if newActor == "Taylor V.":
                    newActor = "Taylor Vixen"
                if newActor == "Tegan S.":
                    newActor = "Teagan Summers"
                if newActor == "Tess L.":
                    newActor = "Tess Lyndon"
                if newActor == "Tiffany F.":
                    newActor = "Tiffany Fox"
                if newActor == "Tiffany T.":
                    newActor = "Tiffany Thompson"
                if newActor == "Tina":
                    newActor = "Tina Blade"
                if newActor == "Tina H.":
                    newActor = "Tina Hot"
                if newActor == "Tracy":
                    newActor = "Tracy Lindsay"
                if newActor == "Tracy A.":
                    newActor = "Tracy Gold"
                if newActor == "Tracy S.":
                    newActor = "Tracy Smile"
                if newActor == "Uma Z.":
                    newActor = "Uma Zex"
                if newActor == "Valentina N.":
                    newActor = "Valentina Nappi"
                if newActor == "Vanda":
                    newActor = "Vanda Lust"
                if newActor == "Vanea H.":
                    newActor = "Viola Bailey"
                if newActor == "Victoria B.":
                    newActor = "Victoria Blaze"
                if newActor == "Victoria P.":
                    newActor = "Victoria Puppy"
                if newActor == "Victoria R.":
                    newActor = "Victoria Rae Black"
                if newActor == "Viktoria S.":
                    newActor = "Victoria Sweet"
                if newActor == "Vinna R.":
                    newActor = "Vinna Reed"
                if newActor == "Whitney C.":
                    newActor = "Whitney Conroy"
                if newActor == "Zazie S.":
                    newActor = "Zazie Sky"
                if newActor == "Zoe V.":
                    newActor = "Zoe Voss"
            if metadata.studio == "Nubiles":
                if newActor == "Abbey":
                    newActor = "Amia Miley"
                if newActor == "Addie":
                    newActor = "Addie Moore"
                if newActor == "Addison":
                    newActor = "Addison Rose"
                if newActor == "Adella":
                    newActor = "Adel Bye"
                if newActor == "Adelle":
                    newActor = "Keira Albina"
                if newActor == "Adri":
                    newActor = "Sandra Bina"
                if newActor == "Adrianne":
                    newActor = "Adrianna Gold"
                if newActor == "Agnessa":
                    newActor = "Nessa Shine"
                if newActor == "Alana":
                    newActor = "Jayme Langford"
                if newActor == "Alanaleigh":
                    newActor = "Alana Leigh"
                if newActor == "Alana G":
                    newActor = "Alana Jade"
                if newActor == "Alena":
                    newActor = "Lucie Theodorova"
                if newActor == "Aletta":
                    newActor = "Aletta Ocean"
                if newActor == "Alexa":
                    newActor = "Aleska Diamond"
                if newActor == "Alexcia":
                    newActor = "Black Panther"
                if newActor == "Alexiasky":
                    newActor = "Alexia Sky"
                if newActor == "Alexis":
                    newActor = "Alexis Love"
                if newActor == "Aliana":
                    newActor = "Alice Miller"
                if newActor == "Alicia":
                    newActor = "Alicia Angel"
                if newActor == "Alliehaze":
                    newActor = "Allie Haze"
                if newActor == "Allyann":
                    newActor = "Ally Ann"
                if newActor == "Allyssa":
                    newActor = "Allyssa Hall"
                if newActor == "Alyssia":
                    newActor = "Nikita Black"
                if newActor == "Amai":
                    newActor = "Amai Liu"
                if newActor == "Amalie":
                    newActor = "Anita Pearl"
                if newActor == "Amber":
                    newActor = "Roxy Carter"
                if newActor == "Ami":
                    newActor = "Ami Emerson"
                if newActor == "Amy":
                    newActor = "Amy Reid"
                if newActor == "Amybrooke":
                    newActor = "Amy Brooke"
                if newActor == "Amysativa":
                    newActor = "Amy Sativa"
                if newActor == "Andie":
                    newActor = "Andie Valentino"
                if newActor == "Andrea":
                    newActor = "Jenny Sanders"
                if newActor == "Angela":
                    newActor = "Angie Emerald"
                if newActor == "Angelica":
                    newActor = "Black Angelika"
                if newActor == "Angelina":
                    newActor = "Nadia Taylor"
                if newActor == "Angelinaash":
                    newActor = "Angelina Ashe"
                if newActor == "Angellina":
                    newActor = "Angelina Brooke"
                if newActor == "Angie":
                    newActor = "Yulia Bright"
                if newActor == "Aniya":
                    newActor = "Stasia"
                if newActor == "Annabelle":
                    newActor = "Annabelle Lee"
                if newActor == "Annastevens":
                    newActor = "Anna Stevens"
                if newActor == "Anne":
                    newActor = "Playful Ann"
                if newActor == "Annette":
                    newActor = "Annette Allen"
                if newActor == "Annika":
                    newActor = "Annika Eve"
                if newActor == "Anoli":
                    newActor = "Anoli Angel"
                if newActor == "April":
                    newActor = "April Aubrey"
                if newActor == "Apriloneil":
                    newActor = "April O'Neil"
                if newActor == "Ariadna":
                    newActor = "Ariadna Moon"
                if newActor == "Ariel":
                    newActor = "Ariel Rebel"
                if newActor == "Ashlee":
                    newActor = "Ashlee Allure"
                if newActor == "Ashleyjane":
                    newActor = "Ashley Jane"
                if newActor == "Ashlynrae":
                    newActor = "Ashlyn Rae"
                if newActor == "Asuna":
                    newActor = "Asuna Fox"
                if newActor == "Athina":
                    newActor = "Tyra Moon"
                if newActor == "Aundrea":
                    newActor = "Andrea Anderson"
                if newActor == "Austin":
                    newActor = "Austin Reines"
                if newActor == "Barbra":
                    newActor = "Mellisa Medisson"
                if newActor == "Beata":
                    newActor = "Beata Undine"
                if newActor == "Bella B":
                    newActor = "Bella Blue"
                if newActor == "Bernie":
                    newActor = "Bernie Svintis"
                if newActor == "Billie":
                    newActor = "Billy Raise"
                if newActor == "Bliss":
                    newActor = "Bliss Lei"
                if newActor == "Boroka":
                    newActor = "Boroka Balls"
                if newActor == "Brea":
                    newActor = "Bree Olson"
                if newActor == "Bridget":
                    newActor = "Sugar Baby"
                if newActor == "Britne":
                    newActor = "Chloe Morgan"
                if newActor == "Britney":
                    newActor = "Liz Honey"
                if newActor == "Brynn":
                    newActor = "Brynn Tyler"
                if newActor == "Bulgari":
                    newActor = "Ashley Bulgari"
                if newActor == "Caise":
                    newActor = "Jada Gold"
                if newActor == "Calliedee":
                    newActor = "Callie Dee"
                if newActor == "Capri":
                    newActor = "Capri Anderson"
                if newActor == "Carli":
                    newActor = "Carli Banks"
                if newActor == "Carman":
                    newActor = "Carmen Kinsley"
                if newActor == "Carmen":
                    newActor = "Petra E"
                if newActor == "Carmin":
                    newActor = "Carmen McCarthy"
                if newActor == "Carrie":
                    newActor = "Sandra Kalermen"
                if newActor == "Cassandra":
                    newActor = "Cassandra Calogera"
                if newActor == "Cate":
                    newActor = "Cate Harrington"
                if newActor == "Celeste":
                    newActor = "Celeste Star"
                if newActor == "Celina":
                    newActor = "Celina Cross"
                if newActor == "Charlie":
                    newActor = "Charlie Laine"
                if newActor == "Charlielynn":
                    newActor = "Charlie Lynn"
                if newActor == "Charlotte":
                    newActor = "Charlotte Stokely"
                if newActor == "Chastity":
                    newActor = "Chastity Lynn"
                if newActor == "Chloejames":
                    newActor = "Chloe James"
                if newActor == "Chris":
                    newActor = "Christine Alexis"
                if newActor == "Christina":
                    newActor = "Krisztina Banks"
                if newActor == "Christine":
                    newActor = "Christie Lee"
                if newActor == "Cindy":
                    newActor = "Cindy Hope"
                if newActor == "Clover":
                    newActor = "Katya Clover"
                if newActor == "Conny":
                    newActor = "Connie Carter"
                if newActor == "Courtney":
                    newActor = "Courtney Cummz"
                if newActor == "Crissy":
                    newActor = "Crissy Moon"
                if newActor == "Crissysnow":
                    newActor = "Crissy Snow"
                if newActor == "Cristal":
                    newActor = "Cristal Matthews"
                if newActor == "Dana":
                    newActor = "Monica Sweet"
                if newActor == "Dani":
                    newActor = "Dani Jensen"
                if newActor == "Danielle":
                    newActor = "Danielle Maye"
                if newActor == "Daphne":
                    newActor = "Daphne Angel"
                if newActor == "Deanna":
                    newActor = "Deena Daniels"
                if newActor == "Delphine":
                    newActor = "Izzy Delphine"
                if newActor == "Dessa":
                    newActor = "Jessica Valentino"
                if newActor == "Devi":
                    newActor = "Devi Emmerson"
                if newActor == "Diamond":
                    newActor = "Paris Diamond"
                if newActor == "Dimitra":
                    newActor = "Lia Chalizo"
                if newActor == "Dina":
                    newActor = "Dana Sinnz"
                if newActor == "Diore":
                    newActor = "Dolly Diore"
                if newActor == "Dominica":
                    newActor = "Dominic Anna"
                if newActor == "Edenadams":
                    newActor = "Eden Adams"
                if newActor == "Edyphia":
                    newActor = "Pearl Ami"
                if newActor == "Eileen":
                    newActor = "Eileen Sue"
                if newActor == "Elena":
                    newActor = "Elena Rivera"
                if newActor == "Elizabethanne":
                    newActor = "Elizabeth Anne"
                if newActor == "Ella":
                    newActor = "Eufrat Mai"
                if newActor == "Ellington":
                    newActor = "Evah Ellington"
                if newActor == "Elza A":
                    newActor = "Casey Nohrman"
                if newActor == "Emy":
                    newActor = "Emy Reyes"
                if newActor == "Eriko":
                    newActor = "Nikko Jordan"
                if newActor == "Esegna":
                    newActor = "Gabriella Lati"
                if newActor == "Eva":
                    newActor = "Eva Gold"
                if newActor == "Eve":
                    newActor = "Eve Angel"
                if newActor == "Evelin":
                    newActor = "Eveline Dellai"
                if newActor == "Evelyn":
                    newActor = "Evelyn Baum"
                if newActor == "Evonna":
                    newActor = "Regina Prensley"
                if newActor == "Faina":
                    newActor = "Faina Bona"
                if newActor == "Faith":
                    newActor = "Faith Leon"
                if newActor == "Fawn":
                    newActor = "Kimberly Cox"
                if newActor == "Faye":
                    newActor = "Faye Reagan"
                if newActor == "Fayex":
                    newActor = "Faye X Taylor"
                if newActor == "Federica":
                    newActor = "Federica Hill"
                if newActor == "Felicity":
                    newActor = "Jana Jordan"
                if newActor == "Ferrera":
                    newActor = "Ferrera Gomez"
                if newActor == "Franziska":
                    newActor = "Franziska Facella"
                if newActor == "Frida":
                    newActor = "Frida Stark"
                if newActor == "Gabriella":
                    newActor = "Ariel Piper Fawn"
                if newActor == "Gemini":
                    newActor = "Carmen Gemini"
                if newActor == "Georgia":
                    newActor = "Georgia Jones"
                if newActor == "Ginger":
                    newActor = "Ginger Lee"
                if newActor == "Giselle":
                    newActor = "Goldie Baby"
                if newActor == "Grace":
                    newActor = "Lindsay Kay"
                if newActor == "Haleysweet":
                    newActor = "Haley Sweet"
                if newActor == "Hallee":
                    newActor = "Traci Lynn"
                if newActor == "Hanna":
                    newActor = "Hannah West"
                if newActor == "Heather":
                    newActor = "Samantha Sin"
                if newActor == "Heidi C":
                    newActor = "Heidi Harper"
                if newActor == "Hollyfox":
                    newActor = "Holly Fox"
                if newActor == "Ianisha":
                    newActor = "Summer Breeze"
                if newActor == "Inus":
                    newActor = "Anna Nova"
                if newActor == "Jaelyn":
                    newActor = "Jaelyn Fox"
                if newActor == "Jamie":
                    newActor = "Jewel Affair"
                if newActor == "Janelle":
                    newActor = "Karlie Montana"
                if newActor == "Jasmine":
                    newActor = "Jasmine Rouge"
                if newActor == "Jassie":
                    newActor = "Jassie James"
                if newActor == "Jenet":
                    newActor = "Leyla Black"
                if newActor == "Jenna":
                    newActor = "Jenna Presley"
                if newActor == "Jenni":
                    newActor = "Jenni Czech"
                if newActor == "Jenniah":
                    newActor = "Jenny Appach"
                if newActor == "Jenny":
                    newActor = "Jenni Lee"
                if newActor == "Jensen":
                    newActor = "Ashley Jensen"
                if newActor == "Jeny":
                    newActor = "Jeny Baby"
                if newActor == "Jesica":
                    newActor = "Leony April"
                if newActor == "Jess":
                    newActor = "Danielle Trixie"
                if newActor == "Jessie":
                    newActor = "Jessie Cox"
                if newActor == "Jordanbliss":
                    newActor = "Jordan Bliss"
                if newActor == "Jorden":
                    newActor = "Neyla Small"
                if newActor == "Judith":
                    newActor = "Judith Fox"
                if newActor == "Jujana":
                    newActor = "Zuzana Z"
                if newActor == "Julie":
                    newActor = "Juliana Grandi"
                if newActor == "Juliya":
                    newActor = "Crystal Maiden"
                if newActor == "Kacey":
                    newActor = "Kacey Jordan"
                if newActor == "Kaela":
                    newActor = "Lena Nicole"
                if newActor == "Kalilane":
                    newActor = "Kali Lane"
                if newActor == "Kalisy":
                    newActor = "Mary Kalisy"
                if newActor == "Kandi":
                    newActor = "Kandi Milan"
                if newActor == "Karanovak":
                    newActor = "Kara Novak"
                if newActor == "Kari S":
                    newActor = "Kari Sweet"
                if newActor == "Karin":
                    newActor = "Carin Kay"
                if newActor == "Karina":
                    newActor = "Karina Laboom"
                if newActor == "Kate":
                    newActor = "Kathleen Kruz"
                if newActor == "Katie":
                    newActor = "Heather Starlet"
                if newActor == "Katiejordin":
                    newActor = "Katie Jordin"
                if newActor == "Katiek":
                    newActor = "Katie Kay"
                if newActor == "Katy P":
                    newActor = "Cira Nerri"
                if newActor == "Kaula":
                    newActor = "Kayla Louise"
                if newActor == "Kaylee":
                    newActor = "Kaylee Heart"
                if newActor == "Kellie":
                    newActor = "Paige Starr"
                if newActor == "Kennedy":
                    newActor = "Kennedy Kressler"
                if newActor == "Kenzie":
                    newActor = "Mackenzee Pierce"
                if newActor == "Kimber":
                    newActor = "Kimber Lace"
                if newActor == "Kimberly":
                    newActor = "Kimberly Allure"
                if newActor == "Kimmie":
                    newActor = "Kimmie Cream"
                if newActor == "Kira":
                    newActor = "Dido Angel"
                if newActor == "Kiralanai":
                    newActor = "Kira Lanai"
                if newActor == "Kirra":
                    newActor = "Kira Zen"
                if newActor == "Klaudia":
                    newActor = "Cindy Hope"
                if newActor == "Kody":
                    newActor = "Kody Kay"
                if newActor == "Koks":
                    newActor = "Angie Koks"
                if newActor == "Krissie":
                    newActor = "Liona Levi"
                if newActor == "Kristina":
                    newActor = "Kristina Wood"
                if newActor == "Kristinarose":
                    newActor = "Kristina Rose"
                if newActor == "Krystyna":
                    newActor = "Kristina Manson"
                if newActor == "Kyra":
                    newActor = "Kyra Steele"
                if newActor == "Lady D":
                    newActor = "Lady Dee"
                if newActor == "Lanaviolet":
                    newActor = "Lana Violet"
                if newActor == "Lanewood":
                    newActor = "Louisa Lanewood"
                if newActor == "Lauracrystal":
                    newActor = "Laura Crystal"
                if newActor == "Lauren":
                    newActor = "Afrodite Night"
                if newActor == "Layna":
                    newActor = "Brigitte Hunter"
                if newActor == "Lea":
                    newActor = "Lea Tyron"
                if newActor == "Leah":
                    newActor = "Leah Luv"
                if newActor == "Leigh":
                    newActor = "Leighlani Red"
                if newActor == "Leila":
                    newActor = "Leila Smith"
                if newActor == "Lexidiamond":
                    newActor = "Lexi Diamond"
                if newActor == "Lexie":
                    newActor = "Lexi Belle"
                if newActor == "Lilian":
                    newActor = "Lilian Lee"
                if newActor == "Liliane":
                    newActor = "Liliane Tiger"
                if newActor == "Lilit":
                    newActor = "Lola Chic"
                if newActor == "Lily":
                    newActor = "Lily Cute"
                if newActor == "Lindie":
                    newActor = "Kelly Summer"
                if newActor == "Lindsay":
                    newActor = "Jenni Carmichael"
                if newActor == "Linna":
                    newActor = "Evelyn Cage"
                if newActor == "Lola":
                    newActor = "Mia Me"
                if newActor == "Lolashut":
                    newActor = "Little Caprice"
                if newActor == "Lolly":
                    newActor = "Lolly Gartner"
                if newActor == "Lolly J":
                    newActor = "Felicia Rain"
                if newActor == "Lora":
                    newActor = "Lora Craft"
                if newActor == "Loreen":
                    newActor = "Loreen Roxx"
                if newActor == "Lorena":
                    newActor = "Lorena Garcia"
                if newActor == "Luciana":
                    newActor = "Timea Bella"
                if newActor == "Lucie":
                    newActor = "Samantha Wow"
                if newActor == "Lucy":
                    newActor = "Lucy Ive"
                if newActor == "Lucylux":
                    newActor = "Lucy Lux"
                if newActor == "Lussy M":
                    newActor = "Deja Move"
                if newActor == "Lynn":
                    newActor = "Lynn Pleasant"
                if newActor == "Lynnlove":
                    newActor = "Lynn Love"
                if newActor == "Maddy":
                    newActor = "Madison Parker"
                if newActor == "Maggies":
                    newActor = "Maggie Gold"
                if newActor == "Mai":
                    newActor = "Mai Ly"
                if newActor == "Marfa":
                    newActor = "Joanna Pret"
                if newActor == "Marina":
                    newActor = "Marina Mae"
                if newActor == "Marissa":
                    newActor = "Marissa Mendoza"
                if newActor == "Marlie":
                    newActor = "Marlie Moore"
                if newActor == "Marsa":
                    newActor = "Jessi Gold"
                if newActor == "Marsha":
                    newActor = "Monica Sweat"
                if newActor == "Marta":
                    newActor = "Melena Maria Rya"
                if newActor == "Martha":
                    newActor = "Tarra White"
                if newActor == "Maya":
                    newActor = "Maya Hills"
                if newActor == "Mckenzee":
                    newActor = "Mckenzee Miles"
                if newActor == "Meggan":
                    newActor = "Meggan Mallone"
                if newActor == "Melanie":
                    newActor = "Melanie Taylor"
                if newActor == "Melissa":
                    newActor = "Melissa Matthews"
                if newActor == "Melody":
                    newActor = "Melody Kush"
                if newActor == "Mia":
                    newActor = "Mia Moon"
                if newActor == "Miahilton":
                    newActor = "Mia Hilton"
                if newActor == "Micah":
                    newActor = "Micah Moore"
                if newActor == "Michele":
                    newActor = "Michelle Brown"
                if newActor == "Michelle":
                    newActor = "Michelle Maylene"
                if newActor == "Michellemoist":
                    newActor = "Michelle Moist"
                if newActor == "Michellemyers":
                    newActor = "Michelle Myers"
                if newActor == "Miesha":
                    newActor = "Jessika Lux"
                if newActor == "Mikki":
                    newActor = "Elina Mikki"
                if newActor == "Mileyann":
                    newActor = "Miley Ann"
                if newActor == "Mili":
                    newActor = "Mili Jay"
                if newActor == "Minnie":
                    newActor = "Milla Yul"
                if newActor == "Missy":
                    newActor = "Missy Nicole"
                if newActor == "Mollymadison":
                    newActor = "Molly Madison"
                if newActor == "Monika":
                    newActor = "Monika Vesela"
                if newActor == "Monique":
                    newActor = "Monika Cajth"
                if newActor == "Monna":
                    newActor = "Monna Dark"
                if newActor == "Morgan":
                    newActor = "Nataly Gold"
                if newActor == "Ms Faris":
                    newActor = "Athena Faris"
                if newActor == "Nadea":
                    newActor = "Bella Rossi"
                if newActor == "Nancy":
                    newActor = "Nancy Bell"
                if newActor == "Nancy A":
                    newActor = "Nancy Ace"
                if newActor == "Natali":
                    newActor = "Natali Blond"
                if newActor == "Nataliex":
                    newActor = "Natalia Forrest"
                if newActor == "Natalya":
                    newActor = "Little Rita"
                if newActor == "Natosha":
                    newActor = "Monica Beluchi"
                if newActor == "Nelly":
                    newActor = "Nelli Sulivan"
                if newActor == "Nici":
                    newActor = "Nici Dee"
                if newActor == "Nicol":
                    newActor = "Ashley Stillar"
                if newActor == "Nicoleray":
                    newActor = "Nicole Ray"
                if newActor == "Nikala":
                    newActor = "Bella Cole"
                if newActor == "Niki":
                    newActor = "Nika Noire"
                if newActor == "Nikka":
                    newActor = "Scarlett Nika"
                if newActor == "Nikkivee":
                    newActor = "Nikki Vee"
                if newActor == "Nikysweet":
                    newActor = "Niky Sweet"
                if newActor == "Ninoska":
                    newActor = "Connie Rose"
                if newActor == "Nitca":
                    newActor = "Cindy Dee"
                if newActor == "Noleta":
                    newActor = "Tracy Gold"
                if newActor == "Nyusha":
                    newActor = "Olivia Brown"
                if newActor == "Olivia":
                    newActor = "Olivia La Roche"
                if newActor == "Oprah":
                    newActor = "Nathaly Cherie"
                if newActor == "Oxana":
                    newActor = "Oxana Chic"
                if newActor == "Palomino":
                    newActor = "Athena Palomino"
                if newActor == "Paris":
                    newActor = "Paris Parker"
                if newActor == "Patritcy":
                    newActor = "Merry Pie"
                if newActor == "Paula":
                    newActor = "Pavlina St."
                if newActor == "Paulina":
                    newActor = "Paulina James"
                if newActor == "Pavla":
                    newActor = "Teena Dolly"
                if newActor == "Pearl":
                    newActor = "Juicy Pearl"
                if newActor == "Penny":
                    newActor = "Abby Cross"
                if newActor == "Persia":
                    newActor = "Persia DeCarlo"
                if newActor == "Pinkule":
                    newActor = "Billie Star"
                if newActor == "Polly":
                    newActor = "Jasmine Davis"
                if newActor == "Presley":
                    newActor = "Presley Maddox"
                if newActor == "Quenna":
                    newActor = "Maria Devine"
                if newActor == "Rachel":
                    newActor = "Yasmine Gold"
                if newActor == "Rebeccablue":
                    newActor = "Rebecca Blue"
                if newActor == "Reena":
                    newActor = "Reena Sky"
                if newActor == "Renee":
                    newActor = "Renee Perez"
                if newActor == "Roberta":
                    newActor = "Lisa Musa"
                if newActor == "Rosea":
                    newActor = "Rose Delight"
                if newActor == "Roxy":
                    newActor = "Roxy Panther"
                if newActor == "Ruby":
                    newActor = "Ruby Flame"
                if newActor == "Sage":
                    newActor = "Stephanie Sage"
                if newActor == "Sally":
                    newActor = "Demi Scott"
                if newActor == "Sammie":
                    newActor = "Sammie Rhodes"
                if newActor == "Sandra":
                    newActor = "Sandra Shine"
                if newActor == "Sandy":
                    newActor = "Sandy Joy"
                if newActor == "Sandysummers":
                    newActor = "Sandy Summers"
                if newActor == "Sarah":
                    newActor = "Sarah Blake"
                if newActor == "Sarahjo":
                    newActor = "Ava Skye"
                if newActor == "Sarai":
                    newActor = "Sarai Keef"
                if newActor == "Sasha":
                    newActor = "Sasha Cane"
                if newActor == "Sassy":
                    newActor = "Monika Thu"
                if newActor == "Scarlettfay":
                    newActor = "Scarlett Fay"
                if newActor == "Sera":
                    newActor = "Sera Passion"
                if newActor == "Serendipity":
                    newActor = "Jessica Foxx"
                if newActor == "Sharon":
                    newActor = "Kristina Rud"
                if newActor == "Sheridan":
                    newActor = "Jana Sheridan"
                if newActor == "Shyla":
                    newActor = "Shyla Jennings"
                if newActor == "Sierra":
                    newActor = "Nina Stevens"
                if newActor == "Sima":
                    newActor = "Shrima Malati"
                if newActor == "Simone":
                    newActor = "Nikki Chase"
                if newActor == "Smokie":
                    newActor = "Smokie Flame"
                if newActor == "Solstice":
                    newActor = "Summer Solstice"
                if newActor == "Stacy":
                    newActor = "Mandy Dee"
                if newActor == "Summersilver":
                    newActor = "Summer Silver"
                if newActor == "Suze":
                    newActor = "Suzy Black"
                if newActor == "Suzie":
                    newActor = "Suzie Diamond"
                if newActor == "Sveta":
                    newActor = "Lita Phoenix"
                if newActor == "Sylvia":
                    newActor = "Silvie Deluxe"
                if newActor == "Talya":
                    newActor = "Lindsey Olsen"
                if newActor == "Tannermays":
                    newActor = "Tanner Mayes"
                if newActor == "Taylor":
                    newActor = "Roxanna Milana"
                if newActor == "Tea":
                    newActor = "Deny Moor"
                if newActor == "Tegan":
                    newActor = "Tegan Jane"
                if newActor == "Teresina":
                    newActor = "Teri Sweet"
                if newActor == "Tereza":
                    newActor = "Tereza Ilova"
                if newActor == "Tess":
                    newActor = "Tess Lyndon"
                if newActor == "Tessa":
                    newActor = "Sonya Durganova"
                if newActor == "Tiff":
                    newActor = "Tiffany Sweet"
                if newActor == "Toni":
                    newActor = "Kyra Black"
                if newActor == "Tonya":
                    newActor = "Casey Donell"
                if newActor == "Traci":
                    newActor = "Kirsten Andrews"
                if newActor == "Tyra":
                    newActor = "Naomi Cruise"
                if newActor == "Valerie":
                    newActor = "Valerie Herrera"
                if newActor == "Vanessa":
                    newActor = "Vanessa Monroe"
                if newActor == "Vania":
                    newActor = "Ivana Sugar"
                if newActor == "Vendula":
                    newActor = "Tiffany Diamond"
                if newActor == "Veronica":
                    newActor = "Veronica Jones"
                if newActor == "Veronicahill":
                    newActor = "Veronica Hill"
                if newActor == "Veronique":
                    newActor = "Veronique Vega"
                if newActor == "Victoria":
                    newActor = "Talia Shepard"
                if newActor == "Victoria P":
                    newActor = "Victoria Puppy"
                if newActor == "Victoriasweet":
                    newActor = "Victoria Sweet"
                if newActor == "Viera":
                    newActor = "Vika Lita"
                if newActor == "Violet":
                    newActor = "Goldie Glock"
                if newActor == "Violetta":
                    newActor = "Lily Lake"
                if newActor == "Violette":
                    newActor = "Violette Pink"
                if newActor == "Viva":
                    newActor = "Sabina Blue"
                if newActor == "Whitney":
                    newActor = "Whitney Conroy"
                if newActor == "Xenia":
                    newActor = "Zena Little"
                if newActor == "Yanka":
                    newActor = "Sasha Rose"
                if newActor == "Yvonne":
                    newActor = "Cindy Shine"
                if newActor == "Zara":
                    newActor = "Jacqueline Sweet"
                if newActor == "Zazie":
                    newActor = "Zazie Sky"
                if newActor == "Zeina":
                    newActor = "Zeina Heart"
                if newActor == "Zenia":
                    newActor = "Nadine Greenlaw"
            if metadata.studio == "TeamSkeet":
                if newActor == "Ada S":
                    newActor = "Ada Sanchez"
                if newActor == "Ariel R":
                    newActor = "Ariel Rose"
                if newActor == "Artemida":
                    newActor = "Valentina Cross"
                if newActor == "Arika":
                    newActor = "Arika Foxx"
                if newActor == "Ariana":
                    newActor = "Emma Brown"
                if newActor == "Ariadna":
                    newActor = "Ariadna Moon"
                if newActor == "Argentina":
                    newActor = "Lisa Smiles"
                if newActor == "Anfisa":
                    newActor = "Nicoline"
                if newActor == "Aliya":
                    newActor = "Rima"
                if newActor == "Ava":
                    newActor = "Ava Dalush"
                if newActor == "Avery":
                    newActor = "Diana Dali"
                if newActor == "Avina":
                    newActor = "Sunny Rise"
                if newActor == "Bailey":
                    newActor = "Lena Love"
                if newActor == "Bella":
                    newActor = "Bella Rossi"
                if newActor == "Betty":
                    newActor = "Camila"
                if newActor == "Jane":
                    newActor = "Camila"
                if newActor == "Briana":
                    newActor = "Milana Blanc"
                if newActor == "Brianna":
                    newActor = "Milana Blanc"
                if newActor == "Callie":
                    newActor = "Callie Nicole"
                if newActor == "Carre":
                    newActor = "Candy C"
                if newActor == "Casi J":
                    newActor = "Casi James"
                if newActor == "Catania":
                    newActor = "Jessi Gold"
                if newActor == "Colette":
                    newActor = "Inga E"
                if newActor == "Darla":
                    newActor = "Alektra Sky"
                if newActor == "Dinara":
                    newActor = "Arian Joy"
                if newActor == "Dunya":
                    newActor = "Alice Marshall"
                if newActor == "Ema":
                    newActor = "Chloe Blue"
                if newActor == "Erica":
                    newActor = "Kristall Rush"
                if newActor == "Sasha":
                    newActor = "Kristall Rush"
                if newActor == "Eva":
                    newActor = "Mia Reese"
                if newActor == "Fantina":
                    newActor = "Mariya C"
                if newActor == "Olga":
                    newActor = "Mariya C"
                if newActor == "Gabi":
                    newActor = "Izi"
                if newActor == "Gerta":
                    newActor = "Erika Bellucci"
                if newActor == "Hannah":
                    newActor = "Milana Fox"
                if newActor == "Jade":
                    newActor = "Netta"
                if newActor == "Jana":
                    newActor = "Janna"
                if newActor == "Janette":
                    newActor = "Lisa C"
                if newActor == "Joanna":
                    newActor = "Joanna Pret"
                if newActor == "Jordan":
                    newActor = "Rebeca Taylor"
                if newActor == "Kail":
                    newActor = "Kortny"
                if newActor == "Kajira":
                    newActor = "Kajira Bound"
                if newActor == "Kameya":
                    newActor = "Sandra Luberc"
                if newActor == "Katherine":
                    newActor = "Selena Stuart"
                if newActor == "Katie C":
                    newActor = "Katie Cummings"
                if newActor == "Katie K":
                    newActor = "Katie Kay"
                if newActor == "Kendall":
                    newActor = "Alison Faye"
                if newActor == "Kimberly":
                    newActor = "Pola Sunshine"
                if newActor == "Krista":
                    newActor = "Krista Evans"
                if newActor == "Lily L":
                    newActor = "Lily Labeau"
                if newActor == "Lada":
                    newActor = "Jay Dee"
                if newActor == "Luna":
                    newActor = "Rita Rush"
                if newActor == "Lusil":
                    newActor = "Ananta Shakti"
                if newActor == "Mackenzie":
                    newActor = "Alice Smack"
                if newActor == "Madelyn":
                    newActor = "Anna Taylor"
                if newActor == "Madison":
                    newActor = "Karina Grand"
                if newActor == "Magda":
                    newActor = "Taissia Shanti"
                if newActor == "Mai":
                    newActor = "Mai Ly"
                if newActor == "Mara":
                    newActor = "Marly Romero"
                if newActor == "Mariah":
                    newActor = "Aubree Jade"
                if newActor == "Mina":
                    newActor = "Mila Beth"
                if newActor == "Nadya":
                    newActor = "Nadia Bella"
                if newActor == "Seren":
                    newActor = "Nadia Bella"
                if newActor == "Nika":
                    newActor = "Sabrina Moor"
                if newActor == "Nora R":
                    newActor = "Sheri Vi"
                if newActor == "Parvin":
                    newActor = "Adelle Booty"
                if newActor == "Peachy":
                    newActor = "Margarita C"
                if newActor == "Petra":
                    newActor = "Dominica Phoenix"
                if newActor == "Rahyndee":
                    newActor = "Rahyndee James"
                if newActor == "Rebecca":
                    newActor = "Anita Sparkle"
                if newActor == "Riley J":
                    newActor = "Riley Jensen"
                if newActor == "Rosanna":
                    newActor = "Kate G."
                if newActor == "Sadine G":
                    newActor = "Sadine Godiva"
                if newActor == "Sarai":
                    newActor = "Sarai Keef"
                if newActor == "Serena":
                    newActor = "Carol Miller"
                if newActor == "Sheila":
                    newActor = "Marina Visconti"
                if newActor == "Sierra":
                    newActor = "Sierra Sanders"
                if newActor == "Skye":
                    newActor = "Skye West"
                if newActor == "Soleil":
                    newActor = "Soliel Marks"
                if newActor == "Sophia":
                    newActor = "Grace C"
                if newActor == "Stella":
                    newActor = "Stella Banxxx"
                if newActor == "Tori":
                    newActor = "Lola Taylor"
                if newActor == "Veiki":
                    newActor = "Miranda Deen"
                if newActor == "Viki":
                    newActor = "Bonnie Shai"
                if newActor == "Vilia":
                    newActor = "Lilu Tattoo"
                if newActor == "Viviana":
                    newActor = "Autumn Viviana"
                if newActor == "Yanie":
                    newActor = "Milla Yul"
                if newActor == "Yoga":
                    newActor = "Arya Fae, Megan Sage, and Nina North"
                if newActor == "Zarina":
                    newActor = "Aruna Aghora"
                if newActor == "Zoi":
                    newActor = "Liona Levi"

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
    actorEncoded = urllib.quote(actorName)
    try:
        databaseName = "AdultDVDEmpire"
        actorsearch = HTML.ElementFromURL("https://www.adultdvdempire.com/performer/search?q=" + actorEncoded)
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
            actorPageURL = "http://www.boobpedia.com/boobs/" + actorName.title().replace(" ", "_")
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
                actorPageURL = "http://www.babesandstars.com/" + actorName[0:1].lower() + "/" + actorName.lower().replace(" ","-").replace("'","-") +"/"
                actorPage = HTML.ElementFromURL(actorPageURL)
                actorPhotoURL = actorPage.xpath('//div[@class="profile"]//div[@class="thumb"]/img')[0].get("src")
                Log(actorName + " found in " + databaseName)
                Log("PhotoURL: " + actorPhotoURL)
            except:
                try:
                    databaseName = "IAFD"
                    searchURL = "http://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=" + actorEncoded
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
                        Log("PhotoURL: " + actorPhotoURL)
                    except:
                        Log(actorName + "not found.")
                        actorPhotoURL = ""
    return actorPhotoURL
