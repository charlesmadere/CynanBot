from dataclasses import dataclass

from CynanBot.google.googleTranslation import GoogleTranslation


@dataclass(frozen = True)
class GoogleTranslateTextResponse():
    glossaryTranslations: list[GoogleTranslation] | None = None
    translations: list[GoogleTranslation] | None = None
