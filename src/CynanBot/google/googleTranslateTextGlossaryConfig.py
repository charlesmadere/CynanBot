from dataclasses import dataclass


@dataclass(frozen = True)
class GoogleTranslateTextGlossaryConfig():
    ignoreCase: bool
    glossary: str | None
