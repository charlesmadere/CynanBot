import pytest

from src.storage.jsonStaticReader import JsonStaticReader
from src.streamElements.streamElementsMessageCleaner import StreamElementsMessageCleaner
from src.streamElements.streamElementsMessageCleanerInterface import StreamElementsMessageCleanerInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.settings.ttsSettingsRepository import TtsSettingsRepository
from src.tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from src.twitch.twitchMessageStringUtils import TwitchMessageStringUtils
from src.twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class TestStreamElementsMessageCleaner:

    timber: TimberInterface = TimberStub()

    ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    twitchMessageStringUtils: TwitchMessageStringUtilsInterface = TwitchMessageStringUtils()

    cleaner: StreamElementsMessageCleanerInterface = StreamElementsMessageCleaner(
        ttsSettingsRepository = ttsSettingsRepository,
        twitchMessageStringUtils = twitchMessageStringUtils
    )

    @pytest.mark.asyncio
    async def test_clean_withVoiceMessage(self):
        result = await self.cleaner.clean('brian: test')
        assert result == 'brian: test'

    @pytest.mark.asyncio
    async def test_clean_withComplicatedCheerMessage(self):
        result = await self.cleaner.clean('cheer500 good uni25 luck cheer50 with cheer25 the uni25 runs! cheer10')
        assert result == 'good luck with the runs!'

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
    async def test_clean_withSimpleCheerMessage(self):
        result = await self.cleaner.clean('cheer500 good luck with the runs!')
        assert result == 'good luck with the runs!'

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None
