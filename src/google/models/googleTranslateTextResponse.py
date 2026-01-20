from dataclasses import dataclass

from frozenlist import FrozenList

from .googleTranslation import GoogleTranslation


@dataclass(frozen = True, slots = True)
class GoogleTranslateTextResponse:
    glossaryTranslations: FrozenList[GoogleTranslation] | None = None
    translations: FrozenList[GoogleTranslation] | None = None
