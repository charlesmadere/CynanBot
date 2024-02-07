from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.wordOfTheDayResponse import WordOfTheDayResponse


def test_toStr_no_romaji() -> None:
    # TODO: Why is LanguagesRepository.__getLanguageEntries async? It doesn't look like it's awaiting anything.
    # making new LanguageEntry here instead of getting it from repo

    english = LanguageEntry(
        commandNames = [ 'en', 'eng', 'english', '英語' ],
        flag = '🇬🇧',
        iso6391Code = 'en',
        name = 'English'
    )
    res = WordOfTheDayResponse(english, "def", None, None, "ay bee see", "abc")
    assert res.toStr() == "🇬🇧 English — abc (ay bee see) — def"


def test_toStr_with_romaji() -> None:
    japanese = LanguageEntry(
        commandNames = [ 'ja', 'japan', 'japanese', 'jp', '日本語', 'にほんご' ],
        flag = '🇯🇵',
        iso6391Code = 'ja',
        name = 'Japanese',
        wotdApiCode = 'ja'
    )
    res = WordOfTheDayResponse(
        japanese,
        "a fresh start, a clean start, turning over a new leaf",
        "Because spring has come, let's make a fresh start and do our best.",
        "もう春ですから、心機一転、頑張りましょう。",
        "しんきいってん",
        "心機一転"
    )
    assert res.toStr() == (
        "🇯🇵 Japanese — 心機一転 (しんきいってん - shinkiitten) — "
        "a fresh start, a clean start, turning over a new leaf. "
        "Example: もう春ですから、心機一転、頑張りましょう。 "
        "Because spring has come, let's make a fresh start and do our best."
    )
