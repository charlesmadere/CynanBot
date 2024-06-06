from dataclasses import dataclass

from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig


@dataclass(frozen = True)
class GoogleTranslation():
    glossaryConfig: GoogleTranslateTextGlossaryConfig | None
    detectedLanguageCode: str | None
    model: str | None
    translatedText: str | None
