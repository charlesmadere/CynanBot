import pytest

from CynanBot.cheerActions.cheerActionJsonMapper import CheerActionJsonMapper
from CynanBot.cheerActions.cheerActionJsonMapperInterface import \
    CheerActionJsonMapperInterface
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestCheerActionJsonMapper():

    timber: TimberInterface = TimberStub()

    jsonMapper: CheerActionJsonMapperInterface = CheerActionJsonMapper(
        timber = timber
    )

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
    async def test_requireCheerActionType_withSoundAlertString(self):
        result = await self.jsonMapper.requireCheerActionType('sound_alert')
        assert result is CheerActionType.SOUND_ALERT

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withTimeoutString(self):
        result = await self.jsonMapper.requireCheerActionType('timeout')
        assert result is CheerActionType.TIMEOUT

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withSoundAlert(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.SOUND_ALERT)
        assert result is 'sound_alert'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withTimeout(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.TIMEOUT)
        assert result is 'timeout'
