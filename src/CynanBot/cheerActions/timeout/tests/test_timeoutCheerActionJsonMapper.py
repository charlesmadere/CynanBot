import pytest

from CynanBot.cheerActions.timeout.timeoutCheerActionJsonMapper import \
    TimeoutCheerActionJsonMapper
from CynanBot.cheerActions.timeout.timeoutCheerActionJsonMapperInterface import \
    TimeoutCheerActionJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestTimeoutCheerActionJsonMapper():

    timber: TimberInterface = TimberStub()

    jsonMapper: TimeoutCheerActionJsonMapperInterface = TimeoutCheerActionJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntry_withEmptyDictionary(self):
        result = await self.jsonMapper.parseTimeoutCheerActionEntry(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntry_withNone(self):
        result = await self.jsonMapper.parseTimeoutCheerActionEntry(None)
        assert result is None
