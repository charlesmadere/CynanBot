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

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withBigMixedMessage(self):
        result = await self.utils.removeCheerStrings(' cheer50  Hey good  cheer75 luck!!   cheer100  cheer100 \n')
        assert result == 'Hey good luck!!'

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withBitbossAndHelloWorldString(self):
        result = await self.utils.removeCheerStrings('bitboss100 Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withCheerAndHelloWorldString(self):
        result = await self.utils.removeCheerStrings('cheer100 Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withCheerOnly(self):
        result = await self.utils.removeCheerStrings('cheer100')
        assert result == ''

        result = await self.utils.removeCheerStrings('cheer100\n')
        assert result == ''

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withDoodleCheerAndHelloWorldString(self):
        result = await self.utils.removeCheerStrings('doodlecheer100 Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withHelloWorldString(self):
        result = await self.utils.removeCheerStrings('Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withLotsOfCheers(self):
        result = await self.utils.removeCheerStrings('cheer100 cheer500')
        assert result == ''

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withMuxyWorldString(self):
        result = await self.utils.removeCheerStrings('muxy100 Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withStreamLabsWorldString(self):
        result = await self.utils.removeCheerStrings('streamlabs100 Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_removeCheerStrings_withUniAndHelloWorldString(self):
        result = await self.utils.removeCheerStrings('uni50 Hello, World!')
        assert result == 'Hello, World!'

    def test_sanity(self):
        assert self.utils is not None
        assert isinstance(self.utils, TwitchMessageStringUtils)
        assert isinstance(self.utils, TwitchMessageStringUtilsInterface)
