from typing import Final

import pytest

from src.twitch.twitchMessageStringUtils import TwitchMessageStringUtils
from src.twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class TestTwitchMessageStringUtils:

    utils: Final[TwitchMessageStringUtilsInterface] = TwitchMessageStringUtils()

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
    async def test_parseUserNameCommandMessage_withAtSignString(self):
        result = await self.utils.parseUserNameCommandMessage('@')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withCommandAndUserNameString1(self):
        result = await self.utils.parseUserNameCommandMessage('!cuteness @smcharles')
        assert result is not None
        assert result.command == 'cuteness'
        assert result.rawMessage == '!cuteness @smcharles'
        assert result.remainingMessage is None
        assert result.userName == 'smcharles'

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withCommandAndUserNameString2(self):
        result = await self.utils.parseUserNameCommandMessage('!givecuteness @stashiocat 500')
        assert result is not None
        assert result.command == 'givecuteness'
        assert result.rawMessage == '!givecuteness @stashiocat 500'
        assert result.remainingMessage == '500'
        assert result.userName == 'stashiocat'

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withCommandAndUserNameString3(self):
        result = await self.utils.parseUserNameCommandMessage(' !triviascore    imyt  \n')
        assert result is not None
        assert result.command == 'triviascore'
        assert result.rawMessage == '!triviascore imyt'
        assert result.remainingMessage is None
        assert result.userName == 'imyt'

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withCommandAndUserNameString4(self):
        result = await self.utils.parseUserNameCommandMessage(' !triviascore    dr_girl_friend  \n')
        assert result is not None
        assert result.command == 'triviascore'
        assert result.rawMessage == '!triviascore dr_girl_friend'
        assert result.remainingMessage is None
        assert result.userName == 'dr_girl_friend'

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withCommandOnly1(self):
        result = await self.utils.parseUserNameCommandMessage('!test123')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withCommandOnly2(self):
        result = await self.utils.parseUserNameCommandMessage('!weather')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withEmptyString(self):
        result = await self.utils.parseUserNameCommandMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withExclamationMarkString(self):
        result = await self.utils.parseUserNameCommandMessage('!')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withNone(self):
        result = await self.utils.parseUserNameCommandMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withRandomWord1(self):
        result = await self.utils.parseUserNameCommandMessage('random')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withRandomWord2(self):
        result = await self.utils.parseUserNameCommandMessage('hello world')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserNameCommandMessage_withWhitespaceString(self):
        result = await self.utils.parseUserNameCommandMessage(' ')
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
