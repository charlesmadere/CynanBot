from typing import Final

import pytest

from src.chatterPreferredName.helpers.chatterPreferredNameStringCleaner import ChatterPreferredNameStringCleaner


class TestChatterPreferredNameStringCleaner:

    cleaner: Final[ChatterPreferredNameStringCleaner] = ChatterPreferredNameStringCleaner()

    @pytest.mark.asyncio
    async def test_clean_withCrazyString1(self):
        result = await self.cleaner.clean('||||``$$|')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withCrazyString2(self):
        result = await self.cleaner.clean('...')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withEmptyString(self):
        result = await self.cleaner.clean('')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withHelloWorld(self):
        result = await self.cleaner.clean('Hello, World!')
        assert result == 'Hello World'

    @pytest.mark.asyncio
    async def test_clean_withInt(self):
        result = await self.cleaner.clean(100)
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withNone(self):
        result = await self.cleaner.clean(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withName1(self):
        result = await self.cleaner.clean('stashiocat')
        assert result == 'stashiocat'

    @pytest.mark.asyncio
    async def test_clean_withName2(self):
        result = await self.cleaner.clean(' imyt ')
        assert result == 'imyt'

    @pytest.mark.asyncio
    async def test_clean_withName3(self):
        result = await self.cleaner.clean('\"gaR\"')
        assert result == 'gaR'

    @pytest.mark.asyncio
    async def test_clean_withName4(self):
        result = await self.cleaner.clean('\"bastion_blue_succubus87\"')
        assert result == 'bastion blue succubus87'

    @pytest.mark.asyncio
    async def test_clean_withSentence1(self):
        result = await self.cleaner.clean('\"Here\'s a really long name! That\'ll be $10.00. A lot of these characters should\'ve been removed!\"')
        assert result == 'Heres a really long name'

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None

    def test_sanity(self):
        assert self.cleaner is not None
        assert isinstance(self.cleaner, ChatterPreferredNameStringCleaner)
