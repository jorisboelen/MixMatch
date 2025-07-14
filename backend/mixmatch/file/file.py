from abc import ABC, abstractmethod
from datetime import date as datetime_date
from mutagen import File as MutagenFile, FileType as MutagenFileType, MutagenError
from mutagen.flac import Picture as FlacPicture, FLAC
from mutagen.id3 import APIC, PictureType, TALB, TBPM, TCON, TDRC, TIT2, TKEY, TPE1
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.mp4 import AtomDataType, MP4, MP4Cover, MP4FreeForm
from pathlib import Path
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, FilePath, PositiveInt, computed_field, model_validator
from typing import Annotated, Any
from typing_extensions import Self
from .utils import calculate_bpm_key
from .validators import parse_bpm, parse_date, parse_key


class MixMatchFileError(Exception):
    pass


class MixMatchFileCover(BaseModel):
    data: bytes
    mime: str
    type: int = PictureType.COVER_FRONT


class MixMatchFile(BaseModel, ABC):
    model_config = ConfigDict(strict=True, validate_assignment=True)
    file_path: FilePath = Field(exclude=True)
    type: str = Field(default='')
    bitrate: int = Field(ge=0, default=0)
    length: int = Field(ge=0, default=0)
    artist_list: list[str] = Field(default=[], exclude=True)
    title_list: list[str] = Field(default=[], exclude=True)
    album_list: list[str] = Field(default=[], exclude=True)
    genre_list: list[str] = Field(default=[], exclude=True)
    date_list: Annotated[list[datetime_date], BeforeValidator(parse_date)] = Field(default=[], exclude=True)
    bpm_list: Annotated[list[PositiveInt], BeforeValidator(parse_bpm)] = Field(default=[], exclude=True)
    key_list: Annotated[list[str], BeforeValidator(parse_key)] = Field(default=[], exclude=True)
    cover_list: list[MixMatchFileCover] = Field(default=[], exclude=True)

    @computed_field
    @property
    def path(self) -> str:
        return str(self.file_path)

    @computed_field
    @property
    def mtime(self) -> int:
        return int(Path(self.file_path).stat().st_mtime)

    @computed_field
    @property
    def artist(self) -> str:
        return next(iter(self.artist_list), '')

    @artist.setter
    def artist(self, value: str):
        self.artist_list.pop(0)
        self.artist_list.insert(0, value)

    @computed_field
    @property
    def title(self) -> str:
        return next(iter(self.title_list), '')

    @title.setter
    def title(self, value: str):
        self.title_list.pop(0)
        self.title_list.insert(0, value)

    @computed_field
    @property
    def album(self) -> str:
        return next(iter(self.album_list), '')

    @album.setter
    def album(self, value: str):
        self.album_list.pop(0)
        self.album_list.insert(0, value)

    @computed_field
    @property
    def genre(self) -> str:
        return next(iter(self.genre_list), '')

    @genre.setter
    def genre(self, value: str):
        self.genre_list.pop(0)
        self.genre_list.insert(0, value)

    @computed_field
    @property
    def date(self) -> datetime_date | None:
        return next(iter(self.date_list), None)

    @date.setter
    def date(self, value: datetime_date):
        self.date_list.pop(0)
        self.date_list.insert(0, value)

    @computed_field
    @property
    def bpm(self) -> PositiveInt | None:
        return next(iter(self.bpm_list), None)

    @bpm.setter
    def bpm(self, value: int):
        self.bpm_list.pop(0)
        self.bpm_list.insert(0, value)

    @computed_field
    @property
    def key(self) -> str | None:
        return next(iter(self.key_list), None)

    @key.setter
    def key(self, value: str):
        self.key_list.pop(0)
        self.key_list.insert(0, value)

    @computed_field
    @property
    def cover(self) -> MixMatchFileCover | None:
        return next(iter([c for c in self.cover_list if c.type == PictureType.COVER_FRONT]), None)

    @cover.setter
    def cover(self, value: MixMatchFileCover):
        self.cover_list = [c for c in self.cover_list if c.type != PictureType.COVER_FRONT]
        self.cover_list.insert(0, value)

    @model_validator(mode='before')
    @classmethod
    def _init_data(cls, data: Any) -> Any:
        mutagen_file: MutagenFileType = MutagenFile(data.get('file_path'), easy=False)
        data['type'] = type(mutagen_file).__name__.lower()
        data['bitrate'] = int(mutagen_file.info.bitrate)
        data['length'] = int(mutagen_file.info.length)
        data = cls._get_values_from_tags(data, mutagen_file)
        return data

    @model_validator(mode='after')
    def _check_bpm_key(self) -> Self:
        if not self.bpm or not self.key:
            bpm, key = calculate_bpm_key(path=self.file_path)
            if not self.bpm:
                self.bpm_list.insert(0, bpm)
            if not self.key:
                self.key_list.insert(0, key)
            self._set_values_in_tags()
        return self

    @classmethod
    @abstractmethod
    def _get_values_from_tags(cls, data: Any, mutagen_file: MutagenFileType) -> Any:
        pass

    @abstractmethod
    def _set_values_in_tags(self):
        pass

    def save(self):
        self._set_values_in_tags()


