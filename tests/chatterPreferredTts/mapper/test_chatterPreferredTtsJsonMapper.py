from typing import Any

import pytest

from src.chatterPreferredTts.mapper.chatterPreferredTtsJsonMapper import ChatterPreferredTtsJsonMapper
from src.chatterPreferredTts.mapper.chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
from src.chatterPreferredTts.models.commodoreSam.commodoreSamPreferredTts import CommodoreSamPreferredTts
from src.chatterPreferredTts.models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from src.chatterPreferredTts.models.google.googlePreferredTts import GooglePreferredTts
from src.chatterPreferredTts.models.halfLife.halfLifePreferredTts import HalfLifePreferredTts
from src.chatterPreferredTts.models.microsoft.microsoftTtsPreferredTts import MicrosoftTtsPreferredTts
from src.chatterPreferredTts.models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from src.chatterPreferredTts.models.streamElements.streamElementsPreferredTts import StreamElementsPreferredTts
from src.decTalk.mapper.decTalkVoiceMapper import DecTalkVoiceMapper
from src.decTalk.mapper.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from src.decTalk.models.decTalkVoice import DecTalkVoice
from src.halfLife.models.halfLifeVoice import HalfLifeVoice
from src.halfLife.parser.halfLifeVoiceParser import HalfLifeVoiceParser
from src.halfLife.parser.halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from src.language.languageEntry import LanguageEntry
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from src.microsoft.parser.microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface
from src.microsoft.parser.microsoftTtsJsonParser import MicrosoftTtsJsonParser
from src.microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from src.microsoftSam.parser.microsoftSamJsonParser import MicrosoftSamJsonParser
from src.microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from src.streamElements.models.streamElementsVoice import StreamElementsVoice
from src.streamElements.parser.streamElementsJsonParser import StreamElementsJsonParser
from src.streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.models.ttsProvider import TtsProvider
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapper import TtsMonsterPrivateApiJsonMapper
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface


class TestChatterPreferredTtsJsonMapper:

    decTalkVoiceMapper: DecTalkVoiceMapperInterface = DecTalkVoiceMapper()

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    halfLifeJsonParser: HalfLifeVoiceParserInterface = HalfLifeVoiceParser()

    microsoftSamJsonParser: MicrosoftSamJsonParserInterface = MicrosoftSamJsonParser()

    microsoftTtsJsonParser: MicrosoftTtsJsonParserInterface = MicrosoftTtsJsonParser()

    streamElementsJsonParser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

    timber: TimberInterface = TimberStub()

    ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface = TtsMonsterPrivateApiJsonMapper(
        timber = timber
    )

    mapper: ChatterPreferredTtsJsonMapperInterface = ChatterPreferredTtsJsonMapper(
        decTalkVoiceMapper = decTalkVoiceMapper,
        halfLifeVoiceParser = halfLifeJsonParser,
        languagesRepository = languagesRepository,
        microsoftSamJsonParser = microsoftSamJsonParser,
        microsoftTtsJsonParser = microsoftTtsJsonParser,
        streamElementsJsonParser = streamElementsJsonParser,
        ttsMonsterPrivateApiJsonMapper = ttsMonsterPrivateApiJsonMapper
    )

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withCommodoreSam(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.COMMODORE_SAM
        )

        assert isinstance(result, CommodoreSamPreferredTts)

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withDecTalk(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.DEC_TALK
        )

        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withDecTalkAndFrankVoice(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = {
                'voice': await self.decTalkVoiceMapper.serializeVoice(DecTalkVoice.FRANK)
            },
            provider = TtsProvider.DEC_TALK
        )

        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is DecTalkVoice.FRANK

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
    async def test_serializePreferredTts_withDecTalk(self):
        preferredTts = DecTalkPreferredTts(
            voice = None
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
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
    async def test_parsePreferredTts_withMicrosoft(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.MICROSOFT
        )

        assert isinstance(result, MicrosoftTtsPreferredTts)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withMicrosoftAndHarukaVoiceEntry(self):
        preferredTts = MicrosoftTtsPreferredTts(
            voice = MicrosoftTtsVoice.HARUKA
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 1

        microsoftTtsVoiceString: str | Any | None = result.get('microsoftTtsVoice', None)
        assert isinstance(microsoftTtsVoiceString, str)

        microsoftTtsVoice = await self.microsoftTtsJsonParser.parseVoice(microsoftTtsVoiceString)
        assert microsoftTtsVoice is MicrosoftTtsVoice.HARUKA

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withMicrosoftSam(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.MICROSOFT_SAM
        )

        assert isinstance(result, MicrosoftSamPreferredTts)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withMicrosoftSamAndMaryInSpaceVoiceEntry(self):
        preferredTts = MicrosoftSamPreferredTts(
            voice = MicrosoftSamVoice.MARY_SPACE
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 1

        microsoftSamVoiceString: str | Any | None = result.get('microsoftSamVoice', None)
        assert isinstance(microsoftSamVoiceString, str)

        microsoftSamVoice = await self.microsoftSamJsonParser.parseVoice(microsoftSamVoiceString)
        assert microsoftSamVoice is MicrosoftSamVoice.MARY_SPACE

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withStreamElements(self):
        preferredTts = StreamElementsPreferredTts(
            voice = None
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withStreamElementsAndJoey(self):
        preferredTts = StreamElementsPreferredTts(
            voice = StreamElementsVoice.JOEY
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 1

        streamElementsVoiceString: str | Any | None = result.get('streamElementsVoice', None)
        assert isinstance(streamElementsVoiceString, str)

        streamElementsVoice = await self.streamElementsJsonParser.parseVoice(streamElementsVoiceString)
        assert streamElementsVoice is StreamElementsVoice.JOEY

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
            preferredTts = MicrosoftSamPreferredTts(
                voice = None
            )
        )

        assert isinstance(result, dict)
        assert len(result) == 0

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, ChatterPreferredTtsJsonMapper)
        assert isinstance(self.mapper, ChatterPreferredTtsJsonMapperInterface)
