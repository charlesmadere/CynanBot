from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchCategoryOrGameEntry import TwitchCategoryOrGameEntry
from .twitchPaginationResponse import TwitchPaginationResponse


@dataclass(frozen = True, slots = True)
class TwitchSearchCategoriesResponse:
    data: FrozenList[TwitchCategoryOrGameEntry]
    pagination: TwitchPaginationResponse | None
