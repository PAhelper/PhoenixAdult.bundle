
import PAdatabaseGenres
import PAutils


class PhoenixGenres:
    genresTable = []

    def addGenre(self, newGenre):
        newGenre = newGenre.encode('UTF-8') if isinstance(newGenre, unicode) else newGenre
        if newGenre.lower() not in map(str.lower, self.genresTable):
            self.genresTable.append(newGenre)

    def clearGenres(self):
        self.genresTable = []

    def processGenres(self, metadata, siteNum):
        for genreLink in self.genresTable:
            skip = False
            genreName = genreLink.replace('"', '').replace('\xc2\xa0', ' ').strip()

            searchGenreName = genreName.lower()
            for genre in PAdatabaseGenres.GenresSkip:
                if searchGenreName == genre.lower():
                    skip = True
                    break

            if not skip:
                for genre in PAdatabaseGenres.GenresPartialSkip:
                    if genre.lower() in searchGenreName:
                        skip = True
                        break

            found = False
            if not skip:
                for genre, aliases in PAdatabaseGenres.GenresReplace.items():
                    if searchGenreName == genre.lower() or searchGenreName in map(str.lower, aliases):
                        found = True
                        genreName = genre
                        break

            if not found:
                genreName = PAutils.parseTitle(genreName, siteNum)

            if not found and not skip:
                if len(genreName) > 25:
                    skip = True
                if ':' in metadata.title:
                    if genreName.lower() in metadata.title.split(':')[0].lower():
                        skip = True
                if '-' in metadata.title:
                    if genreName.lower() in metadata.title.split('-')[0].lower():
                        skip = True
                if ' ' in genreName:
                    if 3 < len(genreName.split()):
                        skip = True

            if not skip:
                metadata.genres.add(genreName)
