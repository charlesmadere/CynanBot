from dataclasses import dataclass


@dataclass(frozen = True)
class JishoJapaneseWord:
    reading: str | None
    word: str | None
