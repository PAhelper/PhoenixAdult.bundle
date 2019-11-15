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
            newPhoto = str(self.photosTable[actorsProcessed]).strip()

            ##### Skip an actor completely; this could be used to filter out male actors if desired
            if newActor == "Bad Name":
                skip = True
            if newActor == "Test Model Name":
                skip = True

            ##### Replace by actor name; for actors that have different aliases in the industry
            if newActor == "Abby Rains":
                newActor = "Abbey Rain"
            if newActor == "Ms Addie Juniper":
                newActor = "Addie Juniper"
            if newActor == "Adrianna Chechik":
                newActor = "Adriana Chechik"
            if newActor == "Alex D":
                newActor = "Alex D."
            if newActor == "Amia Moretti":
                newActor = "Amia Miley"
            if newActor == "Amy Reid":
                newActor = "Amy Ried"
            if newActor == "Anikka Albrite":
                newActor = "Annika Albrite"
            if newActor == "Anita Bellini":
                newActor = "Anita Bellini Berlusconi"
            if newActor == "Anjelica" or newActor == "Ebbi" or newActor == "Abby H" or newActor == "Katherine A":
                newActor = "Krystal Boyd"
            if newActor == "Anna Morna":
                newActor = "Anastasia Morna"
            if newActor == "April ONeil" or newActor == "April Oneil" or newActor == "April O'neil":
                newActor = "April O'Neil"
            if newActor == "Bibi Jones" or newActor == "Bibi Jones™":
                newActor = "Britney Beth"
            if newActor == "Bridgette B.":
                newActor = "Bridgette B"
            if newActor == "Capri Cavalli":
                newActor = "Capri Cavanni"
            if newActor == "Ce Ce Capella":
                newActor = "CeCe Capella"
            if newActor == "Charlotte Lee":
                newActor = "Jaye Summers"
            if newActor == "Criss Strokes":
                newActor = "Chris Strokes"
            if newActor == "Crissy Kay" or newActor == "Emma Hicks" or newActor == "Emma Hixx":
                newActor = "Emma Hix"
            if newActor == "Crystal Rae":
                newActor = "Cyrstal Rae"
            if newActor == "Doris Ivy":
                newActor = "Gina Gerson"
            if newActor == "Eden Sin":
                newActor = "Eden Sinclair"
            if newActor == "Elsa Dream":
                newActor = "Elsa Jean"
            if newActor == "Eve Lawrence":
                newActor = "Eve Laurence"
            if newActor == "Grace Hartley":
                newActor = "Pinky June"
            if newActor == "Hailey Reed":
                newActor = "Haley Reed"
            if newActor == "Jane Doux":
                newActor = "Pristine Edge"
            if newActor == "Jade Indica":
                newActor = "Miss Jade Indica"
            if newActor == "Jassie Gold" or newActor == "Jaggie Gold":
                newActor = "Jessi Gold"
            if newActor == "Jenna J Ross" or newActor == "Jenna J. Ross":
                newActor = "Jenna Ross"
            if newActor == "Jenny Ferri":
                newActor = "Jenny Fer"
            if newActor == "Jessica Blue" or newActor == "Jessica Cute":
                newActor = "Jessica Foxx"
            if newActor == "Jo Jo Kiss":
                newActor = "Jojo Kiss"
            if newActor == "Josephine" or newActor == "Conny" or newActor == "Conny Carter" or newActor == "Connie":
                newActor = "Connie Carter"
            if newActor == "Kagney Lynn Karter":
                newActor = "Kagney Linn Karter"
            if newActor == "Kari Sweets":
                newActor = "Kari Sweet"
            if newActor == "Katarina":
                newActor = "Katerina Hartlova"
            if newActor == "Kendra May Lust":
                newActor = "Kendra Lust"
            if newActor == "Khloe Capri" or newActor == "Chloe Capri":
                newActor = "Khloe Kapri"
            if newActor == "Lara Craft":
                newActor = "Lora Craft"
            if newActor == "Lilly LaBeau" or newActor == "Lilly Labuea" or newActor == "Lily La Beau" or newActor == "Lily Lebeau" or newActor == "Lily Luvs":
                newActor = "Lily Labeau"
            if newActor == "Lilly Lit":
                newActor = "Lilly Ford"
            if newActor == "Maddy OReilly" or newActor == "Maddy Oreilly" or newActor == "Maddy O'reilly":
                newActor = "Maddy O'Reilly"
            if newActor == "Maria Rya" or newActor == "Melena Maria":
                newActor = "Melena Maria Rya"
            if newActor == "Moe The Monster Johnson":
                newActor = "Moe Johnson"
            if newActor == "Nadya Nabakova" or newActor == "Nadya Nabokova":
                newActor = "Bunny Colby"
            if newActor == "Nancy A." or newActor == "Nancy A":
                newActor = "Nancy Ace"
            if newActor == "Nathaly" or newActor == "Nathalie Cherie" or newActor == "Natalie Cherie":
                newActor = "Nathaly Cherie"
            if newActor == "Nika Noir":
                newActor = "Nika Noire"
            if newActor == "Noe Milk" or newActor == "Noemiek":
                newActor = "Noemilk"
            if newActor == "Rebel Lynn (Contract Star)":
                newActor = "Rebel Lynn"
            if newActor == "Riley Jenson" or newActor == "Riley Anne" or newActor == "Rilee Jensen":
                newActor = "Riley Jensen"
            if newActor == "Sara Luv":
                newActor = "Sara Luvv"
            if newActor == "Dylann Vox" or newActor == "Dylan Vox":
                newActor = "Skylar Vox"
            if newActor == "Sedona" or newActor == "Stefanie Renee":
                newActor = "Stephanie Renee"
            if newActor == "Stella Bankxxx" or newActor == "Stella Ferrari":
                newActor = "Stella Banxxx"
            if newActor == "Steven St.Croix":
                newActor = "Steven St. Croix"
            if newActor == "Sybil Kailena" or newActor == "Sybil":
                newActor = "Sybil A"
            if newActor == "Tiny Teen" or newActor == "Tieny Mieny" or newActor == "Lady Jay":
                newActor = "Eva Elfie"
            if newActor == "Veronica Vega":
                newActor = "Veronica Valentine"
            ##### Replace by site + actor; use when an actor just has an alias or abbreviated name on one site
            if metadata.studio == "21Sextury":
                if newActor == "Abbie":
                    newActor = "Krystal Boyd"
                if newActor == "Ariel Temple":
                    newActor = "Katarina Muti"
            if metadata.studio == "Babes":
               if newActor == "Angelica":
                    newActor = "Krystal Boyd"
            if metadata.studio == "Bang Bros":
               if newActor == "Amy":
                    newActor = "Abella Anderson"
            if metadata.studio == "FuckedHard18":
               if newActor == "Allie H":
                    newActor = "Allie Haze"
               if newActor == "Remy":
                   newActor = "Remy LaCroix"
            if metadata.studio == "LegalPorno":
                if newActor == "Abby":
                    newActor = "Krystal Boyd"
                if newActor == "Olivia":
                    newActor = "Sophia Traxler"
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
                    newActor = "Sybil A"
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
            if metadata.studio == "Kink":
                if newActor == "Alana":
                    newActor = "Alana Evans"
                if newActor == "Kade":
                    newActor = "Deviant Kade"
                if newActor == "Alexa Jaymes":
                    newActor = "Lola Milano"
                if newActor == "Avi Scott":
                    newActor = "Avy Scott"
                if newActor == "Boo":
                    newActor = "Boo Delicious"
                if newActor == "Courtney":
                    newActor = "Courtney Devine"
                if newActor == "Cowgirl":
                    newActor = "Liz Tyler"
                if newActor == "Danielle":
                    newActor = "Natalia Wood"
                if newActor == "Diamond":
                    newActor = "Diamond Foxxx"
                if newActor == "Elyse":
                    newActor = "Elyse Stone"
                if newActor == "Emily":
                    newActor = "Emilie Davinci"
                if newActor == "Harmony":
                    newActor = "Harmony Rose"
                if newActor == "Heather Starlett":
                    newActor = "Heather Starlet"
                if newActor == "Jassie":
                    newActor = "Jassie James"
                if newActor == "Julie Night":
                    newActor = "Julie Knight"
                if newActor == "Kristine":
                    newActor = "Kristine Andrews"
                if newActor == "Leah":
                    newActor = "Leah Parker"
                if newActor == "Melanie":
                    newActor = "Melanie Jagger"
                if newActor == "Meriesa":
                    newActor = "Meriesa Arroyo"
                if newActor == "Michele Avanti":
                    newActor = "Michelle Avanti"
                if newActor == "Molly Matthews":
                    newActor = "Emily Marilyn"
                if newActor == "Naidyne":
                    newActor = "Nadine Sage"
                if newActor == "Phoenix":
                    newActor = "Phoenix Ray"
                if newActor == "Phyllisha":
                    newActor = "Phyllisha Anne"
                if newActor == "Porsha":
                    newActor = "Porsha Blaze"
                if newActor == "Ramona":
                    newActor = "Ramona Luv"
                if newActor == "Sabrine":
                    newActor = "Sabrine Maui"
                if newActor == "Sandy":
                    newActor = "Anna Ashton"
                if newActor == "Sarah Jaymes":
                    newActor = "Sara Jaymes"
                if newActor == "Sascha Sin":
                    newActor = "Sasha Sin"
                if newActor == "Tegan Summer":
                    newActor = "Teagan Summers"
                if newActor == "Wanda":
                    newActor = "Wanda Curtis"
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
                if newActor == "Chloe Cherry":
                    newActor = "Chloe Couture"
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
            if metadata.studio == "Porn Pros":
                if newActor == "Bailey Brookes":
                    newActor = "Bailey Brooke"
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
                if newActor == "Chloe Cherry":
                    newActor = "Chloe Couture"
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
            if metadata.studio == "X-Art":
                if newActor == "Abby":
                    newActor = "Abigaile Johnson"
                if newActor == "Addison":
                    newActor = "Mia Manarote"
                if newActor == "Addison C":
                    newActor = "Davina Davis"
                if newActor == "Adel":
                    newActor = "Angel Piaff"
                if newActor == "Adel M":
                    newActor = "Adel Morel"
                if newActor == "Adria":
                    newActor = "Adria Rae"
                if newActor == "Adriana":
                    newActor = "Adriana Chechik"
                if newActor == "Aidra":
                    newActor = "Aidra Fox"
                if newActor == "Aika":
                    newActor = "Aika May"
                if newActor == "Aj":
                    newActor = "Alessandra Jane"
                if newActor == "Alecia":
                    newActor = "Alecia Fox"
                if newActor == "Alena":
                    newActor = "Kiara Lord"
                if newActor == "Alexa":
                    newActor = "Alexa Grace"
                if newActor == "Alexes":
                    newActor = "Alexis Adams"
                if newActor == "Alexis":
                    newActor = "Alexis Love"
                if newActor == "Alina":
                    newActor = "Alexa Tomas"
                if newActor == "Alina H":
                    newActor = "Henessy"
                if newActor == "Aliyah":
                    newActor = "Aaliyah Love"
                if newActor == "Allie":
                    newActor = "Allie Haze"
                if newActor == "Alyssia":
                    newActor = "Alyssia Kent"
                if newActor == "Amelie":
                    newActor = "Chloe Amour"
                if newActor == "Ana":
                    newActor = "Ana Foxxx"
                if newActor == "Anais":
                    newActor = "Mae Olsen"
                if newActor == "Angel":
                    newActor = "Rosemary Radeva"
                if newActor == "Angelica":
                    newActor = "Anjelica"
                if newActor == "Angie":
                    newActor = "Angelica Kitten"
                if newActor == "Anikka":
                    newActor = "Annika Albrite"
                if newActor == "Anita":
                    newActor = "Anita Bellini Berlusconi"
                if newActor == "Anna":
                    newActor = "Gwen"
                if newActor == "Anna M":
                    newActor = "Anastasia Morna"
                if newActor == "Anneli":
                    newActor = "Pinky June"
                if newActor == "Annemarie":
                    newActor = "Samantha Heat"
                if newActor == "Anya":
                    newActor = "Anya Olsen"
                if newActor == "Aria":
                    newActor = "Sunny A"
                if newActor == "Arianna":
                    newActor = "Ariana Marie"
                if newActor == "Ariel":
                    newActor = "Ariel Piper Fawn"
                if newActor == "Ashley S":
                    newActor = "Ashlyn Molloy"
                if newActor == "Aubrey":
                    newActor = "Aubrey Star"
                if newActor == "Avril":
                    newActor = "Avril Hall"
                if newActor == "Baby":
                    newActor = "Karina"
                if newActor == "Bailey":
                    newActor = "Bailey Ryder"
                if newActor == "Bambi":
                    newActor = "Olivia Grace"
                if newActor == "Barbie":
                    newActor = "Blanche Bradburry"
                if newActor == "Poppy":
                    newActor = "Victoria Puppy"
                if newActor == "Bea":
                    newActor = "Victoria Puppy"
                if newActor == "Beatrice":
                    newActor = "Beata Undine"
                if newActor == "Becky":
                    newActor = "Bridgit A"
                if newActor == "Belle":
                    newActor = "Belle Knox"
                if newActor == "Breanne":
                    newActor = "Brea Bennett"
                if newActor == "Bree":
                    newActor = "Bree Daniels"
                if newActor == "Brooklyn":
                    newActor = "Brooklyn Lee"
                if newActor == "Brynn":
                    newActor = "Brynn Tyler"
                if newActor == "Bunny":
                    newActor = "Chloe Foster"
                if newActor == "Capri":
                    newActor = "Capri Anderson"
                if newActor == "Caprice":
                    newActor = "Little Caprice"
                if newActor == "Carla":
                    newActor = "Carla Cox"
                if newActor == "Carlie":
                    newActor = "Kasey Chase"
                if newActor == "Carmen":
                    newActor = "Jessie Rogers"
                if newActor == "Carrie":
                    newActor = "Alexis Crystal"
                if newActor == "Carrol":
                    newActor = "Lexi Dona"
                if newActor == "Casey":
                    newActor = "Vanessa"
                if newActor == "Cassidy":
                    newActor = "Cassidey Rae"
                if newActor == "Cassie":
                    newActor = "Cassie Laine"
                if newActor == "Catie":
                    newActor = "Catie Parker"
                if newActor == "Cecilia":
                    newActor = "Sicilia"
                if newActor == "Chantal":
                    newActor = "Nelly A"
                if newActor == "Charity":
                    newActor = "Charity Crawford"
                if newActor == "Charlotte":
                    newActor = "Charlotte Stokely"
                if newActor == "Chelsea":
                    newActor = "Victoria Lynn"
                if newActor == "Chloe":
                    newActor = "Victoria Sweet"
                if newActor == "Chloelynn":
                    newActor = "Chloe Lynn"
                if newActor == "Christine":
                    newActor = "Christine Paradise"
                if newActor == "Cindy":
                    newActor = "Sindy Vega"
                if newActor == "Clover":
                    newActor = "Katya Clover"
                if newActor == "Connie":
                    newActor = "Connie Carter"
                if newActor == "Corinne":
                    newActor = "Summer Breeze"
                if newActor == "Cornelia":
                    newActor = "Stacy Cruz"
                if newActor == "Crystal":
                    newActor = "Bethany"
                if newActor == "Danielle":
                    newActor = "AJ Applegate"
                if newActor == "Daphne":
                    newActor = "Daphne Klyde"
                if newActor == "Diana":
                    newActor = "Diana Fox"
                if newActor == "Dillion":
                    newActor = "Dillion Harper"
                if newActor == "Dina":
                    newActor = "Lady Dee"
                if newActor == "Dominica":
                    newActor = "Dominic Anna"
                if newActor == "Dominique":
                    newActor = "Dominika C."
                if newActor == "Elle":
                    newActor = "Elle Alexandra"
                if newActor == "Ellie":
                    newActor = "Rima B"
                if newActor == "Emilie":
                    newActor = "Emily Grey"
                if newActor == "Emily":
                    newActor = "Cassandra Nix"
                if newActor == "Emily B":
                    newActor = "Emily Brix"
                if newActor == "Emma":
                    newActor = "Emma Mae"
                if newActor == "Erica":
                    newActor = "Erica Fontes"
                if newActor == "Eufrat":
                    newActor = "Eufrat Mai"
                if newActor == "Eve":
                    newActor = "Janetta"
                if newActor == "Eve A":
                    newActor = "Ivana Sugar"
                if newActor == "Eveline":
                    newActor = "Eveline Dellai"
                if newActor == "Faye":
                    newActor = "Faye Reagan"
                if newActor == "Foxi":
                    newActor = "Foxxi Black"
                if newActor == "Francesca":
                    newActor = "Franziska Facella"
                if newActor == "Gabriella":
                    newActor = "Katie Oliver"
                if newActor == "Georgia":
                    newActor = "Georgia Jones"
                if newActor == "Gianna":
                    newActor = "Victoria Blaze"
                if newActor == "Gigi":
                    newActor = "Gigi Labonne"
                if newActor == "Gigi R":
                    newActor = "Gigi Rivera"
                if newActor == "GiiGi":
                    newActor = "Gigi Allens"
                if newActor == "Gina":
                    newActor = "Gina Gerson"
                if newActor == "Grace":
                    newActor = "Teena Dolly"
                if newActor == "Hanna":
                    newActor = "Hannah Hawthorne"
                if newActor == "Hannah":
                    newActor = "Cayla Lyons"
                if newActor == "Cayla":
                    newActor = "Cayla Lyons"
                if newActor == "Hayden":
                    newActor = "Hayden Winters"
                if newActor == "Hayden H":
                    newActor = "Hayden Hawkens"
                if newActor == "Heather":
                    newActor = "Kamila"
                if newActor == "Heidi":
                    newActor = "Taylor Sands"
                if newActor == "Heidi R":
                    newActor = "Heidi Romanova"
                if newActor == "Holly":
                    newActor = "Leonie"
                if newActor == "Ivana":
                    newActor = "Megan Promesita"
                if newActor == "Ivy":
                    newActor = "Iwia"
                if newActor == "Izzy":
                    newActor = "Izzy Delphine"
                if newActor == "Jackie":
                    newActor = "Masha D."
                if newActor == "Jade":
                    newActor = "Jade Baker"
                if newActor == "Janie":
                    newActor = "Leila Smith"
                if newActor == "Jasmine":
                    newActor = "Gina Devine"
                if newActor == "Jayden":
                    newActor = "Jayden Taylors"
                if newActor == "Jenna":
                    newActor = "Jenna Ross"
                if newActor == "Jenni":
                    newActor = "Jenni Czech"
                if newActor == "Jenny":
                    newActor = "Alicia A"
                if newActor == "Jenny M":
                    newActor = "Janny Manson"
                if newActor == "Jericha":
                    newActor = "Jericha Jem"
                if newActor == "Jessica":
                    newActor = "Aleksa Slusarchi"
                if newActor == "Jessie":
                    newActor = "Jessie Andrews"
                if newActor == "Jewel":
                    newActor = "Julia I"
                if newActor == "Jillian":
                    newActor = "Jillian Janson"
                if newActor == "Jocelyn":
                    newActor = "Ellena Woods"
                if newActor == "Joseline":
                    newActor = "Joseline Kelly"
                if newActor == "Julie":
                    newActor = "Tracy Smile"
                if newActor == "Karina":
                    newActor = "Karina White"
                if newActor == "Kassondra":
                    newActor = "Kassondra Raine"
                if newActor == "Kat":
                    newActor = "Talia Shepard"
                if newActor == "Kate":
                    newActor = "Foxy Di"
                if newActor == "Katerina":
                    newActor = "Antonia Sainz"
                if newActor == "Katherine":
                    newActor = "Kari Sweet"
                if newActor == "Katia":
                    newActor = "Joleyn Burst"
                if newActor == "Katie Jayne":
                    newActor = "Katy Jayne"
                if newActor == "Katka":
                    newActor = "Ferrera Gomez"
                if newActor == "Kato":
                    newActor = "Kimberly Kato"
                if newActor == "Katrina":
                    newActor = "Nessa Devil"
                if newActor == "Katy":
                    newActor = "Kya"
                if newActor == "Kaye":
                    newActor = "Celine"
                if newActor == "Kaylee":
                    newActor = "Candice Luca"
                if newActor == "Keira":
                    newActor = "Keira Albina"
                if newActor == "Kendall":
                    newActor = "Kendall White"
                if newActor == "Kenna":
                    newActor = "Kenna James"
                if newActor == "Kennedy":
                    newActor = "Kennedy Kressler"
                if newActor == "Kenzie":
                    newActor = "Kenze Thomas"
                if newActor == "Kiera":
                    newActor = "Kiera Winters"
                if newActor == "Kim":
                    newActor = "Katy Rose"
                if newActor == "Kimmy":
                    newActor = "Kimmy Granger"
                if newActor == "Kinsley":
                    newActor = "Kinsley Ann"
                if newActor == "Kira":
                    newActor = "Kira Thorn"
                if newActor == "Kirra":
                    newActor = "Kira Zen"
                if newActor == "Kirsten Lee":
                    newActor = "Kirsten Nicole Lee"
                if newActor == "Kitty":
                    newActor = "Kitty Jane"
                if newActor == "Klara":
                    newActor = "Zoe"
                if newActor == "Kristen":
                    newActor = "Jessica Rox"
                if newActor == "Kristi":
                    newActor = "Allison"
                if newActor == "Kristin Scott":
                    newActor = "Kristen Scott"
                if newActor == "Kylie":
                    newActor = "Kylie Nicole"
                if newActor == "Lana":
                    newActor = "Mia Hilton"
                if newActor == "Laura":
                    newActor = "Kalea Taylor"
                if newActor == "Leah":
                    newActor = "Vika T"
                if newActor == "Leila":
                    newActor = "Blue Angel"
                if newActor == "Lena":
                    newActor = "Lena Anderson"
                if newActor == "Leony":
                    newActor = "Cherry Kiss"
                if newActor == "Lexi":
                    newActor = "Lexi Belle"
                if newActor == "Lexy":
                    newActor = "Lexi Layo"
                if newActor == "Lia":
                    newActor = "Lia Lor"
                if newActor == "Lilit":
                    newActor = "Lilit Sweet"
                if newActor == "Lillianne":
                    newActor = "Ariel"
                if newActor == "Lilly":
                    newActor = "Lily Labeau"
                if newActor == "Lilly Ivy":
                    newActor = "Lily Ivy "
                if newActor == "Lilu":
                    newActor = "Lilu Moon"
                if newActor == "Lily":
                    newActor = "Naomi Nevena"
                if newActor == "Linsay":
                    newActor = "Nataly Gold"
                if newActor == "Lisa":
                    newActor = "Lauren Crist"
                if newActor == "Liv":
                    newActor = "Elisa"
                if newActor == "Liza Dawn":
                    newActor = "Lisa Dawn"
                if newActor == "Lola":
                    newActor = "Penelope Lynn"
                if newActor == "Lolita":
                    newActor = "Lexie Fox"
                if newActor == "Lorena":
                    newActor = "Lorena Garcia"
                if newActor == "Lovita":
                    newActor = "Lovita Fate"
                if newActor == "Lyra":
                    newActor = "Lyra Louvel"
                if newActor == "Malena":
                    newActor = "Malena Morgan"
                if newActor == "Malena A":
                    newActor = "Melena Maria Rya"
                if newActor == "Maria":
                    newActor = "Anna Rose"
                if newActor == "Marica":
                    newActor = "Marica Hase"
                if newActor == "Marie":
                    newActor = "Satin Bloom"
                if newActor == "Marie M.":
                    newActor = "Marie McCray"
                if newActor == "Mary":
                    newActor = "Marry Queen"
                if newActor == "Maryjane":
                    newActor = "Maryjane Johnson"
                if newActor == "Maya":
                    newActor = "Lynette"
                if newActor == "Maya M":
                    newActor = "Sapphira A"
                if newActor == "Megan":
                    newActor = "Natali Blond"
                if newActor == "Melanie":
                    newActor = "Melanie Rios"
                if newActor == "Mia":
                    newActor = "Mia Lina"
                if newActor == "Mia M":
                    newActor = "Mia Malkova"
                if newActor == "Michelle":
                    newActor = "Irina J"
                if newActor == "Mikah":
                    newActor = "Katerina"
                if newActor == "Mila K":
                    newActor = "Michaela Isizzu"
                if newActor == "Milla":
                    newActor = "Mila Azul"
                if newActor == "Mira":
                    newActor = "Diana G"
                if newActor == "Miss Pac Man":
                    newActor = "Nedda A"
                if newActor == "Misty":
                    newActor = "Paula Shy"
                if newActor == "Miu":
                    newActor = "Sabrisse"
                if newActor == "Anastasia":
                    newActor = "Monika Benz"
                if newActor == "Monika":
                    newActor = "Monika Benz"
                if newActor == "Monique":
                    newActor = "Monika Thu"
                if newActor == "Nadia":
                    newActor = "Nadia Nickels"
                if newActor == "Nancy":
                    newActor = "Nancy Ace"
                if newActor == "Naomi":
                    newActor = "Silvie Luca"
                if newActor == "Naomi B":
                    newActor = "Naomi Bennet"
                if newActor == "Nastia":
                    newActor = "Lindsey Olsen"
                if newActor == "Nastya":
                    newActor = "Nikki Stills"
                if newActor == "Natali":
                    newActor = "Elouisa"
                if newActor == "Natalie":
                    newActor = "Jaslene Jade"
                if newActor == "Natasha B":
                    newActor = "Kelly E"
                if newActor == "Nella":
                    newActor = "Lexi Foxy"
                if newActor == "Nicola":
                    newActor = "Nika"
                if newActor == "Nicole":
                    newActor = "Gina"
                if newActor == "Niki":
                    newActor = "Nikki Fox"
                if newActor == "Nikki":
                    newActor = "Nici Dee"
                if newActor == "Nikki Peaches":
                    newActor = "Nikki Peach"
                if newActor == "Nina":
                    newActor = "Nina James"
                if newActor == "Olivia":
                    newActor = "Livia Godiva"
                if newActor == "Oliya":
                    newActor = "Isabel B"
                if newActor == "Paige":
                    newActor = "Paige Owens"
                if newActor == "Pam":
                    newActor = "Lena Love"
                if newActor == "Patsy":
                    newActor = "Angelic Anya"
                if newActor == "Paulina":
                    newActor = "Susan Ayn"
                if newActor == "Pink Violet":
                    newActor = "Violette Pink"
                if newActor == "Presley":
                    newActor = "Presley Hart"
                if newActor == "Rainbow":
                    newActor = "Hannah Hays"
                if newActor == "Rebecca":
                    newActor = "Rebecca Volpetti"
                if newActor == "Reese":
                    newActor = "Paloma B"
                if newActor == "Reina":
                    newActor = "Artemis"
                if newActor == "Ria Sun":
                    newActor = "Ria Sunn"
                if newActor == "Riley":
                    newActor = "Dakoda Brookes"
                if newActor == "Ruby":
                    newActor = "Heather Starlet"
                if newActor == "Sam":
                    newActor = "Alyssa Branch"
                if newActor == "Samantha":
                    newActor = "Samantha Jolie"
                if newActor == "Sammy":
                    newActor = "Samantha Rone"
                if newActor == "Sandra":
                    newActor = "Zena Little"
                if newActor == "Sandy":
                    newActor = "Izabelle A"
                if newActor == "Sasha":
                    newActor = "Sasha Grey"
                if newActor == "Sasha D":
                    newActor = "Catina"
                if newActor == "Scarlet":
                    newActor = "Veronica Radke"
                if newActor == "Scarlett":
                    newActor = "Heather Carolin"
                if newActor == "Serena":
                    newActor = "Amarna Miller"
                if newActor == "Shrima":
                    newActor = "Shrima Malati"
                if newActor == "Silvie":
                    newActor = "Silvie Deluxe"
                if newActor == "Sophia":
                    newActor = "Sophia Fiore"
                if newActor == "Sophie":
                    newActor = "Sophia Knight"
                if newActor == "Stacy":
                    newActor = "Deina"
                if newActor == "Star":
                    newActor = "Zoey Kush"
                if newActor == "Stasha":
                    newActor = "Irina K"
                if newActor == "Stefanie":
                    newActor = "Eileen Sue"
                if newActor == "Stephanie":
                    newActor = "Stefanie"
                if newActor == "Stevie":
                    newActor = "Barbamiska"
                if newActor == "Summer":
                    newActor = "Tracy Lindsay"
                if newActor == "Sunshine":
                    newActor = "Adele Sunshine"
                if newActor == "Susie":
                    newActor = "Dido Angel"
                if newActor == "Suzie C":
                    newActor = "Suzie Carina"
                if newActor == "Sweetie":
                    newActor = "Lilith Lee"
                if newActor == "Sybil":
                    newActor = "Sybil A"
                if newActor == "Tabitha":
                    newActor = "Sarka"
                if newActor == "Talia":
                    newActor = "Talia Mint"
                if newActor == "Tara":
                    newActor = "Xandra B"
                if newActor == "Tasha":
                    newActor = "Lena"
                if newActor == "Tatiana":
                    newActor = "Leo"
                if newActor == "Teal":
                    newActor = "Lucy Li"
                if newActor == "Tess":
                    newActor = "Nadine"
                if newActor == "The Red Fox":
                    newActor = "Red Fox"
                if newActor == "Tiffany":
                    newActor = "Tiffany Thompson"
                if newActor == "Tiffany F":
                    newActor = "Tiffany Fox"
                if newActor == "Tina":
                    newActor = "Heather Night"
                if newActor == "Tori":
                    newActor = "Tori Black"
                if newActor == "Tracy":
                    newActor = "Sinovia"
                if newActor == "Vanna":
                    newActor = "Vanna Bardot"
                if newActor == "Veronica":
                    newActor = "Veronica Clark"
                if newActor == "Veronika":
                    newActor = "Anetta V."
                if newActor == "Vicki":
                    newActor = "Vicky Love"
                if newActor == "Vicky":
                    newActor = "Vicki Chase"
                if newActor == "Victoria":
                    newActor = "Victoria Rae Black"
                if newActor == "Viktoria":
                    newActor = "Scyley Jam"
                if newActor == "Vinna":
                    newActor = "Vinna Reed"
                if newActor == "Willow":
                    newActor = "Jana Mrhacova"
                if newActor == "Zazie":
                    newActor = "Zazie Sky"
            if metadata.studio == "DDFProd":
                if newActor == "Ms White-Kitten":
                    newActor = "Goldie Baby"
                if newActor == "Helen":
                    newActor = "Alena H"
            if metadata.studio == "Reality Kings":
                if newActor == "Morgan":
                    newActor = "Morgan Layne"
            if metadata.studio == "WowGirls":
                if newActor == "Clover":
                    newActor = "Katya Clover"

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
        try:
            actorPhotoURL = actorPage.xpath('//a[@class="fancy headshot"]')[0].get("href")
        except:
            actorPhotoURL = actorPage.xpath('//div[@class="fancy headshot"]')[0].get("style").replace('background-image:url(','').replace(');','')
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
