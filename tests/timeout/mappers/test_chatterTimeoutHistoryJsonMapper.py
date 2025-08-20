import json
from datetime import datetime

import pytest
from frozenlist import FrozenList

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timeout.mappers.chatterTimeoutHistoryMapper import ChatterTimeoutHistoryMapper
from src.timeout.mappers.chatterTimeoutHistoryMapperInterface import ChatterTimeoutHistoryMapperInterface
from src.timeout.models.chatterTimeoutHistoryEntry import ChatterTimeoutHistoryEntry


class TestChatterTimeoutHistoryJsonMapper:

    mapper: ChatterTimeoutHistoryMapperInterface = ChatterTimeoutHistoryMapper()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    @pytest.mark.asyncio
    async def test_parseHistoryEntries(self):
        first = ChatterTimeoutHistoryEntry(
            dateTime = datetime.fromisoformat('2025-07-20T07:27:14.000000+00:00'),
            durationSeconds = 30,
            timedOutByUserId = 'abc123',
        )

        second = ChatterTimeoutHistoryEntry(
            dateTime = datetime.fromisoformat('2024-12-20T09:33:58.000000+00:00'),
            durationSeconds = 60,
            timedOutByUserId = 'def456',
        )

        third = ChatterTimeoutHistoryEntry(
            dateTime = datetime.fromisoformat('2025-05-01T12:12:12.000000+00:00'),
            durationSeconds = 60,
            timedOutByUserId = 'ghi789',
        )

        historyEntries: list[ChatterTimeoutHistoryEntry] = [ first, second, third ]
        historyEntriesJson = await self.mapper.serializeHistoryEntries(historyEntries)

        results = await self.mapper.parseHistoryEntries(historyEntriesJson)
        assert isinstance(results, FrozenList)
        assert len(results) == 3
        assert results.frozen

        # parsing the entries should also sort them in newest-to-oldest order
        assert results[0] == first
        assert results[1] == third
        assert results[2] == second

    @pytest.mark.asyncio
    async def test_parseHistoryEntries_withEmptyList(self):
        jsonString = json.dumps(list())
        results = await self.mapper.parseHistoryEntries(jsonString)
        assert isinstance(results, FrozenList)
        assert len(results) == 0
        assert results.frozen

    @pytest.mark.asyncio
    async def test_parseHistoryEntries_withEmptyString(self):
        results = await self.mapper.parseHistoryEntries('')
        assert isinstance(results, FrozenList)
        assert len(results) == 0
        assert results.frozen

    @pytest.mark.asyncio
    async def test_parseHistoryEntries_withNone(self):
        results = await self.mapper.parseHistoryEntries(None)
        assert isinstance(results, FrozenList)
        assert len(results) == 0
        assert results.frozen

    @pytest.mark.asyncio
    async def test_parseHistoryEntries_withWhitespaceString(self):
        results = await self.mapper.parseHistoryEntries(' ')
        assert isinstance(results, FrozenList)
        assert len(results) == 0
        assert results.frozen

    @pytest.mark.asyncio
    async def test_requireHistoryEntry(self):
        historyEntry = ChatterTimeoutHistoryEntry(
            dateTime = datetime.now(self.timeZoneRepository.getDefault()),
            durationSeconds = 30,
            timedOutByUserId = 'abc123',
        )

        result = await self.mapper.requireHistoryEntry({
            'dateTime': historyEntry.dateTime.isoformat(),
            'durationSeconds': historyEntry.durationSeconds,
            'timedOutBy': historyEntry.timedOutByUserId,
        })

        assert result == historyEntry
        assert result.dateTime == historyEntry.dateTime
        assert result.durationSeconds == historyEntry.durationSeconds
        assert result.timedOutByUserId == historyEntry.timedOutByUserId

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, ChatterTimeoutHistoryMapper)
        assert isinstance(self.mapper, ChatterTimeoutHistoryMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeHistoryEntries(self):
        first = ChatterTimeoutHistoryEntry(
            dateTime = datetime.fromisoformat('2025-07-20T07:27:14.000000+00:00'),
            durationSeconds = 30,
            timedOutByUserId = 'abc123',
        )

        second = ChatterTimeoutHistoryEntry(
            dateTime = datetime.fromisoformat('2024-12-20T09:33:58.000000+00:00'),
            durationSeconds = 60,
            timedOutByUserId = 'def456',
        )

        third = ChatterTimeoutHistoryEntry(
            dateTime = datetime.fromisoformat('2025-05-01T12:12:12.000000+00:00'),
            durationSeconds = 60,
            timedOutByUserId = 'ghi789',
        )

        historyEntries: list[ChatterTimeoutHistoryEntry] = [ first, second, third ]
        historyEntriesJson = await self.mapper.serializeHistoryEntries(historyEntries)
        assert isinstance(historyEntriesJson, str)
        assert not historyEntriesJson.isspace()

        parsedHistoryEntries = json.loads(historyEntriesJson)
        assert isinstance(parsedHistoryEntries, list)
        assert len(parsedHistoryEntries) == 3

        for parsedHistoryEntry in parsedHistoryEntries:
            assert isinstance(parsedHistoryEntry, dict)
            assert len(parsedHistoryEntry) == 3

    @pytest.mark.asyncio
    async def test_serializeHistoryEntry(self):
        historyEntry = ChatterTimeoutHistoryEntry(
            dateTime = datetime.now(self.timeZoneRepository.getDefault()),
            durationSeconds = 30,
            timedOutByUserId = 'abc123',
        )

        result = await self.mapper.serializeHistoryEntry(historyEntry)
        assert len(result) == 3
        assert result['dateTime'] == historyEntry.dateTime.isoformat()
        assert result['durationSeconds'] == historyEntry.durationSeconds
        assert result['timedOutBy'] == historyEntry.timedOutByUserId
