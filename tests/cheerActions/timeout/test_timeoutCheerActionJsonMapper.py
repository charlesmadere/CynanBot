import json
from datetime import datetime
from typing import Any

import pytest
from src.cheerActions.timeout.timeoutCheerActionEntry import \
    TimeoutCheerActionEntry
from src.cheerActions.timeout.timeoutCheerActionJsonMapper import \
    TimeoutCheerActionJsonMapper
from src.cheerActions.timeout.timeoutCheerActionJsonMapperInterface import \
    TimeoutCheerActionJsonMapperInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


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
    async def test_serializeTimeoutCheerActionEntriesToJsonString(self):
        entry = TimeoutCheerActionEntry(
            timedOutAtDateTime = datetime.now(self.timeZoneRepository.getDefault()),
            bitAmount = 100,
            durationSeconds = 60,
            timedOutByUserId = 'abc123'
        )

        entries: list[TimeoutCheerActionEntry] = list()
        entries.append(entry)

        jsonString = await self.jsonMapper.serializeTimeoutCheerActionEntriesToJsonString(entries)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert jsonString.isspace() is False

        jsonList: list[dict[str, Any]] = json.loads(jsonString)
        assert isinstance(jsonList, list)
        assert len(jsonList) == 1

        jsonEntry = jsonList[0]
        assert isinstance(jsonEntry, dict)
        assert len(jsonEntry) == 4
        assert jsonEntry['bitAmount'] == entry.bitAmount
        assert jsonEntry['durationSeconds'] == entry.durationSeconds
        assert jsonEntry['timedOutAtDateTime'] == entry.timedOutAtDateTime.isoformat()
        assert jsonEntry['timedOutByUserId'] == entry.timedOutByUserId

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

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, TimeoutCheerActionJsonMapperInterface)
        assert isinstance(self.jsonMapper, TimeoutCheerActionJsonMapper)
