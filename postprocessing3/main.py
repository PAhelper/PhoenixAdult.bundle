#!/usr/bin/python3

import time
from datetime import date
import re
from pathlib import Path
import argparse
import logging
import json

import requests
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler


FILE_NAME_FORMAT = '{site}/{title} - {date} ~ {actors}'
EXTENSIONS = (
    '.mp4', '.mkv', '.avi', '.wmv'
)
MINIMAL_FILE_SIZE = 15728640


class PhoenixAdultRenamer():
    def __init__(self):
        for file in searching_all_files(input_path):
            work_with_file(file)

        self.observer = Observer()

    def run(self):
        self.observer.schedule(WatchFileHandler(), input_path, recursive=True)
        self.observer.start()
        while True:
            time.sleep(1)

    def stop(self):
        self.observer.stop()
        self.observer.join()


class WatchFileHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            file_path = None

            if event.event_type == 'created' or event.event_type == 'modified':
                file_path = event.src_path
            elif event.event_type == 'moved':
                file_path = event.dest_path

            if file_path:
                file_path = Path(file_path)

                # A dirty hack for copied files
                if event.event_type == 'created':
                    while True:
                        try:
                            file = open(file_path, 'rb')
                            file.close()
                            break
                        except PermissionError:
                            time.sleep(1)

                if file_path.is_file():
                    work_with_file(file_path)
        else:
            pass


def work_with_file(file_path: Path):
    if file_path.suffix in EXTENSIONS and file_path.stat().st_size > MINIMAL_FILE_SIZE:
        logging.info('Working with `%s`', ''.join(file_path.name))

        ohash = None
        if OHASH and opensubtitle_hash:
            try:
                ohash = oshash.oshash(file_path)
            except:
                pass

            if ohash:
                logging.info('Calculated hash is `%s`', ohash)

        data = get_data_from_api(file_path, ohash)
        if data:
            new_file_name = get_new_file_name(data)
            new_file_name = output_path / (new_file_name + file_path.suffix)

            if not new_file_name.is_file():
                title_clean = True
                if cleanup:
                    title = get_title_from_metadata(file_path)
                    if title:
                        title_clean = False

                if not new_file_name.parent.is_dir():
                    new_file_name.parent.mkdir(parents=True, exist_ok=True)

                answ = True
                if CONFIRM:
                    logging.info('Is new name correct `%s`?', new_file_name)
                    answ = is_confirm()

                if answ:
                    if cleanup and not title_clean:
                        cleanup_metadata(file_path, new_file_name)
                    else:
                        file_path.rename(new_file_name)

                    logging.info('Saving as `%s`', new_file_name)
                else:
                    logging.info('User not confirm')
            else:
                logging.error('Already exist `%s`', new_file_name)
        else:
            logging.info('Nothing found')


def get_new_file_name(data: dict) -> str:
    result = {
        'site': get_clean_str(data['site']['name']),
        'title': get_clean_str(data['title']),
        'date': data['date'],
        'actors': ', '.join([actor_link['name'] for actor_link in data['performers']])
    }

    new_file_name = FILE_NAME_FORMAT.format(**result)

    # Cutting filename if it's too long for OS
    if len(new_file_name) > 250:
        new_file_name = new_file_name[:250]

    return new_file_name


