from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class GoogleTranslateTextTransliterationConfig:
    enableTransliteration: bool
