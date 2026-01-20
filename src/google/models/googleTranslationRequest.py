from dataclasses import dataclass

from frozenlist import FrozenList

from .googleTranslateTextGlossaryConfig import GoogleTranslateTextGlossaryConfig
from .googleTranslateTextTransliterationConfig import GoogleTranslateTextTransliterationConfig


@dataclass(frozen = True, slots = True)
class GoogleTranslationRequest:
    contents: FrozenList[str]
    glossaryConfig: GoogleTranslateTextGlossaryConfig | None
    transliterationConfig: GoogleTranslateTextTransliterationConfig | None
    mimeType: str
    model: str | None
    sourceLanguageCode: str | None
    targetLanguageCode: str
