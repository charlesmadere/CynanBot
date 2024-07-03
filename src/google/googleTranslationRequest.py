from dataclasses import dataclass

from .googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig
from .googleTranslateTextTransliterationConfig import \
    GoogleTranslateTextTransliterationConfig


@dataclass(frozen = True)
class GoogleTranslationRequest():
    glossaryConfig: GoogleTranslateTextGlossaryConfig | None
    transliterationConfig: GoogleTranslateTextTransliterationConfig | None
    contents: list[str]
    mimeType: str
    model: str | None
    sourceLanguageCode: str | None
    targetLanguageCode: str
