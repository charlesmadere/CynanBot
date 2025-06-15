from typing import Any

import pytest

from src.chatterPreferredTts.mapper.chatterPreferredTtsJsonMapper import ChatterPreferredTtsJsonMapper
from src.chatterPreferredTts.mapper.chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
from src.chatterPreferredTts.models.commodoreSam.commodoreSamTtsProperties import CommodoreSamTtsProperties
from src.chatterPreferredTts.models.decTalk.decTalkTtsProperties import DecTalkTtsProperties
from src.chatterPreferredTts.models.google.googleTtsProperties import GoogleTtsProperties
from src.chatterPreferredTts.models.halfLife.halfLifeTtsProperties import HalfLifeTtsProperties
from src.chatterPreferredTts.models.microsoft.microsoftTtsTtsProperties import MicrosoftTtsTtsProperties
from src.chatterPreferredTts.models.microsoftSam.microsoftSamTtsProperties import MicrosoftSamTtsProperties
from src.chatterPreferredTts.models.streamElements.streamElementsTtsProperties import StreamElementsTtsProperties
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
from src.microsoft.parser.microsoftTtsJsonParser import MicrosoftTtsJsonParser
from src.microsoft.parser.microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface
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

        assert isinstance(result, CommodoreSamTtsProperties)

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withDecTalk(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.DEC_TALK
        )

        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withDecTalkAndFrankVoice(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = {
                'voice': await self.decTalkVoiceMapper.serializeVoice(DecTalkVoice.FRANK)
            },
            provider = TtsProvider.DEC_TALK
        )

        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.FRANK

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withGoogle(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.GOOGLE
        )

        assert isinstance(result, GoogleTtsProperties)
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

        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.JAPANESE

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withHalfLife(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.HALF_LIFE
        )

        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withHalfLifeAndScientistVoice(self):
        halfLifeVoiceString = HalfLifeVoice.SCIENTIST.keyName

        result = await self.mapper.parsePreferredTts(
            configurationJson = {
                'halfLifeVoice': halfLifeVoiceString
            },
            provider = TtsProvider.HALF_LIFE
        )

        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is HalfLifeVoice.SCIENTIST

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withMicrosoft(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.MICROSOFT
        )

        assert isinstance(result, MicrosoftTtsTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withMicrosoftSam(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.MICROSOFT_SAM
        )

        assert isinstance(result, MicrosoftSamTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withStreamElements(self):
        result = await self.mapper.parsePreferredTts(
            configurationJson = dict(),
            provider = TtsProvider.STREAM_ELEMENTS
        )

        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parsePreferredTts_withStreamElementsAndAmyVoice(self):
        streamElementsVoiceString = await self.streamElementsJsonParser.serializeVoice(
            voice = StreamElementsVoice.AMY
        )

        result = await self.mapper.parsePreferredTts(
            configurationJson = {
                'streamElementsVoice': streamElementsVoiceString
            },
            provider = TtsProvider.STREAM_ELEMENTS
        )

        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is StreamElementsVoice.AMY

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, ChatterPreferredTtsJsonMapper)
        assert isinstance(self.mapper, ChatterPreferredTtsJsonMapperInterface)

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withDecTalk(self):
        preferredTts = DecTalkTtsProperties(
            voice = None
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withDecTalkAndWendyVoice(self):
        preferredTts = DecTalkTtsProperties(
            voice = DecTalkVoice.WENDY
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 1

        decTalkVoiceString: str | Any | None = result.get('voice', None)
        assert isinstance(decTalkVoiceString, str)

        decTalkVoice = await self.decTalkVoiceMapper.requireVoice(decTalkVoiceString)
        assert decTalkVoice is DecTalkVoice.WENDY

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withGoogle(self):
        preferredTts = GoogleTtsProperties(
            languageEntry = None
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withGoogleAndKoreanLanguageEntry(self):
        preferredTts = GoogleTtsProperties(
            languageEntry = LanguageEntry.KOREAN
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 1

        iso6391Code: str | Any | None = result.get('iso6391', None)
        assert isinstance(iso6391Code, str)

        assert iso6391Code == LanguageEntry.KOREAN.iso6391Code

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withGoogleAndSwedishLanguageEntry(self):
        preferredTts = GoogleTtsProperties(
            languageEntry = LanguageEntry.SWEDISH
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 1

        iso6391Code: str | Any | None = result.get('iso6391', None)
        assert isinstance(iso6391Code, str)

        assert iso6391Code == LanguageEntry.SWEDISH.iso6391Code

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withMicrosoftAndHarukaVoiceEntry(self):
        preferredTts = MicrosoftTtsTtsProperties(
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
    async def test_serializePreferredTts_withMicrosoftSam(self):
        result = await self.mapper.serializePreferredTts(
            preferredTts = MicrosoftSamTtsProperties(
                voice = None
            )
        )

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withMicrosoftSamAndMaryInSpaceVoiceEntry(self):
        preferredTts = MicrosoftSamTtsProperties(
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
        preferredTts = StreamElementsTtsProperties(
            voice = None
        )

        result = await self.mapper.serializePreferredTts(
            preferredTts = preferredTts
        )

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializePreferredTts_withStreamElementsAndJoeyVoice(self):
        preferredTts = StreamElementsTtsProperties(
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
