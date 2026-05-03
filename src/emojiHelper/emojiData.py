from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class EmojiData:
    codes: frozenset[str]
    category: str | None
    emoji: str
    name: str
    subCategory: str | None
