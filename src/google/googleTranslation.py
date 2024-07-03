from dataclasses import dataclass

from .googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig


@dataclass(frozen = True)
class GoogleTranslation():
    glossaryConfig: GoogleTranslateTextGlossaryConfig | None
    detectedLanguageCode: str | None
    model: str | None
    translatedText: str | None
