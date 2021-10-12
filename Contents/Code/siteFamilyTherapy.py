import PAsearchSites
import PAutils
import siteClips4Sale


class FakeResults:
    def __init__(self):
        self.list = list()

    def Append(self, item):
        self.list.append(item)


def clean(title):
    ext = {'mp4', 'wmv'}
    quality = {'sd', 'hd'}
    for word in ext:
        title = title.replace(word.upper(), '')
    for word in quality:
        title = title.replace(word.upper(), '')
    return title


def search(results, lang, siteNum, searchData):
    sceneURL = PAsearchSites.getSearchSearchURL(siteNum) + searchData.encoded.replace('and', '&')
    req = PAutils.HTTPRequest(sceneURL)
    searchPageElements = HTML.ElementFromString(req.text)
    searchResults = searchPageElements.xpath('//article')
    for searchResult in searchResults:
        titleNoFormatting = searchResult.xpath('./h2/a/text()')[0].strip()
        curID = PAutils.Encode(searchResult.xpath('./h2/a/@href')[0])
        date = searchResult.xpath('./p/span[1]/text()')[0].strip()
        releaseDate = parse(date).strftime('%b %d, %Y')
        score = 100 - Util.LevenshteinDistance(searchData.title.lower(), titleNoFormatting.lower())
        results.Append(MetadataSearchResult(id='%s|%d|%d' % (curID, siteNum, 0), name='%s [FamilyTherapy] %s' % (titleNoFormatting, releaseDate), score=score, lang=lang))

    if len(searchResults) == 0:
        Log("Using Clips4Sale")
        parts = searchData.title.split()
        if len(parts) > 2:
            title = (' ').join(parts[2:])
            actress = (' ').join(parts[:2])
        searchData.title = "81593 " + actress
        matches = siteClips4Sale.search(FakeResults(), lang, 760, searchData)
        for match in matches.list:
            match.name = clean(match.name)
            match.score = 100 - Util.LevenshteinDistance(title.lower(), re.search(r'.*(?=\[)', match.name.lower()).group().strip())
            match.id = ('|').join([match.id.split('|')[0], str(siteNum), str(1)])
            results.Append(match)

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    sceneURL = PAutils.Decode(metadata_id[0])
    siteNum = metadata_id[1]
    mode = int(metadata_id[2])
    if mode == 1:
        # Using Clips4Sale
        metadata = siteClips4Sale.update(metadata, lang, 760, movieGenres, movieActors)
        if not sceneURL.startswith('http'):
            sceneURL = PAsearchSites.getSearchBaseURL(760) + sceneURL
        req = PAutils.HTTPRequest(sceneURL)
        detailsPageElements = HTML.ElementFromString(req.text)

        # Title
        metadata.title = clean(metadata.title)

        # Actor
        actorPhotoURL = ''
        try:
            actorName = detailsPageElements.xpath('//div[@class="[ mt-1-5 ] clip_details"]/div[3]/span[2]/span[1]/a/text()')[0]
            movieActors.addActor(actorName, actorPhotoURL)
        except:
            summary = detailsPageElements.xpath('//div[@class="individualClipDescription"]/p/text()')[0]
            actorName = re.search(r'(?<=[Ss]tarring\s)\w*\s\w*', summary).group()
            movieActors.addActor(actorName, actorPhotoURL)
            pass

        # Studio
        metadata.studio = 'Family Therapy'

        return metadata

    if not sceneURL.startswith('http'):
        sceneURL = PAsearchSites.getSearchBaseURL(siteNum) + sceneURL
    req = PAutils.HTTPRequest(sceneURL)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//h1/text()')[0].title().strip()

    # Summary
    summary = ''
    try:
        summary = detailsPageElements.xpath('//div[@class="entry-content"]/p[1]/text()')[0].strip()
    except:
        summary = detailsPageElements.xpath('//div[@class="entry-content"]/text()')[1].strip()
    metadata.summary = summary

    # Studio
    metadata.studio = 'Family Therapy'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = 'Family Therapy'
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Genres
    movieGenres.clearGenres()
    genres = detailsPageElements.xpath('//a[@rel="category tag"]/text()')
    for tag in genres:
        movieGenres.addGenre(tag.strip())

    # Release Date
    date = detailsPageElements.xpath('//p[@class="post-meta"]/span/text()')[0]
    if date:
        date_object = datetime.strptime(date, '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    for actorLink in detailsPageElements.xpath('//div[@class="entry-content"]/p[contains(text(),"starring") or contains(text(), "Starring")]/text()'):
        actorName = re.search(r'(?<=[Ss]tarring\s)\w*\s\w*', actorLink).group()
        actorPhotoURL = ''

        movieActors.addActor(actorName, actorPhotoURL)

    return metadata
