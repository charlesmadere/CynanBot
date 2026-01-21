from dataclasses import dataclass

from ..languageEntry import LanguageEntry
from ...transparent.transparentResponse import TransparentResponse


@dataclass(frozen = True, slots = True)
class WordOfTheDayResponse:
    languageEntry: LanguageEntry
    romaji: str | None
    transparentResponse: TransparentResponse
