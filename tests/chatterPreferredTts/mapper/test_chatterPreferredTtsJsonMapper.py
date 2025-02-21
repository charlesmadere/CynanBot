import pytest

from src.chatterPreferredTts.mapper.chatterPreferredTtsJsonMapper import ChatterPreferredTtsJsonMapper
from src.chatterPreferredTts.mapper.chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
from src.chatterPreferredTts.models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from src.chatterPreferredTts.models.google.googlePreferredTts import GooglePreferredTts
from src.chatterPreferredTts.models.halfLife.halfLifePreferredTts import HalfLifePreferredTts
from src.chatterPreferredTts.models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from src.halfLife.models.halfLifeVoice import HalfLifeVoice
from src.halfLife.parser.halfLifeVoiceParser import HalfLifeVoiceParser
from src.halfLife.parser.halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from src.language.languageEntry import LanguageEntry
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.tts.ttsProvider import TtsProvider


class TestChatterPreferredTtsJsonMapper:

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()
    halfLifeJsonParser: HalfLifeVoiceParserInterface = HalfLifeVoiceParser()

    mapper: ChatterPreferredTtsJsonMapperInterface = ChatterPreferredTtsJsonMapper(
        halfLifeVoiceParser = halfLifeJsonParser,
        languagesRepository = languagesRepository
    )

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withDecTalk(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.DEC_TALK
        )

        assert isinstance(result, DecTalkPreferredTts)

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withGoogle(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.GOOGLE
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
            provider = TtsProvider.GOOGLE
        )

        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is LanguageEntry.JAPANESE

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withHalfLife(self):
        halfLifeVoiceString = HalfLifeVoice.SCIENTIST.keyName

        result = await self.mapper.parsePreferredTts(
            configurationJson = {
                'halfLifeVoice': halfLifeVoiceString
            },
            provider = TtsProvider.HALF_LIFE
        )

        assert isinstance(result, HalfLifePreferredTts)
        assert result.halfLifeVoiceEntry is HalfLifeVoice.SCIENTIST

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withMicrosoftSam(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.MICROSOFT_SAM
        )

        assert isinstance(result, MicrosoftSamPreferredTts)

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

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, ChatterPreferredTtsJsonMapper)
        assert isinstance(self.mapper, ChatterPreferredTtsJsonMapperInterface)
