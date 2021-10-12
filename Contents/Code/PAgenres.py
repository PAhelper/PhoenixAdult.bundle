
import PAdatabaseGenres


class PhoenixGenres:
    genresTable = []

    def addGenre(self, newGenre):
        newGenre = newGenre.encode('UTF-8') if isinstance(newGenre, unicode) else newGenre
        if newGenre.lower() not in map(str.lower, self.genresTable):
            self.genresTable.append(newGenre)

    def clearGenres(self):
        self.genresTable = []

    def processGenres(self, metadata):
        for genreLink in self.genresTable:
            skip = False
            genreName = genreLink.replace('"', '').strip()

            searchGenreName = genreName.lower()
            for genre in PAdatabaseGenres.GenresSkip:
                if searchGenreName == genre.lower():
                    skip = True
                    break

            for genre in PAdatabaseGenres.GenresPartialSkip:
                if searchGenreName in genre.lower():
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
                genreName = genreName.title()

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
