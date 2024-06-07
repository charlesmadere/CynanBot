from dataclasses import dataclass


@dataclass(frozen = True)
class JishoSense():
    englishDefinitions: list[str]
    partsOfSpech: list[str]
    tags: list[str] | None
