from src.language.jsonMapper.languageEntryJsonMapper import LanguageEntryJsonMapper
from src.language.jsonMapper.languageEntryJsonMapperInterface import LanguageEntryJsonMapperInterface
from src.language.languageEntry import LanguageEntry


class TestLanguageEntryJsonMapper:

    jsonMapper: LanguageEntryJsonMapperInterface = LanguageEntryJsonMapper()

    def test_parseLanguageEntry_withEnglishString(self):
        result = self.jsonMapper.parseLanguageEntry('english')
        assert result is LanguageEntry.ENGLISH

    def test_parseLanguageEntry_withJapaneseString(self):
        result = self.jsonMapper.parseLanguageEntry('japanese')
        assert result is LanguageEntry.JAPANESE

    def test_parseLanguageEntry_withSpanishString(self):
        result = self.jsonMapper.parseLanguageEntry('spanish')
        assert result is LanguageEntry.SPANISH

    def test_requireLanguageEntry_withEnglishString(self):
        result = self.jsonMapper.requireLanguageEntry('english')
        assert result is LanguageEntry.ENGLISH

    def test_requireLanguageEntry_withJapaneseString(self):
        result = self.jsonMapper.requireLanguageEntry('japanese')
        assert result is LanguageEntry.JAPANESE

    def test_requireLanguageEntry_withSpanishString(self):
        result = self.jsonMapper.requireLanguageEntry('spanish')
        assert result is LanguageEntry.SPANISH

    def test_serializeLanguageEntry_withEnglish(self):
        result = self.jsonMapper.serializeLanguageEntry(LanguageEntry.ENGLISH)
        assert result == 'english'

    def test_serializeLanguageEntry_withJapanese(self):
        result = self.jsonMapper.serializeLanguageEntry(LanguageEntry.JAPANESE)
        assert result == 'japanese'

    def test_serializeLanguageEntry_withSpanish(self):
        result = self.jsonMapper.serializeLanguageEntry(LanguageEntry.SPANISH)
        assert result == 'spanish'
