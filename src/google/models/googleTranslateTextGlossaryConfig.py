from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class GoogleTranslateTextGlossaryConfig:
    ignoreCase: bool
    glossary: str | None
