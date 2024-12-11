from dataclasses import dataclass


@dataclass(frozen = True)
class GoogleTranslateTextTransliterationConfig:
    enableTransliteration: bool
