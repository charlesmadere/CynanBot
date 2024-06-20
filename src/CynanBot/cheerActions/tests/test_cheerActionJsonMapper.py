import pytest

from CynanBot.cheerActions.cheerActionBitRequirement import CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionJsonMapper import CheerActionJsonMapper
from CynanBot.cheerActions.cheerActionJsonMapperInterface import \
    CheerActionJsonMapperInterface
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestCheerActionJsonMapper():

    timber: TimberInterface = TimberStub()

    jsonMapper: CheerActionJsonMapperInterface = CheerActionJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseCheerActionBitRequirement_withEmptyString(self):
        result = await self.jsonMapper.parseCheerActionBitRequirement('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionBitRequirement_withExactString(self):
        result = await self.jsonMapper.parseCheerActionBitRequirement('exact')
        assert result is CheerActionBitRequirement.EXACT

    @pytest.mark.asyncio
    async def test_parseCheerActionBitRequirement_withGreaterThanOrEqualToString(self):
        result = await self.jsonMapper.parseCheerActionBitRequirement('greater_than_or_equal_to')
        assert result is CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO

    @pytest.mark.asyncio
    async def test_parseCheerActionBitRequirement_withNone(self):
        result = await self.jsonMapper.parseCheerActionBitRequirement(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionBitRequirement_withWhitespaceString(self):
        result = await self.jsonMapper.parseCheerActionBitRequirement(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withAnyString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withNone(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOfflineString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOnlineString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withWhitespaceString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withAnyString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOfflineString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOnlineString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withEmptyString(self):
        result = await self.jsonMapper.parseCheerActionType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withNone(self):
        result = await self.jsonMapper.parseCheerActionType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withSoundAlertString(self):
        result = await self.jsonMapper.parseCheerActionType('sound_alert')
        assert result is CheerActionType.SOUND_ALERT

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withTimeoutString(self):
        result = await self.jsonMapper.parseCheerActionType('timeout')
        assert result is CheerActionType.TIMEOUT

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withWhitespaceString(self):
        result = await self.jsonMapper.parseCheerActionType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireCheerActionBitRequirement_withExactString(self):
        result = await self.jsonMapper.requireCheerActionBitRequirement('exact')
        assert result is CheerActionBitRequirement.EXACT

    @pytest.mark.asyncio
    async def test_requireCheerActionBitRequirement_withGreaterThanOrEqualTo(self):
        result = await self.jsonMapper.requireCheerActionBitRequirement('greater_than_or_equal_to')
        assert result is CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withAnyString(self):
        result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withOfflineString(self):
        result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withOnlineString(self):
        result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withSoundAlertString(self):
        result = await self.jsonMapper.requireCheerActionType('sound_alert')
        assert result is CheerActionType.SOUND_ALERT

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withTimeoutString(self):
        result = await self.jsonMapper.requireCheerActionType('timeout')
        assert result is CheerActionType.TIMEOUT

    @pytest.mark.asyncio
    async def test_serializeCheerActionBitRequirement_withExact(self):
        result = await self.jsonMapper.serializeCheerActionBitRequirement(CheerActionBitRequirement.EXACT)
        assert result == 'exact'

    @pytest.mark.asyncio
    async def test_serializeCheerActionBitRequirement_withGreaterThanOrEqualTo(self):
        result = await self.jsonMapper.serializeCheerActionBitRequirement(CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO)
        assert result == 'greater_than_or_equal_to'

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement_withAny(self):
        result = await self.jsonMapper.serializeCheerActionStreamStatusRequirement(CheerActionStreamStatusRequirement.ANY)
        assert result == 'any'

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement_withOffline(self):
        result = await self.jsonMapper.serializeCheerActionStreamStatusRequirement(CheerActionStreamStatusRequirement.OFFLINE)
        assert result == 'offline'

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement_withOnline(self):
        result = await self.jsonMapper.serializeCheerActionStreamStatusRequirement(CheerActionStreamStatusRequirement.ONLINE)
        assert result == 'online'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withSoundAlert(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.SOUND_ALERT)
        assert result == 'sound_alert'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withTimeout(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.TIMEOUT)
        assert result == 'timeout'
