import PAsearchSites
import PAgenres
import PAactors
import PAutils


def search(results, encodedTitle, searchTitle, siteNum, lang, searchDate):

    pageNum = 1
    while pageNum > 0:
        req = PAutils.HTTPRequest(PAsearchSites.getSearchSearchURL(siteNum) + str(pageNum))
        indexPageResults = HTML.ElementFromString(req.text)

        videos = indexPageResults.xpath('//div[@class="item"]')
        Log.Info('Parsing %d results' % len(videos))

        for video in videos:
            titleLink = video.xpath('.//a[@class="dark"]')[0]

            title = str(titleLink.text_content().strip())

            m = re.search("/video/(\d+)/([a-z0-9\-]+)", titleLink.get('href'))
            if m:
                videoTitle = m.group(2)
                videoId = m.group(1)
                curID = PAutils.Encode(videoTitle + '-mea-melone-' + videoId)

                score = 100
                score = score - String.LevenshteinDistance(searchTitle.lower(), title.lower())

                Log.Info('Found: %s / %d', title, score)
                
                if score > 95:
                    results.Append(
                        MetadataSearchResult(
                            id = '%s|%d' % (curID, siteNum),
                            name = '%s [%s]' % (title, 'Melone Challenge'),
                            score = score,
                            lang = lang
                        )
                    )

                    return results

        pageNum += 1
        if len(indexPageResults.xpath('//a[text() = "page ' + str(pageNum) + '"]')) == 0:
            Log.Debug('No more pages.')
            pageNum = -1

    return results

def update(metadata, siteID, movieGenres, movieActors):

    metadata_id = str(metadata.id).split('|')[0]

    req = PAutils.HTTPRequest(PAsearchSites.getSearchBaseURL(siteID) + PAutils.Decode(metadata_id))
    detailsPageElement = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElement.xpath('.//a[@class="dark"]')[0].text_content().strip()
    
    # Summary
    metadata.summary = detailsPageElement.xpath('//p[@style="line-height:130%; font-size:13px"]')[0].text_content().strip()

    metadata.studio = 'Melone Challenge'

    # Tagline and Collection(s)
    metadata.collections.clear()
    tagline = PAsearchSites.getSearchSiteName(siteID).strip()
    metadata.tagline = tagline
    metadata.collections.add(tagline)

    # Posters/Background
    valid_names = list()
    metadata.posters.validate_keys(valid_names)
    metadata.art.validate_keys(valid_names)

    posters = [ detailsPageElement.xpath('.//figure/img/@src')[0] ]
    
    posterNum = 1
    for posterUrl in posters:
        image = PAutils.HTTPRequest(posterUrl, headers={'Referer': 'http://www.google.com'})
        metadata.posters[posterUrl] = Proxy.Preview(image.content, sort_order = posterNum)
        posterNum = posterNum + 1

    return metadata