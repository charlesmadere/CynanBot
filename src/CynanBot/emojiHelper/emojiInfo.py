from dataclasses import dataclass


@dataclass(frozen = True)
class EmojiInfo():
    codes: set[str]
    category: str
    emoji: str
    name: str
    subCategory: str
