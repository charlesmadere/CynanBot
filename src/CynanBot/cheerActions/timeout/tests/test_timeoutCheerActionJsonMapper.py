from datetime import datetime

import pytest

from CynanBot.cheerActions.timeout.timeoutCheerActionJsonMapper import \
    TimeoutCheerActionJsonMapper
from CynanBot.cheerActions.timeout.timeoutCheerActionJsonMapperInterface import \
    TimeoutCheerActionJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from CynanBot.cheerActions.timeout.timeoutCheerActionEntry import TimeoutCheerActionEntry
from CynanBot.timber.timberStub import TimberStub


class TestTimeoutCheerActionJsonMapper():

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    jsonMapper: TimeoutCheerActionJsonMapperInterface = TimeoutCheerActionJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntriesString_withEmptyString(self):
        result = await self.jsonMapper.parseTimeoutCheerActionEntriesString('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntriesString_withNone(self):
        result = await self.jsonMapper.parseTimeoutCheerActionEntriesString(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntriesString_withWhitespaceString(self):
        result = await self.jsonMapper.parseTimeoutCheerActionEntriesString(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntry_withEmptyDictionary(self):
        result = await self.jsonMapper.parseTimeoutCheerActionEntry(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntry_withNone(self):
        result = await self.jsonMapper.parseTimeoutCheerActionEntry(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionEntriesToJsonString_withEmptyList(self):
        result = await self.jsonMapper.serializeTimeoutCheerActionEntriesToJsonString(list())
        assert result is None

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionEntriesToJsonString_withNone(self):
        result = await self.jsonMapper.serializeTimeoutCheerActionEntriesToJsonString(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionEntry(self):
        now = datetime.now(self.timeZoneRepository.getDefault())

        entry = TimeoutCheerActionEntry(
            timedOutAtDateTime = now,
            bitAmount = 50,
            durationSeconds = 120,
            timedOutByUserId = 'abc123'
        )

        result = await self.jsonMapper.serializeTimeoutCheerActionEntry(entry)
        assert isinstance(result, dict)
        assert len(result) == 4
        assert result['bitAmount'] == 50
        assert result['durationSeconds'] == 120
        assert result['timedOutAtDateTime'] == now.isoformat()
        assert result['timedOutByUserId'] == 'abc123'

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionEntry_withNone(self):
        result = await self.jsonMapper.serializeTimeoutCheerActionEntry(None)
        assert result is None
