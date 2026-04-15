import pytest

from src.halfLife.halfLifeMessageCleaner import HalfLifeMessageCleaner
from src.halfLife.halfLifeMessageCleanerInterface import HalfLifeMessageCleanerInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.jsonMapper.ttsJsonMapper import TtsJsonMapper
from src.tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.settings.ttsSettingsRepository import TtsSettingsRepository
from src.tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class TestHalfLifeMessageCleaner:

    timber: TimberInterface = TimberStub()

    ttsJsonMapper: TtsJsonMapperInterface = TtsJsonMapper(
        timber = timber,
    )

    ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict()),
        ttsJsonMapper = ttsJsonMapper,
    )

    cleaner: HalfLifeMessageCleanerInterface = HalfLifeMessageCleaner(
        ttsSettingsRepository = ttsSettingsRepository,
    )

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
        assert result == 'Hello, World'

    @pytest.mark.asyncio
    async def test_clean_withSimpleMessageAndLotsOfWhitespace(self):
        result = await self.cleaner.clean('   \n  Hello,     World!\n \n')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_clean_withVoiceMessage(self):
        result = await self.cleaner.clean('brian: test')
        assert result == 'brian: test'

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None

    def test_sanity(self):
        assert self.cleaner is not None
        assert isinstance(self.cleaner, HalfLifeMessageCleaner)
        assert isinstance(self.cleaner, HalfLifeMessageCleanerInterface)
