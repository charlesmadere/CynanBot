import pytest

from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.jsonMapper.ttsJsonMapper import TtsJsonMapper
from src.tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.settings.ttsSettingsRepository import TtsSettingsRepository
from src.tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from src.ttsMonster.ttsMonsterMessageCleaner import TtsMonsterMessageCleaner
from src.ttsMonster.ttsMonsterMessageCleanerInterface import TtsMonsterMessageCleanerInterface
from src.twitch.twitchMessageStringUtils import TwitchMessageStringUtils
from src.twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class TestTtsMonsterMessageCleaner:

    timber: TimberInterface = TimberStub()

    ttsJsonMapper: TtsJsonMapperInterface = TtsJsonMapper(
        timber = timber,
    )

    ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict()),
        ttsJsonMapper = ttsJsonMapper,
    )

    twitchMessageStringUtils: TwitchMessageStringUtilsInterface = TwitchMessageStringUtils()

    cleaner: TtsMonsterMessageCleanerInterface = TtsMonsterMessageCleaner(
        ttsSettingsRepository = ttsSettingsRepository,
        twitchMessageStringUtils = twitchMessageStringUtils
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
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None
