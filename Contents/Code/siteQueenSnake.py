import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.replace(' ', '-').lower()

    # Log(Title)
    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.lower() + '/', headers={'Cookie': 'cLegalAge=true'})
    # Log(req.text)
    searchResults = HTML.ElementFromString(req.text)
    # Log(searchResults.xpath('//div[@class="contentBlock"]'))
    for searchResult in searchResults.xpath('//div[@class="contentBlock"]'):
        
        titleNoFormatting = searchResult.xpath('.//span[@class="contentFilmName"]')[0].text_content().strip().title()
        # Log(titleNoFormatting)

        date = searchResult.xpath('.//span[@class="contentFileDate"]')[0].text_content().strip().split(' • ')[0]
        releaseDate = parse(date).strftime('%Y-%m-%d')
        # Log(releaseDate)

        curID = PAutils.Encode(encodedTitle.lower())

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        results.Append(MetadataSearchResult(id='%s|%d|%s' % (curID, siteNum, releaseDate), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    Log(sceneURL)
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchSearchURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL, headers={'Cookie': 'cLegalAge=true'})
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    Title = detailsPageElements.xpath('//div[@class="contentBlock"]//span[@class="contentFilmName"]')[0].text_content().strip().title()
    metadata.title = Title.title()

    # Studio
    metadata.studio = 'QueenSnake.com'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = 'QueenSnake'
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//div[@class="contentBlock"]//span[@class="contentFileDate"]')[0].text_content().strip().split(' • ')[0]
    date_object = datetime.strptime(date, '%Y %B %d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Summary

    # Basic Summary
    try:
        description = detailsPageElements.xpath('//div[@class="contentBlock"]//div[@class="contentPreviewDescription"]')[0].text_content()
        metadata.summary = description.strip()
    except:
        pass
    
    # Blog Summary
    ## ToDo

    # Genres
    movieGenres.clearGenres()

    # Default Genres
    genres = ['BDSM', 'S&M']
    for genreName in genres:
        movieGenres.addGenre(genreName)

    # Dynamic Genres
    for genreLink in detailsPageElements.xpath('//div[@class="contentPreviewTags"]/a'):
        genreName = genreLink.text_content().strip()
        movieGenres.addGenre(genreName)

    # Blog Genres
    ## ToDo

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
        ,'Queensnake'
        ,'Rachel'
        ,'Ruby'
        ,'Sharon'
        ,'Suzy'
        ,'Tanita'
        ,'Tracy'
        ,'Zara'
    ]

    for actorLink in detailsPageElements.xpath('//div[@class="contentBlock"]//div[@class="contentPreviewTags"]/a'):
        if actorLink in siteActors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    for poster in detailsPageElements.xpath('//div[@class="contentBlock"]//img/@src'):
        posterUrl = PAsearchSites.getSearchBaseURL(siteID) + poster.split('?')[0]
        art.append(posterUrl)

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
