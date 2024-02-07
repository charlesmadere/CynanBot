from CynanBot.language.kana2ascii import kana2ascii
from CynanBot.language.romaji import is_kana, to_romaji

shinkiitten = "しんきいってん"


def test_is_kana() -> None:
    assert not is_kana("abc")
    assert is_kana(shinkiitten), f"{[c in kana2ascii for c in shinkiitten]}"
    assert not is_kana("")
    assert not is_kana(None)


def test_to_romaji() -> None:
    assert to_romaji(shinkiitten) == "shinkiitten"
    assert to_romaji("する") == "suru"
    assert to_romaji("ょ") == "o"

    assert to_romaji("きょ") == "kyo"
    assert to_romaji("ショ") == "sho"
    assert to_romaji("ちゃ") == "cha"
    assert to_romaji("ニャ") == "nya"
    assert to_romaji("ひゅ") == "hyu"
    assert to_romaji("ミュ") == "myu"
    assert to_romaji("りゅ") == "ryu"
    assert to_romaji("ヰャ") == "iya"
    assert to_romaji("ギョ") == "gyo"
    assert to_romaji("ぢゅ") == "ju"

    assert to_romaji("abc") is None
    assert to_romaji(" ") is None
    assert to_romaji("") is None
    assert to_romaji(None) is None
    assert to_romaji("結婚") is None
