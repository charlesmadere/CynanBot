import pytest

from src.google.googleJsonMapper import GoogleJsonMapper
from src.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.streamElements.streamElementsMessageCleaner import StreamElementsMessageCleaner
from src.streamElements.streamElementsMessageCleanerInterface import StreamElementsMessageCleanerInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.ttsSettingsRepository import TtsSettingsRepository
from src.tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class TestStreamElementsMessageCleaner:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
        googleJsonMapper = googleJsonMapper,
        settingsJsonReader = JsonStaticReader(dict())
    )

    cleaner: StreamElementsMessageCleanerInterface = StreamElementsMessageCleaner(
        ttsSettingsRepository = ttsSettingsRepository
    )

    @pytest.mark.asyncio
    async def test_clean_withSimpleAmpersandMessage(self):
        result = await self.cleaner.clean('Nintendo & Microsoft & Sony?')
        assert result == 'Nintendo+%26+Microsoft+%26+Sony%3F'

    @pytest.mark.asyncio
    async def test_clean_withComplicatedCheerMessage(self):
        result = await self.cleaner.clean('cheer500 good uni25 luck cheer50 with cheer25 the uni25 runs! cheer10')
        assert result == 'good+luck+with+the+runs%21'

    @pytest.mark.asyncio
    async def test_clean_withEmptyString(self):
        result = await self.cleaner.clean('')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withNone(self):
        result = await self.cleaner.clean(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withSimpleMessage(self):
        result = await self.cleaner.clean('Hello, World')
        assert result == 'Hello%2C+World'

    @pytest.mark.asyncio
    async def test_clean_withSimpleMessageAndLotsOfWhitespace(self):
        result = await self.cleaner.clean('   \n  Hello,     World!\n \n')
        assert result == 'Hello%2C+World%21'

    @pytest.mark.asyncio
    async def test_clean_withSimpleCheerMessage(self):
        result = await self.cleaner.clean('cheer500 good luck with the runs!')
        assert result == 'good+luck+with+the+runs%21'

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None
