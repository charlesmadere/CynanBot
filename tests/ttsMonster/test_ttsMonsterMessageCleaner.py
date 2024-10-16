import pytest

from src.google.googleJsonMapper import GoogleJsonMapper
from src.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.ttsSettingsRepository import TtsSettingsRepository
from src.tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from src.ttsMonster.ttsMonsterMessageCleaner import TtsMonsterMessageCleaner
from src.ttsMonster.ttsMonsterMessageCleanerInterface import TtsMonsterMessageCleanerInterface


class TestTtsMonsterMessageCleaner:

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

    cleaner: TtsMonsterMessageCleanerInterface = TtsMonsterMessageCleaner(
        ttsSettingsRepository = ttsSettingsRepository
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
