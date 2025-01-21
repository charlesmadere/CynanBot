from dataclasses import dataclass


@dataclass(frozen = True)
class EmojiInfo:
    codes: frozenset[str]
    category: str
    emoji: str
    name: str
    subCategory: str
