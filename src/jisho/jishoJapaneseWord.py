from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class JishoJapaneseWord:
    reading: str | None
    word: str | None
