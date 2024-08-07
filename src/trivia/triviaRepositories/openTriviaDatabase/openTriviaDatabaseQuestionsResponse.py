from dataclasses import dataclass

from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseResponseCode import OpenTriviaDatabaseResponseCode


@dataclass(frozen = True)
class OpenTriviaDatabaseQuestionsResponse:
    results: list[OpenTriviaDatabaseQuestion] | None
    responseCode: OpenTriviaDatabaseResponseCode
