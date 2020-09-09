#!/usr/bin/python3

import time
from datetime import date
import re
from pathlib import Path
import argparse
import logging

import requests
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

FILE_NAME_FORMAT = '{site} - {date} - {title} ~ {actors}'
EXTENSIONS = (
    '.mp4', '.mkv', '.avi', '.wmv'
)
MINIMAL_FILE_SIZE = 15728640
TRASH_TITLE = (
    'RARBG', 'COM', r'\d{3,4}x\d{3,4}', 'HEVC', 'H265', 'AVC', r'\dK',
    r'\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4', 'KLEENEX', 'SD', 'HD', 'rq'
)


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


def work_with_file(file_path):
    if file_path.suffix in EXTENSIONS and file_path.stat().st_size > MINIMAL_FILE_SIZE:
        logging.info('Working with `%s`', ''.join(file_path.name))
        data = get_data_from_api(get_clean_str(file_path.name, True))
        if data:
            new_file_name = get_new_file_name(data)
            new_file_name = output_path / (new_file_name + file_path.suffix)

            if not new_file_name.is_file():
                title_clean = True
                if cleanup:
                    title = get_title_from_metadata(file_path)
                    if title:
                        title_clean = False

                if cleanup and not title_clean:
                    cleanup_metadata(file_path, new_file_name)
                else:
                    file_path.rename(new_file_name)
                logging.info('Saving as `%s`', new_file_name.name)
            else:
                logging.error('Already exist `%s`', new_file_name.name)
        else:
            logging.info('Nothing found')


def get_new_file_name(data):
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


def get_data_from_api(file_name):
    logging.info('Searching `%s`', file_name)
    response = requests.get('https://api.metadataapi.net/scenes', headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }, params={
        'parse': file_name,
        'limit': 1
    })

    data = response.json()
    if data and 'data' in data and data['data']:
        return data['data'][0]

    return None


def get_title_from_metadata(file_name):
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


def get_clean_str(title, delete_trash=False):
    title = re.sub(r'[\'\"]', '', title)
    title = re.sub(r'(?:\W|[_])', ' ', title)

    if delete_trash:
        for trash in TRASH_TITLE:
            title = re.sub(r'\b%s\b' % trash, '', title, flags=re.IGNORECASE)

    title = ' '.join(title.split())

    return title


def searching_all_files(directory: Path):
    return [file for file in directory.rglob('*.*') if file.is_file()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Watchdog Adult Renamer.')
    parser.add_argument('-i', '--input_path', required=True, help='Directory to watch files')
    parser.add_argument('-o', '--output_path', required=True, help='Directory to store renamed files')
    parser.add_argument('-c', '--cleanup', action='store_true', help='Remove metadata title from file')
    parser.add_argument('-a', '--additional_info', action='store_true', help='Add additional info to filename')

    args = parser.parse_args()
    input_path = Path(args.input_path).resolve()
    output_path = Path(args.output_path).resolve()
    cleanup = args.cleanup
    additional_info = args.additional_info
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
