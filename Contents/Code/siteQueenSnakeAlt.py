import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    if searchDate:
        encodedTitle = parse(searchDate).strftime('%Y/%m/%d')
    else:
        encodedTitle = '?s=%s' % searchTitle.replace(' ', '+')

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle)
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//article'):
        sceneURL = searchResult.xpath('.//h2/a[@rel="bookmark"]/@href')[0].strip()
        curID = PAutils.Encode(sceneURL)
        titleNoFormatting = searchResult.xpath('.//h2[@class="entry-title"]/a')[0].text_content().strip().replace(' + GAME for free membership'. '').replace('New movie on queensnake.com – ', '').replace('New movie update on queensect.com – ', '')

        date = searchResult.xpath('.//time[@class="entry-date published"]')[0].text_content().strip()
        releaseDate = parse(date).strftime('%Y-%m-%d')

        if searchDate:
            score = 100 - Util.LevenshteinDistance(searchDate, releaseDate)
        else:
            score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        badTitles = [
            'Welcome to my blog',
            'Poll Results',
            'Poll Results VI',
            'Poll Results V',
            'Poll Results IV',
            'Tackrider Series',
            'Sex in BDSM',
            'Fetish Party',
            'I Had A Dream',
            'A Technical Question',
            'Streaming or download?',
            'Subscription',
            'New Website Issue',
            'New Subscription System',
            'How to use the staples safely? Practical tips',
            'New Separated Blog',
            'New skin',
            'Comments Disabled :(',
            'New Blog Rules',
            'Review',
            'Queensect.com',
            'News – Holy Shit Award 2015',
            'Queensnake.com is online',
            'Queensnake.com server issues on 2017-03-21',
        ]
        if titleNoFormatting not in badTitles:
            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchSearchURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    Title = detailsPageElements.xpath('//article/header/h1[@class="entry-title"]')[0].text_content().strip()
    Title = Title.replace('New movie on queensnake.com – ').replace('New movie on queensect.com – ')
    metadata.title = Title.title()

    # Studio
    metadata.studio = 'QueenSnake.com'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = 'QueenSnake'
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
   date = detailsPageElements.xpath('//time[@class="entry-date published"]')[0].text_content().strip()
    date_object = datetime.strptime(date, '%Y/%m/%d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Summary
        description = detailsPageElements.xpath('//div[@class="entry-content"]')[0].text_content()
        metadata.summary = description.strip()

    # Genres
    movieGenres.clearGenres()

    # Default Genres
    genres = ['BDSM', 'S&M']
    for genreName in genres:
        movieGenres.addGenre(genreName)

    # Dynamic Genres
    for genreLink in detailsPageElements.xpath('//a[@rel="category tag"]|//a[@rel="tag"]'):
        genreName = genreLink.text_content().strip()

        movieGenres.addGenre(genreName)

    # Actors
    movieActors.clearActors()
    siteActors = [
        'Abby'
        ,'Briana'
        ,'David'
        ,'Diamond'
        ,'Greta'
        ,'Hellia'
        ,'Hilda'
        ,'Holly'
        ,'Jade'
        ,'Jeby'
        ,'Jessica'
        ,'Keya'
        ,'Lilith'
        ,'Luna'
        ,'Marc'
        ,'Micha'
        ,'Misty'
        ,'Nastee'
        ,'Nazryana'
        ,'Pearl'
        ,'QS'
        ,'Queensnake'
        ,'Rachel'
        ,'Ruby'
        ,'Sharon'
        ,'Suzy'
        ,'Tanita'
        ,'Tracy'
        ,'Zara'
    ]

    for actorLink in detailsPageElements.xpath('//a[@rel="tag"]'):
        if actorLink in siteActors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    for poster in detailsPageElements.xpath('//article//img/@src'):
        art.append(poster)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.google.com'})
                im = StringIO(image.content)
                resized_image = Image.open(im)
                width, height = resized_image.size
                # Add the image proxy items to the collection
                if width > 1:
                    # Item is a poster
                    metadata.posters[posterUrl] = Proxy.Media(image.content, sort_order=idx)
                if width > 100 and idx > 1:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
