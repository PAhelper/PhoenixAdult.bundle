import PAsearchSites
import PAutils


def search(results, lang, siteNum, searchData):
    scene_id = searchData.title.replace(' ', '-').replace('\'', '-').lower()
    scene_url = PAsearchSites.getSearchSearchURL(siteNum) + scene_id + '.html'
    req = PAutils.HTTPRequest(scene_url)
    result = HTML.ElementFromString(req.text)

    titleNoFormatting = result.xpath('//meta[@name="twitter:image:alt"]/@content')[0]

    score = 100

    cur_id = PAutils.Encode(scene_url)
    results.Append(MetadataSearchResult(id='%s|%d' % (cur_id, siteNum), name='%s [%s]' % (titleNoFormatting, PAsearchSites.getSearchSiteName(siteNum)), score=score, lang=lang))

    return results


def update(metadata, lang, siteNum, movieGenres, movieActors):
    metadata_id = str(metadata.id).split('|')
    scene_url = PAutils.Decode(metadata_id[0])
    req = PAutils.HTTPRequest(scene_url)
    detailsPageElements = HTML.ElementFromString(req.text)

    # Title
    metadata.title = detailsPageElements.xpath('//meta[@name="twitter:image:alt"]/@content')[0]

    # Summary
    metadata.summary = detailsPageElements.xpath('//div[@class="content-desc more-desc"]')[0].text_content()

    # Studio
    metadata.studio = 'Swallow Bay'

    # Release Date
    str_date = detailsPageElements.xpath('//div//div[@class="content-date"]')[0].text_content().strip().replace('Date: ', '')
    date = re.sub(r'(\d)(st|nd|rd|th)', r'\1', str_date)
    date_object = datetime.strptime(date, "%d %b %Y")

    metadata.originally_available_at = date_object
    metadata.year = metadata.originally_available_at.year

    # Actors
    movieActors.clearActors()
    section = detailsPageElements.xpath('//div[@class="content-models"]/a')
    for actor_section in section:
        actor_name = actor_section.get('title')
        actor_photo_xpath = './/div[@class="content-models-photos"]/a[@title="' + actor_name + '"]/span/img'
        actor_photo_URL = detailsPageElements.xpath(actor_photo_xpath)[0].get('src')

        movieActors.addActor(actor_name, actor_photo_URL)

    # Genres
    movieGenres.clearGenres()
    for genre_link in detailsPageElements.xpath('//div[@class="box"]/a'):
        genre_name = genre_link.text_content().strip()

        movieGenres.addGenre(genre_name)

    # Posters/Background
    art = []
    poster = detailsPageElements.xpath('//meta[@property="og:image"]/@content')[0]
    art.append(poster)

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
                if width > 100:
                    # Item is an art item
                    metadata.art[posterUrl] = Proxy.Media(image.content, sort_order=idx)
            except:
                pass

    return metadata
