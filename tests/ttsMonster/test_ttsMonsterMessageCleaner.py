import pytest

from src.ttsMonster.ttsMonsterMessageCleaner import TtsMonsterMessageCleaner


class TestTtsMonsterMessageCleaner:

    cleaner = TtsMonsterMessageCleaner()

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
