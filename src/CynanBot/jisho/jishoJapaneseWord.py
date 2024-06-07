from dataclasses import dataclass


@dataclass(frozen = True)
class JishoJapaneseWord():
    reading: str
    word: str
