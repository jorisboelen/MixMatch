from abc import ABC, abstractmethod
from base64 import b64decode, b64encode
from json import loads
from mimetypes import guess_extension
from mixmatch.core.settings import settings
from mixmatch.core.utils import is_base64, is_json, round_bpm, MUSIC_KEYS, MUSIC_KEYS_CAMELOT
from mutagen import File as MutagenFile, MutagenError
from mutagen.flac import Picture as FlacPicture
from mutagen.id3 import APIC, PictureType, TALB, TBPM, TCON, TDRC, TIT2, TKEY, TPE1
from mutagen.mp3 import HeaderNotFoundError
from mutagen.mp4 import AtomDataType, MP4Cover
from os.path import basename, join
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4

import essentia
essentia.log.infoActive = False
essentia.log.warningActive = False
import essentia.standard as es


class MixMatchFileError(Exception):
    pass


class MixMatchFile(ABC):
    def __init__(self, path: str):
        self._mutagen_file: MutagenFile = MutagenFile(path, easy=False)
        self.path: str = path
        self.type: str = type(self._mutagen_file).__name__.lower()
        self.bitrate: int = self._mutagen_file.info.bitrate
        self.length: int = int(self._mutagen_file.info.length)
        self.cover: str | None = None
        self.artist: str | None = None
        self.title: str | None = None
        self.album: str | None = None
        self.genre: str | None = None
        self.date: str | None = None
        self.bpm: int | None = None
        self.key: str | None = None
        self.cover: str | None = None
        self._get_values_from_tags()
        self._process_values()

    def _calculate_bpm_key(self):
        features, features_frames = es.MusicExtractor(rhythmStats=['mean'], tonalStats=['mean'])(self.path)
        bpm = round_bpm(features['rhythm.bpm'])
        key = MUSIC_KEYS_CAMELOT.get(str(f'{features["tonal.key_edma.key"]} {features["tonal.key_edma.scale"]}'))
        return bpm, key

    def _get_mtime(self):
        return int(Path(self.path).stat().st_mtime)

    def _process_values(self):
        # make sure date is a string and not an ID3TimeStamp or similar
        if not isinstance(self.date, str):
            self.date = str(self.date)
        # if bpm is set, make sure the string representation of an int/float is cast to an integer
        if self.bpm and isinstance(self.bpm, str):
            self.bpm = int(float(self.bpm))
        # convert key if it is in mixed-in-key format
        if self.key and is_base64(self.key) and is_json(b64decode(self.key)):
            self.key = loads(b64decode(self.key)).get('key')
        # convert keys if they are in a different format
        if self.key in MUSIC_KEYS_CAMELOT.keys():
            self.key = MUSIC_KEYS_CAMELOT.get(self.key)
        # discard keys in incompatible format
        if self.key not in MUSIC_KEYS:
            self.key = ''
        # if key or bpm is not set, calculate the values
        if not self.key or not self.bpm:
            calc_bpm, calc_key = self._calculate_bpm_key()
            if not self.bpm:
                self.bpm = calc_bpm
            if not self.key:
                self.key = calc_key
            # update tags with calculated values
            self._update_music_data_in_tags()
            self._mutagen_file.save()

    @abstractmethod
    def _get_values_from_tags(self):
        pass

    @abstractmethod
    def _get_cover_data_from_tags(self):
        pass

    @abstractmethod
    def _update_cover_data_in_tags(self, cover_data: BinaryIO, cover_mime: str):
        pass

    @abstractmethod
    def _update_music_data_in_tags(self):
        pass

    def save_cover(self):
        cover_data, cover_mime = self._get_cover_data_from_tags()
        if cover_data and cover_mime:
            cover_file = open(join(settings.IMAGE_DIRECTORY, str(uuid4()) + guess_extension(cover_mime)), 'wb')
            cover_file.write(cover_data)
            cover_file.close()
            self.cover = basename(cover_file.name)

    def update_cover(self, cover_data: BinaryIO, cover_mime: str):
        self._update_cover_data_in_tags(cover_data, cover_mime)
        self.save_cover()
        return self._get_mtime()

    def update_music_data(self, music_data: dict):
        self.artist = music_data.get('artist', self.artist)
        self.title = music_data.get('title', self.title)
        self.album = music_data.get('album', self.album)
        self.genre = music_data.get('genre', self.genre)
        self._update_music_data_in_tags()
        self._mutagen_file.save()
        self.save_cover()
        return self._get_mtime()

    def to_dict(self):
        return {
            'path': self.path,
            'mtime': self._get_mtime(),
            'type': self.type,
            'bitrate': self.bitrate,
            'length': self.length,
            'artist': self.artist,
            'title': self.title,
            'album': self.album,
            'date': self.date,
            'bpm': self.bpm,
            'key': self.key,
            'cover': self.cover,
        }


