import pytest

from src.chatterPreferredTts.mapper.chatterPreferredTtsJsonMapper import ChatterPreferredTtsJsonMapper
from src.chatterPreferredTts.mapper.chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
from src.chatterPreferredTts.models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from src.chatterPreferredTts.models.google.googlePreferredTts import GooglePreferredTts
from src.chatterPreferredTts.models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from src.chatterPreferredTts.models.preferredTtsProvider import PreferredTtsProvider
from src.language.languageEntry import LanguageEntry
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface


class TestChatterPreferredTtsJsonMapper:

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    mapper: ChatterPreferredTtsJsonMapperInterface = ChatterPreferredTtsJsonMapper(
        languagesRepository = languagesRepository
    )

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withDecTalk(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = PreferredTtsProvider.DEC_TALK
        )

        assert isinstance(result, DecTalkPreferredTts)

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withGoogle(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = PreferredTtsProvider.GOOGLE
        )

        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is None

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withGoogleAndJapaneseLanguageEntry(self):
        iso6391Code = LanguageEntry.JAPANESE.iso6391Code

        result = await self.mapper.parsePreferredTts(
            configurationJson = {
                'iso6391': iso6391Code
            },
            provider = PreferredTtsProvider.GOOGLE
        )

        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is LanguageEntry.JAPANESE

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withMicrosoftSam(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = PreferredTtsProvider.MICROSOFT_SAM
        )

        assert isinstance(result, MicrosoftSamPreferredTts)

    @pytest.mark.asyncio
    async def test_parsePreferredTtsProvider_withDecTalkString(self):
        result = await self.mapper.parsePreferredTtsProvider('dec_talk')
        assert result == PreferredTtsProvider.DEC_TALK

    @pytest.mark.asyncio
    async def test_parsePreferredTtsProvider_withGoogleString(self):
        result = await self.mapper.parsePreferredTtsProvider('google')
        assert result == PreferredTtsProvider.GOOGLE

    @pytest.mark.asyncio
    async def test_parsePreferredTtsProvider_withMicrosoftSamString(self):
        result = await self.mapper.parsePreferredTtsProvider('microsoft_sam')
        assert result == PreferredTtsProvider.MICROSOFT_SAM

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withDecTalk(self):
        result = await self.mapper.serializePreferredTts(
            preferredTts = DecTalkPreferredTts()
        )

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withGoogle(self):
        preferredTts = GooglePreferredTts(
            languageEntry = None
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withGoogleAndSwedishLanguageEntry(self):
        preferredTts = GooglePreferredTts(
            languageEntry = LanguageEntry.SWEDISH
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 1

        iso6391Code = result['iso6391']
        assert iso6391Code == LanguageEntry.SWEDISH.iso6391Code

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withMicrosoftSam(self):
        result = await self.mapper.serializePreferredTts(
            preferredTts = MicrosoftSamPreferredTts()
        )

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializePreferredTtsProvider_withDecTalk(self):
        result = await self.mapper.serializePreferredTtsProvider(PreferredTtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    @pytest.mark.asyncio
    async def test_serializePreferredTtsProvider_withGoogle(self):
        result = await self.mapper.serializePreferredTtsProvider(PreferredTtsProvider.GOOGLE)
        assert result == 'google'

    @pytest.mark.asyncio
    async def test_serializePreferredTtsProvider_withMicrosoftSam(self):
        result = await self.mapper.serializePreferredTtsProvider(PreferredTtsProvider.MICROSOFT_SAM)
        assert result == 'microsoft_sam'

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, ChatterPreferredTtsJsonMapper)
        assert isinstance(self.mapper, ChatterPreferredTtsJsonMapperInterface)
