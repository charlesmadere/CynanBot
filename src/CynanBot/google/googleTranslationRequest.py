from dataclasses import dataclass

from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig
from CynanBot.google.googleTranslateTextTransliterationConfig import \
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
