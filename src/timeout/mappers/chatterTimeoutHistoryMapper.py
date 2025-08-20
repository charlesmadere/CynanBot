import json
from typing import Any, Collection

from frozenlist import FrozenList

from .chatterTimeoutHistoryMapperInterface import ChatterTimeoutHistoryMapperInterface
from ..models.chatterTimeoutHistoryEntry import ChatterTimeoutHistoryEntry
from ...misc import utils as utils


class ChatterTimeoutHistoryMapper(ChatterTimeoutHistoryMapperInterface):

    async def parseHistoryEntries(
        self,
        jsonString: str | Any | None,
    ) -> FrozenList[ChatterTimeoutHistoryEntry]:
        frozenHistoryEntries: FrozenList[ChatterTimeoutHistoryEntry] = FrozenList()

        if not utils.isValidStr(jsonString):
            frozenHistoryEntries.freeze()
            return frozenHistoryEntries

        historyEntriesJson: list[dict[str, Any]] | Any | None = json.loads(jsonString)
        if not isinstance(historyEntriesJson, list) or len(historyEntriesJson) == 0:
            frozenHistoryEntries.freeze()
            return frozenHistoryEntries

        historyEntries: list[ChatterTimeoutHistoryEntry] = list()

        for historyEntryJson in historyEntriesJson:
            historyEntry = await self.requireHistoryEntry(historyEntryJson)
            historyEntries.append(historyEntry)

        historyEntries.sort(key = lambda historyEntry: historyEntry.dateTime, reverse = True)
        frozenHistoryEntries.extend(historyEntries)
        frozenHistoryEntries.freeze()
        return frozenHistoryEntries

    async def requireHistoryEntry(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> ChatterTimeoutHistoryEntry:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        dateTime = utils.getDateTimeFromDict(jsonContents, 'dateTime')
        durationSeconds = utils.getIntFromDict(jsonContents, 'durationSeconds')
        timedOutBy = utils.getStrFromDict(jsonContents, 'timedOutBy')

        return ChatterTimeoutHistoryEntry(
            dateTime = dateTime,
            durationSeconds = durationSeconds,
            timedOutByUserId = timedOutBy,
        )

    async def serializeHistoryEntries(
        self,
        historyEntries: Collection[ChatterTimeoutHistoryEntry] | Any | None,
    ) -> str | None:
        if not isinstance(historyEntries, Collection):
            return None

        frozenHistoryEntries: FrozenList[ChatterTimeoutHistoryEntry] = FrozenList(historyEntries)
        frozenHistoryEntries.freeze()

        if len(frozenHistoryEntries) == 0:
            return None

        historyEntriesJson: list[dict[str, Any]] = list()

        for historyEntry in frozenHistoryEntries:
            historyEntryJson = await self.serializeHistoryEntry(historyEntry)
            historyEntriesJson.append(historyEntryJson)

        return json.dumps(historyEntriesJson, sort_keys = True, allow_nan = False)

    async def serializeHistoryEntry(
        self,
        historyEntry: ChatterTimeoutHistoryEntry,
    ) -> dict[str, Any]:
        if not isinstance(historyEntry, ChatterTimeoutHistoryEntry):
            raise TypeError(f'historyEntry argument is malformed: \"{historyEntry}\"')

        return {
            'dateTime': historyEntry.dateTime.isoformat(),
            'durationSeconds': historyEntry.durationSeconds,
            'timedOutBy': historyEntry.timedOutByUserId,
        }