class MixMatchFlacFile(MixMatchFile):
    @classmethod
    def _get_values_from_tags(cls, data: Any, mutagen_file: FLAC):
        data['artist_list'] = mutagen_file.tags.get('artist', [])
        data['title_list'] = mutagen_file.tags.get('title', [])
        data['album_list'] = mutagen_file.tags.get('album', [])
        data['genre_list'] = mutagen_file.tags.get('genre', [])
        data['date_list'] = parse_date(mutagen_file.tags.get('date', []))
        data['bpm_list'] = parse_bpm(mutagen_file.tags.get('bpm', []))
        data['key_list'] = parse_key(mutagen_file.tags.get('key', []))
        data['cover_list'] = [MixMatchFileCover(data=p.data, mime=p.mime, type=p.type) for p in mutagen_file.pictures]
        return data

    def _set_values_in_tags(self):
        def save_cover_pictures():
            mutagen_file.clear_pictures()
            for cover in self.cover_list:
                flac_picture = FlacPicture()
                flac_picture.mime = cover.mime
                flac_picture.type = cover.type
                flac_picture.data = cover.data
                mutagen_file.add_picture(flac_picture)

        mutagen_file: FLAC = FLAC(self.file_path)
        mutagen_file.tags['ARTIST'] = self.artist_list
        mutagen_file.tags['TITLE'] = self.title_list
        mutagen_file.tags['ALBUM'] = self.album_list
        mutagen_file.tags['GENRE'] = self.genre_list
        mutagen_file.tags['DATE'] = [d.strftime('%Y-%m-%d') for d in self.date_list]
        mutagen_file.tags['BPM'] = [str(b) for b in self.bpm_list]
        mutagen_file.tags['KEY'] = self.key_list
        save_cover_pictures()
        mutagen_file.save()


class MixMatchID3File(MixMatchFile):
    @classmethod
    def _get_values_from_tags(cls, data: Any, mutagen_file: MP3):
        data['artist_list'] = list(mutagen_file.tags.get('TPE1', []))
        data['title_list'] = list(mutagen_file.tags.get('TIT2', []))
        data['album_list'] = list(mutagen_file.tags.get('TALB', []))
        data['genre_list'] = list(mutagen_file.tags.get('TCON', []))
        data['date_list'] = list(parse_date(mutagen_file.tags.getall('TDRC')))
        data['bpm_list'] = list(parse_bpm(mutagen_file.tags.get('TBPM', [])))
        data['key_list'] = list(parse_key(mutagen_file.tags.get('TKEY', [])))
        data['cover_list'] = [MixMatchFileCover(data=p.data, mime=p.mime, type=p.type) for p in mutagen_file.tags.getall('APIC')]
        return data

    def _set_values_in_tags(self):
        mutagen_file: MP3 = MP3(self.file_path)
        mutagen_file.tags.setall('TPE1', [TPE1(encoding=3, text=self.artist_list)])
        mutagen_file.tags.setall('TIT2', [TIT2(encoding=3, text=self.title_list)])
        mutagen_file.tags.setall('TALB', [TALB(encoding=3, text=self.album_list)])
        mutagen_file.tags.setall('TCON', [TCON(encoding=3, text=self.genre_list)])
        mutagen_file.tags.setall('TDRC', [TDRC(encoding=3, text=[d.strftime('%Y-%m-%d') for d in self.date_list])])
        mutagen_file.tags.setall('TBPM', [TBPM(encoding=3, text=[str(b) for b in self.bpm_list])])
        mutagen_file.tags.setall('TKEY', [TKEY(encoding=3, text=self.key_list)])
        mutagen_file.tags.setall('APIC', [APIC(mime=c.mime, type=c.type, data=c.data) for c in self.cover_list])
        mutagen_file.save()


