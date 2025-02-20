import pytest

from src.language.languageEntry import LanguageEntry
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface


class TestLanguagesRepository:

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    @pytest.mark.asyncio
    async def test_getLanguageForCommand_withAllEnglishCommandNames(self):
        for commandName in LanguageEntry.ENGLISH.commandNames:
            languageEntry = await self.languagesRepository.getLanguageForCommand(
                command = commandName
            )

            assert languageEntry is LanguageEntry.ENGLISH

    @pytest.mark.asyncio
    async def test_getLanguageForCommand_withAllJapaneseCommandNames(self):
        for commandName in LanguageEntry.JAPANESE.commandNames:
            languageEntry = await self.languagesRepository.getLanguageForCommand(
                command = commandName
            )

            assert languageEntry is LanguageEntry.JAPANESE

    @pytest.mark.asyncio
    async def test_getLanguageForCommand_withAllSwedishCommandNames(self):
        for commandName in LanguageEntry.SWEDISH.commandNames:
            languageEntry = await self.languagesRepository.getLanguageForCommand(
                command = commandName
            )

            assert languageEntry is LanguageEntry.SWEDISH

    @pytest.mark.asyncio
    async def test_getLanguageForCommand_withEnglish(self):
        languageEntry = await self.languagesRepository.getLanguageForCommand(
            command = 'english'
        )

        assert languageEntry is LanguageEntry.ENGLISH

    @pytest.mark.asyncio
    async def test_getLanguageForIso6391Code_withAllLanguageEntries(self):
        for languageEntry in LanguageEntry:
            iso6391Code = languageEntry.iso6391Code

            if iso6391Code is None:
                continue

            result = await self.languagesRepository.getLanguageForIso6391Code(iso6391Code)
            assert result is languageEntry

    def test_sanity(self):
        assert self.languagesRepository is not None
        assert isinstance(self.languagesRepository, LanguagesRepository)
        assert isinstance(self.languagesRepository, LanguagesRepositoryInterface)
