from typing_extensions import TypeGuard

from .kana2ascii import kana2ascii
from ..misc.utils import isValidStr


def is_kana(string: str | None) -> TypeGuard[str]:
    """ is a non-empty string that is all hiragana or katakana """
    return isValidStr(string) and all(c in kana2ascii for c in string)


def to_romaji(word: str | None) -> str | None:
    """ take a string that is all hiragana or katakana and return romaji """
    if not is_kana(word):
        return None

    build_return: list[str] = []
    for c in word:
        build_return.append(kana2ascii[c])
    out = "".join(build_return)

    out = out.replace("`^*^", "y")
    out = out.replace("~^*^", "")
    out = out.replace("&^*^", "y")
    out = out.replace("`^", "i")
    out = out.replace("~^", "i")
    out = out.replace("&^", "")
    out = out.replace("*^", "")

    return out