class MixMatchMP4File(MixMatchFile):
    @classmethod
    def _get_values_from_tags(cls, data: Any, mutagen_file: MP4):
        data['artist_list'] = list(mutagen_file.tags.get('©ART', []))
        data['title_list'] = list(mutagen_file.tags.get('©nam', []))
        data['album_list'] = list(mutagen_file.tags.get('©alb', []))
        data['genre_list'] = list(mutagen_file.tags.get('©gen', []))
        data['date_list'] = list(parse_date(mutagen_file.tags.get('©day', [])))
        data['bpm_list'] = list(parse_bpm(mutagen_file.tags.get('tmpo', [])))
        data['key_list'] = list(parse_key([k.decode() for k in
                                           mutagen_file.tags.get('----:com.apple.iTunes:initialkey', [])]))
        data['cover_list'] = [MixMatchFileCover(data=p, type=PictureType.COVER_FRONT,
                                                mime='image/jpeg' if p.imageformat == AtomDataType.JPEG
                                                else 'image/png') for p in mutagen_file.tags.get('covr')]
        return data

    def _set_values_in_tags(self):
        mutagen_file: MP4 = MP4(self.file_path)
        mutagen_file.tags['©ART'] = self.artist_list
        mutagen_file.tags['©nam'] = self.title_list
        mutagen_file.tags['©alb'] = self.album_list
        mutagen_file.tags['©gen'] = self.genre_list
        mutagen_file.tags['©day'] = [d.strftime('%Y-%m-%d') for d in self.date_list]
        mutagen_file.tags['tmpo'] = self.bpm_list
        mutagen_file.tags['----:com.apple.iTunes:initialkey'] = [MP4FreeForm(k.encode(), AtomDataType.UTF8)
                                                                 for k in self.key_list]
        mutagen_file.tags['covr'] = [MP4Cover(c.data, imageformat=MP4Cover.FORMAT_JPEG if c.mime == 'image/jpeg' else MP4Cover.FORMAT_PNG)
                                     for c in self.cover_list]
        mutagen_file.save()


def mixmatch_file(file_path: FilePath) -> MixMatchFile:
    try:
        mutagen_file = MutagenFile(file_path, easy=False)
        if mutagen_file:
            music_file_type = type(mutagen_file).__name__.lower()
            if music_file_type == 'flac':
                return MixMatchFlacFile(file_path=file_path)
            elif music_file_type in ('aiff', 'mp3'):
                return MixMatchID3File(file_path=file_path)
            elif music_file_type == 'mp4':
                return MixMatchMP4File(file_path=file_path)
            else:
                raise MixMatchFileError(f'Unimplemented Filetype: {music_file_type} :: {file_path}')
        else:
            raise MixMatchFileError(f'Unsupported Filetype :: {file_path}')
    except HeaderNotFoundError:
        raise MixMatchFileError(f"Unable to Read Tags :: {file_path}")
    except (MutagenError, RuntimeError):
        raise MixMatchFileError(f"Unable to Load :: {file_path}")
    except FileNotFoundError:
        raise MixMatchFileError(f"File not found :: {file_path}")
