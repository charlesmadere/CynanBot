import pytest

from src.twitch.twitchMessageStringUtils import TwitchMessageStringUtils
from src.twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class TestTwitchMessageStringUtils:

    utils: TwitchMessageStringUtilsInterface = TwitchMessageStringUtils()

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withEmptyString(self):
        result = await self.utils.getUserNameFromCheerMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withNone(self):
        result = await self.utils.getUserNameFromCheerMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withRealMessage1(self):
        result = await self.utils.getUserNameFromCheerMessage('cheer100 stashiocat')
        assert result == 'stashiocat'

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withRealMessage2(self):
        result = await self.utils.getUserNameFromCheerMessage('cheer100 @stashiocat')
        assert result == 'stashiocat'

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withWhitespaceString(self):
        result = await self.utils.getUserNameFromCheerMessage(' ')
        assert result is None
