from datetime import datetime
from enum import Enum
from mixmatch.db.filters.enums import SortOrderEnum
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel


class GenreBase(SQLModel):
    name: str = Field(max_length=50, unique=True)


class Genre(GenreBase, table=True):
    __tablename__ = "genres"
    id: int | None = Field(default=None, primary_key=True)
    tracks: list["Track"] = Relationship(back_populates="genre")


class GenreCreate(GenreBase):
    pass


class GenreRead(GenreBase):
    id: int


class TrackBase(SQLModel):
    path: str = Field(max_length=4096, index=True, unique=True)
    mtime: int
    type: str = Field(max_length=4)
    bitrate: int
    length: int
    artist: str | None = Field(default=None, max_length=200)
    title: str | None = Field(default=None, max_length=200)
    album: str | None = Field(default=None, max_length=200)
    date: str | None = Field(default=None, max_length=10)
    bpm: int
    key: str = Field(max_length=3)
    rating: int = Field(default=0, ge=0, le=5)
    cover: str | None = Field(default=None, max_length=4096)


class Track(TrackBase, table=True):
    __tablename__ = "tracks"
    id: int | None = Field(default=None, primary_key=True)
    genre_id: int | None = Field(default=None, foreign_key="genres.id")
    genre: Genre | None = Relationship(back_populates="tracks")
    playlist_items: list["PlaylistItem"] = Relationship(sa_relationship_kwargs={"cascade": "delete"},
                                                        back_populates="track")


class TrackUpdate(SQLModel):
    artist: str | None = Field(default=None, max_length=200)
    title: str | None = Field(default=None, max_length=200)
    album: str | None = Field(default=None, max_length=200)
    genre_id: int | None = Field(default=None, foreign_key="genres.id")
    date: str | None = Field(default=None, max_length=10)
    rating: int = Field(default=0, ge=0, le=5)


class TrackRead(TrackBase):
    id: int
    genre: GenreRead | None


class TrackSearchQuerySortByEnum(str, Enum):
    DEFAULT = ""
    MTIME = "mtime"
    ARTIST = "artist"
    TITLE = "title"
    DATE = "date"
    BPM = "bpm"
    KEY = "key"
    RATING = "rating"


class TrackSearchQuery(SQLModel):
    artist: str | None = None
    title: str | None = None
    genre_id: int | None = None
    year_lowest: str | None = None
    year_highest: str | None = None
    bpm_lowest: int | None = None
    bpm_highest: int | None = None
    key: list[str] | None = None
    include_compatible_keys: bool | None = None
    rating_lowest: int | None = None
    rating_highest: int | None = None
    random: bool | None = False
    sort_by: TrackSearchQuerySortByEnum | None = None
    sort_order: SortOrderEnum | None = None


class PlaylistBase(SQLModel):
    name: str = Field(max_length=100)
    created: datetime | None = Field(default=None, index=True, nullable=False,
                                     sa_column_kwargs={"server_default": func.now()})
    modified: datetime | None = Field(default=None, index=True, nullable=False,
                                      sa_column_kwargs={"server_default": func.now()})


class Playlist(PlaylistBase, table=True):
    __tablename__ = "playlists"
    id: int | None = Field(default=None, primary_key=True)
    owner_username: str | None = Field(default=None, foreign_key="users.username")
    owner: "User" = Relationship(back_populates="playlists")
    playlist_items: list["PlaylistItem"] = Relationship(back_populates="playlist",
                                                        sa_relationship_kwargs={"cascade": "delete",
                                                                                "order_by": "PlaylistItem.order"})


class PlaylistCreate(SQLModel):
    name: str = Field(max_length=100)


class PlaylistUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=100)


class PlaylistRead(PlaylistBase):
    id: int
    playlist_items: list["PlaylistItemRead"]


class PlaylistSearchQuerySortByEnum(str, Enum):
    DEFAULT = ""
    NAME = "name"
    CREATED = "created"
    MODIFIED = "modified"


class PlaylistSearchQuery(SQLModel):
    name: str | None = None
    sort_by: PlaylistSearchQuerySortByEnum | None = None
    sort_order: SortOrderEnum | None = None


class PlaylistItemBase(SQLModel):
    order: int = Field(default=0, ge=0, le=999)


class PlaylistItem(PlaylistItemBase, table=True):
    __tablename__ = "playlist_items"
    id: int | None = Field(default=None, primary_key=True)
    playlist_id: int | None = Field(foreign_key="playlists.id")
    playlist: Playlist = Relationship(back_populates="playlist_items")
    track_id: int | None = Field(foreign_key="tracks.id")
    track: Track = Relationship(back_populates="playlist_items")


class PlaylistItemCreate(PlaylistItemBase):
    playlist_id: int
    track_id: int


class PlaylistItemRead(PlaylistItemBase):
    id: int
    track: TrackRead


class PlaylistItemUpdate(PlaylistItemBase):
    pass


class TaskBase(SQLModel):
    id: str = Field(primary_key=True, max_length=50)
    name: str = Field(nullable=False)


class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    results: list["TaskResult"] = Relationship(back_populates="task",
                                               sa_relationship_kwargs={"order_by": "desc(TaskResult.started)"})


class TaskRead(TaskBase):
    results: list["TaskResultRead"]


class TaskResultBase(SQLModel):
    id: str = Field(primary_key=True, max_length=36)
    state: str = Field(nullable=False)
    result: str | None = Field(default=None)
    started: datetime | None = Field(default=None)
    completed: datetime | None = Field(default=None)


class TaskResult(TaskResultBase, table=True):
    __tablename__ = "task_results"
    task_id: str = Field(foreign_key="tasks.id")
    task: Task = Relationship(back_populates="results")


class TaskResultRead(TaskResultBase):
    pass


class TaskResultWithTaskRead(TaskResultBase):
    task: Task


class UserBase(SQLModel):
    username: str = Field(primary_key=True)
    is_admin: bool = Field(nullable=False)


class User(UserBase, table=True):
    __tablename__ = "users"
    password: str = Field(nullable=False)
    playlists: list[Playlist] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "delete"})


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    is_admin: bool | None = None
    password: str | None = None


class UserCurrentUpdate(SQLModel):
    password: str | None = None


class UserLogin(SQLModel):
    username: str
    password: str


class UserSession(SQLModel, table=True):
    __tablename__ = "user_sessions"
    token: str = Field(primary_key=True, max_length=64)
    username: str = Field(foreign_key="users.username")
    expires: datetime = Field(index=True)
