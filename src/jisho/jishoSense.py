from dataclasses import dataclass


@dataclass(frozen = True)
class JishoSense():
    englishDefinitions: list[str]
    partsOfSpeech: list[str] | None
    tags: list[str] | None