class MixMatchFlacFile(MixMatchFile):
    def _get_values_from_tags(self):
        self.artist = next(iter(self._mutagen_file.tags.get('artist', [])), '')
        self.title = next(iter(self._mutagen_file.tags.get('title', [])), '')
        self.album = next(iter(self._mutagen_file.tags.get('album', [])), '')
        self.genre = next(iter(self._mutagen_file.tags.get('genre', [])), '')
        self.date = next(iter(self._mutagen_file.tags.get('date', [])), '')
        self.bpm = next(iter(self._mutagen_file.tags.get('bpm', [])), 0)
        self.key = next(iter(self._mutagen_file.tags.get('key', [])), '')

    def _get_cover_data_from_tags(self):
        if self._mutagen_file.pictures:
            return self._mutagen_file.pictures[0].data, self._mutagen_file.pictures[0].mime
        else:
            return None, None

    def _update_cover_data_in_tags(self, cover_data: BinaryIO, cover_mime: str):
        flac_picture = FlacPicture()
        flac_picture.type = PictureType.COVER_FRONT
        flac_picture.mime = cover_mime
        flac_picture.data = cover_data.read()
        self._mutagen_file.clear_pictures()
        self._mutagen_file.add_picture(flac_picture)
        self._mutagen_file.save()

    def _update_music_data_in_tags(self):
        self._mutagen_file.tags['ARTIST'] = self.artist
        self._mutagen_file.tags['TITLE'] = self.title
        self._mutagen_file.tags['ALBUM'] = self.album
        self._mutagen_file.tags['GENRE'] = self.genre
        self._mutagen_file.tags['DATE'] = self.date
        self._mutagen_file.tags['BPM'] = str(self.bpm)
        self._mutagen_file.tags['KEY'] = self.key


class MixMatchID3File(MixMatchFile):
    def _get_values_from_tags(self):
        self.artist = next(iter(self._mutagen_file.tags.get('TPE1', [])), '')
        self.title = next(iter(self._mutagen_file.tags.get('TIT2', [])), '')
        self.album = next(iter(self._mutagen_file.tags.get('TALB', [])), '')
        self.genre = next(iter(self._mutagen_file.tags.get('TCON', [])), '')
        self.date = next(iter(self._mutagen_file.tags.get('TDRC', [])), '')
        self.bpm = next(iter(self._mutagen_file.tags.get('TBPM', [])), 0)
        self.key = next(iter(self._mutagen_file.tags.get('TKEY', [])), '')

    def _get_cover_data_from_tags(self):
        if self._mutagen_file.tags.getall("APIC"):
            return self._mutagen_file.tags.getall("APIC")[0].data, self._mutagen_file.tags.getall("APIC")[0].mime
        else:
            return None, None

    def _update_cover_data_in_tags(self, cover_data: BinaryIO, cover_mime: str):
        if self._mutagen_file.tags.getall("APIC"):
            self._mutagen_file.tags.delall("APIC")
        self._mutagen_file.tags.add(APIC(mime=cover_mime,
                                         type=PictureType.COVER_FRONT,
                                         data=cover_data.read()))
        self._mutagen_file.save()

    def _update_music_data_in_tags(self):
        self._mutagen_file.tags['TPE1'] = TPE1(encoding=3, text=self.artist)
        self._mutagen_file.tags['TIT2'] = TIT2(encoding=3, text=self.title)
        self._mutagen_file.tags['TALB'] = TALB(encoding=3, text=self.album)
        self._mutagen_file.tags['TCON'] = TCON(encoding=3, text=self.genre)
        self._mutagen_file.tags['TDRC'] = TDRC(encoding=3, text=self.date)
        self._mutagen_file.tags['TBPM'] = TBPM(encoding=3, text=str(self.bpm))
        self._mutagen_file.tags['TKEY'] = TKEY(encoding=3, text=self.key)


