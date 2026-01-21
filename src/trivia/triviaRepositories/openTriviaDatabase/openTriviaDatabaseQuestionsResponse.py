from dataclasses import dataclass

from frozenlist import FrozenList

from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseResponseCode import OpenTriviaDatabaseResponseCode


@dataclass(frozen = True, slots = True)
class OpenTriviaDatabaseQuestionsResponse:
    results: FrozenList[OpenTriviaDatabaseQuestion] | None
    responseCode: OpenTriviaDatabaseResponseCode