def get_data_from_api(file_path: str, ohash: str) -> dict:
    logging.info('Searching `%s`', file_path)

    if ohash:
        url = 'https://stashdb.org/graphql'
        headers = {
            'Content-Type': 'application/json',
            'apiKey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJhZTA1NmQ0ZC0wYjRmLTQzNmMtYmVhMy0zNjNjMTQ2MmZlNjMiLCJpYXQiOjE1ODYwNDAzOTUsInN1YiI6IkFQSUtleSJ9.5VENvrLtJXTGcdOhA0QC1SyPQ59padh1XiQRDQelzA4',
        }
        data = {
            'operationName': 'Scene',
            'variables': {
                'fingerprints': [ohash],
            },
            'query': 'query Scene($fingerprints:[String!]!){findScenesByFingerprints(fingerprints:$fingerprints){date title studio{name}}}',
        }

        response = requests.post(url, headers=headers, data=json.dumps(data)).json()
        if 'data' in response and response['data'] and response['data']['findScenesByFingerprints'] and response['data']['findScenesByFingerprints'][0]:
            response = response['data']['findScenesByFingerprints'][0]

            result = {
                'title': response['title'],
                'date': response['date'],
                'site': response['studio']['name'].replace(' ', ''),
            }
            file_path = '{site} - {date} - {title}'.format(**result)

            logging.info('Founded in StashDB searching `%s`', file_path)

    url = 'https://api.metadataapi.net/scenes?parse=%s&per_page=1' % file_path
    # if ohash:
        # url += '&hash=%s' % ohash

    headers = {
        'Authorization': 'Bearer %s' % token,
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    if data and 'data' in data and data['data']:
        return data['data'][0]

    return None


def get_title_from_metadata(file_name: Path) -> str:
    media_info = MediaInfo.parse(str(file_name))
    for track in media_info.tracks:
        if track.track_type == 'General':
            return track.title

    return None


def cleanup_metadata(file_name, new_file_name):
    stream = ffmpeg.input(str(file_name))
    stream = ffmpeg.output(
        stream,
        str(new_file_name),
        codec='copy',
        metadata='title='
    )
    ffmpeg.run(stream, quiet=True)
    file_name.unlink()


def get_clean_str(title: str) -> str:
    title = re.sub(r'[\'\"]', '', title)
    title = re.sub(r'(?:\W|[_])', ' ', title)

    title = ' '.join(title.split())

    return title


def searching_all_files(directory: Path) -> list:
    return [file for file in directory.rglob('*.*') if file.is_file()]


def is_confirm() -> bool:
    answer = ''
    while answer not in ['y', 'n']:
        answer = input('OK to push to continue [Y/N]?').lower()

    return answer == 'y'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Watchdog Adult Renamer.')
    parser.add_argument('-i', '--input_path', required=True, help='Directory to watch files')
    parser.add_argument('-o', '--output_path', required=True, help='Directory to store renamed files')
    parser.add_argument('-t', '--token', required=True, help='MetadataAPI Token')
    parser.add_argument('-c', '--cleanup', action='store_true', help='Remove metadata title from file')
    parser.add_argument('-a', '--additional_info', action='store_true', help='Add additional info to filename')
    parser.add_argument('-oh', '--oshash', action='store_true', help='Use OpenSubtitle Hash for search')
    parser.add_argument('-co', '--confirm', action='store_true', help='Ask user confirm before rename')

    args = parser.parse_args()
    input_path = Path(args.input_path).resolve()
    output_path = Path(args.output_path).resolve()
    token = args.token
    cleanup = args.cleanup
    additional_info = args.additional_info
    opensubtitle_hash = args.oshash
    confirm = args.confirm
    if not str(output_path).startswith(str(input_path)):
        log_path = Path.cwd() / 'logs'
        log_path.mkdir(parents=True, exist_ok=True)
        log_name = log_path / ('renamer_%s.log' % date.today().strftime('%Y%m%d'))
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s : %(levelname)-8s : %(message)s',
                            handlers=[
                                logging.FileHandler(str(log_name)),
                                logging.StreamHandler()
                            ])
        logging.info('Input directory `%s`', input_path)
        logging.info('Output directory `%s`', output_path)

        IMPORTED = True
        if cleanup:
            try:
                import ffmpeg
                from pymediainfo import MediaInfo
            except ImportError:
                IMPORTED = False
                logging.error('Required `ffmpeg-python` and `pymediainfo` for cleanup methods')

        OHASH = True
        if opensubtitle_hash:
            try:
                import oshash
            except ImportError:
                OHASH = False

        CONFIRM = False
        if confirm:
            CONFIRM = True

        CACHE = True
        try:
            import requests_cache
        except:
            CACHE = False

        if CACHE:
            requests_cache.install_cache(Path(__file__).stem)

        if IMPORTED:
            if not additional_info:
                FILE_NAME_FORMAT = FILE_NAME_FORMAT.split('~')[0].strip()
            logging.info('File Name Format `%s`', FILE_NAME_FORMAT)

            output_path.mkdir(parents=True, exist_ok=True)
            renamer = PhoenixAdultRenamer()
            try:
                renamer.run()
            except KeyboardInterrupt:
                renamer.stop()
    else:
        logging.error('`Output path` should\'t be in `Input path`')