class MixMatchMP4File(MixMatchFile):
    def _get_values_from_tags(self):
        self.artist = next(iter(self._mutagen_file.tags.get('©ART', [])), '')
        self.title = next(iter(self._mutagen_file.tags.get('©nam', [])), '')
        self.album = next(iter(self._mutagen_file.tags.get('©alb', [])), '')
        self.genre = next(iter(self._mutagen_file.tags.get('©gen', [])), '')
        self.date = next(iter(self._mutagen_file.tags.get('©day', [])), '')
        self.bpm = next(iter(self._mutagen_file.tags.get('tmpo', [])), 0)
        self.key = next(iter(self._mutagen_file.tags.get('----:com.apple.iTunes:initialkey', [])), b'').decode()

    def _get_cover_data_from_tags(self):
        if self._mutagen_file.tags.get('covr'):
            if self._mutagen_file.tags.get('covr')[0].imageformat == AtomDataType.JPEG:
                return self._mutagen_file.tags.get('covr')[0], "image/jpeg"
            elif self._mutagen_file.tags.get('covr')[0].imageformat == AtomDataType.PNG:
                return self._mutagen_file.tags.get('covr')[0], "image/png"
            else:
                return None, None
        else:
            return None, None

    def _update_cover_data_in_tags(self, cover_data: BinaryIO, cover_mime: str):
        self._mutagen_file['covr'] = [MP4Cover(cover_data.read(),
                                               imageformat=MP4Cover.FORMAT_JPEG if cover_mime == 'image/jpeg'
                                               else MP4Cover.FORMAT_PNG)]
        self._mutagen_file.save()

    def _update_music_data_in_tags(self):
        self._mutagen_file.tags['©ART'] = self.artist
        self._mutagen_file.tags['©nam'] = self.title
        self._mutagen_file.tags['©alb'] = self.album
        self._mutagen_file.tags['©gen'] = self.genre
        self._mutagen_file.tags['©day'] = self.date
        self._mutagen_file.tags['tmpo'] = [self.bpm]
        self._mutagen_file.tags['----:com.apple.iTunes:initialkey'] = self.key.encode()


def MusicFile(path: str) -> MixMatchFile:
    try:
        mutagen_file = MutagenFile(path, easy=False)
        if mutagen_file:
            music_file_type = type(mutagen_file).__name__.lower()
            if music_file_type == 'flac':
                return MixMatchFlacFile(path)
            elif music_file_type in ('aiff', 'mp3'):
                return MixMatchID3File(path)
            elif music_file_type == 'mp4':
                return MixMatchMP4File(path)
            else:
                raise MixMatchFileError(f'Unimplemented Filetype: {music_file_type} :: {path}')
        else:
            raise MixMatchFileError(f'Unsupported Filetype :: {path}')
    except HeaderNotFoundError:
        raise MixMatchFileError(f"Unable to Read Tags :: {path}")
    except (MutagenError, RuntimeError, FileNotFoundError):
        raise MixMatchFileError(f"Unable to Load :: {path}")
