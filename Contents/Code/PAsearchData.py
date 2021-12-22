class SearchData:
    title = ''
    encoded = ''
    date = ''
    filepath = ''
    filename = ''
    duration = ''
    ohash = ''

    def __init__(self, media, searchTitle, searchDate, filepath):
        self.title = searchTitle
        if searchTitle:
            self.encoded = urllib.quote(searchTitle)
        self.date = searchDate
        self.filepath = filepath
        if filepath:
            self.filename = str(os.path.splitext(os.path.basename(filepath))[0])
            self.filename = PAutils.getSearchTitleStrip(self.filename)
        self.duration = media.duration
        if media.openSubtitlesHash:
            self.ohash = media.openSubtitlesHash

        Log('SearchData.title: %s' % self.title)

        if self.date:
            Log('SearchData.date: %s' % self.date)

        if self.filename:
            Log('SearchData.filename: %s' % self.filename)

    def dateFormat(self, format='%Y-%m-%d'):
        date = ''
        if self.date:
            date = parse(self.date).strftime(format)

        return date

    def durationFormat(self, hoursFormat='%02d:%02d:%02d', minutesFormat='%d:%02d'):
        durationString = ''

        if self.duration:
            import math
            seconds = round(float(self.duration) / 1000)
            hours = math.floor(seconds / 3600)
            seconds = seconds - hours * 3600
            minutes = math.floor(seconds / 60)
            seconds = seconds - minutes * 60

            if hours:
                durationString = hoursFormat % (hours, minutes, seconds)
            else:
                durationString = minutesFormat % (minutes, seconds)

        return durationString
