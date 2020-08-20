import PAsearchSites
import PAgenres
import PAactors
import PAutils

# Known Issues
#   - Images sometimes return placeholders (black and white swirls). Unknown cause.
#
#   - [Resolved/Code Fix] Occassionally title matches will stop working, and site will redirect to front page instead. Unknown cause.
#       - Fix: Redirect was on non-match, even though occasionally it's a false negative. Added check to search function
# To Do (maybe):
# - Pull Artwork, Genres, and extended description from blog at qsbdsm.com. Exact date matches should work for this.
# - Add actor photos manually.


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):
    encodedTitle = searchTitle.replace(' ', '-').lower()

    req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + encodedTitle.lower() + '/', headers={'Cookie': 'cLegalAge=true'})
    searchResults = HTML.ElementFromString(req.text)
    for searchResult in searchResults.xpath('//div[@class="contentBlock"]'):
        titleNoFormatting = searchResult.xpath('.//span[@class="contentFilmName"]')[0].text_content().strip().title()

        date = searchResult.xpath('.//span[@class="contentFileDate"]')[0].text_content().strip().split(' • ')[0]
        releaseDate = parse(date).strftime('%Y-%m-%d')

        curID = PAutils.Encode(encodedTitle.lower())

        score = 100 - Util.LevenshteinDistance(searchTitle.lower(), titleNoFormatting.lower())

        if '/previewmovies/0' not in str(searchResult.xpath('//div[@class="pagerWrapper"]/a/@href')[0]):
            results.Append(MetadataSearchResult(id='%s|%d' % (curID, siteNum), name='%s [%s] %s' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum), releaseDate), score=score, lang=lang))

    return results


def update(metadata, siteID, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchSearchURL(siteID) + sceneURL
    req = PAutils.HTTPRequest(sceneURL, headers={'Cookie': 'cLegalAge=true'})

    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    Title = detailsPageElements.xpath('//span[@class="contentFilmName"]')[0].text_content().strip().title()
    metadata.title = Title.title()

    # Studio
    metadata.studio = PAsearchSites.getSearchSiteName(siteID)

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID)
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Release Date
    date = detailsPageElements.xpath('//span[@class="contentFileDate"]')[0].text_content().strip().split(' • ')[0]
    date_object = datetime.strptime(date, '%Y %B %d')
    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Summary

    # Basic Summary
    try:
        description = detailsPageElements.xpath('//div[@class="contentPreviewDescription"]')[0].text_content()
        metadata.summary = description.strip()
    except:
        pass

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

    # Actors
    movieActors.clearActors()
    siteActors = [
        'abby', 'briana', 'david', 'diamond', 'greta', 'hellia',
        'hilda', 'holly', 'jade', 'jeby', 'jessica', 'keya', 'lilith',
        'luna', 'marc', 'micha', 'misty', 'nastee', 'nazryana',
        'pearl', 'qs', 'queensnake', 'rachel', 'ruby', 'sharon',
        'suzy', 'tanita', 'tracy', 'zara'
    ]

    for actorLink in detailsPageElements.xpath('//div[@class="contentPreviewTags"]/a'):
        if actorLink.text_content().strip().lower() in siteActors:
            actorName = actorLink.text_content().strip()
            actorPhotoURL = ''

            movieActors.addActor(actorName, actorPhotoURL)

    # Posters
    art = []
    for poster in detailsPageElements.xpath('//div[@class="contentBlock"]//img[contains(@src,"preview")]/@src'):
        posterUrl = PAsearchSites.getSearchBaseURL(siteID) + poster.split('?')[0]
        art.append(posterUrl)

    Log('Artwork found: %d' % len(art))
    for idx, posterUrl in enumerate(art, 1):
        if not PAsearchSites.posterAlreadyExists(posterUrl, metadata):
            # Download image file for analysis
            try:
                image = PAutils.HTTPRequest(posterUrl)
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
