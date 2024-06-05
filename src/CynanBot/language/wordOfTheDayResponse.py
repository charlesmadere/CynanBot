from dataclasses import dataclass

from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.transparent.transparentResponse import TransparentResponse


@dataclass(frozen = True)
class WordOfTheDayResponse():
    languageEntry: LanguageEntry
    romaji: str | None
    transparentResponse: TransparentResponse
