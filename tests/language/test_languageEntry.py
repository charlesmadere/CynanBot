from typing import Collection

import src.misc.utils as utils
from src.language.languageEntry import LanguageEntry


class TestLanguageEntry:

    def test_commandNames_withAll(self):
        allCommandNames: list[Collection[str]] = list()

        for languageEntry in LanguageEntry:
            commandNames = languageEntry.commandNames
            assert len(commandNames) >= 1

            allCommandNames.append(commandNames)

            for commandName in commandNames:
                assert utils.isValidStr(commandName)

        assert len(allCommandNames) == len(LanguageEntry)

    def test_flag_withAll(self):
        allFlags: list[str] = list()

        for languageEntry in LanguageEntry:
            allFlags.append(languageEntry.flag)

        assert len(allFlags) == len(LanguageEntry)

    def test_humanName_withAll(self):
        for languageEntry in LanguageEntry:
            humanName = languageEntry.humanName
            assert utils.isValidStr(humanName)

    def test_humanName_withChinese(self):
        humanName = LanguageEntry.CHINESE.humanName
        assert humanName == 'Chinese'

    def test_humanName_withDutch(self):
        humanName = LanguageEntry.DUTCH.humanName
        assert humanName == 'Dutch'

    def test_humanName_withEnglish(self):
        humanName = LanguageEntry.ENGLISH.humanName
        assert humanName == 'English'

    def test_humanName_withEnglishForPortugueseSpeakers(self):
        humanName = LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS.humanName
        assert humanName == 'English for Portuguese speakers'

    def test_humanName_withEnglishForSpanishSpeakers(self):
        humanName = LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS.humanName
        assert humanName == 'English for Spanish speakers'

    def test_humanName_withFinnish(self):
        humanName = LanguageEntry.FINNISH.humanName
        assert humanName == 'Finnish'

    def test_humanName_withFrench(self):
        humanName = LanguageEntry.FRENCH.humanName
        assert humanName == 'French'

    def test_humanName_withGerman(self):
        humanName = LanguageEntry.GERMAN.humanName
        assert humanName == 'German'

    def test_humanName_withGreek(self):
        humanName = LanguageEntry.GREEK.humanName
        assert humanName == 'Greek'

    def test_humanName_withHindi(self):
        humanName = LanguageEntry.HINDI.humanName
        assert humanName == 'Hindi'

    def test_humanName_withItalian(self):
        humanName = LanguageEntry.ITALIAN.humanName
        assert humanName == 'Italian'

    def test_humanName_withJapanese(self):
        humanName = LanguageEntry.JAPANESE.humanName
        assert humanName == 'Japanese'

    def test_humanName_withKorean(self):
        humanName = LanguageEntry.KOREAN.humanName
        assert humanName == 'Korean'

    def test_humanName_withLatin(self):
        humanName = LanguageEntry.LATIN.humanName
        assert humanName == 'Latin'

    def test_humanName_withNorwegian(self):
        humanName = LanguageEntry.NORWEGIAN.humanName
        assert humanName == 'Norwegian'

    def test_humanName_withPolish(self):
        humanName = LanguageEntry.POLISH.humanName
        assert humanName == 'Polish'

    def test_humanName_withPortuguese(self):
        humanName = LanguageEntry.PORTUGUESE.humanName
        assert humanName == 'Portuguese'

    def test_humanName_withRussian(self):
        humanName = LanguageEntry.RUSSIAN.humanName
        assert humanName == 'Russian'

    def test_humanName_withSpanish(self):
        humanName = LanguageEntry.SPANISH.humanName
        assert humanName == 'Spanish'

    def test_humanName_withSwedish(self):
        humanName = LanguageEntry.SWEDISH.humanName
        assert humanName == 'Swedish'

    def test_humanName_withThai(self):
        humanName = LanguageEntry.THAI.humanName
        assert humanName == 'Thai'

    def test_humanName_withUrdu(self):
        humanName = LanguageEntry.URDU.humanName
        assert humanName == 'Urdu'

    def test_primaryCommandName_withAll(self):
        primaryCommandNames: set[str] = set()

        for languageEntry in LanguageEntry:
            primaryCommandNames.add(languageEntry.primaryCommandName)

        assert len(primaryCommandNames) == len(LanguageEntry)

    def test_wotdApiCode_withAll(self):
        wotdApiCodes: list[str | None] = list()

        for languageEntry in LanguageEntry:
            wotdApiCodes.append(languageEntry.wotdApiCode)

        assert len(wotdApiCodes) == len(LanguageEntry)
