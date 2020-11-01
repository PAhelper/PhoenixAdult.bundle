import PAutils


class PhoenixActors:
    actorsTable = None
    photosTable = None
    actorsNum = 0

    def __init__(self):
        self.actorsTable = [None] * 100
        self.photosTable = [None] * 100
        self.actorsNum = 0

    def addActor(self, newActor, newPhoto):
        self.actorsTable[self.actorsNum] = newActor
        self.photosTable[self.actorsNum] = newPhoto
        self.actorsNum = self.actorsNum + 1

    def clearActors(self):
        self.actorsNum = 0

    def processActors(self, metadata):
        actorsProcessed = 0
        while actorsProcessed < self.actorsNum:
            skip = False
            # Save the potentional new Actor or Actress to a new variable, replace &nbsp; with a true space, and strip off any surrounding whitespace
            newActor = self.actorsTable[actorsProcessed].replace('\xc2\xa0', ' ').replace(',', '').strip().title()
            newPhoto = str(self.photosTable[actorsProcessed]).strip()

            newActor = ' '.join(newActor.split())

            # Skip an actor completely; this could be used to filter out male actors if desired
            if newActor == 'Bad Name':
                skip = True
            elif newActor == 'Test Model Name':
                skip = True

            if not skip:
                req = None
                if newPhoto:
                    try:
                        req = PAutils.HTTPRequest(newPhoto, 'HEAD')
                    except:
                        pass

                if not req or not req.ok:
                    newPhoto = ''

                # Replace by actor name; for actors that have different aliases in the industry
                if newActor == 'Abby Lee':
                    newActor = 'Abby Lee Brazil'
                elif newActor == 'Abby Rains':
                    newActor = 'Abbey Rain'
                elif newActor == 'Ms Addie Juniper':
                    newActor = 'Addie Juniper'
                elif newActor == 'Adrianna Chechik' or newActor == 'Adriana Chechick':
                    newActor = 'Adriana Chechik'
                elif newActor == 'Alex D':
                    newActor = 'Alex D.'
                elif newActor == 'Alura Tnt Jenson' or newActor == 'Alura \'Tnt\' Jenson':
                    newActor = 'Alura Jenson'
                elif newActor == 'Amia Moretti':
                    newActor = 'Amia Miley'
                elif newActor == 'Amy Reid':
                    newActor = 'Amy Ried'
                elif newActor == 'Ana Fox' or newActor == 'Ana Foxx':
                    newActor = 'Ana Foxxx'
                elif newActor == 'Andreina De Lux' or newActor == 'Andreina De Luxe' or newActor == 'Andreina Dlux':
                    newActor = 'Andreina Deluxe'
                elif newActor == 'Angela Piaf' or newActor == 'Angel Piaf':
                    newActor = 'Angel Piaff'
                elif newActor == 'Ani Black Fox' or newActor == 'Ani Black':
                    newActor = 'Ani Blackfox'
                elif newActor == 'Anikka Albrite':
                    newActor = 'Annika Albrite'
                elif newActor == 'Anita Bellini':
                    newActor = 'Anita Bellini Berlusconi'
                elif newActor == 'Anjelica' or newActor == 'Ebbi' or newActor == 'Abby H' or newActor == 'Katherine A':
                    newActor = 'Krystal Boyd'
                elif newActor == 'Anna Deville' or newActor == 'Anna DeVille':
                    newActor = 'Anna De Ville'
                elif newActor == 'Anna Morna':
                    newActor = 'Anastasia Morna'
                elif newActor == 'April ONeil' or newActor == 'April Oneil' or newActor == 'April O\'neil':
                    newActor = 'April O\'Neil'
                elif newActor == 'Ashley Graham':
                    newActor = 'Ashlee Graham'
                elif newActor == 'Bella Danger':
                    newActor = 'Abella Danger'
                elif newActor == 'Bibi Jones' or newActor == 'Bibi Jones™':
                    newActor = 'Britney Beth'
                elif newActor == 'Bridgette B.':
                    newActor = 'Bridgette B'
                elif newActor == 'Capri Cavalli':
                    newActor = 'Capri Cavanni'
                elif newActor == 'Carrie Cherry' or newActor == 'Carry Cherri' or newActor == 'Corry Cherry' or newActor == 'Kerry Cherry' or newActor == 'Dormiona':
                    newActor = 'Carry Cherry'
                elif newActor == 'Ce Ce Capella':
                    newActor = 'CeCe Capella'
                elif newActor == 'Charli Red':
                    newActor = 'Charlie Red'
                elif newActor == 'Charlotte Lee':
                    newActor = 'Jaye Summers'
                elif newActor == 'Criss Strokes':
                    newActor = 'Chris Strokes'
                elif newActor == 'Christy Charming':
                    newActor = 'Paula Shy'
                elif newActor == 'CléA Gaultier':
                    newActor = 'Clea Gaultier'
                elif newActor == 'Crissy Kay' or newActor == 'Emma Hicks' or newActor == 'Emma Hixx':
                    newActor = 'Emma Hix'
                elif newActor == 'Crystal Rae':
                    newActor = 'Cyrstal Rae'
                elif newActor == 'Doris Ivy':
                    newActor = 'Gina Gerson'
                elif newActor == 'Eden Sin':
                    newActor = 'Eden Sinclair'
                elif newActor == 'Elsa Dream':
                    newActor = 'Elsa Jean'
                elif newActor == 'Eve Lawrence':
                    newActor = 'Eve Laurence'
                elif newActor == 'Francesca Di Caprio' or newActor == 'Francesca Dicaprio':
                    newActor = 'Francesca DiCaprio'
                elif newActor == 'Goldie':
                    newActor = 'Goldie Glock'
                elif newActor == 'Guiliana Alexis':
                    newActor = 'Gulliana Alexis'
                elif newActor == 'Grace Hartley':
                    newActor = 'Pinky June'
                elif newActor == 'Hailey Reed':
                    newActor = 'Haley Reed'
                elif newActor == 'Josephina Jackson':
                    newActor = 'Josephine Jackson'
                elif newActor == 'Jane Doux':
                    newActor = 'Pristine Edge'
                elif newActor == 'Jade Indica':
                    newActor = 'Miss Jade Indica'
                elif newActor == 'Jassie Gold' or newActor == 'Jaggie Gold':
                    newActor = 'Jessi Gold'
                elif newActor == 'Jenna J Ross' or newActor == 'Jenna J. Ross':
                    newActor = 'Jenna Ross'
                elif newActor == 'Jenny Ferri':
                    newActor = 'Jenny Fer'
                elif newActor == 'Jessica Blue' or newActor == 'Jessica Cute':
                    newActor = 'Jessica Foxx'
                elif newActor == 'Jo Jo Kiss':
                    newActor = 'Jojo Kiss'
                elif newActor == 'Josephine' or newActor == 'Conny' or newActor == 'Conny Carter' or newActor == 'Connie':
                    newActor = 'Connie Carter'
                elif newActor == 'Kagney Lynn Karter':
                    newActor = 'Kagney Linn Karter'
                elif newActor == 'Kari Sweets':
                    newActor = 'Kari Sweet'
                elif newActor == 'Katarina':
                    newActor = 'Katerina Hartlova'
                elif newActor == 'Kendra May Lust':
                    newActor = 'Kendra Lust'
                elif newActor == 'Khloe Capri' or newActor == 'Chloe Capri':
                    newActor = 'Khloe Kapri'
                elif newActor == 'Lara Craft':
                    newActor = 'Lora Craft'
                elif newActor == 'Lilly LaBeau' or newActor == 'Lilly Labuea' or newActor == 'Lily La Beau' or newActor == 'Lily Lebeau' or newActor == 'Lily Luvs':
                    newActor = 'Lily Labeau'
                elif newActor == 'Lilly Lit':
                    newActor = 'Lilly Ford'
                elif newActor == 'Maddy OReilly' or newActor == 'Maddy Oreilly' or newActor == 'Maddy O\'reilly':
                    newActor = 'Maddy O\'Reilly'
                elif newActor == 'Maria Rya' or newActor == 'Melena Maria':
                    newActor = 'Melena Maria Rya'
                elif newActor == 'Moe The Monster Johnson':
                    newActor = 'Moe Johnson'
                elif newActor == 'Nadya Nabakova' or newActor == 'Nadya Nabokova':
                    newActor = 'Bunny Colby'
                elif newActor == 'Nancy A.' or newActor == 'Nancy A':
                    newActor = 'Nancy Ace'
                elif newActor == 'Nathaly' or newActor == 'Nathalie Cherie' or newActor == 'Natalie Cherie':
                    newActor = 'Nathaly Cherie'
                elif newActor == 'Nika Noir':
                    newActor = 'Nika Noire'
                elif newActor == 'Noe Milk' or newActor == 'Noemiek':
                    newActor = 'Noemilk'
                elif newActor == 'Rebel Lynn (Contract Star)':
                    newActor = 'Rebel Lynn'
                elif newActor == 'Remy La Croix':
                    newActor = 'Remy Lacroix'
                elif newActor == 'Riley Jenson' or newActor == 'Riley Anne' or newActor == 'Rilee Jensen':
                    newActor = 'Riley Jensen'
                elif newActor == 'Sara Luv':
                    newActor = 'Sara Luvv'
                elif newActor == 'Scarlet Rebel' or newActor == 'Scarlett Rebel' or newActor == 'Scarlett Domingo':
                    newActor = 'Scarlet Domingo'
                elif newActor == 'Shalina Devine':
                    newActor = 'Shalina Divine'
                elif newActor == 'Dylann Vox' or newActor == 'Dylan Vox':
                    newActor = 'Skylar Vox'
                elif newActor == 'Stephanie Moon' or newActor == 'Steffy Moon':
                    newActor = 'Stefanie Moon'
                elif newActor == 'Sedona' or newActor == 'Stefanie Renee':
                    newActor = 'Stephanie Renee'
                elif newActor == 'Stella Bankxxx' or newActor == 'Stella Ferrari':
                    newActor = 'Stella Banxxx'
                elif newActor == 'Steven St.Croix':
                    newActor = 'Steven St. Croix'
                elif newActor == 'Sybil Kailena' or newActor == 'Sybil':
                    newActor = 'Sybil A'
                elif newActor == 'Tiny Teen' or newActor == 'Tieny Mieny' or newActor == 'Lady Jay' or newActor == 'Tiny Teen / Eva Elfie':
                    newActor = 'Eva Elfie'
                elif newActor == 'Veronica Vega':
                    newActor = 'Veronica Valentine'
                elif newActor == 'Zoey Bloom':
                    newActor = 'Zoe Bloom'
                elif newActor == 'Shinoda Yuu':
                    newActor = 'Yu Shinoda'
                elif newActor == 'Viola Bailey’S':
                    newActor = 'Viola Bailey'
                elif newActor == 'Ornella Morgen':
                    newActor = 'Ornella Morgan'
                elif newActor == 'Polly Pon':
                    newActor = 'Polly Pons'
                elif newActor == 'Riley Starr':
                    newActor = 'Riley Star'
                elif newActor == 'Rosaline Rose':
                    newActor = 'Rosaline Rosa'
                elif newActor == 'Selvaggia':
                    newActor = 'Selvaggia Babe'

                # Replace by site + actor; use when an actor just has an alias or abbreviated name on one site
                if metadata.studio == '21Sextury' or metadata.studio == 'Footsie Babes':
                    if newActor == 'Abbie':
                        newActor = 'Krystal Boyd'
                    elif newActor == 'Ariel Temple':
                        newActor = 'Katarina Muti'
                    elif newActor == 'Henna Ssy':
                        newActor = 'Henessy'
                    elif newActor == 'Stefanie':
                        newActor = 'Stefanie Moon'
                elif metadata.studio == 'Babes':
                    if newActor == 'Angelica':
                        newActor = 'Krystal Boyd'
                    elif newActor == 'Ariel':
                        newActor = 'Ariel Piper Fawn'
                    elif newActor == 'Aiko May':
                        newActor = 'Aika May'
                    elif newActor == 'Clover':
                        newActor = 'Katya Clover'
                elif metadata.studio == 'Bang Bros':
                    if newActor == 'Amy':
                        newActor = 'Abella Anderson'
                    elif newActor == 'Noemi Bilas':
                        newActor = 'Noemie Bilas'
                elif metadata.studio == 'ClubSeventeen':
                    if newActor == 'Scarlet':
                        newActor = 'Scarlet Domingo'
                    elif newActor == 'Katy E':
                        newActor = 'Katy Rose'
                elif metadata.studio == 'CumLouder':
                    if newActor == 'Scarlett':
                        newActor = 'Scarlet Domingo'
                elif metadata.studio == 'Deeper' or metadata.studio == 'Tushyraw' or metadata.studio == 'Tushy' or metadata.studio == 'Blacked' or metadata.studio == 'Blackedraw' or metadata.studio == 'Vixen':
                    if newActor == 'Vikalita':
                        newActor = 'Vika Lita'
                    elif newActor == 'Vina Skyy':
                        newActor = 'Vina Sky'
                elif metadata.studio == 'Evilangel':
                    if newActor == 'Scarlet':
                        newActor = 'Scarlet Domingo'
                elif metadata.studio == 'FuelVirtual':
                    if newActor == 'Nicole':
                        newActor = 'Nicole Ray'
                    elif newActor == 'August':
                        newActor = 'August Ames'
                    elif newActor == 'Lexi':
                        newActor = 'Lexi Belle'
                    elif newActor == 'Victoria R':
                        newActor = 'Victoria Rae Black'
                    elif newActor == 'Tori':
                        newActor = 'Tori Black'
                    elif newActor == 'Tessa':
                        newActor = 'Tessa Taylor'
                    elif newActor == 'Holly':
                        newActor = 'Holly Michaels'
                    elif newActor == 'Molly':
                        newActor = 'Molly Bennett'
                    elif newActor == 'Jaslene':
                        newActor = 'Jaslene Jade'
                    elif newActor == 'Mia':
                        newActor = 'Mia Malkova'
                    elif newActor == 'Lily':
                        newActor = 'Lily Carter'
                    elif newActor == 'Vanessa':
                        newActor = 'Vanessa Cage'
                    elif newActor == 'Riley':
                        newActor = 'Riley Reid'
                    elif newActor == 'Casi':
                        newActor = 'Casi James'
                    elif newActor == 'Karina':
                        newActor = 'Karina White'
                    elif newActor == 'Dillion':
                        newActor = 'Dillion Harper'
                    elif newActor == 'Lola':
                        newActor = 'Lola Foxx'
                    elif newActor == 'Stacie':
                        newActor = 'Stacie Jaxx'
                    elif newActor == 'Dillon':
                        newActor = 'Dillion Harper'
                    elif newActor == 'Belle':
                        newActor = 'Belle Knox'
                    elif newActor == 'Emily':
                        newActor = 'Emily Grey'
                    elif newActor == 'Kennedy':
                        newActor = 'Kennedy Leigh'
                    elif newActor == 'Alina':
                        newActor = 'Alina Li'
                    elif newActor == 'Brittany':
                        newActor = 'Bibi Jones'
                    elif newActor == 'Lexi B':
                        newActor = 'Lexi Bloom'
                    elif newActor == 'Maryjane':
                        newActor = 'Mary Jane Johnson'
                    elif newActor == 'Ella M':
                        newActor = 'Ella Milano'
                    elif newActor == 'Rebecca':
                        newActor = 'Rebecca Linares'
                    elif newActor == 'Hayden':
                        newActor = 'Hayden Winters'
                    elif newActor == 'Victoria':
                        newActor = 'Victoria Rae Black'
                    elif newActor == 'Erin':
                        newActor = 'Erin Stone'
                    elif newActor == 'Hope':
                        newActor = 'Hope Howell'
                    elif newActor == 'Whitney':
                        newActor = 'Whitney Westgate'
                    elif newActor == 'Lily':
                        newActor = 'Lily Love'
                    elif newActor == 'Allie':
                        newActor = 'Allie Rae'
                    elif newActor == 'Jenna':
                        newActor = 'Jenna Rose'
                    elif newActor == 'Isis':
                        newActor = 'Isis Taylor'
                    elif newActor == 'Kodi':
                        newActor = 'Kodi Gamble'
                    elif newActor == 'Haley':
                        newActor = 'Haley Cummings'
                    elif newActor == 'Lily C':
                        newActor = 'Lily Carter'
                    elif newActor == 'Jynx':
                        newActor = 'Jynx Maze'
                    elif newActor == 'Allie H':
                        newActor = 'Allie Haze'
                    elif newActor == 'Lizz':
                        newActor = 'Lizz Taylor'
                    elif newActor == 'Evilyn':
                        newActor = 'Evilyn Fierce'
                    elif newActor == 'Lexi D':
                        newActor = 'Lexi Diamond'
                    elif newActor == 'Ashlyn':
                        newActor = 'Ashlyn Rae'
                    elif newActor == 'Presley':
                        newActor = 'Presley Carter'
                    elif newActor == 'Zoey':
                        newActor = 'Zoey Kush'
                    elif newActor == 'Madison':
                        newActor = 'Madison Ivy'
                    elif newActor == 'Britney B':
                        newActor = 'Bibi jones'
                    elif newActor == 'Staci':
                        newActor = 'Staci Silverstone'
                    elif newActor == 'Tealey':
                        newActor = 'Teal Conrad'
                    elif newActor == 'Brooklyn':
                        newActor = 'Brooklyn Chase'
                    elif newActor == 'Casana':
                        newActor = 'Casana Lei'
                    elif newActor == 'Jessica':
                        newActor = 'Jessica Robbins'
                    elif newActor == 'Naomi':
                        newActor = 'Naomi West'
                    elif newActor == 'Janice':
                        newActor = 'Janice Griffith'
                    elif newActor == 'Scarlet':
                        newActor = 'Scarlet Red'
                    elif newActor == 'Jayden':
                        newActor = 'Jayden Taylors'
                    elif newActor == 'Lacy':
                        newActor = 'Lacy Channing'
                    elif newActor == 'Alexis':
                        newActor = 'Alexis Adams'
                    elif newActor == 'Pristine':
                        newActor = 'Pristine Edge'
                    elif newActor == 'Elsa':
                        newActor = 'Elsa Jean'
                    elif newActor == 'Lucy':
                        newActor = 'Lucy Doll'
                    elif newActor == 'Abigaile':
                        newActor = 'Abigaile Johnson'
                    elif newActor == 'Stephanie C':
                        newActor = 'Stephanie Cane'
                    elif newActor == 'Aletta':
                        newActor = 'Aletta Ocean'
                    elif newActor == 'Remy':
                        newActor = 'Remy LaCroix'
                elif metadata.studio == 'Holed':
                    if newActor == 'Scarlet':
                        newActor = 'Scarlet Domingo'
                elif metadata.studio == 'LegalPorno':
                    if newActor == 'Abby':
                        newActor = 'Krystal Boyd'
                    elif newActor == 'Olivia':
                        newActor = 'Sophia Traxler'
                elif metadata.studio == 'Joymii':
                    if newActor == 'Abigail':
                        newActor = 'Abigaile Johnson'
                    elif newActor == 'Aleska D.':
                        newActor = 'Aleska Diamond'
                    elif newActor == 'Alessandra J.':
                        newActor = 'Alessandra Jane'
                    elif newActor == 'Alexa':
                        newActor = 'Alexa Tomas'
                    elif newActor == 'Alexis':
                        newActor = 'Alexis Crystal'
                    elif newActor == 'Alexis B.':
                        newActor = 'Alexis Brill'
                    elif newActor == 'Alexis T.':
                        newActor = 'Alexis Texas'
                    elif newActor == 'Alexis V.':
                        newActor = 'Alexis Venton'
                    elif newActor == 'Alice B.':
                        newActor = 'Mira Sunset'
                    elif newActor == 'Allie J.':
                        newActor = 'Allie Jordan'
                    elif newActor == 'Alysa':
                        newActor = 'Alyssa Branch'
                    elif newActor == 'Amirah A.':
                        newActor = 'Amirah Adara'
                    elif newActor == 'Andie':
                        newActor = 'Andie Darling'
                    elif newActor == 'Angel B.':
                        newActor = 'Angel Blade'
                    elif newActor == 'Anita B.':
                        newActor = 'Anita Bellini'
                    elif newActor == 'Anna P.':
                        newActor = 'Cayenne Klein'
                    elif newActor == 'Anneli':
                        newActor = 'Pinky June'
                    elif newActor == 'Apolonia':
                        newActor = 'Apolonia Lapiedra'
                    elif newActor == 'Ariel':
                        newActor = 'Ariel Piper Fawn'
                    elif newActor == 'Athina':
                        newActor = 'Tyra Moon'
                    elif newActor == 'Aubrey J.':
                        newActor = 'Aubrey James'
                    elif newActor == 'Avril H.':
                        newActor = 'Avril Hall'
                    elif newActor == 'Bailey D.':
                        newActor = 'Lovenia Lux'
                    elif newActor == 'Bailey R.':
                        newActor = 'Bailey Ryder'
                    elif newActor == 'Belinda':
                        newActor = 'Rose Delight'
                    elif newActor == 'Billie':
                        newActor = 'Billie Star'
                    elif newActor == 'Blanche B.':
                        newActor = 'Blanche Bradburry'
                    elif newActor == 'Brittany':
                        newActor = 'Brittney Banxxx'
                    elif newActor == 'Candice':
                        newActor = 'Candice Luca'
                    elif newActor == 'Candy B.':
                        newActor = 'Candy Blond'
                    elif newActor == 'Caprice':
                        newActor = 'Little Caprice'
                    elif newActor == 'Carmen C.':
                        newActor = 'Carmen McCarthy'
                    elif newActor == 'Carolina':
                        newActor = 'Carolina Abril'
                    elif newActor == 'Cayla L.':
                        newActor = 'Cayla Lyons'
                    elif newActor == 'Celeste':
                        newActor = 'Celeste Star'
                    elif newActor == 'Chastity L.':
                        newActor = 'Chastity Lynn'
                    elif newActor == 'Cherry K.':
                        newActor = 'Cherry Kiss'
                    elif newActor == 'Christen':
                        newActor = 'Christen Courtney'
                    elif newActor == 'Cindy D.':
                        newActor = 'Cindy Dollar'
                    elif newActor == 'Cindy L.':
                        newActor = 'Cindy Carson'
                    elif newActor == 'Clea G':
                        newActor = 'Clea Gaultier'
                    elif newActor == 'Clover':
                        newActor = 'Katya Clover'
                    elif newActor == 'Coco':
                        newActor = 'Coco de Mal'
                    elif newActor == 'Dani D.':
                        newActor = 'Dani Daniels'
                    elif newActor == 'Davina E.':
                        newActor = 'Sybil A'
                    elif newActor == 'Dee':
                        newActor = 'Lady Dee'
                    elif newActor == 'Defrancesca':
                        newActor = 'Defrancesca Gallardo'
                    elif newActor == 'Delphine':
                        newActor = 'Izzy Delphine'
                    elif newActor == 'Denisa':
                        newActor = 'Denisa Heaven'
                    elif newActor == 'Eliana R.':
                        newActor = 'Elaina Raye'
                    elif newActor == 'Ella M.':
                        newActor = 'Ella Milano'
                    elif newActor == 'Erika K.':
                        newActor = 'Erika Kortni'
                    elif newActor == 'Eufrat':
                        newActor = 'Eufrat Mai'
                    elif newActor == 'Eveline D.':
                        newActor = 'Eveline Dellai'
                    elif newActor == 'Evi F.':
                        newActor = 'Evi Fox'
                    elif newActor == 'Evilyn F.':
                        newActor = 'Evilyn Fierce'
                    elif newActor == 'Faye R.':
                        newActor = 'Faye Reagan'
                    elif newActor == 'Ferrera':
                        newActor = 'Ferrera Gomez'
                    elif newActor == 'Frida S.':
                        newActor = 'Frida Sante'
                    elif newActor == 'Gina G.':
                        newActor = 'Gina Gerson'
                    elif newActor == 'Gina V.':
                        newActor = 'Gina Devine'
                    elif newActor == 'Ginebra B.':
                        newActor = 'Ginebra Bellucci'
                    elif newActor == 'Ginger':
                        newActor = 'Ginger Fox'
                    elif newActor == 'Giselle L.':
                        newActor = 'Giselle Leon'
                    elif newActor == 'Hayden W.':
                        newActor = 'Hayden Winters'
                    elif newActor == 'Heather S.':
                        newActor = 'Heather Starlet'
                    elif newActor == 'Holly':
                        newActor = 'Holly Anderson'
                    elif newActor == 'Holly M.':
                        newActor = 'Holly Michaels'
                    elif newActor == 'Ivy':
                        newActor = 'Iwia'
                    elif newActor == 'Jana J.':
                        newActor = 'Jana Jordan'
                    elif newActor == 'Jana Q.':
                        newActor = 'Emma Brown'
                    elif newActor == 'Jane F.':
                        newActor = 'Nancy Ace'
                    elif newActor == 'Jayden C.':
                        newActor = 'Jayden Cole'
                    elif newActor == 'Jennifer W.':
                        newActor = 'Jennifer White'
                    elif newActor == 'Jessica':
                        newActor = 'Leony April'
                    elif newActor == 'Jessica B.':
                        newActor = 'Jessica Bee'
                    elif newActor == 'Jessie':
                        newActor = 'Jessie Jazz'
                    elif newActor == 'Josephine':
                        newActor = 'Connie Carter'
                    elif newActor == 'Julia R.':
                        newActor = 'Julia Roca'
                    elif newActor == 'Kaci S.':
                        newActor = 'Kaci Starr'
                    elif newActor == 'Kari':
                        newActor = 'Kari Sweet'
                    elif newActor == 'Karlie':
                        newActor = 'Karlie Montana'
                    elif newActor == 'Karol T.':
                        newActor = 'Karol Lilien'
                    elif newActor == 'Katie G.':
                        newActor = 'Kattie Gold'
                    elif newActor == 'Katie J.':
                        newActor = 'Katie Jordin'
                    elif newActor == 'Katy R.':
                        newActor = 'Katy Rose'
                    elif newActor == 'Kelly W':
                        newActor = 'Kelly White'
                    elif newActor == 'Kiara D.':
                        newActor = 'Kiara Diane'
                    elif newActor == 'Kiara L.':
                        newActor = 'Kiara Lord'
                    elif newActor == 'Kira T.':
                        newActor = 'Kira Thorn'
                    elif newActor == 'Kitty J.':
                        newActor = 'Kitty Jane'
                    elif newActor == 'Lara':
                        newActor = 'Dido Angel'
                    elif newActor == 'Lena N.':
                        newActor = 'Lena Nicole'
                    elif newActor == 'Lexi D.':
                        newActor = 'Lexi Dona'
                    elif newActor == 'Lexi S.':
                        newActor = 'Lexi Swallow'
                    elif newActor == 'Lilly K.':
                        newActor = 'Zena Little'
                    elif newActor == 'Lilu':
                        newActor = 'Lilu Moon'
                    elif newActor == 'Lily B.':
                        newActor = 'Lily Carter'
                    elif newActor == 'Lily L.':
                        newActor = 'Lily Labeau'
                    elif newActor == 'Lucy H.':
                        newActor = 'Lucy Heart'
                    elif newActor == 'Lucy L.':
                        newActor = 'Lucy Li'
                    elif newActor == 'Luna C.':
                        newActor = 'Luna Corazon'
                    elif newActor == 'Maria C.':
                        newActor = 'Marie McCray'
                    elif newActor == 'Medina U.':
                        newActor = 'Foxy Di'
                    elif newActor == 'Mia D.':
                        newActor = 'Mia Manarote'
                    elif newActor == 'Miela':
                        newActor = 'Marry Queen'
                    elif newActor == 'Mila K.':
                        newActor = 'Michaela Isizzu'
                    elif newActor == 'Milana R.':
                        newActor = 'Milana Blanc'
                    elif newActor == 'Milena D.':
                        newActor = 'Milena Devi'
                    elif newActor == 'Misty S.':
                        newActor = 'Misty Stone'
                    elif newActor == 'Mona L.':
                        newActor = 'Mona Lee'
                    elif newActor == 'Natalie N.':
                        newActor = 'Natalie Nice'
                    elif newActor == 'Natalli':
                        newActor = 'Nathaly Cherie'
                    elif newActor == 'Nataly G.':
                        newActor = 'Nataly Gold'
                    elif newActor == 'Nikki':
                        newActor = 'Nikki Daniels'
                    elif newActor == 'Niky S.':
                        newActor = 'Niki Sweet'
                    elif newActor == 'Patricya L.':
                        newActor = 'Merry Pie'
                    elif newActor == 'Paula S.':
                        newActor = 'Paula Shy'
                    elif newActor == 'Paulina S':
                        newActor = 'Paulina Soul'
                    elif newActor == 'Piper P.':
                        newActor = 'Piper Perri'
                    elif newActor == 'Presley H.':
                        newActor = 'Presley Hart'
                    elif newActor == 'Pristine E.':
                        newActor = 'Pristine Edge'
                    elif newActor == 'Reena':
                        newActor = 'Reena Sky'
                    elif newActor == 'Rena':
                        newActor = 'Cara Mell'
                    elif newActor == 'Renee P.':
                        newActor = 'Renee Perez'
                    elif newActor == 'Ria R.':
                        newActor = 'Ria Rodrigez'
                    elif newActor == 'Rihanna':
                        newActor = 'Rihanna Samuel'
                    elif newActor == 'Riley':
                        newActor = 'Riley Jensen'
                    elif newActor == 'Rina':
                        newActor = 'Rina Ellis'
                    elif newActor == 'Sage E.':
                        newActor = 'Sage Evans'
                    elif newActor == 'Sally C.':
                        newActor = 'Sally Charles'
                    elif newActor == 'Sandy A.':
                        newActor = 'Sandy Ambrosia'
                    elif newActor == 'Sara':
                        newActor = 'Sara Jaymes'
                    elif newActor == 'Sara L.':
                        newActor = 'Sara Luvv'
                    elif newActor == 'Scarlet B.':
                        newActor = 'Scarlet Banks'
                    elif newActor == 'Shyla':
                        newActor = 'Shyla Jennings'
                    elif newActor == 'Shyla G.':
                        newActor = 'Shyla Jennings'
                    elif newActor == 'Simona':
                        newActor = 'Silvie Deluxe'
                    elif newActor == 'Sophia J.':
                        newActor = 'Sophia Jade'
                    elif newActor == 'Stacey':
                        newActor = 'Monika Benz'
                    elif newActor == 'Stella C':
                        newActor = 'Stella Cox'
                    elif newActor == 'Sunny G.':
                        newActor = 'Adele Sunshine'
                    elif newActor == 'Suzie':
                        newActor = 'Suzie Carina'
                    elif newActor == 'Tarra W.':
                        newActor = 'Tarra White'
                    elif newActor == 'Tasha R.':
                        newActor = 'Tasha Reign'
                    elif newActor == 'Taylor V.':
                        newActor = 'Taylor Vixen'
                    elif newActor == 'Tegan S.':
                        newActor = 'Teagan Summers'
                    elif newActor == 'Tess L.':
                        newActor = 'Tess Lyndon'
                    elif newActor == 'Tiffany F.':
                        newActor = 'Tiffany Fox'
                    elif newActor == 'Tiffany T.':
                        newActor = 'Tiffany Thompson'
                    elif newActor == 'Tina':
                        newActor = 'Tina Blade'
                    elif newActor == 'Tina H.':
                        newActor = 'Tina Hot'
                    elif newActor == 'Tracy':
                        newActor = 'Tracy Lindsay'
                    elif newActor == 'Tracy A.':
                        newActor = 'Tracy Gold'
                    elif newActor == 'Tracy S.':
                        newActor = 'Tracy Smile'
                    elif newActor == 'Uma Z.':
                        newActor = 'Uma Zex'
                    elif newActor == 'Valentina N.':
                        newActor = 'Valentina Nappi'
                    elif newActor == 'Vanda':
                        newActor = 'Vanda Lust'
                    elif newActor == 'Vanea H.':
                        newActor = 'Viola Bailey'
                    elif newActor == 'Victoria B.':
                        newActor = 'Victoria Blaze'
                    elif newActor == 'Victoria P.':
                        newActor = 'Victoria Puppy'
                    elif newActor == 'Victoria R.':
                        newActor = 'Victoria Rae Black'
                    elif newActor == 'Viktoria S.':
                        newActor = 'Victoria Sweet'
                    elif newActor == 'Vinna R.':
                        newActor = 'Vinna Reed'
                    elif newActor == 'Whitney C.':
                        newActor = 'Whitney Conroy'
                    elif newActor == 'Zazie S.':
                        newActor = 'Zazie Sky'
                    elif newActor == 'Zoe V.':
                        newActor = 'Zoe Voss'
                elif metadata.studio == 'Jules Jordan':
                    if newActor == 'Jesse':
                        newActor = 'Jesse Jane'
                elif metadata.studio == 'Kink':
                    if newActor == 'Alana':
                        newActor = 'Alana Evans'
                    elif newActor == 'Kade':
                        newActor = 'Deviant Kade'
                    elif newActor == 'Alexa Jaymes':
                        newActor = 'Lola Milano'
                    elif newActor == 'Avi Scott':
                        newActor = 'Avy Scott'
                    elif newActor == 'Boo':
                        newActor = 'Boo Delicious'
                    elif newActor == 'Courtney':
                        newActor = 'Courtney Devine'
                    elif newActor == 'Cowgirl':
                        newActor = 'Liz Tyler'
                    elif newActor == 'Danielle':
                        newActor = 'Natalia Wood'
                    elif newActor == 'Diamond':
                        newActor = 'Diamond Foxxx'
                    elif newActor == 'Elyse':
                        newActor = 'Elyse Stone'
                    elif newActor == 'Emily':
                        newActor = 'Emilie Davinci'
                    elif newActor == 'Harmony':
                        newActor = 'Harmony Rose'
                    elif newActor == 'Heather Starlett':
                        newActor = 'Heather Starlet'
                    elif newActor == 'Jassie':
                        newActor = 'Jassie James'
                    elif newActor == 'Julie Night':
                        newActor = 'Julie Knight'
                    elif newActor == 'Kristine':
                        newActor = 'Kristine Andrews'
                    elif newActor == 'Leah':
                        newActor = 'Leah Parker'
                    elif newActor == 'Lolita Taylor':
                        newActor = 'Lola Taylor'
                    elif newActor == 'Melanie':
                        newActor = 'Melanie Jagger'
                    elif newActor == 'Meriesa':
                        newActor = 'Meriesa Arroyo'
                    elif newActor == 'Michele Avanti':
                        newActor = 'Michelle Avanti'
                    elif newActor == 'Molly Matthews':
                        newActor = 'Emily Marilyn'
                    elif newActor == 'Naidyne':
                        newActor = 'Nadine Sage'
                    elif newActor == 'Phoenix':
                        newActor = 'Phoenix Ray'
                    elif newActor == 'Phyllisha':
                        newActor = 'Phyllisha Anne'
                    elif newActor == 'Porsha':
                        newActor = 'Porsha Blaze'
                    elif newActor == 'Ramona':
                        newActor = 'Ramona Luv'
                    elif newActor == 'Sabrine':
                        newActor = 'Sabrine Maui'
                    elif newActor == 'Sandy':
                        newActor = 'Anna Ashton'
                    elif newActor == 'Sarah Jaymes':
                        newActor = 'Sara Jaymes'
                    elif newActor == 'Sascha Sin':
                        newActor = 'Sasha Sin'
                    elif newActor == 'Tegan Summer':
                        newActor = 'Teagan Summers'
                    elif newActor == 'Wanda':
                        newActor = 'Wanda Curtis'
                elif metadata.studio == 'ManyVids':
                    if newActor == 'Imheatherharmon':
                        newActor = 'Heather Harmon'
                    elif newActor == 'Shaiden':
                        newActor = 'Shaiden Rogue'
                    elif newActor == 'Spencer_Bradley':
                        newActor = 'Spencer Bradley'
                elif metadata.studio == 'Mylf':
                    if newActor == 'Scarlett':
                        newActor = 'Scarlet Domingo'
                elif metadata.studio == 'Nubiles':
                    if newActor == 'Abbey':
                        newActor = 'Amia Miley'
                    elif newActor == 'Addie':
                        newActor = 'Addie Moore'
                    elif newActor == 'Addison':
                        newActor = 'Addison Rose'
                    elif newActor == 'Adella':
                        newActor = 'Adel Bye'
                    elif newActor == 'Adelle':
                        newActor = 'Keira Albina'
                    elif newActor == 'Adri':
                        newActor = 'Sandra Bina'
                    elif newActor == 'Adrianne':
                        newActor = 'Adrianna Gold'
                    elif newActor == 'Agnessa':
                        newActor = 'Nessa Shine'
                    elif newActor == 'Alana':
                        newActor = 'Jayme Langford'
                    elif newActor == 'Alanaleigh':
                        newActor = 'Alana Leigh'
                    elif newActor == 'Alana G':
                        newActor = 'Alana Jade'
                    elif newActor == 'Alena':
                        newActor = 'Lucie Theodorova'
                    elif newActor == 'Aletta':
                        newActor = 'Aletta Ocean'
                    elif newActor == 'Alexa':
                        newActor = 'Aleska Diamond'
                    elif newActor == 'Alexcia':
                        newActor = 'Black Panther'
                    elif newActor == 'Alexiasky':
                        newActor = 'Alexia Sky'
                    elif newActor == 'Alexis':
                        newActor = 'Alexis Love'
                    elif newActor == 'Aliana':
                        newActor = 'Alice Miller'
                    elif newActor == 'Alicia':
                        newActor = 'Alicia Angel'
                    elif newActor == 'Alliehaze':
                        newActor = 'Allie Haze'
                    elif newActor == 'Allyann':
                        newActor = 'Ally Ann'
                    elif newActor == 'Allyssa':
                        newActor = 'Allyssa Hall'
                    elif newActor == 'Alyssia':
                        newActor = 'Nikita Black'
                    elif newActor == 'Amai':
                        newActor = 'Amai Liu'
                    elif newActor == 'Amalie':
                        newActor = 'Anita Pearl'
                    elif newActor == 'Amber':
                        newActor = 'Roxy Carter'
                    elif newActor == 'Ami':
                        newActor = 'Ami Emerson'
                    elif newActor == 'Amy':
                        newActor = 'Amy Reid'
                    elif newActor == 'Amybrooke':
                        newActor = 'Amy Brooke'
                    elif newActor == 'Amysativa':
                        newActor = 'Amy Sativa'
                    elif newActor == 'Andie':
                        newActor = 'Andie Valentino'
                    elif newActor == 'Andrea':
                        newActor = 'Jenny Sanders'
                    elif newActor == 'Angela':
                        newActor = 'Angie Emerald'
                    elif newActor == 'Angelica':
                        newActor = 'Black Angelika'
                    elif newActor == 'Angelina':
                        newActor = 'Nadia Taylor'
                    elif newActor == 'Angelinaash':
                        newActor = 'Angelina Ashe'
                    elif newActor == 'Angellina':
                        newActor = 'Angelina Brooke'
                    elif newActor == 'Angie':
                        newActor = 'Yulia Bright'
                    elif newActor == 'Aniya':
                        newActor = 'Stasia'
                    elif newActor == 'Annabelle':
                        newActor = 'Annabelle Lee'
                    elif newActor == 'Annastevens':
                        newActor = 'Anna Stevens'
                    elif newActor == 'Anne':
                        newActor = 'Playful Ann'
                    elif newActor == 'Annette':
                        newActor = 'Annette Allen'
                    elif newActor == 'Annika':
                        newActor = 'Annika Eve'
                    elif newActor == 'Anoli':
                        newActor = 'Anoli Angel'
                    elif newActor == 'April':
                        newActor = 'April Aubrey'
                    elif newActor == 'Apriloneil':
                        newActor = 'April O\'Neil'
                    elif newActor == 'Ariadna':
                        newActor = 'Ariadna Moon'
                    elif newActor == 'Ariel':
                        newActor = 'Ariel Rebel'
                    elif newActor == 'Ashlee':
                        newActor = 'Ashlee Allure'
                    elif newActor == 'Ashleyjane':
                        newActor = 'Ashley Jane'
                    elif newActor == 'Ashlynrae':
                        newActor = 'Ashlyn Rae'
                    elif newActor == 'Asuna':
                        newActor = 'Asuna Fox'
                    elif newActor == 'Athina':
                        newActor = 'Tyra Moon'
                    elif newActor == 'Aundrea':
                        newActor = 'Andrea Anderson'
                    elif newActor == 'Austin':
                        newActor = 'Austin Reines'
                    elif newActor == 'Barbra':
                        newActor = 'Mellisa Medisson'
                    elif newActor == 'Beata':
                        newActor = 'Beata Undine'
                    elif newActor == 'Bella B':
                        newActor = 'Bella Blue'
                    elif newActor == 'Bernie':
                        newActor = 'Bernie Svintis'
                    elif newActor == 'Billie':
                        newActor = 'Billy Raise'
                    elif newActor == 'Bliss':
                        newActor = 'Bliss Lei'
                    elif newActor == 'Boroka':
                        newActor = 'Boroka Balls'
                    elif newActor == 'Brea':
                        newActor = 'Bree Olson'
                    elif newActor == 'Bridget':
                        newActor = 'Sugar Baby'
                    elif newActor == 'Britne':
                        newActor = 'Chloe Morgan'
                    elif newActor == 'Britney':
                        newActor = 'Liz Honey'
                    elif newActor == 'Brynn':
                        newActor = 'Brynn Tyler'
                    elif newActor == 'Bulgari':
                        newActor = 'Ashley Bulgari'
                    elif newActor == 'Caise':
                        newActor = 'Jada Gold'
                    elif newActor == 'Calliedee':
                        newActor = 'Callie Dee'
                    elif newActor == 'Capri':
                        newActor = 'Capri Anderson'
                    elif newActor == 'Carli':
                        newActor = 'Carli Banks'
                    elif newActor == 'Carman':
                        newActor = 'Carmen Kinsley'
                    elif newActor == 'Carmen':
                        newActor = 'Petra E'
                    elif newActor == 'Carmin':
                        newActor = 'Carmen McCarthy'
                    elif newActor == 'Carrie':
                        newActor = 'Sandra Kalermen'
                    elif newActor == 'Cassandra':
                        newActor = 'Cassandra Calogera'
                    elif newActor == 'Cate':
                        newActor = 'Cate Harrington'
                    elif newActor == 'Celeste':
                        newActor = 'Celeste Star'
                    elif newActor == 'Celina':
                        newActor = 'Celina Cross'
                    elif newActor == 'Charlie':
                        newActor = 'Charlie Laine'
                    elif newActor == 'Charlielynn':
                        newActor = 'Charlie Lynn'
                    elif newActor == 'Charlotte':
                        newActor = 'Charlotte Stokely'
                    elif newActor == 'Chastity':
                        newActor = 'Chastity Lynn'
                    elif newActor == 'Chloejames':
                        newActor = 'Chloe James'
                    elif newActor == 'Chloe Cherry':
                        newActor = 'Chloe Couture'
                    elif newActor == 'Chris':
                        newActor = 'Christine Alexis'
                    elif newActor == 'Christina':
                        newActor = 'Krisztina Banks'
                    elif newActor == 'Christine':
                        newActor = 'Christie Lee'
                    elif newActor == 'Cindy':
                        newActor = 'Cindy Hope'
                    elif newActor == 'Clover':
                        newActor = 'Katya Clover'
                    elif newActor == 'Conny':
                        newActor = 'Connie Carter'
                    elif newActor == 'Courtney':
                        newActor = 'Courtney Cummz'
                    elif newActor == 'Crissy':
                        newActor = 'Crissy Moon'
                    elif newActor == 'Crissysnow':
                        newActor = 'Crissy Snow'
                    elif newActor == 'Cristal':
                        newActor = 'Cristal Matthews'
                    elif newActor == 'Dana':
                        newActor = 'Monica Sweet'
                    elif newActor == 'Dani':
                        newActor = 'Dani Jensen'
                    elif newActor == 'Danielle':
                        newActor = 'Danielle Maye'
                    elif newActor == 'Daphne':
                        newActor = 'Daphne Angel'
                    elif newActor == 'Deanna':
                        newActor = 'Deena Daniels'
                    elif newActor == 'Delphine':
                        newActor = 'Izzy Delphine'
                    elif newActor == 'Dessa':
                        newActor = 'Jessica Valentino'
                    elif newActor == 'Devi':
                        newActor = 'Devi Emmerson'
                    elif newActor == 'Diamond':
                        newActor = 'Paris Diamond'
                    elif newActor == 'Dimitra':
                        newActor = 'Lia Chalizo'
                    elif newActor == 'Dina':
                        newActor = 'Dana Sinnz'
                    elif newActor == 'Diore':
                        newActor = 'Dolly Diore'
                    elif newActor == 'Dominica':
                        newActor = 'Dominic Anna'
                    elif newActor == 'Edenadams':
                        newActor = 'Eden Adams'
                    elif newActor == 'Edyphia':
                        newActor = 'Pearl Ami'
                    elif newActor == 'Eileen':
                        newActor = 'Eileen Sue'
                    elif newActor == 'Elena':
                        newActor = 'Elena Rivera'
                    elif newActor == 'Elizabethanne':
                        newActor = 'Elizabeth Anne'
                    elif newActor == 'Ella':
                        newActor = 'Eufrat Mai'
                    elif newActor == 'Ellington':
                        newActor = 'Evah Ellington'
                    elif newActor == 'Elza A':
                        newActor = 'Casey Nohrman'
                    elif newActor == 'Emy':
                        newActor = 'Emy Reyes'
                    elif newActor == 'Eriko':
                        newActor = 'Nikko Jordan'
                    elif newActor == 'Esegna':
                        newActor = 'Gabriella Lati'
                    elif newActor == 'Eva':
                        newActor = 'Eva Gold'
                    elif newActor == 'Eve':
                        newActor = 'Eve Angel'
                    elif newActor == 'Evelin':
                        newActor = 'Eveline Dellai'
                    elif newActor == 'Evelyn':
                        newActor = 'Evelyn Baum'
                    elif newActor == 'Evonna':
                        newActor = 'Regina Prensley'
                    elif newActor == 'Faina':
                        newActor = 'Faina Bona'
                    elif newActor == 'Faith':
                        newActor = 'Faith Leon'
                    elif newActor == 'Fawn':
                        newActor = 'Kimberly Cox'
                    elif newActor == 'Faye':
                        newActor = 'Faye Reagan'
                    elif newActor == 'Fayex':
                        newActor = 'Faye X Taylor'
                    elif newActor == 'Federica':
                        newActor = 'Federica Hill'
                    elif newActor == 'Felicity':
                        newActor = 'Jana Jordan'
                    elif newActor == 'Ferrera':
                        newActor = 'Ferrera Gomez'
                    elif newActor == 'Franziska':
                        newActor = 'Franziska Facella'
                    elif newActor == 'Frida':
                        newActor = 'Frida Stark'
                    elif newActor == 'Gabriella':
                        newActor = 'Ariel Piper Fawn'
                    elif newActor == 'Gemini':
                        newActor = 'Carmen Gemini'
                    elif newActor == 'Georgia':
                        newActor = 'Georgia Jones'
                    elif newActor == 'Ginger':
                        newActor = 'Ginger Lee'
                    elif newActor == 'Giselle':
                        newActor = 'Goldie Baby'
                    elif newActor == 'Grace':
                        newActor = 'Lindsay Kay'
                    elif newActor == 'Haleysweet':
                        newActor = 'Haley Sweet'
                    elif newActor == 'Hallee':
                        newActor = 'Traci Lynn'
                    elif newActor == 'Hanna':
                        newActor = 'Hannah West'
                    elif newActor == 'Heather':
                        newActor = 'Samantha Sin'
                    elif newActor == 'Heidi C':
                        newActor = 'Heidi Harper'
                    elif newActor == 'Hollyfox':
                        newActor = 'Holly Fox'
                    elif newActor == 'Ianisha':
                        newActor = 'Summer Breeze'
                    elif newActor == 'Inus':
                        newActor = 'Anna Nova'
                    elif newActor == 'Jaelyn':
                        newActor = 'Jaelyn Fox'
                    elif newActor == 'Jamie':
                        newActor = 'Jewel Affair'
                    elif newActor == 'Janelle':
                        newActor = 'Karlie Montana'
                    elif newActor == 'Jasmine':
                        newActor = 'Jasmine Rouge'
                    elif newActor == 'Jassie':
                        newActor = 'Jassie James'
                    elif newActor == 'Jenet':
                        newActor = 'Leyla Black'
                    elif newActor == 'Jenna':
                        newActor = 'Jenna Presley'
                    elif newActor == 'Jenni':
                        newActor = 'Jenni Czech'
                    elif newActor == 'Jenniah':
                        newActor = 'Jenny Appach'
                    elif newActor == 'Jenny':
                        newActor = 'Jenni Lee'
                    elif newActor == 'Jensen':
                        newActor = 'Ashley Jensen'
                    elif newActor == 'Jeny':
                        newActor = 'Jeny Baby'
                    elif newActor == 'Jesica':
                        newActor = 'Leony April'
                    elif newActor == 'Jess':
                        newActor = 'Danielle Trixie'
                    elif newActor == 'Jessie':
                        newActor = 'Jessie Cox'
                    elif newActor == 'Jordanbliss':
                        newActor = 'Jordan Bliss'
                    elif newActor == 'Jorden':
                        newActor = 'Neyla Small'
                    elif newActor == 'Judith':
                        newActor = 'Judith Fox'
                    elif newActor == 'Jujana':
                        newActor = 'Zuzana Z'
                    elif newActor == 'Julie':
                        newActor = 'Juliana Grandi'
                    elif newActor == 'Juliya':
                        newActor = 'Crystal Maiden'
                    elif newActor == 'Kacey':
                        newActor = 'Kacey Jordan'
                    elif newActor == 'Kaela':
                        newActor = 'Lena Nicole'
                    elif newActor == 'Kalilane':
                        newActor = 'Kali Lane'
                    elif newActor == 'Kalisy':
                        newActor = 'Mary Kalisy'
                    elif newActor == 'Kandi':
                        newActor = 'Kandi Milan'
                    elif newActor == 'Karanovak':
                        newActor = 'Kara Novak'
                    elif newActor == 'Kari S':
                        newActor = 'Kari Sweet'
                    elif newActor == 'Karin':
                        newActor = 'Carin Kay'
                    elif newActor == 'Karina':
                        newActor = 'Karina Laboom'
                    elif newActor == 'Kate':
                        newActor = 'Kathleen Kruz'
                    elif newActor == 'Katie':
                        newActor = 'Heather Starlet'
                    elif newActor == 'Katiejordin':
                        newActor = 'Katie Jordin'
                    elif newActor == 'Katiek':
                        newActor = 'Katie Kay'
                    elif newActor == 'Katy P':
                        newActor = 'Cira Nerri'
                    elif newActor == 'Kaula':
                        newActor = 'Kayla Louise'
                    elif newActor == 'Kaylee':
                        newActor = 'Kaylee Heart'
                    elif newActor == 'Kellie':
                        newActor = 'Paige Starr'
                    elif newActor == 'Kennedy':
                        newActor = 'Kennedy Kressler'
                    elif newActor == 'Kenzie':
                        newActor = 'Mackenzee Pierce'
                    elif newActor == 'Kimber':
                        newActor = 'Kimber Lace'
                    elif newActor == 'Kimberly':
                        newActor = 'Kimberly Allure'
                    elif newActor == 'Kimmie':
                        newActor = 'Kimmie Cream'
                    elif newActor == 'Kira':
                        newActor = 'Dido Angel'
                    elif newActor == 'Kiralanai':
                        newActor = 'Kira Lanai'
                    elif newActor == 'Kirra':
                        newActor = 'Kira Zen'
                    elif newActor == 'Klaudia':
                        newActor = 'Cindy Hope'
                    elif newActor == 'Kody':
                        newActor = 'Kody Kay'
                    elif newActor == 'Koks':
                        newActor = 'Angie Koks'
                    elif newActor == 'Krissie':
                        newActor = 'Liona Levi'
                    elif newActor == 'Kristina':
                        newActor = 'Kristina Wood'
                    elif newActor == 'Kristinarose':
                        newActor = 'Kristina Rose'
                    elif newActor == 'Krystyna':
                        newActor = 'Kristina Manson'
                    elif newActor == 'Kyra':
                        newActor = 'Kyra Steele'
                    elif newActor == 'Lady D':
                        newActor = 'Lady Dee'
                    elif newActor == 'Lanaviolet':
                        newActor = 'Lana Violet'
                    elif newActor == 'Lanewood':
                        newActor = 'Louisa Lanewood'
                    elif newActor == 'Lauracrystal':
                        newActor = 'Laura Crystal'
                    elif newActor == 'Lauren':
                        newActor = 'Afrodite Night'
                    elif newActor == 'Layna':
                        newActor = 'Brigitte Hunter'
                    elif newActor == 'Lea':
                        newActor = 'Lea Tyron'
                    elif newActor == 'Leah':
                        newActor = 'Leah Luv'
                    elif newActor == 'Leigh':
                        newActor = 'Leighlani Red'
                    elif newActor == 'Leila':
                        newActor = 'Leila Smith'
                    elif newActor == 'Lexidiamond':
                        newActor = 'Lexi Diamond'
                    elif newActor == 'Lexie':
                        newActor = 'Lexi Belle'
                    elif newActor == 'Lilian':
                        newActor = 'Lilian Lee'
                    elif newActor == 'Liliane':
                        newActor = 'Liliane Tiger'
                    elif newActor == 'Lilit':
                        newActor = 'Lola Chic'
                    elif newActor == 'Lily':
                        newActor = 'Lily Cute'
                    elif newActor == 'Lindie':
                        newActor = 'Kelly Summer'
                    elif newActor == 'Lindsay':
                        newActor = 'Jenni Carmichael'
                    elif newActor == 'Linna':
                        newActor = 'Evelyn Cage'
                    elif newActor == 'Lola':
                        newActor = 'Mia Me'
                    elif newActor == 'Lolashut':
                        newActor = 'Little Caprice'
                    elif newActor == 'Lolly':
                        newActor = 'Lolly Gartner'
                    elif newActor == 'Lolly J':
                        newActor = 'Felicia Rain'
                    elif newActor == 'Lora':
                        newActor = 'Lora Craft'
                    elif newActor == 'Loreen':
                        newActor = 'Loreen Roxx'
                    elif newActor == 'Lorena':
                        newActor = 'Lorena Garcia'
                    elif newActor == 'Luciana':
                        newActor = 'Timea Bella'
                    elif newActor == 'Lucie':
                        newActor = 'Samantha Wow'
                    elif newActor == 'Lucy':
                        newActor = 'Lucy Ive'
                    elif newActor == 'Lucylux':
                        newActor = 'Lucy Lux'
                    elif newActor == 'Lussy M':
                        newActor = 'Deja Move'
                    elif newActor == 'Lynn':
                        newActor = 'Lynn Pleasant'
                    elif newActor == 'Lynnlove':
                        newActor = 'Lynn Love'
                    elif newActor == 'Maddy':
                        newActor = 'Madison Parker'
                    elif newActor == 'Maggies':
                        newActor = 'Maggie Gold'
                    elif newActor == 'Mai':
                        newActor = 'Mai Ly'
                    elif newActor == 'Marfa':
                        newActor = 'Joanna Pret'
                    elif newActor == 'Marina':
                        newActor = 'Marina Mae'
                    elif newActor == 'Marissa':
                        newActor = 'Marissa Mendoza'
                    elif newActor == 'Marlie':
                        newActor = 'Marlie Moore'
                    elif newActor == 'Marsa':
                        newActor = 'Jessi Gold'
                    elif newActor == 'Marsha':
                        newActor = 'Monica Sweat'
                    elif newActor == 'Marta':
                        newActor = 'Melena Maria Rya'
                    elif newActor == 'Martha':
                        newActor = 'Tarra White'
                    elif newActor == 'Maya':
                        newActor = 'Maya Hills'
                    elif newActor == 'Mckenzee':
                        newActor = 'Mckenzee Miles'
                    elif newActor == 'Meggan':
                        newActor = 'Meggan Mallone'
                    elif newActor == 'Melanie':
                        newActor = 'Melanie Taylor'
                    elif newActor == 'Melissa':
                        newActor = 'Melissa Matthews'
                    elif newActor == 'Melody':
                        newActor = 'Melody Kush'
                    elif newActor == 'Mia':
                        newActor = 'Mia Moon'
                    elif newActor == 'Miahilton':
                        newActor = 'Mia Hilton'
                    elif newActor == 'Micah':
                        newActor = 'Micah Moore'
                    elif newActor == 'Michele':
                        newActor = 'Michelle Brown'
                    elif newActor == 'Michelle':
                        newActor = 'Michelle Maylene'
                    elif newActor == 'Michellemoist':
                        newActor = 'Michelle Moist'
                    elif newActor == 'Michellemyers':
                        newActor = 'Michelle Myers'
                    elif newActor == 'Miesha':
                        newActor = 'Jessika Lux'
                    elif newActor == 'Mikki':
                        newActor = 'Elina Mikki'
                    elif newActor == 'Mileyann':
                        newActor = 'Miley Ann'
                    elif newActor == 'Mili':
                        newActor = 'Mili Jay'
                    elif newActor == 'Minnie':
                        newActor = 'Milla Yul'
                    elif newActor == 'Missy':
                        newActor = 'Missy Nicole'
                    elif newActor == 'Mollymadison':
                        newActor = 'Molly Madison'
                    elif newActor == 'Monika':
                        newActor = 'Monika Vesela'
                    elif newActor == 'Monique':
                        newActor = 'Monika Cajth'
                    elif newActor == 'Monna':
                        newActor = 'Monna Dark'
                    elif newActor == 'Morgan':
                        newActor = 'Nataly Gold'
                    elif newActor == 'Ms Faris':
                        newActor = 'Athena Faris'
                    elif newActor == 'Nadea':
                        newActor = 'Bella Rossi'
                    elif newActor == 'Nancy':
                        newActor = 'Nancy Bell'
                    elif newActor == 'Nancy A':
                        newActor = 'Nancy Ace'
                    elif newActor == 'Natali':
                        newActor = 'Natali Blond'
                    elif newActor == 'Nataliex':
                        newActor = 'Natalia Forrest'
                    elif newActor == 'Natalya':
                        newActor = 'Little Rita'
                    elif newActor == 'Natosha':
                        newActor = 'Monica Beluchi'
                    elif newActor == 'Nelly':
                        newActor = 'Nelli Sulivan'
                    elif newActor == 'Nici':
                        newActor = 'Nici Dee'
                    elif newActor == 'Nicol':
                        newActor = 'Ashley Stillar'
                    elif newActor == 'Nicoleray':
                        newActor = 'Nicole Ray'
                    elif newActor == 'Nikala':
                        newActor = 'Bella Cole'
                    elif newActor == 'Niki':
                        newActor = 'Nika Noire'
                    elif newActor == 'Nikka':
                        newActor = 'Scarlett Nika'
                    elif newActor == 'Nikkivee':
                        newActor = 'Nikki Vee'
                    elif newActor == 'Nikysweet':
                        newActor = 'Niky Sweet'
                    elif newActor == 'Ninoska':
                        newActor = 'Connie Rose'
                    elif newActor == 'Nitca':
                        newActor = 'Cindy Dee'
                    elif newActor == 'Noleta':
                        newActor = 'Tracy Gold'
                    elif newActor == 'Nyusha':
                        newActor = 'Olivia Brown'
                    elif newActor == 'Olivia':
                        newActor = 'Olivia La Roche'
                    elif newActor == 'Oprah':
                        newActor = 'Nathaly Cherie'
                    elif newActor == 'Oxana':
                        newActor = 'Oxana Chic'
                    elif newActor == 'Palomino':
                        newActor = 'Athena Palomino'
                    elif newActor == 'Paris':
                        newActor = 'Paris Parker'
                    elif newActor == 'Patritcy':
                        newActor = 'Merry Pie'
                    elif newActor == 'Paula':
                        newActor = 'Pavlina St.'
                    elif newActor == 'Paulina':
                        newActor = 'Paulina James'
                    elif newActor == 'Pavla':
                        newActor = 'Teena Dolly'
                    elif newActor == 'Pearl':
                        newActor = 'Juicy Pearl'
                    elif newActor == 'Penny':
                        newActor = 'Abby Cross'
                    elif newActor == 'Persia':
                        newActor = 'Persia DeCarlo'
                    elif newActor == 'Pinkule':
                        newActor = 'Billie Star'
                    elif newActor == 'Polly':
                        newActor = 'Jasmine Davis'
                    elif newActor == 'Presley':
                        newActor = 'Presley Maddox'
                    elif newActor == 'Quenna':
                        newActor = 'Maria Devine'
                    elif newActor == 'Rachel':
                        newActor = 'Yasmine Gold'
                    elif newActor == 'Rebeccablue':
                        newActor = 'Rebecca Blue'
                    elif newActor == 'Reena':
                        newActor = 'Reena Sky'
                    elif newActor == 'Renee':
                        newActor = 'Renee Perez'
                    elif newActor == 'Roberta':
                        newActor = 'Lisa Musa'
                    elif newActor == 'Rosea':
                        newActor = 'Rose Delight'
                    elif newActor == 'Roxy':
                        newActor = 'Roxy Panther'
                    elif newActor == 'Ruby':
                        newActor = 'Ruby Flame'
                    elif newActor == 'Sage':
                        newActor = 'Stephanie Sage'
                    elif newActor == 'Sally':
                        newActor = 'Demi Scott'
                    elif newActor == 'Sammie':
                        newActor = 'Sammie Rhodes'
                    elif newActor == 'Sandra':
                        newActor = 'Sandra Shine'
                    elif newActor == 'Sandy':
                        newActor = 'Sandy Joy'
                    elif newActor == 'Sandysummers':
                        newActor = 'Sandy Summers'
                    elif newActor == 'Sarah':
                        newActor = 'Sarah Blake'
                    elif newActor == 'Sarahjo':
                        newActor = 'Ava Skye'
                    elif newActor == 'Sarai':
                        newActor = 'Sarai Keef'
                    elif newActor == 'Sasha':
                        newActor = 'Sasha Cane'
                    elif newActor == 'Sassy':
                        newActor = 'Monika Thu'
                    elif newActor == 'Scarlettfay':
                        newActor = 'Scarlett Fay'
                    elif newActor == 'Sera':
                        newActor = 'Sera Passion'
                    elif newActor == 'Serendipity':
                        newActor = 'Jessica Foxx'
                    elif newActor == 'Sharon':
                        newActor = 'Kristina Rud'
                    elif newActor == 'Sheridan':
                        newActor = 'Jana Sheridan'
                    elif newActor == 'Shyla':
                        newActor = 'Shyla Jennings'
                    elif newActor == 'Sierra':
                        newActor = 'Nina Stevens'
                    elif newActor == 'Sima':
                        newActor = 'Shrima Malati'
                    elif newActor == 'Simone':
                        newActor = 'Nikki Chase'
                    elif newActor == 'Smokie':
                        newActor = 'Smokie Flame'
                    elif newActor == 'Solstice':
                        newActor = 'Summer Solstice'
                    elif newActor == 'Stacy':
                        newActor = 'Mandy Dee'
                    elif newActor == 'Summersilver':
                        newActor = 'Summer Silver'
                    elif newActor == 'Suze':
                        newActor = 'Suzy Black'
                    elif newActor == 'Suzie':
                        newActor = 'Suzie Diamond'
                    elif newActor == 'Sveta':
                        newActor = 'Lita Phoenix'
                    elif newActor == 'Sylvia':
                        newActor = 'Silvie Deluxe'
                    elif newActor == 'Talya':
                        newActor = 'Lindsey Olsen'
                    elif newActor == 'Tannermays':
                        newActor = 'Tanner Mayes'
                    elif newActor == 'Taylor':
                        newActor = 'Roxanna Milana'
                    elif newActor == 'Tea':
                        newActor = 'Deny Moor'
                    elif newActor == 'Tegan':
                        newActor = 'Tegan Jane'
                    elif newActor == 'Teresina':
                        newActor = 'Teri Sweet'
                    elif newActor == 'Tereza':
                        newActor = 'Tereza Ilova'
                    elif newActor == 'Tess':
                        newActor = 'Tess Lyndon'
                    elif newActor == 'Tessa':
                        newActor = 'Sonya Durganova'
                    elif newActor == 'Tiff':
                        newActor = 'Tiffany Sweet'
                    elif newActor == 'Toni':
                        newActor = 'Kyra Black'
                    elif newActor == 'Tonya':
                        newActor = 'Casey Donell'
                    elif newActor == 'Traci':
                        newActor = 'Kirsten Andrews'
                    elif newActor == 'Tyra':
                        newActor = 'Naomi Cruise'
                    elif newActor == 'Valerie':
                        newActor = 'Valerie Herrera'
                    elif newActor == 'Vanessa':
                        newActor = 'Vanessa Monroe'
                    elif newActor == 'Vania':
                        newActor = 'Ivana Sugar'
                    elif newActor == 'Vendula':
                        newActor = 'Tiffany Diamond'
                    elif newActor == 'Veronica':
                        newActor = 'Veronica Jones'
                    elif newActor == 'Veronicahill':
                        newActor = 'Veronica Hill'
                    elif newActor == 'Veronique':
                        newActor = 'Veronique Vega'
                    elif newActor == 'Victoria':
                        newActor = 'Talia Shepard'
                    elif newActor == 'Victoria P':
                        newActor = 'Victoria Puppy'
                    elif newActor == 'Victoriasweet':
                        newActor = 'Victoria Sweet'
                    elif newActor == 'Viera':
                        newActor = 'Vika Lita'
                    elif newActor == 'Violet':
                        newActor = 'Goldie Glock'
                    elif newActor == 'Violetta':
                        newActor = 'Lily Lake'
                    elif newActor == 'Violette':
                        newActor = 'Violette Pink'
                    elif newActor == 'Viva':
                        newActor = 'Sabina Blue'
                    elif newActor == 'Whitney':
                        newActor = 'Whitney Conroy'
                    elif newActor == 'Xenia':
                        newActor = 'Zena Little'
                    elif newActor == 'Yanka':
                        newActor = 'Sasha Rose'
                    elif newActor == 'Yvonne':
                        newActor = 'Cindy Shine'
                    elif newActor == 'Zara':
                        newActor = 'Jacqueline Sweet'
                    elif newActor == 'Zazie':
                        newActor = 'Zazie Sky'
                    elif newActor == 'Zeina':
                        newActor = 'Zeina Heart'
                    elif newActor == 'Zenia':
                        newActor = 'Nadine Greenlaw'
                elif metadata.studio == 'Porn Pros':
                    if newActor == 'Bailey Brookes':
                        newActor = 'Bailey Brooke'
                elif metadata.studio == 'Porndoe Premium':
                    if newActor == 'Scarlett D':
                        newActor = 'Scarlet Domingo'
                elif metadata.studio == 'TeamSkeet':
                    if newActor == 'Ada S':
                        newActor = 'Ada Sanchez'
                    elif newActor == 'Ariel R':
                        newActor = 'Ariel Rose'
                    elif newActor == 'Artemida':
                        newActor = 'Valentina Cross'
                    elif newActor == 'Arika':
                        newActor = 'Arika Foxx'
                    elif newActor == 'Ariana':
                        newActor = 'Emma Brown'
                    elif newActor == 'Ariadna':
                        newActor = 'Ariadna Moon'
                    elif newActor == 'Argentina':
                        newActor = 'Lisa Smiles'
                    elif newActor == 'Anfisa':
                        newActor = 'Nicoline'
                    elif newActor == 'Aliya':
                        newActor = 'Rima'
                    elif newActor == 'Ava':
                        newActor = 'Ava Dalush'
                    elif newActor == 'Avery':
                        newActor = 'Diana Dali'
                    elif newActor == 'Avina':
                        newActor = 'Sunny Rise'
                    elif newActor == 'Bailey':
                        newActor = 'Lena Love'
                    elif newActor == 'Bella':
                        newActor = 'Bella Rossi'
                    elif newActor == 'Betty':
                        newActor = 'Camila'
                    elif newActor == 'Jane':
                        newActor = 'Camila'
                    elif newActor == 'Briana':
                        newActor = 'Milana Blanc'
                    elif newActor == 'Brianna':
                        newActor = 'Milana Blanc'
                    elif newActor == 'Callie':
                        newActor = 'Callie Nicole'
                    elif newActor == 'Carre':
                        newActor = 'Candy C'
                    elif newActor == 'Casi J':
                        newActor = 'Casi James'
                    elif newActor == 'Catania':
                        newActor = 'Jessi Gold'
                    elif newActor == 'Chloe Cherry':
                        newActor = 'Chloe Couture'
                    elif newActor == 'Colette':
                        newActor = 'Inga E'
                    elif newActor == 'Darla':
                        newActor = 'Alektra Sky'
                    elif newActor == 'Dinara':
                        newActor = 'Arian Joy'
                    elif newActor == 'Dunya':
                        newActor = 'Alice Marshall'
                    elif newActor == 'Ema':
                        newActor = 'Chloe Blue'
                    elif newActor == 'Erica':
                        newActor = 'Kristall Rush'
                    elif newActor == 'Sasha':
                        newActor = 'Kristall Rush'
                    elif newActor == 'Eva':
                        newActor = 'Mia Reese'
                    elif newActor == 'Fantina':
                        newActor = 'Mariya C'
                    elif newActor == 'Olga':
                        newActor = 'Mariya C'
                    elif newActor == 'Gabi':
                        newActor = 'Izi'
                    elif newActor == 'Gerta':
                        newActor = 'Erika Bellucci'
                    elif newActor == 'Hannah':
                        newActor = 'Milana Fox'
                    elif newActor == 'Jade':
                        newActor = 'Netta'
                    elif newActor == 'Jana':
                        newActor = 'Janna'
                    elif newActor == 'Janette':
                        newActor = 'Lisa C'
                    elif newActor == 'Joanna':
                        newActor = 'Joanna Pret'
                    elif newActor == 'Jordan':
                        newActor = 'Rebeca Taylor'
                    elif newActor == 'Kail':
                        newActor = 'Kortny'
                    elif newActor == 'Kajira':
                        newActor = 'Kajira Bound'
                    elif newActor == 'Kameya':
                        newActor = 'Sandra Luberc'
                    elif newActor == 'Katherine':
                        newActor = 'Selena Stuart'
                    elif newActor == 'Katie C':
                        newActor = 'Katie Cummings'
                    elif newActor == 'Katie K':
                        newActor = 'Katie Kay'
                    elif newActor == 'Kendall':
                        newActor = 'Alison Faye'
                    elif newActor == 'Kimberly':
                        newActor = 'Pola Sunshine'
                    elif newActor == 'Krista':
                        newActor = 'Krista Evans'
                    elif newActor == 'Lily L':
                        newActor = 'Lily Labeau'
                    elif newActor == 'Lada':
                        newActor = 'Jay Dee'
                    elif newActor == 'Luna':
                        newActor = 'Rita Rush'
                    elif newActor == 'Lusil':
                        newActor = 'Ananta Shakti'
                    elif newActor == 'Mackenzie':
                        newActor = 'Alice Smack'
                    elif newActor == 'Madelyn':
                        newActor = 'Anna Taylor'
                    elif newActor == 'Madison':
                        newActor = 'Karina Grand'
                    elif newActor == 'Magda':
                        newActor = 'Taissia Shanti'
                    elif newActor == 'Mai':
                        newActor = 'Mai Ly'
                    elif newActor == 'Mara':
                        newActor = 'Marly Romero'
                    elif newActor == 'Mariah':
                        newActor = 'Aubree Jade'
                    elif newActor == 'Mina':
                        newActor = 'Mila Beth'
                    elif newActor == 'Nadya':
                        newActor = 'Nadia Bella'
                    elif newActor == 'Seren':
                        newActor = 'Nadia Bella'
                    elif newActor == 'Nika':
                        newActor = 'Sabrina Moor'
                    elif newActor == 'Nora R':
                        newActor = 'Sheri Vi'
                    elif newActor == 'Parvin':
                        newActor = 'Adelle Booty'
                    elif newActor == 'Peachy':
                        newActor = 'Margarita C'
                    elif newActor == 'Petra':
                        newActor = 'Dominica Phoenix'
                    elif newActor == 'Rahyndee':
                        newActor = 'Rahyndee James'
                    elif newActor == 'Rebecca':
                        newActor = 'Anita Sparkle'
                    elif newActor == 'Riley J':
                        newActor = 'Riley Jensen'
                    elif newActor == 'Rosanna':
                        newActor = 'Kate G.'
                    elif newActor == 'Sadine G':
                        newActor = 'Sadine Godiva'
                    elif newActor == 'Sarai':
                        newActor = 'Sarai Keef'
                    elif newActor == 'Serena':
                        newActor = 'Carol Miller'
                    elif newActor == 'Sheila':
                        newActor = 'Marina Visconti'
                    elif newActor == 'Sierra':
                        newActor = 'Sierra Sanders'
                    elif newActor == 'Skye':
                        newActor = 'Skye West'
                    elif newActor == 'Soleil':
                        newActor = 'Soliel Marks'
                    elif newActor == 'Sophia':
                        newActor = 'Grace C'
                    elif newActor == 'Stella':
                        newActor = 'Stella Banxxx'
                    elif newActor == 'Tori':
                        newActor = 'Lola Taylor'
                    elif newActor == 'Veiki':
                        newActor = 'Miranda Deen'
                    elif newActor == 'Viki':
                        newActor = 'Bonnie Shai'
                    elif newActor == 'Vilia':
                        newActor = 'Lilu Tattoo'
                    elif newActor == 'Viviana':
                        newActor = 'Autumn Viviana'
                    elif newActor == 'Yanie':
                        newActor = 'Milla Yul'
                    elif newActor == 'Yoga':
                        newActor = 'Arya Fae, Megan Sage, and Nina North'
                    elif newActor == 'Zarina':
                        newActor = 'Aruna Aghora'
                    elif newActor == 'Zoi':
                        newActor = 'Liona Levi'
                elif metadata.studio == 'Twistys':
                    if newActor == 'Blaire Ivory':
                        newActor = 'Lena Anderson'
                elif metadata.studio == 'X-Art':
                    if newActor == 'Abby':
                        newActor = 'Abigaile Johnson'
                    elif newActor == 'Addison':
                        newActor = 'Mia Manarote'
                    elif newActor == 'Addison C':
                        newActor = 'Davina Davis'
                    elif newActor == 'Adel':
                        newActor = 'Angel Piaff'
                    elif newActor == 'Adel M':
                        newActor = 'Adel Morel'
                    elif newActor == 'Adria':
                        newActor = 'Adria Rae'
                    elif newActor == 'Adriana':
                        newActor = 'Adriana Chechik'
                    elif newActor == 'Aidra':
                        newActor = 'Aidra Fox'
                    elif newActor == 'Aika':
                        newActor = 'Aika May'
                    elif newActor == 'Aj':
                        newActor = 'Alessandra Jane'
                    elif newActor == 'Alecia':
                        newActor = 'Alecia Fox'
                    elif newActor == 'Alena':
                        newActor = 'Kiara Lord'
                    elif newActor == 'Alexa':
                        newActor = 'Alexa Grace'
                    elif newActor == 'Alexes':
                        newActor = 'Alexis Adams'
                    elif newActor == 'Alexis':
                        newActor = 'Alexis Love'
                    elif newActor == 'Alina':
                        newActor = 'Alexa Tomas'
                    elif newActor == 'Alina H':
                        newActor = 'Henessy'
                    elif newActor == 'Aliyah':
                        newActor = 'Aaliyah Love'
                    elif newActor == 'Allie':
                        newActor = 'Allie Haze'
                    elif newActor == 'Alyssia':
                        newActor = 'Alyssia Kent'
                    elif newActor == 'Amelie':
                        newActor = 'Chloe Amour'
                    elif newActor == 'Ana':
                        newActor = 'Ana Foxxx'
                    elif newActor == 'Anais':
                        newActor = 'Mae Olsen'
                    elif newActor == 'Angel':
                        newActor = 'Rosemary Radeva'
                    elif newActor == 'Angelica':
                        newActor = 'Anjelica'
                    elif newActor == 'Angie':
                        newActor = 'Angelica Kitten'
                    elif newActor == 'Anikka':
                        newActor = 'Annika Albrite'
                    elif newActor == 'Anita':
                        newActor = 'Anita Bellini Berlusconi'
                    elif newActor == 'Anna':
                        newActor = 'Gwen'
                    elif newActor == 'Anna M':
                        newActor = 'Anastasia Morna'
                    elif newActor == 'Anneli':
                        newActor = 'Pinky June'
                    elif newActor == 'Annemarie':
                        newActor = 'Samantha Heat'
                    elif newActor == 'Anya':
                        newActor = 'Anya Olsen'
                    elif newActor == 'Aria':
                        newActor = 'Sunny A'
                    elif newActor == 'Arianna':
                        newActor = 'Ariana Marie'
                    elif newActor == 'Ariel':
                        newActor = 'Ariel Piper Fawn'
                    elif newActor == 'Ashley S':
                        newActor = 'Ashlyn Molloy'
                    elif newActor == 'Aubrey':
                        newActor = 'Aubrey Star'
                    elif newActor == 'Avril':
                        newActor = 'Avril Hall'
                    elif newActor == 'Baby':
                        newActor = 'Karina'
                    elif newActor == 'Bailey':
                        newActor = 'Bailey Ryder'
                    elif newActor == 'Bambi':
                        newActor = 'Olivia Grace'
                    elif newActor == 'Barbie':
                        newActor = 'Blanche Bradburry'
                    elif newActor == 'Poppy':
                        newActor = 'Victoria Puppy'
                    elif newActor == 'Bea':
                        newActor = 'Victoria Puppy'
                    elif newActor == 'Beatrice':
                        newActor = 'Beata Undine'
                    elif newActor == 'Becky':
                        newActor = 'Bridgit A'
                    elif newActor == 'Belle':
                        newActor = 'Belle Knox'
                    elif newActor == 'Breanne':
                        newActor = 'Brea Bennett'
                    elif newActor == 'Bree':
                        newActor = 'Bree Daniels'
                    elif newActor == 'Brooklyn':
                        newActor = 'Brooklyn Lee'
                    elif newActor == 'Brynn':
                        newActor = 'Brynn Tyler'
                    elif newActor == 'Bunny':
                        newActor = 'Chloe Foster'
                    elif newActor == 'Capri':
                        newActor = 'Capri Anderson'
                    elif newActor == 'Caprice':
                        newActor = 'Little Caprice'
                    elif newActor == 'Carla':
                        newActor = 'Carla Cox'
                    elif newActor == 'Carlie':
                        newActor = 'Kasey Chase'
                    elif newActor == 'Carmen':
                        newActor = 'Jessie Rogers'
                    elif newActor == 'Carrie':
                        newActor = 'Alexis Crystal'
                    elif newActor == 'Carrol':
                        newActor = 'Lexi Dona'
                    elif newActor == 'Casey':
                        newActor = 'Vanessa'
                    elif newActor == 'Cassidy':
                        newActor = 'Cassidey Rae'
                    elif newActor == 'Cassie':
                        newActor = 'Cassie Laine'
                    elif newActor == 'Catie':
                        newActor = 'Catie Parker'
                    elif newActor == 'Cecilia':
                        newActor = 'Sicilia'
                    elif newActor == 'Chantal':
                        newActor = 'Nelly A'
                    elif newActor == 'Charity':
                        newActor = 'Charity Crawford'
                    elif newActor == 'Charlie':
                        newActor = 'Charlie Red'
                    elif newActor == 'Charlotte':
                        newActor = 'Charlotte Stokely'
                    elif newActor == 'Chelsea':
                        newActor = 'Victoria Lynn'
                    elif newActor == 'Chloe':
                        newActor = 'Victoria Sweet'
                    elif newActor == 'Chloelynn':
                        newActor = 'Chloe Lynn'
                    elif newActor == 'Christine':
                        newActor = 'Christine Paradise'
                    elif newActor == 'Cindy':
                        newActor = 'Sindy Vega'
                    elif newActor == 'Clover':
                        newActor = 'Katya Clover'
                    elif newActor == 'Connie':
                        newActor = 'Connie Carter'
                    elif newActor == 'Corinne':
                        newActor = 'Summer Breeze'
                    elif newActor == 'Cornelia':
                        newActor = 'Stacy Cruz'
                    elif newActor == 'Crystal':
                        newActor = 'Bethany'
                    elif newActor == 'Danielle':
                        newActor = 'AJ Applegate'
                    elif newActor == 'Daphne':
                        newActor = 'Daphne Klyde'
                    elif newActor == 'Diana':
                        newActor = 'Diana Fox'
                    elif newActor == 'Dillion':
                        newActor = 'Dillion Harper'
                    elif newActor == 'Dina':
                        newActor = 'Lady Dee'
                    elif newActor == 'Dominica':
                        newActor = 'Dominic Anna'
                    elif newActor == 'Dominique':
                        newActor = 'Dominika C.'
                    elif newActor == 'Elle':
                        newActor = 'Elle Alexandra'
                    elif newActor == 'Ellie':
                        newActor = 'Rima B'
                    elif newActor == 'Emilie':
                        newActor = 'Emily Grey'
                    elif newActor == 'Emily':
                        newActor = 'Cassandra Nix'
                    elif newActor == 'Emily B':
                        newActor = 'Emily Brix'
                    elif newActor == 'Emma':
                        newActor = 'Emma Mae'
                    elif newActor == 'Erica':
                        newActor = 'Erica Fontes'
                    elif newActor == 'Eufrat':
                        newActor = 'Eufrat Mai'
                    elif newActor == 'Eve':
                        newActor = 'Janetta'
                    elif newActor == 'Eve A':
                        newActor = 'Ivana Sugar'
                    elif newActor == 'Eveline':
                        newActor = 'Eveline Dellai'
                    elif newActor == 'Faye':
                        newActor = 'Faye Reagan'
                    elif newActor == 'Foxi':
                        newActor = 'Foxxi Black'
                    elif newActor == 'Francesca':
                        newActor = 'Franziska Facella'
                    elif newActor == 'Gabriella':
                        newActor = 'Katie Oliver'
                    elif newActor == 'Georgia':
                        newActor = 'Georgia Jones'
                    elif newActor == 'Gianna':
                        newActor = 'Victoria Blaze'
                    elif newActor == 'Gigi':
                        newActor = 'Gigi Labonne'
                    elif newActor == 'Gigi R':
                        newActor = 'Gigi Rivera'
                    elif newActor == 'GiiGi':
                        newActor = 'Gigi Allens'
                    elif newActor == 'Gina':
                        newActor = 'Gina Gerson'
                    elif newActor == 'Grace':
                        newActor = 'Teena Dolly'
                    elif newActor == 'Hanna':
                        newActor = 'Hannah Hawthorne'
                    elif newActor == 'Hannah':
                        newActor = 'Cayla Lyons'
                    elif newActor == 'Cayla':
                        newActor = 'Cayla Lyons'
                    elif newActor == 'Hayden':
                        newActor = 'Hayden Winters'
                    elif newActor == 'Hayden H':
                        newActor = 'Hayden Hawkens'
                    elif newActor == 'Heather':
                        newActor = 'Kamila'
                    elif newActor == 'Heidi':
                        newActor = 'Taylor Sands'
                    elif newActor == 'Heidi R':
                        newActor = 'Heidi Romanova'
                    elif newActor == 'Holly':
                        newActor = 'Leonie'
                    elif newActor == 'Ivana':
                        newActor = 'Megan Promesita'
                    elif newActor == 'Ivy':
                        newActor = 'Iwia'
                    elif newActor == 'Izzy':
                        newActor = 'Izzy Delphine'
                    elif newActor == 'Jackie':
                        newActor = 'Masha D.'
                    elif newActor == 'Jade':
                        newActor = 'Jade Baker'
                    elif newActor == 'Janie':
                        newActor = 'Leila Smith'
                    elif newActor == 'Jasmine':
                        newActor = 'Gina Devine'
                    elif newActor == 'Jayden':
                        newActor = 'Jayden Taylors'
                    elif newActor == 'Jenna':
                        newActor = 'Jenna Ross'
                    elif newActor == 'Jenni':
                        newActor = 'Jenni Czech'
                    elif newActor == 'Jenny':
                        newActor = 'Alicia A'
                    elif newActor == 'Jenny M':
                        newActor = 'Janny Manson'
                    elif newActor == 'Jericha':
                        newActor = 'Jericha Jem'
                    elif newActor == 'Jessica':
                        newActor = 'Aleksa Slusarchi'
                    elif newActor == 'Jessie':
                        newActor = 'Jessie Andrews'
                    elif newActor == 'Jewel':
                        newActor = 'Julia I'
                    elif newActor == 'Jillian':
                        newActor = 'Jillian Janson'
                    elif newActor == 'Jocelyn':
                        newActor = 'Ellena Woods'
                    elif newActor == 'Joseline':
                        newActor = 'Joseline Kelly'
                    elif newActor == 'Julie':
                        newActor = 'Tracy Smile'
                    elif newActor == 'Karina':
                        newActor = 'Karina White'
                    elif newActor == 'Kassondra':
                        newActor = 'Kassondra Raine'
                    elif newActor == 'Kat':
                        newActor = 'Talia Shepard'
                    elif newActor == 'Kate':
                        newActor = 'Foxy Di'
                    elif newActor == 'Katerina':
                        newActor = 'Antonia Sainz'
                    elif newActor == 'Katherine':
                        newActor = 'Kari Sweet'
                    elif newActor == 'Katia':
                        newActor = 'Joleyn Burst'
                    elif newActor == 'Katie Jayne':
                        newActor = 'Katy Jayne'
                    elif newActor == 'Katka':
                        newActor = 'Ferrera Gomez'
                    elif newActor == 'Kato':
                        newActor = 'Kimberly Kato'
                    elif newActor == 'Katrina':
                        newActor = 'Nessa Devil'
                    elif newActor == 'Katy':
                        newActor = 'Kya'
                    elif newActor == 'Kaye':
                        newActor = 'Celine'
                    elif newActor == 'Kaylee':
                        newActor = 'Candice Luca'
                    elif newActor == 'Keira':
                        newActor = 'Keira Albina'
                    elif newActor == 'Kendall':
                        newActor = 'Kendall White'
                    elif newActor == 'Kenna':
                        newActor = 'Kenna James'
                    elif newActor == 'Kennedy':
                        newActor = 'Kennedy Kressler'
                    elif newActor == 'Kenzie':
                        newActor = 'Kenze Thomas'
                    elif newActor == 'Kiera':
                        newActor = 'Kiera Winters'
                    elif newActor == 'Kim':
                        newActor = 'Katy Rose'
                    elif newActor == 'Kimmy':
                        newActor = 'Kimmy Granger'
                    elif newActor == 'Kinsley':
                        newActor = 'Kinsley Ann'
                    elif newActor == 'Kira':
                        newActor = 'Kira Thorn'
                    elif newActor == 'Kirra':
                        newActor = 'Kira Zen'
                    elif newActor == 'Kirsten Lee':
                        newActor = 'Kirsten Nicole Lee'
                    elif newActor == 'Kitty':
                        newActor = 'Kitty Jane'
                    elif newActor == 'Klara':
                        newActor = 'Zoe'
                    elif newActor == 'Kristen':
                        newActor = 'Jessica Rox'
                    elif newActor == 'Kristi':
                        newActor = 'Allison'
                    elif newActor == 'Kristin Scott':
                        newActor = 'Kristen Scott'
                    elif newActor == 'Kylie':
                        newActor = 'Kylie Nicole'
                    elif newActor == 'Lana':
                        newActor = 'Mia Hilton'
                    elif newActor == 'Laura':
                        newActor = 'Kalea Taylor'
                    elif newActor == 'Leah':
                        newActor = 'Vika T'
                    elif newActor == 'Leila':
                        newActor = 'Blue Angel'
                    elif newActor == 'Lena':
                        newActor = 'Lena Anderson'
                    elif newActor == 'Leony':
                        newActor = 'Cherry Kiss'
                    elif newActor == 'Lexi':
                        newActor = 'Lexi Belle'
                    elif newActor == 'Lexy':
                        newActor = 'Lexi Layo'
                    elif newActor == 'Lia':
                        newActor = 'Lia Lor'
                    elif newActor == 'Lilit':
                        newActor = 'Lilit Sweet'
                    elif newActor == 'Lillianne':
                        newActor = 'Ariel'
                    elif newActor == 'Lilly':
                        newActor = 'Lily Labeau'
                    elif newActor == 'Lilly Ivy':
                        newActor = 'Lily Ivy '
                    elif newActor == 'Lilu':
                        newActor = 'Lilu Moon'
                    elif newActor == 'Lily':
                        newActor = 'Naomi Nevena'
                    elif newActor == 'Linsay':
                        newActor = 'Nataly Gold'
                    elif newActor == 'Lisa':
                        newActor = 'Lauren Crist'
                    elif newActor == 'Liv':
                        newActor = 'Elisa'
                    elif newActor == 'Liza Dawn':
                        newActor = 'Lisa Dawn'
                    elif newActor == 'Lola':
                        newActor = 'Penelope Lynn'
                    elif newActor == 'Lolita':
                        newActor = 'Lexie Fox'
                    elif newActor == 'Lorena':
                        newActor = 'Lorena Garcia'
                    elif newActor == 'Lovita':
                        newActor = 'Lovita Fate'
                    elif newActor == 'Lyra':
                        newActor = 'Lyra Louvel'
                    elif newActor == 'Malena':
                        newActor = 'Malena Morgan'
                    elif newActor == 'Malena A':
                        newActor = 'Melena Maria Rya'
                    elif newActor == 'Maria':
                        newActor = 'Anna Rose'
                    elif newActor == 'Marica':
                        newActor = 'Marica Hase'
                    elif newActor == 'Marie':
                        newActor = 'Satin Bloom'
                    elif newActor == 'Marie M.':
                        newActor = 'Marie McCray'
                    elif newActor == 'Mary':
                        newActor = 'Marry Queen'
                    elif newActor == 'Maryjane':
                        newActor = 'Maryjane Johnson'
                    elif newActor == 'Maya':
                        newActor = 'Lynette'
                    elif newActor == 'Maya M':
                        newActor = 'Sapphira A'
                    elif newActor == 'Megan':
                        newActor = 'Natali Blond'
                    elif newActor == 'Melanie':
                        newActor = 'Melanie Rios'
                    elif newActor == 'Mia':
                        newActor = 'Mia Lina'
                    elif newActor == 'Mia M':
                        newActor = 'Mia Malkova'
                    elif newActor == 'Michelle':
                        newActor = 'Irina J'
                    elif newActor == 'Mikah':
                        newActor = 'Katerina'
                    elif newActor == 'Mila K':
                        newActor = 'Michaela Isizzu'
                    elif newActor == 'Milla':
                        newActor = 'Mila Azul'
                    elif newActor == 'Mira':
                        newActor = 'Diana G'
                    elif newActor == 'Miss Pac Man':
                        newActor = 'Nedda A'
                    elif newActor == 'Misty':
                        newActor = 'Paula Shy'
                    elif newActor == 'Miu':
                        newActor = 'Sabrisse'
                    elif newActor == 'Anastasia':
                        newActor = 'Monika Benz'
                    elif newActor == 'Monika':
                        newActor = 'Monika Benz'
                    elif newActor == 'Monique':
                        newActor = 'Monika Thu'
                    elif newActor == 'Nadia':
                        newActor = 'Nadia Nickels'
                    elif newActor == 'Nancy':
                        newActor = 'Nancy Ace'
                    elif newActor == 'Naomi':
                        newActor = 'Silvie Luca'
                    elif newActor == 'Naomi B':
                        newActor = 'Naomi Bennet'
                    elif newActor == 'Nastia':
                        newActor = 'Lindsey Olsen'
                    elif newActor == 'Nastya':
                        newActor = 'Nikki Stills'
                    elif newActor == 'Natali':
                        newActor = 'Elouisa'
                    elif newActor == 'Natalie':
                        newActor = 'Jaslene Jade'
                    elif newActor == 'Natasha B':
                        newActor = 'Kelly E'
                    elif newActor == 'Nella':
                        newActor = 'Lexi Foxy'
                    elif newActor == 'Nicola':
                        newActor = 'Nika'
                    elif newActor == 'Nicole':
                        newActor = 'Gina'
                    elif newActor == 'Niki':
                        newActor = 'Nikki Fox'
                    elif newActor == 'Nikki':
                        newActor = 'Nici Dee'
                    elif newActor == 'Nikki Peaches':
                        newActor = 'Nikki Peach'
                    elif newActor == 'Nina':
                        newActor = 'Nina James'
                    elif newActor == 'Olivia':
                        newActor = 'Livia Godiva'
                    elif newActor == 'Oliya':
                        newActor = 'Isabel B'
                    elif newActor == 'Paige':
                        newActor = 'Paige Owens'
                    elif newActor == 'Pam':
                        newActor = 'Lena Love'
                    elif newActor == 'Patsy':
                        newActor = 'Angelic Anya'
                    elif newActor == 'Paulina':
                        newActor = 'Susan Ayn'
                    elif newActor == 'Pink Violet':
                        newActor = 'Violette Pink'
                    elif newActor == 'Presley':
                        newActor = 'Presley Hart'
                    elif newActor == 'Rainbow':
                        newActor = 'Hannah Hays'
                    elif newActor == 'Rebecca':
                        newActor = 'Rebecca Volpetti'
                    elif newActor == 'Reese':
                        newActor = 'Paloma B'
                    elif newActor == 'Reina':
                        newActor = 'Artemis'
                    elif newActor == 'Ria Sun':
                        newActor = 'Ria Sunn'
                    elif newActor == 'Riley':
                        newActor = 'Dakoda Brookes'
                    elif newActor == 'Ruby':
                        newActor = 'Heather Starlet'
                    elif newActor == 'Sam':
                        newActor = 'Alyssa Branch'
                    elif newActor == 'Samantha':
                        newActor = 'Samantha Jolie'
                    elif newActor == 'Sammy':
                        newActor = 'Samantha Rone'
                    elif newActor == 'Sandra':
                        newActor = 'Zena Little'
                    elif newActor == 'Sandy':
                        newActor = 'Izabelle A'
                    elif newActor == 'Sasha':
                        newActor = 'Sasha Grey'
                    elif newActor == 'Sasha D':
                        newActor = 'Catina'
                    elif newActor == 'Scarlet':
                        newActor = 'Veronica Radke'
                    elif newActor == 'Scarlett':
                        newActor = 'Heather Carolin'
                    elif newActor == 'Serena':
                        newActor = 'Amarna Miller'
                    elif newActor == 'Shrima':
                        newActor = 'Shrima Malati'
                    elif newActor == 'Silvie':
                        newActor = 'Silvie Deluxe'
                    elif newActor == 'Sophia':
                        newActor = 'Sophia Fiore'
                    elif newActor == 'Sophie':
                        newActor = 'Sophia Knight'
                    elif newActor == 'Stacy':
                        newActor = 'Deina'
                    elif newActor == 'Star':
                        newActor = 'Zoey Kush'
                    elif newActor == 'Stasha':
                        newActor = 'Irina K'
                    elif newActor == 'Stefanie':
                        newActor = 'Eileen Sue'
                    elif newActor == 'Stephanie':
                        newActor = 'Stefanie'
                    elif newActor == 'Stevie':
                        newActor = 'Barbamiska'
                    elif newActor == 'Summer':
                        newActor = 'Tracy Lindsay'
                    elif newActor == 'Sunshine':
                        newActor = 'Adele Sunshine'
                    elif newActor == 'Susie':
                        newActor = 'Dido Angel'
                    elif newActor == 'Suzie C':
                        newActor = 'Suzie Carina'
                    elif newActor == 'Sweetie':
                        newActor = 'Lilith Lee'
                    elif newActor == 'Sybil':
                        newActor = 'Sybil A'
                    elif newActor == 'Tabitha':
                        newActor = 'Sarka'
                    elif newActor == 'Talia':
                        newActor = 'Talia Mint'
                    elif newActor == 'Tara':
                        newActor = 'Xandra B'
                    elif newActor == 'Tasha':
                        newActor = 'Lena'
                    elif newActor == 'Tatiana':
                        newActor = 'Leo'
                    elif newActor == 'Teal':
                        newActor = 'Lucy Li'
                    elif newActor == 'Tess':
                        newActor = 'Nadine'
                    elif newActor == 'The Red Fox':
                        newActor = 'Red Fox'
                    elif newActor == 'Tiffany':
                        newActor = 'Tiffany Thompson'
                    elif newActor == 'Tiffany F':
                        newActor = 'Tiffany Fox'
                    elif newActor == 'Tina':
                        newActor = 'Heather Night'
                    elif newActor == 'Tori':
                        newActor = 'Tori Black'
                    elif newActor == 'Tracy':
                        newActor = 'Sinovia'
                    elif newActor == 'Vanna':
                        newActor = 'Vanna Bardot'
                    elif newActor == 'Veronica':
                        newActor = 'Veronica Clark'
                    elif newActor == 'Veronika':
                        newActor = 'Anetta V.'
                    elif newActor == 'Vicki':
                        newActor = 'Vicky Love'
                    elif newActor == 'Vicky':
                        newActor = 'Vicki Chase'
                    elif newActor == 'Victoria':
                        newActor = 'Victoria Rae Black'
                    elif newActor == 'Viktoria':
                        newActor = 'Scyley Jam'
                    elif newActor == 'Vinna':
                        newActor = 'Vinna Reed'
                    elif newActor == 'Willow':
                        newActor = 'Jana Mrhacova'
                    elif newActor == 'Zazie':
                        newActor = 'Zazie Sky'
                elif metadata.studio == 'DDFProd':
                    if newActor == 'Ms White-Kitten':
                        newActor = 'Goldie Baby'
                    elif newActor == 'Helen':
                        newActor = 'Alena H'
                elif metadata.studio == 'Reality Kings':
                    if newActor == 'Morgan':
                        newActor = 'Morgan Layne'
                elif metadata.studio == 'WowGirls':
                    if newActor == 'Clover':
                        newActor = 'Katya Clover'
                elif metadata.studio == 'Private':
                    if newActor == 'Lolita Taylor':
                        newActor = 'Lola Taylor'
                    elif newActor == 'Scarlet':
                        newActor = 'Scarlet Domingo'
                elif metadata.studio == 'VIPissy':
                    if newActor == 'Susan Ayne':
                        newActor = 'Susan Ayn'
                elif metadata.studio == 'Erika Lust Films':
                    if newActor == 'Luna Corazón':
                        newActor = 'Luna Corazon'
                elif metadata.studio == 'Bang Com':
                    if newActor == 'London Keys':
                        newActor = 'London Keyes'
                elif metadata.studio == 'Milehigh' or metadata.studio == 'Doghouse Digital':
                    if newActor == 'Gabrielle Lati':
                        newActor = 'Gabriella Lati'
                elif metadata.studio == 'Rocco Siffredi':
                    if newActor == 'Abbie':
                        newActor = 'Krystal Boyd'
                elif metadata.studio == 'Puffy Network':
                    if newActor == 'Stefany':
                        newActor = 'Stefanie Moon'
                elif metadata.studio == 'HuCows.com':
                    if newActor == 'Daisy':
                        newActor = 'Emma Green'
                    elif newActor == 'Liz':
                        newActor = 'Liz Rainbow'
                    elif newActor == 'Buttercup':
                        newActor = 'Kaitlin Grey'
                    elif newActor == 'Cory':
                        newActor = 'Cory Spice'
                    elif newActor == 'Izzy':
                        newActor = 'Izzy Delphine'
                    elif newActor == 'Katie':
                        newActor = 'Katie Thornton'
                    elif newActor == 'Lisa':
                        newActor = 'Lisa Scott'
                    elif newActor == 'Darina':
                        newActor = 'Darina Nikitina'
                    elif newActor == 'Olga':
                        newActor = 'Olga Cabaeva'
                    elif newActor == 'Roxy':
                        newActor = 'Roxy Mendez'
                    elif newActor == 'Dolly':
                        newActor = 'Bad Dolly'
                    elif newActor == 'Alais':
                        newActor = 'Alais Peach'
                    elif newActor == 'Arabella':
                        newActor = 'Arabella Langford'
                    elif newActor == 'Katarina':
                        newActor = 'Katarina Hartlova'
                    elif newActor == 'Sam':
                        newActor = 'Domenica'
                    elif newActor == 'Samantha':
                        newActor = 'Samantha Bentley'
                    elif newActor == 'Fayth':
                        newActor = 'Fayth On Fire'
                elif metadata.studio == 'QueenSnake' or metadata.studio == 'QueenSect':
                    if newActor == 'Qs':
                        newActor = 'Queensnake'
                    elif newActor != 'Queensnake':
                        newActor = newActor + ' QueenSnake'
                elif metadata.studio == 'VirtualTaboo':
                    if newActor == 'Penelope':
                        newActor = 'Penelope Cum'
                elif metadata.studio == 'VR Bangers':
                    if newActor == 'Victoria P':
                        newActor = 'Victoria Puppy'
                elif metadata.studio == 'HighTechVR':
                    if newActor == 'Lady D':
                        newActor = 'Lady Dee'

                if not newPhoto:
                    newPhoto = actorDBfinder(newActor)
                Log('Actor: %s %s' % (newActor, newPhoto))

                role = metadata.roles.new()
                role.name = newActor
                role.photo = newPhoto
            actorsProcessed = actorsProcessed + 1


