import pytest

from src.twitch.twitchMessageStringUtils import TwitchMessageStringUtils
from src.twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class TestTwitchMessageStringUtils:

    utils: TwitchMessageStringUtilsInterface = TwitchMessageStringUtils()

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withEmptyString(self):
        result = await self.utils.getUserNameFromMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withNone(self):
        result = await self.utils.getUserNameFromMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withRealMessage1(self):
        result = await self.utils.getUserNameFromMessage('stashiocat')
        assert result == 'stashiocat'

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withRealMessage2(self):
        result = await self.utils.getUserNameFromMessage('@eddie')
        assert result == 'eddie'

    @pytest.mark.asyncio
    async def test_getUserNameFromMessage_withRealMessage3(self):
        result = await self.utils.getUserNameFromMessage('@imyt  ')
        assert result == 'imyt'

    @pytest.mark.asyncio
    async def test_getUserNameFromCheerMessage_withEmptyString(self):
        result = await self.utils.getUserNameFromCheerMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_getUserNameFromCheerMessage_withNone(self):
        result = await self.utils.getUserNameFromCheerMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_getUserNameFromCheerMessage_withRealMessage1(self):
        result = await self.utils.getUserNameFromCheerMessage('cheer100 stashiocat')
        assert result == 'stashiocat'

    @pytest.mark.asyncio
    async def test_getUserNameFromCheerMessage_withRealMessage2(self):
        result = await self.utils.getUserNameFromCheerMessage('cheer100 @stashiocat')
        assert result == 'stashiocat'

    @pytest.mark.asyncio
    async def test_getUserNameFromCheerMessage_withRealMessage3(self):
        result = await self.utils.getUserNameFromCheerMessage('cheer1234567890 @a_n_i_v')
        assert result == 'a_n_i_v'

    @pytest.mark.asyncio
    async def test_getUserNameFromCheerMessage_withRealMessage4(self):
        result = await self.utils.getUserNameFromCheerMessage(' cheer9876543210    a_n_i_v  ')
        assert result == 'a_n_i_v'

    @pytest.mark.asyncio
    async def test_getUserNameFromCheerMessage_withRealMessage5(self):
        result = await self.utils.getUserNameFromCheerMessage(' cheer50  JRP2234')
        assert result == 'JRP2234'

    @pytest.mark.asyncio
    async def test_getUserNameFromCheerMessage_withWhitespaceString(self):
        result = await self.utils.getUserNameFromCheerMessage(' ')
        assert result is None

    def test_sanity(self):
        assert self.utils is not None
        assert isinstance(self.utils, TwitchMessageStringUtils)
        assert isinstance(self.utils, TwitchMessageStringUtilsInterface)
