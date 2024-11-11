import json
from datetime import datetime
from typing import Any

import pytest
from frozenlist import FrozenList

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from CynanBot.src.timeout.timeoutActionHistoryEntry import TimeoutActionHistoryEntry
from CynanBot.src.timeout.timeoutActionJsonMapper import TimeoutActionJsonMapper
from CynanBot.src.timeout.timeoutActionJsonMapperInterface import TimeoutActionJsonMapperInterface


class TestTimeoutCheerActionJsonMapper:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    jsonMapper: TimeoutActionJsonMapperInterface = TimeoutActionJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntriesString_with1Entry(self):
        entry = TimeoutActionHistoryEntry(
            timedOutAtDateTime = datetime.now(self.timeZoneRepository.getDefault()),
            bitAmount = 100,
            durationSeconds = 60,
            timedOutByUserId = 'abc123'
        )

        entries: list[TimeoutActionHistoryEntry] = [ entry ]
        jsonString = await self.jsonMapper.serializeTimeoutActionEntriesToJsonString(entries)
        assert isinstance(jsonString, str)

        result = await self.jsonMapper.parseTimeoutActionEntriesString(jsonString)
        assert isinstance(result, FrozenList)
        assert len(result) == 1

        newEntry = result[0]
        assert isinstance(newEntry, TimeoutActionHistoryEntry)
        assert newEntry == entry

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntriesString_withEmptyString(self):
        result = await self.jsonMapper.parseTimeoutActionEntriesString('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntriesString_withNone(self):
        result = await self.jsonMapper.parseTimeoutActionEntriesString(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntriesString_withWhitespaceString(self):
        result = await self.jsonMapper.parseTimeoutActionEntriesString(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntry_withEmptyDictionary(self):
        result = await self.jsonMapper.parseTimeoutActionEntry(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionEntry_withNone(self):
        result = await self.jsonMapper.parseTimeoutActionEntry(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionEntriesToJsonString_with1Entry(self):
        entry = TimeoutActionHistoryEntry(
            timedOutAtDateTime = datetime.now(self.timeZoneRepository.getDefault()),
            bitAmount = 100,
            durationSeconds = 60,
            timedOutByUserId = 'abc123'
        )

        entries: list[TimeoutActionHistoryEntry] = [ entry ]
        jsonString = await self.jsonMapper.serializeTimeoutActionEntriesToJsonString(entries)
        assert isinstance(jsonString, str)

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
    async def test_serializeTimeoutCheerActionEntriesToJsonString_with2Entries(self):
        entry = TimeoutActionHistoryEntry(
            timedOutAtDateTime = datetime.now(self.timeZoneRepository.getDefault()),
            bitAmount = 50,
            durationSeconds = 60,
            timedOutByUserId = 'abc123'
        )

        entries: list[TimeoutActionHistoryEntry] = [ entry, entry ]
        jsonString = await self.jsonMapper.serializeTimeoutActionEntriesToJsonString(entries)
        assert isinstance(jsonString, str)

        jsonList: list[dict[str, Any]] = json.loads(jsonString)
        assert isinstance(jsonList, list)
        assert len(jsonList) == 2

        jsonEntry = jsonList[0]
        assert isinstance(jsonEntry, dict)
        assert len(jsonEntry) == 4

        assert jsonEntry['bitAmount'] == entry.bitAmount
        assert jsonEntry['durationSeconds'] == entry.durationSeconds
        assert jsonEntry['timedOutAtDateTime'] == entry.timedOutAtDateTime.isoformat()
        assert jsonEntry['timedOutByUserId'] == entry.timedOutByUserId

        jsonEntry = jsonList[1]
        assert isinstance(jsonEntry, dict)
        assert len(jsonEntry) == 4

        assert jsonEntry['bitAmount'] == entry.bitAmount
        assert jsonEntry['durationSeconds'] == entry.durationSeconds
        assert jsonEntry['timedOutAtDateTime'] == entry.timedOutAtDateTime.isoformat()
        assert jsonEntry['timedOutByUserId'] == entry.timedOutByUserId

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionEntriesToJsonString_withEmptyList(self):
        result = await self.jsonMapper.serializeTimeoutActionEntriesToJsonString(list())
        assert result is None

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionEntriesToJsonString_withNone(self):
        result = await self.jsonMapper.serializeTimeoutActionEntriesToJsonString(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionEntry(self):
        now = datetime.now(self.timeZoneRepository.getDefault())

        entry = TimeoutActionHistoryEntry(
            timedOutAtDateTime = now,
            bitAmount = 50,
            durationSeconds = 120,
            timedOutByUserId = 'abc123'
        )

        result = await self.jsonMapper.serializeTimeoutActionEntry(entry)
        assert isinstance(result, dict)
        assert len(result) == 4

        assert result['bitAmount'] == 50
        assert result['durationSeconds'] == 120
        assert result['timedOutAtDateTime'] == now.isoformat()
        assert result['timedOutByUserId'] == 'abc123'

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionEntry_withNone(self):
        result = await self.jsonMapper.serializeTimeoutActionEntry(None)
        assert result is None

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, TimeoutActionJsonMapperInterface)
        assert isinstance(self.jsonMapper, TimeoutActionJsonMapper)