def actorDBfinder(actorName):
    actorEncoded = urllib.quote(actorName)
    actorPhotoURL = ''

    if actorName:
        databaseName = 'AdultDVDEmpire'
        req = PAutils.HTTPRequest('https://www.adultdvdempire.com/performer/search?q=' + actorEncoded)
        actorSearch = HTML.ElementFromString(req.text)
        actorPageURL = actorSearch.xpath('//div[@id="performerlist"]/div//a/@href')
        if actorPageURL:
            actorPageURL = 'https://www.adultdvdempire.com' + actorPageURL[0]
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            img = actorPage.xpath('//div[contains(@class, "performer-image-container")]/a/@href')
            if img:
                actorPhotoURL = img[0]

        if not actorPhotoURL:
            databaseName = 'Boobpedia'
            actorPageURL = 'http://www.boobpedia.com/boobs/' + actorName.title().replace(' ', '_')
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            img = actorPage.xpath('//table[@class="infobox"]//a[@class="image"]//img/@src')
            if img:
                actorPhotoURL = 'http://www.boobpedia.com' + img[0]

        if not actorPhotoURL:
            databaseName = 'Babes and Stars'
            actorPageURL = 'http://www.babesandstars.com/' + actorName[0:1].lower() + '/' + actorName.lower().replace(' ', '-').replace('\'', '-') + '/'
            req = PAutils.HTTPRequest(actorPageURL)
            actorPage = HTML.ElementFromString(req.text)
            img = actorPage.xpath('//div[@class="profile"]//div[@class="thumb"]/img/@src')
            if img:
                actorPhotoURL = img[0]

        if not actorPhotoURL:
            databaseName = 'IAFD'
            req = PAutils.HTTPRequest('http://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=' + actorEncoded)
            actorSearch = HTML.ElementFromString(req.text)
            actorPageURL = actorSearch.xpath('//table[@id="tblFem"]//tbody//a/@href')
            if actorPageURL:
                actorPageURL = 'http://www.iafd.com' + actorPageURL[0]
                req = PAutils.HTTPRequest(actorPageURL)
                actorPage = HTML.ElementFromString(req.text)
                img = actorPage.xpath('//div[@id="headshot"]//img/@src')
                if img and 'nophoto' not in img[0]:
                    actorPhotoURL = img[0]

        if not actorPhotoURL:
            databaseName = 'Babepedia'
            img = 'http://www.babepedia.com/pics/' + actorName.title().replace(' ', '%20') + '.jpg'
            req = PAutils.HTTPRequest(img, 'HEAD', bypass=False)
            if req.ok:
                actorPhotoURL = img

        if actorPhotoURL:
            Log('%s found in %s ' % (actorName, databaseName))
            Log('PhotoURL: %s' % actorPhotoURL)
        else:
            Log('%s not found' % actorName)

    return actorPhotoURL
