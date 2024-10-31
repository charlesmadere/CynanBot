from src.language.languageEntry import LanguageEntry
import src.misc.utils as utils


class TestLanguageEntry:

    def test_name(self):
        for languageEntry in LanguageEntry:
            assert utils.isValidStr(languageEntry.name)

    def test_name_withChinese(self):
        name = LanguageEntry.CHINESE.name
        assert name == 'Chinese'

    def test_name_withDutch(self):
        name = LanguageEntry.DUTCH.name
        assert name == 'Dutch'

    def test_name_withEnglish(self):
        name = LanguageEntry.ENGLISH.name
        assert name == 'English'

    def test_name_withEnglishForPortugueseSpeakers(self):
        name = LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS.name
        assert name == 'English for Portuguese speakers'

    def test_name_withEnglishForSpanishSpeakers(self):
        name = LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS.name
        assert name == 'English for Spanish speakers'

    def test_name_withFrench(self):
        name = LanguageEntry.FRENCH.name
        assert name == 'French'

    def test_name_withGerman(self):
        name = LanguageEntry.GERMAN.name
        assert name == 'German'

    def test_name_withGreek(self):
        name = LanguageEntry.GREEK.name
        assert name == 'Greek'

    def test_name_withHindi(self):
        name = LanguageEntry.HINDI.name
        assert name == 'Hindi'

    def test_name_withItalian(self):
        name = LanguageEntry.ITALIAN.name
        assert name == 'Italian'

    def test_name_withJapanese(self):
        name = LanguageEntry.JAPANESE.name
        assert name == 'Japanese'

    def test_name_withKorean(self):
        name = LanguageEntry.KOREAN.name
        assert name == 'Korean'

    def test_name_withLatin(self):
        name = LanguageEntry.LATIN.name
        assert name == 'Latin'

    def test_name_withNorwegian(self):
        name = LanguageEntry.NORWEGIAN.name
        assert name == 'Norwegian'

    def test_name_withPolish(self):
        name = LanguageEntry.POLISH.name
        assert name == 'Polish'

    def test_name_withPortuguese(self):
        name = LanguageEntry.PORTUGUESE.name
        assert name == 'Portuguese'

    def test_name_withRussian(self):
        name = LanguageEntry.RUSSIAN.name
        assert name == 'Russian'

    def test_name_withSpanish(self):
        name = LanguageEntry.SPANISH.name
        assert name == 'Spanish'

    def test_name_withSwedish(self):
        name = LanguageEntry.SWEDISH.name
        assert name == 'Swedish'

    def test_name_withThai(self):
        name = LanguageEntry.THAI.name
        assert name == 'Thai'

    def test_name_withUrdu(self):
        name = LanguageEntry.URDU.name
        assert name == 'Urdu'
