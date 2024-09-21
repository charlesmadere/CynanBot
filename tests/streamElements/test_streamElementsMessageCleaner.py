import pytest

from src.streamElements.streamElementsMessageCleaner import StreamElementsMessageCleaner


class TestStreamElementsMessageCleaner:

    cleaner = StreamElementsMessageCleaner()

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
        result = await self.cleaner.clean('Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None
