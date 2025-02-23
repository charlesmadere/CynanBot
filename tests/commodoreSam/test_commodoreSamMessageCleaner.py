import pytest

from src.commodoreSam.commodoreSamMessageCleaner import CommodoreSamMessageCleaner
from src.commodoreSam.commodoreSamMessageCleanerInterface import CommodoreSamMessageCleanerInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.tts.ttsSettingsRepository import TtsSettingsRepository
from src.tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from src.twitch.twitchMessageStringUtils import TwitchMessageStringUtils
from src.twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class TestCommodoreSamMessageCleaner:

    ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    twitchMessageStringUtils: TwitchMessageStringUtilsInterface = TwitchMessageStringUtils()

    cleaner: CommodoreSamMessageCleanerInterface = CommodoreSamMessageCleaner(
        ttsSettingsRepository = ttsSettingsRepository,
        twitchMessageStringUtils = twitchMessageStringUtils
    )

    @pytest.mark.asyncio
    async def test_clean_withBasicMessage1(self):
        result = await self.cleaner.clean('Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_clean_withCheerMessage1(self):
        result = await self.cleaner.clean('cheer100 Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_clean_withCheerMessage2(self):
        result = await self.cleaner.clean('cheer100 Hello, cheer50 World!\ncheer123456')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_clean_withEmptyString(self):
        result = await self.cleaner.clean('')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withNone(self):
        result = await self.cleaner.clean(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None

    def test_sanity(self):
        assert self.cleaner is not None
        assert isinstance(self.cleaner, CommodoreSamMessageCleaner)
        assert isinstance(self.cleaner, CommodoreSamMessageCleanerInterface)
