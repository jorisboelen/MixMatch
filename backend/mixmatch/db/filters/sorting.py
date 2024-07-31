from .enums import SortOrderEnum
from abc import ABC, abstractmethod
from mixmatch.db.models import Music, Playlist
from sqlalchemy.sql.expression import func
from sqlmodel import SQLModel
from sqlmodel.sql.expression import SelectOfScalar


class SortingFilter(ABC):
    def __init__(self, model: SQLModel, sort_by: str, sort_order: SortOrderEnum = SortOrderEnum.ASC):
        self.model = model
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.sort_field = self._get_sort_field()
        self.sort_functions = [self._get_sort_function()]
        self.additional_sort_functions()

    def _get_sort_field(self):
        if self.sort_by not in self.model.model_fields.keys():
            raise ValueError(f'Invalid key {self.sort_by} for object {self.model.__name__}')
        return getattr(self.model, self.sort_by)

    def _get_sort_function(self):
        if self.sort_order == SortOrderEnum.ASC:
            return self.sort_field.asc()
        else:
            return self.sort_field.desc()

    def apply_filter(self, statement: SelectOfScalar):
        return statement.order_by(*self.sort_functions)

    @abstractmethod
    def additional_sort_functions(self):
        pass


class MusicSortingFilter(SortingFilter):
    def additional_sort_functions(self):
        if self.sort_by == 'key':
            if self.sort_order == SortOrderEnum.ASC:
                self.sort_functions.insert(0, func.length(self.sort_field).asc())
            else:
                self.sort_functions.insert(0, func.length(self.sort_field).desc())


class PlaylistSortingFilter(SortingFilter):
    def additional_sort_functions(self):
        pass


def music_sort(statement: SelectOfScalar, sort_by: str, sort_order: SortOrderEnum = SortOrderEnum.ASC):
    return MusicSortingFilter(Music, sort_by, sort_order).apply_filter(statement)


def playlist_sort(statement: SelectOfScalar, sort_by: str, sort_order: SortOrderEnum = SortOrderEnum.ASC):
    return PlaylistSortingFilter(Playlist, sort_by, sort_order).apply_filter(statement)
