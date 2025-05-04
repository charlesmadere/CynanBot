import pytest

from src.supStreamer.supStreamerHelper import SupStreamerHelper
from src.supStreamer.supStreamerHelperInterface import SupStreamerHelperInterface


class TestSupStreamerHelper:

    helper: SupStreamerHelperInterface = SupStreamerHelper()

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withBadMessage1(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'hello',
            supStreamerMessage = 'charles sup'
        )

        assert not result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withBadMessage2(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'c h a r l e s   s u p',
            supStreamerMessage = 'charles sup'
        )

        assert not result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withBadMessage3(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'ch4rl3s 5up',
            supStreamerMessage = 'charles sup'
        )

        assert not result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withBadMessagePrefix(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'blahcharles sup',
            supStreamerMessage = 'charles sup'
        )

        assert not result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withBadMessagePrefixAndSuffix(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'blahcharles supblah',
            supStreamerMessage = 'charles sup'
        )

        assert not result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withBadMessageSuffix(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'charles supblah',
            supStreamerMessage = 'charles sup'
        )

        assert not result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withEmptyStringChatMessageArgument(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = '',
            supStreamerMessage = 'charles sup'
        )

        assert not result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withEmptyStringSupStreamerArgument(self):
        result: bool | None = None

        with pytest.raises(Exception):
            result = await self.helper.isSupStreamerMessage(
                chatMessage = 'charles sup',
                supStreamerMessage = ''
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withGoodMessage1(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'charles sup',
            supStreamerMessage = 'charles sup'
        )

        assert result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withGoodMessage2(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'CHARLES SUP',
            supStreamerMessage = 'charles sup'
        )

        assert result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withGoodMessageAndPrefix(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'peepoArrive charles sup',
            supStreamerMessage = 'charles sup'
        )

        assert result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withGoodMessageAndPrefixAndSuffix(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'peepoArrive charles sup peepoArrive',
            supStreamerMessage = 'charles sup'
        )

        assert result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withGoodMessageAndSuffix(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = 'charles sup peepoArrive',
            supStreamerMessage = 'charles sup'
        )

        assert result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withNoneChatMessageArgument(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = None,
            supStreamerMessage = 'charles sup'
        )

        assert not result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withNoneSupStreamerArgument(self):
        result: bool | None = None

        with pytest.raises(Exception):
            result = await self.helper.isSupStreamerMessage(
                chatMessage = 'charles sup',
                supStreamerMessage = None # type: ignore
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withWhitespaceStringChatMessageArgument(self):
        result = await self.helper.isSupStreamerMessage(
            chatMessage = ' ',
            supStreamerMessage = 'charles sup'
        )

        assert not result

    @pytest.mark.asyncio
    async def test_isSupStreamerMessage_withWhitespaceStringSupStreamerArgument(self):
        result: bool | None = None

        with pytest.raises(Exception):
            result = await self.helper.isSupStreamerMessage(
                chatMessage = 'charles sup',
                supStreamerMessage = ' '
            )

        assert result is None

    def test_sanity(self):
        assert self.helper is not None
        assert isinstance(self.helper, SupStreamerHelper)
        assert isinstance(self.helper, SupStreamerHelperInterface)
